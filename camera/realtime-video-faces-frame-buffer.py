#!/usr/bin/env python3
CAMERA_ID = 0
print(f'Loading modules')
import os, sys, time, logging, spidev as SPI, cv2, face_recognition, numpy as np, subprocess, signal, sys
sys.path.append('../lcd')
from lib import LCD_2inch
from PIL import Image,ImageDraw
print(f'Loaded modules')

def signal_handler(sig, frame):
  print('You pressed Ctrl+C!')
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

RESIZE_IMAGE_FOR_FACE_RECOGNITION = True
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
disp = LCD_2inch.LCD_2inch()
disp.Init()
disp.clear()

#print(f'{disp.width}x{disp.height}')

image1 = Image.new("RGB", (disp.height, disp.width ), "WHITE")
draw = ImageDraw.Draw(image1)

vid = cv2.VideoCapture(CAMERA_ID)


if RESIZE_IMAGE_FOR_FACE_RECOGNITION:
    start = time.time()
    print('Loading Faces.')
    katie_face = face_recognition.load_image_file("faces/katie.jpeg")
    katie = face_recognition.face_encodings(katie_face)[0]
    joey_face = face_recognition.load_image_file("faces/joey.jpeg")
    joey = face_recognition.face_encodings(joey_face)[0]
    rick_face = face_recognition.load_image_file("faces/rick.jpeg")
    rick = face_recognition.face_encodings(rick_face)[0]
    lily_face = face_recognition.load_image_file("faces/lily.jpeg")
    lily = face_recognition.face_encodings(lily_face)[0]
    known_face_encodings = [
      rick,
      katie,
      joey,
      lily,
    ]
    known_face_names = [
      "Rick",
      "Katie",
      "Joey",
      "Lily",
    ]
    dur = time.time()-start
    print(f'Loaded Faces in {int(dur)}ms')



qty = 0
while True:
    ret, frame = vid.read()
    if not ret:
        print('Failed to read frame..')
        time.sleep(1.0)
        continue
    resized = cv2.resize(frame, (320,240))
    started = time.time()

    if RESIZE_IMAGE_FOR_FACE_RECOGNITION:
        locs = face_recognition.face_locations(resized)
    dur = time.time() - started
    print(dur)

    face_encodings = []
    face_names = []

    rgb_small_frame = cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
    if RESIZE_IMAGE_FOR_FACE_RECOGNITION:
        face_encodings = face_recognition.face_encodings(rgb_small_frame, locs)

    for face_encoding in face_encodings:
      matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
      name = "Unknown"
      face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
      best_match_index = np.argmin(face_distances)
      if matches[best_match_index]:
        name = known_face_names[best_match_index]
      face_names.append(name)

    if RESIZE_IMAGE_FOR_FACE_RECOGNITION:
        for (top, right, bottom, left), name in zip(locs, face_names):
          #print(f'{top}/{right}/{bottom}/{left}')
          cv2.rectangle(resized, (left, top), (right, bottom), (0, 0, 255), 2)
          cv2.rectangle(resized, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
          font = cv2.FONT_HERSHEY_DUPLEX
          cv2.putText(resized, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    img_color = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(img_color)
    image = image.rotate(180)
    disp.ShowImage(image)

    out = '/tmp/image.png'
    cv2.imwrite(out,resized)
    subprocess.call(['fbv','-i','-a','-y','-c','-u',out])


    print(f'processed frame #{qty}')
    qty = qty + 1



vid.release()
disp.module_exit()
sys.exit(0)


  
