# Herobot... another one :)

To install the bot it requires pyscreenshot, cv2, pytesseract, numpy and pyuserinput. In debian/ubuntu:

	sudo apt-get install python-pip python-numpy python-opencv tesseract-ocr tesseract-ocr-eng git python-xlib
	sudo pip install pyscreenshot pytesseract numpy pyuserinput enum34
	git clone https://github.com/0xorial/herobot.git
	cd herobot

Make sure the whole clicker heroes window is open in a web browser, then enter: 

	./herobot.py

Clicking can paused/resumed it by pressing 'p' key.

If you use you will probably need to modify source code, since I wrote it just for my ancients configuration, not bothering much about any kind of AI.

