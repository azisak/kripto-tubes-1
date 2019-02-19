


#Pilih bit LSB 1 atau 2 bit
#Pilih frame sekuensial atau acak
#Pilih pixel sekuensial atau acak
import cv2
import os
from Cipher import VigenereExtended
#vf = VigenereExtended()
#x = VigenereExtended.encrypt(vf,"maybe")
#print(x)
#x = VigenereExtended.decrypt(vf,x)
#print(x.decode('UTF-8'))

#
#
#
## STEP 1.0 : Get Video name
filename = input("Enter video name(with extension): ")
while not os.path.isfile(filename):
  filename = input("Video not found, re-enter name(with extension):  ")

## STEP 2.0 : Get Key
key = input("Enter key(max 25 characters): ")
while (len(key)==0 or len(key)>25):
  key = input("Empty key or too long, re-enter valid key(max 25 character):  ")  
## STEP 3.1 : Analyze video
video = filename
cap = cv2.VideoCapture(video)
n_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)          #No of frames in video
width    = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH ))    #Get width, a.k.a horizontal n pixel
height   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT ))   #Get height, a.k.a vertical n pixel


## STEP 4.0 : Start asking
## STEP 4.1 : Ask to save filename?
save = input("Do you want to save filename and extension in the encrypted video?(Y/N)")
while save not in ['Y','N','y','n']:
  save = input("Wrong input. Save filename with extension?(Y/N):  ")  
  
## STEP 4.2 : Ask the message to encrypt

if save in ['Y','y']:
  print("You chose to save filename with extension.")
  print("You can encrypt")
  
i = 0
while i < n_frames:
    ret, frame = cap.read()
    for x in range(0, 30):
      for y in range(0, width-1):
        #        b,g,r = frame[x][y]
        pass
#        frame[x][y] = [0,0,0]
#    cv2.imshow(video, frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    i += 1

cv2.destroyAllWindows()
#print(ord('a') + 10)

