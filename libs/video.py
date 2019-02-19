


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

def bin(s):
  return str(s) if s<=1 else bin(s>>1) + str(s&1)
  
def addzero(s):
  while (len(s)<8):
    s = '0' + s
  return s

# STEP 1.0 : Get Video name
filename = input("Enter video name(with extension): ")
while not os.path.isfile(filename):
  filename = input("Video not found, re-enter name(with extension): ")

## STEP 2.0 : Get Key
key = input("Enter key(max 25 characters): ")
while (len(key)==0 or len(key)>25):
  key = input("Empty key or too long, re-enter valid key(max 25 character): ")
  
## STEP 3.0 : Analyze video
video = filename
cap = cv2.VideoCapture(video)
n_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)              # No of frames in video
width    = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH ))        # Get width, a.k.a horizontal n pixel
height   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT ))       # Get height, a.k.a vertical n pixel
fps      = int(cap.get(cv2.CAP_PROP_FPS))                 # Get FPS
payload  = int(n_frames) * width * height - 2             # No payload = length of message that can be encrypted
                                                          # -2 for mode checking at start
  
## STEP 4.0 : Start asking
## STEP 4.1 : Ask to save filename
save = input("Do you want to save filename and extension in the encrypted video?(Y/N): ")
while save not in ['Y','N','y','n']:
  save = input("Wrong input. Save filename with extension?(Y/N): ")
  
## STEP 4.2 : Ask to use how many bits for LSB
nbit = input("Enter desired LSB bits(1/2): ")
while (nbit != "1" and nbit != "2"):
  print(type(nbit))
  nbit = input("Wrong input. Enter desired LSB bits(1/2): ")

if nbit == '2':
  payload *= 2
  
## STEP 4.3 : Ask the frame placement
print("Choose frame placement mode(1/2): ")
print("1. Sequential")
print("2. Random")
f_place = input()
while (f_place != "1" and f_place != "2"):
  f_place = input("Wrong input. Choose frame placement mode(1/2)): ")

## STEP 4.4 : Ask the pixel placement
print("Choose pixel placement mode(1/2): ")
print("1. Sequential")
print("2. Random")
p_place = input()
while (p_place != "1" and p_place != "2"):
  p_place = input("Wrong input. Choose pixel placement mode(1/2)): ")


## STEP 4.5 : Ask the message
if save in ['Y','y']:
  payload = payload - len(filename)
  print("You chose to save filename with extension.")
else:
  print("You chose to save filename without extension.")
  
print("You can encrypt " + str(payload) + " bits of message / " + str(int(payload/8)) + " characters")
message = input("Please enter your message: ")
while (len(message)==0 or len(message) > payload):
  message = input("Message empty or longer than payload: ")

## STEP 4.6 : Ask to encrypt message or not
encrypt = input("Do you want to encrypt your message?(Y/N): ")
while encrypt not in ['Y','N','y','n']:
  enncrypt = input("Wrong input. Do you want to encrypt your message?(Y/N): ")

## STEP 5 : Turn message into bytes
bytes_message = str(int(f_place) - 1) + "" + str(int(p_place) - 1) 

## 0 0 for sequential frame, sequential pixel 
## 0 1 for sequential frame, random pixel
## 1 0 for random frame, sequential pixel
## 1 1 for random frame, random pixel

for char in message:
  bytes_message += addzero(bin(ord(char)))
  
i = 0
videoLSB = ""
#while i < n_frames:
#    ret, frame = cap.read()
#    for y in range(0, width-1):
#      for x in range(0, height-1):
#        b,g,r = frame[x][y]
#        videoLSB += str(b & 1) + str(g & 1) + str(r & 1) #append LSB
##        frame[x][y] = [0,0,0]
##    cv2.imshow(video, frame)
#    if cv2.waitKey(20) & 0xFF == ord('q'):
#        break
#    i += 1
    
#11 01111001 01100101 01110011

cv2.destroyAllWindows()
print(videoLSB)
print(int(n_frames))
#print(ord('a') + 10)


