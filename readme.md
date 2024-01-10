# Fábio Armando

Trained models to extract key information of enemy bases in a certain game.

Demo of OCR model extracting the amount of loot available in a base:

https://github.com/Tuzi07/Fabio-Armando/assets/37273687/60fe6fe5-f6fe-4488-aa47-9f0b9c7d8541

Demo of object detection of the Inferno Tower structure:

https://github.com/Tuzi07/Fabio-Armando/assets/37273687/ca04d3fb-3e6c-4b18-9d38-8cc003477d21

## Install Tesseract

On Linux:
```
sudo apt-get install tesseract-ocr libleptonica-dev libtesseract-dev
```

On Windows, install Tesseract running the latest installer. It can be found [here](https://github.com/UB-Mannheim/tesseract/wiki).

On Mac, run `brew install tesseract`.

Move `eng.traineddata` to the `tessdata` folder.

Normally located at:
- Linux: `/usr/share/tesseract-ocr/4.00/tessdata`
- Windows: `C:\Program Files\Tesseract-OCR\tessdata`
- Mac: `/opt/homebrew/Cellar/tesseract/5.3.3/share/tessdata/`

## Install ADB

On Mac, run `brew install android-platform-tools`.

## Install Python Packages

Install the following packages using `pip`:

```
pytesseract
torch
torchvision
opencv-python
pandas
ultralytics
```

## Config File

You must have a `main.py` and a `screen_config.py` to run Fábio. Check out the samples in `sample_mains` and `sample_screen_configs`.
