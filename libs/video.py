import random
import cv2
import os
from Cipher import VigenereExtended
#vf = VigenereExtended()
#x = VigenereExtended.encrypt(vf,"maybe")
#print(x)
#x = VigenereExtended.decrypt(vf,x)
#print(x.decode('UTF-8'))
#video = 'output.avi'
#cap = cv2.VideoCapture(video)
#i=0
#while True:
#    ret, frame = cap.read()
#    cv2.imshow(video, frame)
#    i+=1
#    if cv2.waitKey(20) & 0xFF == ord('q'):
#        break
#
def bin(s):
  return str(s) if s<=1 else bin(s>>1) + str(s&1)
  
def addzero(s):
  while (len(s)<8):
    s = '0' + s
  return s

def addzerolength(s):
  while (len(s)<24):
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
payload  = int(n_frames) * width * height * 3 - 2         # Payload = length of message that can be encrypted
                                                          # -2 for mode checking at start
  
## STEP 4.0 : Start asking
## STEP 4.1 : Ask to save filename
save = input("Do you want to save filename and extension in the encrypted video?(Y/N): ")
while save not in ['Y','N','y','n']:
  save = input("Wrong input. Save filename with extension?(Y/N): ")
  
## STEP 4.2 : Ask to use how many bits for LSB
nbit = input("Enter desired LSB bits(1/2): ")
while (nbit != "1" and nbit != "2"):
  nbit = input("Wrong input. Enter desired LSB bits(1/2): ")

if nbit == '2':
  payload *= 2
  
## STEP 4.3 : Ask the frame placement
print("Choose frame placement mode(1/2): ")
print("1. Sequential")
print("2. Random")
p_frame = input()
while (p_frame != "1" and p_frame != "2"):
  p_frame = input("Wrong input. Choose frame placement mode(1/2)): ")

## STEP 4.4 : Ask the pixel placement
print("Choose pixel placement mode(1/2): ")
print("1. Sequential")
print("2. Random")
p_pixel = input()
while (p_pixel != "1" and p_pixel != "2"):
  p_pixel = input("Wrong input. Choose pixel placement mode(1/2)): ")


## STEP 4.5 : Ask the message
if save in ['Y','y']:
  payload = payload - len(filename)
  print("You chose to save filename with extension.")
else:
  print("You chose to save filename without extension.")
  
print("You can encrypt " + str(payload) + " bits of message / " + str(int(payload/8)) + " characters")
message = input("Please enter your message: ")
while (len(message)==0 or len(message) > int(payload/8)):
  message = input("Message empty or longer than payload: ")

## STEP 4.6 : Ask to encrypt message or not
encrypt = input("Do you want to encrypt your message?(Y/N): ")
while encrypt not in ['Y','N','y','n']:
  encrypt = input("Wrong input. Do you want to encrypt your message?(Y/N): ")

## STEP 5 : Turn message into bytes
bytes_message = str(int(p_frame) - 1) + "" + str(int(p_pixel) - 1) 
## 0 0 for sequential frame, sequential pixel 
## 0 1 for sequential frame, random pixel
## 1 0 for random frame, sequential pixel
## 1 1 for random frame, random pixel

if encrypt in ['Y','y']:
  vf = VigenereExtended()
  VigenereExtended.changeKey(vf,key)
  message = VigenereExtended.encrypt(vf,message)
  for char in message:
    bytes_message += addzero(bin(char))
else:  
  for char in message:
    bytes_message += addzero(bin(ord(char)))

## STEP 6 : Put bytes of messages in video frames  
message_length = addzerolength(bin(len(message)))
i = 0
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, fps, (640,480))
j = 0
if [p_frame, p_pixel] == ['1','1']:
  while j < n_frames:
    while i < len(bytes_message):
      ret, frame = cap.read()
      if i == 0:
        length_ = [message_length[i:i+8] for i in range(0, len(message_length), 8)]
        print(length_)
        nlength = []
        nlength.append(int(length_[0], 2))
        nlength.append(int(length_[1], 2))
        nlength.append(int(length_[2], 2))
        print(nlength)
        print(frame[0][0])
        frame[0][0][0] = nlength[0]
        frame[0][0][1] = nlength[1]
        frame[0][0][2] = nlength[2]
        print(frame[0][0])
        out.write(frame)
        j += 1
        i += 1
      for x in range(1, width-1):
        if i >= len(bytes_message):
          break
        for y in range(0, height-1):
          if i >= len(bytes_message):
            break
          if (frame[y][x][0] & 1) != bytes_message[i]:
            if (frame[y][x][0] % 2 == 0):
              frame[y][x][0] += 1
            else:
              frame[y][x][0] -= 1
          i += 1
          if i >= len(bytes_message):
            break
          if (frame[y][x][1] & 1) != bytes_message[i]:
            if (frame[y][x][1] % 2 == 0):
              frame[y][x][1] += 1
            else:
              frame[y][x][1] -= 1
          i += 1
          if i >= len(bytes_message):
            break
          if (frame[y][x][2] & 1) != bytes_message[i]:
            if (frame[y][x][2] % 2 == 0):
              frame[y][x][2] += 1
            else:
              frame[y][x][2] -= 1
          out.write(frame)
          j += 1
          i += 1
          if i >= len(bytes_message):
            break
      if cv2.waitKey(20) & 0xFF == ord('q'):
        break
      if i>= len(bytes_message):
        break
      i+=1
      
    ret, frame = cap.read()
    out.write(frame)
    j += 1
  cap.release()
  out.release()
    
elif [p_frame, p_pixel] == ['1','2']:
  seed = 0
  for char in key:
    seed += ord(char)
  random.seed(seed)
#  random.randint(1, 10)
  while i < len(bytes_message):
    if i == 0:
      ret, frame = cap.read()
      length_ = [message_length[i:i+8] for i in range(0, len(message_length), 8)]
      print(length_)
      nlength = []
      nlength.append(int(length_[0], 2))
      nlength.append(int(length_[1], 2))
      nlength.append(int(length_[2], 2))
      frame[0][0][0] = nlength[0]
      frame[0][0][1] = nlength[1]
      frame[0][0][2] = nlength[2]
      i += 1
    for x in range(1, width-1):
      if i >= len(bytes_message):
        break
      for y in range(0, height-1):
        if i >= len(bytes_message):
          break
        if (frame[y][x][0] & 1) != bytes_message[i]:
          if (frame[y][x][0] % 2 == 0):
            frame[y][x][0] += 1
          else:
            frame[y][x][0] -= 1
        i += 1
        if i >= len(bytes_message):
          break
        if (frame[y][x][1] & 1) != bytes_message[i]:
          if (frame[y][x][1] % 2 == 0):
            frame[y][x][1] += 1
          else:
            frame[y][x][1] -= 1
        i += 1
        if i >= len(bytes_message):
          break
        if (frame[y][x][2] & 1) != bytes_message[i]:
          if (frame[y][x][2] % 2 == 0):
            frame[y][x][2] += 1
          else:
            frame[y][x][2] -= 1
        i += 1
        if i >= len(bytes_message):
          break
    if cv2.waitKey(20) & 0xFF == ord('q'):
      break
    if i>= len(bytes_message):
      break
    i+=1


cv2.destroyAllWindows()
#print(videoLSB)
print(int(n_frames))
#print(ord('a') + 10)

def extract(vid):
  cap = cv2.VideoCapture(vid)
  n_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)              # No of frames in video
  ret, frame = cap.read()
  print(frame[0][0])

extract(video)
#  i=0
#  while i<n_frames:
#    if i==0:
#      
#    ret, frame = cap.read()
#    cv2.imshow(video, frame)
#    i+=1
#    if cv2.waitKey(20) & 0xFF == ord('q'):
#        break



