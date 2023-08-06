# CICV
A Common Interface for OpenCV.

# Support Input
|   Type        |   Describe
|   ---         |   ---
|   Image       |   Image file path.
|   Video       |   Video file path.
|   Directory   |   The directory has several images.
|   V4L2        |   Physical Camera.
|   RTSP        |   RTSP Streaming url.

# Pre-requirements
* [Docker](https://docs.docker.com/engine/install/ubuntu/).
* Python >= 3.8

# Python requirements
```bash
# Install virtualenv and wrapper
$ sudo apt-get install python3-pip
$ sudo pip3 install virtualenv
$ sudo pip3 install virtualenvwrapper

# Add into environment
$ which virtualenvwrapper.sh
$ vim ~/.bashrc
 
export WORKON_HOME=~/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source ~/.bashrc

# Activate Virtualenv
$ mkvirtualenv cicv

# Install OpenCV
$ pip3 install opencv-python build
```

# Getting Started
```bash
sudo docker run cicv:v0.0.1 python3 main.py
```

# Build Docker Image from Dockerfile
```bash
sudo docker build -f ./docker/Dockerfile -t cicv:v0.0.1 .
```

# Distribution
```bash
python setup.py sdist bdist_wheel

```