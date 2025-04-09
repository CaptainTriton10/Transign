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

1. Download the latest release.


2. Extract the ```.tar``` or ```.zip``` file.


3. Create a virtual environment **within the extracted folder**:

```commandline
virtualenv transign_env
```

5. Activate the virtual environment by running:

```commandline
"transign_env/Scripts/activate.bat"
```

4. Ensure you have the correct python packages installed, by running this command **within the virtual environment**:

``` commandline
pip install -r requirements.txt --no-deps
``` 

**It is important that you use the ```--no-deps``` option, as some packages will have version conflicts.** Also, it will take a while to install all the packages, so don't stop the process if you think it's frozen.

## How to run

Run ```main.py``` from within the virtual environment. After the packages load (which may take 7-12 seconds) the GUI will load.

You can do this with the command:
```commandline
py main.py
```
It is important to note that you will have to restart the virtual environment with ```"transign_env/Scripts/activate.bat"``` if you close the command prompt window.

## Usage

A preview of the webcam will appear in the top left of the GUI. When you hold up your hand and sign letters from the
alphabet, the result shown at the bottom.

The loading bar at the bottom of the webcam will show how long you need to hold the sign for it to be recognised, in
order to control the speed.

You can stop and start the webcam by pressing the ```Stop Webcam``` button.

If the webcam is facing the wrong direction, you can change it using the dropdown below the ```Stop Webcam``` button.

To change the sensitivity of the detecter, you can change the ```Sensitivity``` slider.

## Troubleshooting

If you get the error:

```
RuntimeError: This version of jaxlib was built using AVX instructions, which your CPU and/or operating system do not support. You may be able work around this issue by building jaxlib from source.
```

You can fix it by commenting out ```cpu_feature_guard.check_cpu_features()``` in
```[env name]\lib\site-packages\jax\_src\lib\__init__.py```

