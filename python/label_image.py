import argparse
import smbus
import sys
import time
import io

import numpy as np
import picamera
from PIL import Image
import RPi.GPIO as gpio
from tensorflow.contrib.lite.python import interpreter as interpreter_wrapper

# GPIO settings
bus = smbus.SMBus(1)
address = 0x04
camera = picamera.PiCamera()

def main(args):
  # Setup GPIO
  gpio.setmode(gpio.BCM)

  # Set up tflite interpreter
  floating_model = False
  interpreter = interpreter_wrapper.Interpreter(model_path=args.model_file)
  interpreter.allocate_tensors()
  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

  # Check the type of the input tensor
  if input_details[0]['dtype'] == np.float32:
    floating_model = True
  # NxHxWxC, H:1, W:2
  height = input_details[0]['shape'][1]
  width = input_details[0]['shape'][2]

  # Initialize camera
  static_count = 0
  # i=0

  while True:
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg')
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    image = Image.open(stream)
    image = image.resize((width, height))
    # image.save(str(i)+'image.jpeg')
    # i = i+1

    # add N dim
    input_data = np.expand_dims(image, axis=0)
    data = np.float32(input_data)
    if floating_model:
      input_data = (np.float32(input_data) - args.input_mean) / args.input_std
    interpreter.set_num_threads(int(args.num_threads))
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run inference
    start_time = time.time()
    interpreter.invoke()
    stop_time = time.time()
    print("time: ", stop_time - start_time)

    bounding_boxes = interpreter.get_tensor(output_details[0]['index'])
    bounding_boxes = np.squeeze(bounding_boxes)
    classes = interpreter.get_tensor(output_details[1]['index'])
    classes = np.squeeze(classes)
    scores =  interpreter.get_tensor(output_details[2]['index'])
    scores = np.squeeze(scores)
    num_real_detections = interpreter.get_tensor(output_details[3]['index'])
    num_real_detections = int(np.squeeze(num_real_detections))
    
    image_center = np.array((0.5, 0.5))
    distances = []
    distance_vectors = []
    for i in range(num_real_detections):
      if scores[i] > 0.10:
        box_center = center(bounding_boxes[i])
        distances.append(l2_dist(box_center, image_center))
        distance_vectors.append(np.subtract(image_center, box_center))
    if len(distances) > 0:
      min_dist_idx = np.argmin(distances)
      if -0.2 < distances[min_dist_idx] < 0.2:
        static_count += 1
      if static_count >=5:
        shoot_water()
        static_count = 0
      else:
        move_camera(distance_vectors[min_dist_idx])
    else:
      static_count = 0

def center(bounding_box):
  """Find the center of a bounding box."""
  ymin = bounding_box[0]
  xmin = bounding_box[1]
  ymax = bounding_box[2]
  xmax = bounding_box[3]
  ymid = ymin/2+ymax/2
  xmid = xmin/2+xmax/2
  return np.array((xmid, ymid))

def l2_dist(v, o):
  """L2 distance between two points."""
  return np.linalg.norm(v-o)

def move_camera(distance_vector):
  """Convert distances from center of image to theta to move pan tilt camera."""
  print("Vector displacement: {}.".format(distance_vector))
  thetas = np.clip(distance_vector*20, -7, 7).astype(int)
  print("Moving cameras by: {}.".format(thetas))
  send_thetas(thetas[0], thetas[1])


def send_thetas(pan_theta, tilt_theta):
  """Send thetas to Arduino to move camera."""
  try:
    encoded_thetas = (pan_theta+8)*16+tilt_theta+8
    bus.write_byte(address, encoded_thetas)
    # print("Arduino answer to RPI: {}".format( bus.read_byte(address)))
  except:
    print("Can't contact Arduino. No biggie, it might be doing something.")

def shoot_water():
  """Sends 0, which will cause Arduino to shoot water."""
  try:
    bus.write_byte(address, 0)
    # print("Arduino answer to RPI: {}".format( bus.read_byte(address)))
  except:
    print("Can't contact Arduino. No biggie, it might be doing something.")

def cleanup():
  """Cleanup upon user interrupt."""
  camera.close()
  gpio.cleanup()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-m", "--model_file", \
    default="/tmp/mobilenet_v1_1.0_224_quant.tflite", \
    help=".tflite model to be executed")
  parser.add_argument("--input_mean", default=127.5, help="input_mean")
  parser.add_argument("--input_std", default=127.5, \
    help="input standard deviation")
  parser.add_argument("--num_threads", default=1, help="number of threads")
  args = parser.parse_args()

  try:
    main(args)
  except KeyboardInterrupt:
    print('Interrupted')
    cleanup()
    sys.exit(0)