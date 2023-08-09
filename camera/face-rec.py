#!/usr/bin/env python3
import face_recognition, cv2, numpy as np, os, sys, numpy, pyautogui, argparse
from PIL import Image
from pycoral.adapters import classify
from pycoral.adapters import common
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

WIN_X = 640
WIN_Y = 480

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
  '-m', '--model', required=False, help='File path of .tflite file.')
parser.add_argument(
  '-i', '--input', required=False, help='Image to be classified.')
parser.add_argument(
  '-l', '--labels', help='File path of labels file.')
parser.add_argument(
  '-k', '--top_k', type=int, default=1,
  help='Max number of classification results')
parser.add_argument(
  '-t', '--threshold', type=float, default=0.0,
  help='Classification score threshold')
parser.add_argument(
  '-c', '--count', type=int, default=5,
  help='Number of times to run inference')
parser.add_argument(
  '-a', '--input_mean', type=float, default=128.0,
  help='Mean value for input normalization')
parser.add_argument(
  '-s', '--input_std', type=float, default=128.0,
  help='STD value for input normalization')
args = parser.parse_args()


def get_info():
    w, h = pyautogui.size()
    x, y = pyautogui.position()
    return {
      'screen': { 'w':w, 'h': h },
      'mouse': { 'x':x, 'y': y },
    }

info = get_info()
VIDEO_POSITION_X = int(info['screen']['w']/2)
VIDEO_POSITION_Y = 0
print(info)
# https://pyautogui.readthedocs.io/en/latest/
#pyautogui.moveTo(100, 150)
#pyautogui.alert(text='', title='', button='OK')
#c = pyautogui.confirm(text='do you want to continue?', title='continue prompt', buttons=['OK', 'Cancel'])
#print(c)

video_capture = cv2.VideoCapture(0)
print('Loading Faces')
print('Loaded Faces')


rick_image = face_recognition.load_image_file("faces/rick.jpeg")
rick_image_encoding = face_recognition.face_encodings(rick_image)[0]

lily_image = face_recognition.load_image_file("faces/lily.jpeg")
lily_image_encoding = face_recognition.face_encodings(lily_image)[0]

joey_image = face_recognition.load_image_file("faces/joey.jpeg")
joey_image_encoding = face_recognition.face_encodings(joey_image)[0]

katie_image = face_recognition.load_image_file("faces/katie.jpeg")
katie_image_encoding = face_recognition.face_encodings(katie_image)[0]


known_face_encodings = [
    rick_image_encoding,
    lily_image_encoding,
    joey_image_encoding,
    katie_image_encoding,
]
known_face_names = [
    "Rick",
    "Lily",
    "Joey",
    "Katie",
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def blue_image(image):
    face_locations = face_recognition.face_locations(image, model="cnn")
    for top, right, bottom, left in face_locations:
        # Extract the region of the image that contains the face
        face_image = frame[top:bottom, left:right]

        # Blur the face image
        face_image = cv2.GaussianBlur(face_image, (99, 99), 30)

        # Put the blurred face region back into the frame image
        frame[top:bottom, left:right] = face_image

def add_makeup(image):
    face_landmarks_list = face_recognition.face_landmarks(image)

    pil_image = Image.fromarray(image)
    for face_landmarks in face_landmarks_list:
        d = ImageDraw.Draw(pil_image, 'RGBA')

        # Make the eyebrows into a nightmare
        d.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
        d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
        d.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)
        d.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)

        # Gloss the lips
        d.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
        d.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
        d.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=8)
        d.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=8)

        # Sparkle the eyes
        d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
        d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

        # Apply some eyeliner
        d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=6)
        d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)


qty = 0
while True:
    ret, frame = video_capture.read()
    qty += 1

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

    cv2.namedWindow("Video", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("Video", VIDEO_POSITION_X, VIDEO_POSITION_Y)

    #cv2.resizeWindow("Video", WIN_X, WIN_Y)
    cv2.imshow('Video', frame)
    #(x,y,w,h) = cv2.getWindowImageRect('Video')
    #print(x,y,w,h)

    print(f"#{qty} @ %dFPS" % (video_capture.get(5)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
