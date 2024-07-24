import cv2
import time
import urllib
import imutils
import subprocess
import numpy as np
import sys, numpy, os
import time
import serial as s
import threading
from matplotlib import pyplot as plt 
try:
    import queue as Queue
except ImportError:
    import Queue

# bufferless VideoCapture
class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.q = Queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except Queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()
  def quit_it(self):
    self.cap.release()


#url="http://192.168.1.2:8080/shot.jpg"
url= VideoCapture(0)  
arduino = s.Serial('/dev/ttyUSB0')

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(motor,GPIO.OUT)
#GPIO.setup(buzzer,GPIO.OUT)
#GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_UP)

size = 4
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'

print('Training...')
(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1
(width, height) = (130, 100)

(images, labels) = [numpy.array(lis) for lis in [images, labels]]
model = cv2.face.createFisherFaceRecognizer()
#model = cv2.createFisherFaceRecognizer()
#print('time before training: ',time.time())
model.train(images, labels)
predict_cor = []
predict_uncor = []
face_cascade = cv2.CascadeClassifier(haar_file)
#webcam = cv2.VideoCapture(0)
value=False
val = time.time()+6
#print('time after training: ',time.time())
try: 
        
    while True:
    
        if val < time.time():
        	url.quit_it()
        	cv2.destroyAllWindows()
        	break
        if(True):
            
            value=True
            wait_time = 10
            auth = 0
            
            while 1: #value here
                print("capture")
                im=url.read()
 #               rete, im = webcam.read()
                im = imutils.resize(im, width=400)
                cv2.imwrite('/var/www/html/pan.jpg', im)
                #print('time inside after capturing : ',time.time())
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(im,(x,y),(x+w,y+h),(255,255,0),2)
                    face = gray[y:y + h, x:x + w]
                    face_resize = cv2.resize(face, (width, height))
                    #Try to recognize the face
                    prediction = model.predict(face_resize)
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    print("prediction: ",prediction[1])
                    if prediction[1]<70:
                        cv2.putText(im,'%s - %.0f' % (names[prediction[0]],prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(255, 0, 0))
                        #print( names[prediction[0]]);
                        name_of_the_person = names[prediction[0]]
                        auth = 1
                        wait_time = 0
                        value=False
                        break
                    elif(wait_time < 1):
                        auth =2
                        value =False
                    else:
                        wait_time-=1
                        cv2.putText(im,'scanning',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                #print('time in between: ',time.time())
                cv2.imshow('OpenCV', im)
                #cv2.imwrite('/var/www/html/capture.jpg', im);
                cv2.imwrite('capture.jpg', im)
                key = cv2.waitKey(10) & 0xFF
                
                if key == 27:
                     break
                if(auth == 2):
                    cv2.imwrite('capture.jpg', im)
                    cv2.imwrite('/var/www/html/capture.jpg', im);
                    #print("unauthorized user")
                    #print('time unauthorised one: ',time.time())
                    value=True
                    file = open("/home/karthik/tarun/face/log.txt" , "w")
                    file.write("unauthorized user")
                    print("unauthorized user here")
                    predict_uncor.append(prediction[1])
                    arduino.write(b'0') 
                    file.close()
                    #time.sleep(2)
                    arduino.write(b'2')
                    #url.release()
                    #GPIO.output(buzzer,True)
                    subprocess.Popen("sudo python3 mail.py",shell=True).communicate()
                    #time.sleep(1)
                    subprocess.Popen("sudo python3 sms.py",shell=True).communicate()
                    #subprocess.Popen("sudo python3 webpage.py", shell=True).communicate()
                    #GPIO.output(buzzer,False)
                    #cv2.destroyAllWindows()
  
                elif(auth == 1):
                    print(name_of_the_person)
                    predict_cor.append(prediction[1])
                    print("authorized user");
                    arduino.write(b'1'); 
                    time.sleep(2)   
                    arduino.write(b'3');                #GPIO.output(motor,True)                    
                   # subprocess.Popen("sudo python mail.py",shell=True).communicate()                    
                    #time.sleep(5)
                    #GPIO.output(motor,False)

                #print('time in the ending: ',time.time())
               
except Exception as e:
     KeyboardInterrupt()
     print(e)
     time.sleep(3)
     cv2.destroyAllWindows()
     url.quit_it()
if not predict_cor:
    plt.hist(predict_uncor)
    plt.show()
else:
    print("prediction: ", predict_cor,"\n prediction_: ", predict_uncor)
    plt.bar(predict_cor, predict_uncor)
    plt.show()
     #url.release()

