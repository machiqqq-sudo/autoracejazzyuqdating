import rclpy
from rclpy.node import Node
import os
import random

# 強制解決通訊問題
os.environ["GZ_IP"] = "127.0.0.1"

class AutoRaceManager(Node):
    def __init__(self):
        super().__init__('autorace_manager')
        
      
        #  紅綠燈狀態變數
    
        self.light_state = "RED" 
        self.state_timer_count = 0
        self.target_time = random.randint(5, 8)
        
    
        # 🚧 柵欄定時變數
     
        self.bar_state = "UP"       # 初始狀態為升起
        self.bar_timer_count = 0    # 柵欄的專屬計時器
        self.bar_interval = 10      # 設定每幾秒切換一次 
        
        # 建立大腦統一的時鐘 (每秒跳動一次)
        self.timer = self.create_timer(1.0, self.timer_callback)
        
        self.get_logger().info('=== AutoRace (定時升降) 已啟動 ===')
        
        # 初始狀態：確保一開始柵欄是升起的 (1.57 弧度)
        os.system("gz topic -t '/model/traffic_bar/joint/bar_joint/0/cmd_pos' -m gz.msgs.Double -p 'data: 1.57' &")

    def timer_callback(self):
        """ 每秒執行一次的統一主迴圈 """
        
        
        # 1. 紅綠燈控制邏輯
        
        self.state_timer_count += 1
        if self.state_timer_count >= self.target_time:
            self.state_timer_count = 0
            if self.light_state == "RED":
                self.light_state = "YELLOW"
                self.target_time = 5
                self.set_light("yellow")
            elif self.light_state == "YELLOW":
                self.light_state = "GREEN"
                self.target_time = random.randint(5, 8)
                self.set_light("green")
            else:
                self.light_state = "RED"
                self.target_time = random.randint(5, 8)
                self.set_light("red")

      
        # 2. 柵欄定時升降邏輯
     
        self.bar_timer_count += 1
        if self.bar_timer_count >= self.bar_interval:
            self.bar_timer_count = 0 # 時間到，重新倒數
            
            if self.bar_state == "UP":
                self.bar_state = "DOWN"
                self.get_logger().warn('10秒時間到！放下柵欄...')
                os.system("gz topic -t '/model/traffic_bar/joint/bar_joint/0/cmd_pos' -m gz.msgs.Double -p 'data: 0.0' &")
            else:
                self.bar_state = "UP"
                self.get_logger().info('10秒時間到！升起柵欄...')
                os.system("gz topic -t '/model/traffic_bar/joint/bar_joint/0/cmd_pos' -m gz.msgs.Double -p 'data: 1.57' &")

    def set_light(self, color):
        """ 發送指令控制紅綠燈位置 """
        if color == "red":
            os.system("gz topic -t '/model/traffic_light/joint/red_joint/0/cmd_pos' -m gz.msgs.Double -p 'data: 0.0' &")
            os.system("gz topic -t '/model/traffic_light/joint/yellow_joint/0/cmd_pos' -m gz.msgs.Double -p 'data: 0.0' &")
            os.system("gz topic -t '/model/traffic_light/joint/green_joint/0/cmd_pos' -m gz.msgs.Double -p 'data: 0.0' &")
        elif color == "yellow":
            os.system("gz topic -t '/model/traffic_light/joint/red_joint/0/cmd_pos' -m gz.msgs.Double -p 'data: 0.015' &")
            os.system("gz topic -t '/model/traffic_light/joint/yellow_joint/0/cmd_pos' -m gz.msgs.Double -p 'data: -0.016' &")
            os.system("gz topic -t '/model/traffic_light/joint/green_joint/0/cmd_pos' -m gz.msgs.Double -p 'data: 0.0' &")
        elif color == "green":
            os.system("gz topic -t '/model/traffic_light/joint/red_joint/0/cmd_pos' -m gz.msgs.Double -p 'data: 0.015' &")
            os.system("gz topic -t '/model/traffic_light/joint/yellow_joint/0/cmd_pos' -m gz.msgs.Double -p 'data: 0.0' &")
            os.system("gz topic -t '/model/traffic_light/joint/green_joint/0/cmd_pos' -m gz.msgs.Double -p 'data: -0.017' &")

def main(args=None):
    rclpy.init(args=args)
    node = AutoRaceManager()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
