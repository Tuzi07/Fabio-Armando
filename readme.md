# Fábio Armando

## Installation

```
sudo apt-get install android-studio qemu-kvm espeak
```

Add your user to the `kvm` group and restart your machine.

```
sudo apt-get install tesseract-ocr libleptonica-dev libtesseract-dev
```

Move `eng.traineddata` to the `tessdata` folder (normally located at `/usr/share/tesseract-ocr/4.00/tessdata`)

Next, install the following packages using `pip`

```
pyautogui
pyttsx3
tesserocr
pyscreenshot
pyyaml
```

Be sure to enable virtualization on your BIOS or you won't be able to emulate a device.
