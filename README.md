# C++ Cross-compilation of Tflite Binaries
sudo modprobe bcm2835-v4l2
change the model name in label_image
https://github.com/huaxiaozhong1/tensorflow-lite-apps-on-raspberry-pi-3

# Face Detection Model using WIDERFACE
https://github.com/yeephycho/tensorflow-face-detection

# Tensorflow Official Model Zoo
https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md

# Converting Model to .tflite format
https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/running_on_mobile_tensorflowlite.md

toco --graph_def_file=$OUTPUT_DIR/tflite_graph.pb --output_file=$OUTPUT_DIR/detect.tflite --input_shapes=1,320,320,3 --input_arrays=normalized_input_image_tensor --output_arrays='TFLite_Detection_PostProcess','TFLite_Detection_PostProcess:1','TFLite_Detection_PostProcess:2','TFLite_Detection_PostProcess:3' --inference_type=QUANTIZED_UINT8 --mean_values=128 --std_dev_values=128 --change_concat_input_ranges=false --allow_custom_ops

# Google Object Detection API
https://stackoverflow.com/questions/48915003/get-the-bounding-box-coordinates-in-the-tensorflow-object-detection-api-tutorial

Outputs are detection_boxes, detection_classes, detection_scores, and num_detections.

detection_boxes are [ymin, xmin, ymax, xmax].

# Pre-built Tensorflow Binary with Tflite, Multithreading on Armv7l (Rpi 2, 3, 3+)
Pre-built tensorflow binary with lite
https://github.com/PINTO0309/Tensorflow-bin

# Issue Talking About Tflite on Rpi (Multithreading):
https://github.com/tensorflow/tensorflow/issues/21574

# Tensorflow on RPI Original (Deprecated):
https://github.com/samjabrahams/tensorflow-on-raspberry-pi/blob/master/GUIDE.md

# Cross Compiling Tensorflow for Armv6l (Rpi A, A+, Zero) with Multithreading:
https://www.tensorflow.org/install/source_rpi
git clone https://github.com/tensorflow/tensorflow.git
cd tensorflow
git fetch origin pull/25748/head:multithread
git checkout multithread

CI_DOCKER_EXTRA_PARAMS="-e CI_BUILD_PYTHON=python3 -e CROSSTOOL_PYTHON_INCLUDE_PATH=/usr/include/python3.4" \
    tensorflow/tools/ci_build/ci_build.sh PI-PYTHON3 \
    tensorflow/tools/ci_build/pi/build_raspberry_pi.sh PI ONE

# I2C Communication between Rpi and Arduino:
https://dzone.com/articles/arduino-and-raspberry-pi-working-together-part-2-now-with-i2