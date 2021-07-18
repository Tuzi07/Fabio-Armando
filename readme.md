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
opencv-python
imutils
Pillow
```

# Configuration

## Emulator

Be sure to enable virtualization on your BIOS or you won't be able to emulate a device.

Open `android-studio`, create a project and open the AVD Manager section. Create a new virtual device and choose one with Play Store enabled. You may want to configure this virtual device a bit more, to put it in landscape mode and remove the device frame.

After you check that the emulator works, you can ditch `android-studio` and run the emulator by itself by looking for the emulator program in `~/Android/Sdk/emulator/emulator` and running `./emulator -list-avds`, copying the AVD name of your device and running `./emulator -avd {name}`

## Config File

There are a few important pixels on your screen that Fábio needs to know before he can work. Those are the boxes where the gold, elixir and dark elixir quantities are shown and the next button. You can find these values by using `xdotool getmouselocation`.

For the eagle recognition to work, you also need to define a scale. There is no easy way to do this. For now, you need to actually open the `eagle.py` file and program something to look for the best match yourself, and use this number.
