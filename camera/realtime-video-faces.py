#!/usr/bin/env python3
import os, sys, time, logging, cv2, face_recognition, numpy as np
#sys.path.append('../lcd')
#from lib import LCD_2inch
from PIL import Image,ImageDraw

RESIZE_IMAGE_FOR_FACE_RECOGNITION = True
vid = cv2.VideoCapture(0)

print('Loading Faces.')
rick_face = face_recognition.load_image_file("faces/rick.jpeg")
rick = face_recognition.face_encodings(rick_face)[0]
'''
katie_face = face_recognition.load_image_file("faces/katie.jpeg")
katie = face_recognition.face_encodings(katie_face)[0]
joey_face = face_recognition.load_image_file("faces/joey.jpeg")
joey = face_recognition.face_encodings(joey_face)[0]
lily_face = face_recognition.load_image_file("faces/lily.jpeg")
lily = face_recognition.face_encodings(lily_face)[0]
'''
known_face_encodings = [
  rick,
'''
  katie,
  joey,
  lily,
'''
]
known_face_names = [
  "Rick",
'''
  "Katie",
  "Joey",
  "Lily",
'''
]
print('Loaded Faces.')



qty = 0
while True:
    ret, frame = vid.read()
    resized = cv2.resize(frame, (320,240))
    started = time.time()

    if RESIZE_IMAGE_FOR_FACE_RECOGNITION:
        locs = face_recognition.face_locations(resized)
    dur = time.time() - started
    print(dur)
    print(locs)

    face_encodings = []
    face_names = []

    rgb_small_frame = cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, locs)

    for face_encoding in face_encodings:
      try:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
      except:
        pass
      name = "Unknown"
      try:
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
          name = known_face_names[best_match_index]
      except:
        pass
      face_names.append(name)

    if RESIZE_IMAGE_FOR_FACE_RECOGNITION:
        for (top, right, bottom, left), name in zip(locs, face_names):
          print(f'{top}/{right}/{bottom}/{left}')
          cv2.rectangle(resized, (left, top), (right, bottom), (0, 0, 255), 2)
          cv2.rectangle(resized, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
          font = cv2.FONT_HERSHEY_DUPLEX
          cv2.putText(resized, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    img_color = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(img_color)
    image = image.rotate(180)
    #cv2.imshow(image)
    #disp.ShowImage(image)
    print(f'processed frame #{qty}')
    qty = qty + 1



vid.release()
#disp.module_exit()
sys.exit(0)


  
