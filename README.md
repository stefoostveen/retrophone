# RetroPhone
This project converts a raspberry pi rotary phone into a sip client. 
The specific phone is a Heemaf type 1955 bakelite rotary phone, produced for the dutch PTT.

## Installation instructions

1. Install some packages

    `sudo apt-get install libasound2-dev libssl-dev libv4l-dev libsdl2-dev libsdl2-gfx-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-net-dev libsdl2-ttf-dev libx264-dev libavformat-dev libavcodec-dev libavdevice-dev libavfilter-dev libavresample-dev libavutil-dev libavcodec-extra libopus-dev libopencore-amrwb-dev libopencore-amrnb-dev libvo-amrwbenc-dev subversion libportaudio2 libatlas-base-dev swig git python3-dev python3-venv`

2. Download source code 

    Either get it from my gitlab which includes fixes for www-auth headers
    `git clone git@gitlab.com:soostveen/pjproject.git`
    
    Or get it from the original github (without linphone fixes)
    `git clone https://github.com/pjsip/pjproject`

3. Configure the project

    `./configure --enable-shared`
    
    Please note that on some earlier raspberry pis, one should disable libwebrtc due to emmintrin thingies.
    
    `./configure --enable-shared --disable-libwebrtc`

4. Build and install pjsip

    `make dep && make clean && make`
    
    `sudo make install`

5. Build and install the swig python module
    
    Increase the swapfile if necessary on the raspberry pi: 
    
    `sudo nano /etc/dphys-swapfile` and change `CONF_SWAPSIZE=100` to something larger.
    
    Restart the swapfile: `sudo /etc/init.d/dphys-swapfile restart`
    
    `cd pjsip-apps/src/swig`
    
    `make`
    
    Ignore the JAVA error. We don't care for Java.
    
    Install the module:
    
    `sudo make install`

6. Get the project

    `git clone https://gitlab.com/soostveen/retrophone`

8. Create a python virtual env

    `cd retrophone`
    
    `python3 -m venv --system-site-packages venv`

   Activate the venv

    `source venv/bin/activate`

9. Install the other required packages and, depending on the build platform, copy pjsua2 from the swig build location to the venv.

    `pip install -r requirements.txt`
   
    `cp ./pjproject/pjsip-apps/src/swig/python/build/lib.linux-armv7l-3.7/* ./retrophone/venv/lib/python3.7/site-packages/
`

10. Run the project

    `python3 ./`
