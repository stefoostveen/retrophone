# RetroPhone
This project converts a raspberry pi rotary phone into a sip client

## Installation instructions

1. Install some packages

    `sudo apt-get install libasound2-dev libssl-dev libv4l-dev libsdl2-dev libsdl2-gfx-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-net-dev libsdl2-ttf-dev libx264-dev libavformat-dev libavcodec-dev libavdevice-dev libavfilter-dev libavresample-dev libavutil-dev libavcodec-extra libopus-dev libopencore-amrwb-dev libopencore-amrnb-dev libvo-amrwbenc-dev subversion libportaudio2 libatlas-base-dev swig`

2. Download source code 

    `git clone https://github.com/pjsip/pjproject`

3. Configure the project

    `./configure --enable-shared`

4. Build and install pjsip

    `make dep && make clean && make`
    `sudo make install`

5. Build the swig python module
    
    Increase the swapfile if necessary on the raspberry pi: 
    
    `sudo nano /etc/dphys-swapfile` and change `CONF_SWAPSIZE=100` to something larger.
    
    Restart the swapfile: `sudo /etc/init.d/dphys-swapfile restart`
    
    `cd pjsip-apps/src/swig`
    
    `make`

6. Get the project

    `git clone https://gitlab.com/soostveen/retrophone`

7. Copy the built module to the project: copy the contents of `pjsip-apps/src/swig/build/BUILD_NAME` to the `retrophone/venv/lib/python_VERSION_/site-packages` folder

8. Create a python virtual env

    `cd retrophone`
    
    `python3 -m venv venv`

   Activate the venv

    `source venv/bin/activate`

9. Install the other required packages

    `pip install -r requirements.txt`

10. Run the project

    `python3 ./`
