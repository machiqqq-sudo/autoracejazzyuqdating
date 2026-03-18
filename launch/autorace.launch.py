import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable, TimerAction, LogInfo
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 取得 package 的 share 目錄
    pkg_dir = get_package_share_directory('autorace_jazzy')
    
    # 定義路徑
    world_path = os.path.join(pkg_dir, 'worlds', 'turtlebot3_autorace_2020.world')
    models_path = os.path.join(pkg_dir, 'models')
    sdf_path = os.path.join(pkg_dir, 'sdf', 'my_burger.sdf')

    # 讀取 SDF 檔案內容以供 robot_state_publisher 使用
    # 並將 model:// 替換為 file:// 絕對路徑，確保 RViz 能正確顯示模型
    with open(sdf_path, 'r') as f:
        robot_desc = f.read().replace('model://', f'file://{pkg_dir}/models/')

    return LaunchDescription([
     
        # 1. 環境變數設定
        SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', models_path),
        SetEnvironmentVariable('GZ_IP', '127.0.0.1'),
        
        # [for henry] Nvidia RTX 顯卡優化
        SetEnvironmentVariable('__NV_PRIME_RENDER_OFFLOAD', '1'),
        SetEnvironmentVariable('__GLX_VENDOR_LIBRARY_NAME', 'nvidia'),
        SetEnvironmentVariable('__EGL_VENDOR_LIBRARY_FILENAMES', '/usr/share/glvnd/egl_vendor.d/10_nvidia.json'),

        # 2. 啟動賽道 (Gazebo Harmonic)
        LogInfo(msg=" 正在啟動賽道..."),
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', world_path],
            output='screen'
        ),

        # 3. 延遲 5 秒後啟動車輛與大腦
        TimerAction(
            period=5.0,
            actions=[
                LogInfo(msg=" 正在啟動..."),
                Node(
                    package='autorace_jazzy',
                    executable='autorace_manager',
                    output='screen'
                ),

                LogInfo(msg=" 正在召喚機器人..."),
                Node(
                    package='ros_gz_sim',
                    executable='create',
                    arguments=[
                        '-file', sdf_path, 
                        '-name', 'burger', 
                        '-x', '0.44', '-y', '-1.75', '-z', '0.01', '-Y', '0.0'
                    ],
                    output='screen'
                ),

                LogInfo(msg="啟動 robot_state_publisher..."),
                Node(
                    package='robot_state_publisher',
                    executable='robot_state_publisher',
                    name='robot_state_publisher',
                    output='both',
                    parameters=[
                        {'use_sim_time': True},
                        {'robot_description': robot_desc},
                    ]
                ),

                LogInfo(msg="建立 ROS-GZ 通訊橋樑..."),
                Node(
                    package='ros_gz_bridge',
                    executable='parameter_bridge',
                    arguments=[
                        '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                        '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
                        '/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
                        '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                        '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
                        '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
                        '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
                        '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
                        '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V'
                    ],
                    output='screen'
                ),
                
                LogInfo(msg=" 準備就緒！(按 Ctrl+C 可安全關閉)")
            ]
        )
    ])
