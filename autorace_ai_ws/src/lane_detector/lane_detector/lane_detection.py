#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class LaneDetectionNode(Node):
    def __init__(self):
        super().__init__('lane_detection_node')
        
        # 1. 訂閱剛才壓扁的「鳥瞰圖」
        self.subscription = self.create_subscription(
            Image, '/camera/image_projected', self.image_callback, 10)
        
        # 2. 發布過濾後的影像 (分成左邊黃線、右邊白線，方便 rqt 監看)
        self.pub_yellow = self.create_publisher(Image, '/camera/yellow_line', 10)
        self.pub_white = self.create_publisher(Image, '/camera/white_line', 10)
        
        self.bridge = CvBridge()
        self.get_logger().info('🎨 車道線色彩萃取節點 (Lane Detection) 已啟動！')

    def image_callback(self, msg):
        try:
            # 將 ROS 影像轉換為 OpenCV 格式
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
            # 3. 轉換為 HSV 色彩空間 (自駕車視覺核心)
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

            # 4. 擷取黃線 (左車道)
            # 數值設定：H(色相)約在20-40，S(飽和度)與V(亮度)拉高避免抓到暗色雜訊
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([40, 255, 255])
            yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

            # 5. 擷取白線 (右車道)
            # 數值設定：白色的飽和度(S)極低，亮度(V)極高
            lower_white = np.array([0, 0, 200])
            upper_white = np.array([180, 50, 255])
            white_mask = cv2.inRange(hsv, lower_white, upper_white)

            # 6. 將純黑白的 Mask 轉回 ROS 影像格式發布
            # 最佳實踐：使用 "mono8" (單通道 8-bit) 因為遮罩只有黑(0)與白(255)
            self.pub_yellow.publish(self.bridge.cv2_to_imgmsg(yellow_mask, "mono8"))
            self.pub_white.publish(self.bridge.cv2_to_imgmsg(white_mask, "mono8"))

        except Exception as e:
            self.get_logger().error(f'色彩萃取發生錯誤: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = LaneDetectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
