import cv2
import mediapipe as mp
import paho.mqtt.client as mqtt
import time
from esp32tst import cam
mp_drawing = mp.solutions.drawing_utils
mp_face = mp.solutions.face_detection.FaceDetection(model_selection=1,min_detection_confidence=0.5)

width=640
height=480
count=0


    
def stop():
    mqttBroker ="192.168.0.103"
    client = mqtt.Client("raspberry pi 40")
    client.connect(mqttBroker)
    client.publish("test2",(bytes("stop",'utf-8')))
def turn():
    mqttBroker ="192.168.0.103"
    client = mqtt.Client("raspberry pi 40")
    client.connect(mqttBroker)
    client.publish("test2",(bytes("turn",'utf-8')))
def turn1():
    mqttBroker ="192.168.0.103"
    client = mqtt.Client("raspberry pi 40")
    client.connect(mqttBroker)
    client.publish("test2",(bytes("turn1",'utf-8')))
def back():
    mqttBroker ="192.168.0.103"
    client = mqtt.Client("raspberry pi 40")
    client.connect(mqttBroker)
    client.publish("test2",(bytes("back",'utf-8')))
def forward():
    mqttBroker ="192.168.0.103"
    client = mqtt.Client("raspberry pi 40")
    client.connect(mqttBroker)
    client.publish("test2",(bytes("forward",'utf-8')))


def obj_data(img):
    
    image_input = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = mp_face.process(image_input)
    if not results.detections:
       stop()
       
    else:    
         for detection in results.detections:
             bbox = detection.location_data.relative_bounding_box
#             print(bbox)
             x, y, w, h = int(bbox.xmin*width), int(bbox.ymin * height), int(bbox.width*width),int(bbox.height*height)
             cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
             cx=int(x+x+w)//2
             cy=int(y+y+h)//2
           
             cv2.circle(img,(cx,cy),5,(0,0,255),-1)
             a=int(cx)//62
             cv2.putText(img,str(a),(430,50),5,cv2.FONT_HERSHEY_PLAIN,(0,255,0),2)
             b=int(cy -h)//10
#             print(b)
             cv2.putText(img,str(b),(30,50),5,cv2.FONT_HERSHEY_PLAIN,(0,255,0),2)
             if b > 12:
                 forward()
             else:
                 stop()
             if a > 6:
                 time.sleep(0.1)
                 turn1()
                 time.sleep(0.1)
                 stop()
               
             if a < 4:
                 time.sleep(0.1)
                 turn()
                 time.sleep(0.1)
                 stop()
               
while True:

    frame=cam()
    frame=cv2.flip(frame,1)
    frame=cv2.resize(frame,(640,480))
    obj_data(frame)
    cv2.imshow("FRAME",frame)
    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()