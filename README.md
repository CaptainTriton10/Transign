# Transign

***

## Introduction

Transign is a GUI based sign language (ASL) interpreter that can read the alphabet from your webcam.

## Setup

| Python Version | Support   |
|:---------------|:----------|
| 3.12           | ❌         |
| 3.11           | *Unknown* |
| 3.10           | ✅         |
| 3.9            | ✅         |
| < 3.9          | *Unknown* |

1. Create a virtual environment:

2. Ensure you have the correct python packages installed, by running: <br>

``` commandline
pip install -r requirements.txt
``` 

## How to run

Run ```main.py``` in ```./Code/Main/v2``` from within the virtual environment. After the packages load, the GUI will
load.

## Usage

A preview of the webcam will appear in the top left of the GUI. When you hold up your hand and sign letters from the
alphabet, the result shown at the bottom.

The loading bar at the bottom of the webcam will show how long you need to hold the sign for it to be recognised, in
order to control the speed.

You can stop and start the webcam by pressing the ```Stop Webcam``` button.

If the webcam is facing the wrong direction, you can change it using the dropdown below the ```Stop Webcam``` button.

To change the sensetivity of the detecter, you can change the ```Sensetivity``` slider.