# Fábio Armando

## Tesseract

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

## ADB

On Mac, run `brew install android-platform-tools`.

## Python Packages

Install the following packages using `pip`

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
