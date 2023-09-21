import argparse, time, sys, os, numpy as np, cv2
from PIL import Image
from pycoral.adapters import classify
from pycoral.adapters import common
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

class BananaDetector(object):
    labels = None
    interpreter = None
    size = None
    input_mean = 128.0
    input_std = 128.0
    count = 5
    top_k = 10
    threshold = 0.0
    is_banana_threshold = 0.20
    _labels = 'labels/mobilenet_v1_0.75_192_quant_edgetpu.txt'
    _model = 'models/mobilenet_v1_0.75_192_quant_edgetpu.tflite'
    def __init__(self):
        print('banana detector setup')
        self.labels = read_label_file(self._labels) if self._labels else {}
        self.interpreter = make_interpreter(*self._model.split('@'))
        self.interpreter.allocate_tensors()
        if common.input_details(self.interpreter, 'dtype') != np.uint8:
          raise ValueError('Only support uint8 input type.')
        self.size = common.input_size(self.interpreter)
    def is_banana_file(self, FILE):
        if not os.path.isfile(FILE):
            return False
        image = Image.open(FILE).convert('RGB').resize(self.size, Image.LANCZOS)
        params = common.input_details(self.interpreter, 'quantization_parameters')
        scale = params['scales']
        zero_point = params['zero_points']
        if abs(scale * self.input_std - 1) < 1e-5 and abs(self.input_mean - zero_point) < 1e-5:
            common.set_input(self.interpreter, image)
        else:
            normalized_input = (np.asarray(image) - self.input_mean) / (input_std * scale) + zero_point
            np.clip(normalized_input, 0, 255, out=normalized_input)
            common.set_input(self.interpreter, normalized_input.astype(np.uint8))

        for _ in range(self.count):
            start = time.perf_counter()
            self.interpreter.invoke()
            inference_time = time.perf_counter() - start
            classes = classify.get_classes(self.interpreter, self.top_k, self.threshold)
            print('%.1fms' % (inference_time * 1000))

        print('-------RESULTS--------')
        for c in classes:
            l = self.labels.get(c.id, c.id)
            print('%s: %.5f' % (l, c.score))
            if l == 'banana':
                return True
            #if c.score >= self.is_banana_threshold:
        return False


def find_webcam_bananas(bd):
    vid = cv2.VideoCapture(0)
    qty = 0
    while True:
        ret, frame = vid.read()
        #image = cv2.resize(frame, (320,240))
        image = frame
        tf = './.tmp.png'
        cv2.imwrite(tf, image)
        is_banana = bd.is_banana_file(tf)
        print(f'{tf} is banana?   {is_banana}')
        print(f'processed frame #{qty}')
        time.sleep(1.0)
        qty = qty + 1


if __name__ == '__main__':
  bd = BananaDetector()
  images = [
          'images/bananas/banana1.jpg',
          'images/bananas/banana2.jpg',
  ]
  for i in images:
      is_banana = bd.is_banana_file(i)
      print(f'{i} is banana?   {is_banana}')

  find_webcam_bananas(bd)
