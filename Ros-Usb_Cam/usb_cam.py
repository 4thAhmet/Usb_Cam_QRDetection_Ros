import rospy
import cv2
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String
import pyzbar.pyzbar as pyzbar


qr=cv2.QRCodeDetector()


def callback(data):
    cv_image=bridge.imgmsg_to_cv2(data,"bgr8")
    decode(cv_image)


def decode(img):
    decodedObjects=pyzbar.decode(img)
    for decodedObject in decodedObjects:
        print('Type: ',decodedObject.type)
        print('Data: ',decodedObject.data.decode('ascii'),'\n')
        publishData(decodedObject)


def shutdown():
    rospy.loginfo("Terminating ...")
    pub.unregister()


def publishData(data):  
    pub.publish(str(data))



if __name__=="__main__":
    rospy.init_node("Usb_Cam",anonymous=True)
    bridge=CvBridge()
    rospy.loginfo("CTRL+C to Terminate")
    rospy.on_shutdown(shutdown)
    pub=rospy.Publisher('Qr_Data',String,queue_size=1)
    rate=rospy.Rate(1)
    rospy.Subscriber("/usb_cam/image_raw",Image,callback)
    rospy.spin()
