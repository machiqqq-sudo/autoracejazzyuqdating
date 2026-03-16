#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from rclpy.qos import qos_profile_sensor_data

class ImageProjectionNode(Node):
    def __init__(self):
        super().__init__('image_projection_node')
        # 訂閱來自 Gazebo 的原始畫面
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, qos_profile_sensor_data)
        # 發布轉換後的鳥瞰圖
        self.publisher = self.create_publisher(Image, '/camera/image_projected', 10)
        self.bridge = CvBridge()
        self.get_logger().info('🦅 鳥瞰圖轉換節點 (Image Projection Node) 已啟動！')

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            height, width = cv_image.shape[:2]

            # 定義透視轉換的梯形頂點 (擷取畫面下半部的馬路)
            pt_A = [width * 0.2, height * 0.6]  # 左上
            pt_B = [width * 0.8, height * 0.6]  # 右上
            pt_C = [width * 1.0, height * 1.0]  # 右下
            pt_D = [width * 0.0, height * 1.0]  # 左下
            
            pts_src = np.float32([pt_A, pt_B, pt_C, pt_D])
            pts_dst = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

            # 執行 OpenCV 透視變形
            matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
            bird_eye_view = cv2.warpPerspective(cv_image, matrix, (width, height))

            # 將結果發布出去
            projected_msg = self.bridge.cv2_to_imgmsg(bird_eye_view, "bgr8")
            self.publisher.publish(projected_msg)
        except Exception as e:
            self.get_logger().error(f'錯誤: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = ImageProjectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
