#!/bin/bash

sudo apt update
sudo apt -y install cmake

pip3 install --user psutil
pip3 install --user azure-iot-device
pip3 install --user scikit-build
pip3 install --user opencv-python
pip3 install --user dlib
pip3 install --user geocoder
pip3 install --user imutils
pip3 install --user jsonpickle
pip3 install --user zmq

sudo mkdir -p /opt/intel
sudo wget https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3.1/linux/l_openvino_toolkit_debian9_2022.3.1.9227.cf2c7da5689_arm64.tgz -O openvino_2022.3.1.tgz
sudo tar -xf openvino_2022.3.1.tgz
sudo mv l_openvino_toolkit_debian9_2022.3.1.9227.cf2c7da5689_arm64 /opt/intel/openvino_2022.3.1
cd /opt/intel/openvino_2022.3.1
sudo -E ./install_dependencies/install_openvino_dependencies.sh
sudo ln -s openvino_2022.3.1 openvino_2022

wget https://download.01.org/opencv/2020/openvinotoolkit/2020.3/open_model_zoo/models_bin/1/face-detection-retail-0004/FP16/face-detection-retail-0004.bin -P model/
wget https://download.01.org/opencv/2020/openvinotoolkit/2020.3/open_model_zoo/models_bin/1/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -P model/
wget https://download.01.org/opencv/2020/openvinotoolkit/2020.3/open_model_zoo/models_bin/1/face-reidentification-retail-0095/FP16/face-reidentification-retail-0095.bin -P model/
wget https://download.01.org/opencv/2020/openvinotoolkit/2020.3/open_model_zoo/models_bin/1/face-reidentification-retail-0095/FP16/face-reidentification-retail-0095.xml -P model/
wget https://download.01.org/opencv/2020/openvinotoolkit/2020.3/open_model_zoo/models_bin/1/landmarks-regression-retail-0009/FP16/landmarks-regression-retail-0009.bin -P model/
wget https://download.01.org/opencv/2020/openvinotoolkit/2020.3/open_model_zoo/models_bin/1/landmarks-regression-retail-0009/FP16/landmarks-regression-retail-0009.xml -P model/