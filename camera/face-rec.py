#!/usr/bin/env python3
import face_recognition, cv2, numpy as np, os, sys, numpy

WIN_X = 1200
WIN_Y = 500

video_capture = cv2.VideoCapture(0)
rick_image = face_recognition.load_image_file("faces/rick.jpeg")
rick_image_encoding = face_recognition.face_encodings(rick_image)[0]

known_face_encodings = [
    rick_image_encoding,
]
known_face_names = [
    "Rick",
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

qty = 0
while True:
    ret, frame = video_capture.read()
    qty = qty + 1

    if process_this_frame:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = numpy.ascontiguousarray(small_frame[:, :, ::-1])
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        try:
          face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        except Exception as e:
          print(f'exception: {e}')
          continue

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    for (top, right, bottom, left), name in zip(face_locations, face_names):
        print('found face')
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    print(f'Processed Frame #{qty}')

    cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Video", WIN_X, WIN_Y)
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
