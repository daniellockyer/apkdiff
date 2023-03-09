# apkdiff

## Overview
Diff two versions of an APK. Useful for seeing what changes have been made after an update.

The output is currently in a 'git diff'-style but there are plans for HTML reports.

## Setup
There are a few required dependancies. The versions that have I have personally ran against are listed, but other versions most likely work as well.

### Required Dependencies:
- [Python](https://www.python.org/downloads/release/python-3112/) 3.11.2
- [apktool](https://ibotpeaches.github.io/Apktool/install/) 2.7.0

### Optional Dependencies:
- [Meld](https://meldmerge.org/) 3.22.0 - Required for the `-m` flag.

## Usage
Clone the repo and run `python apkdiff.py -h` to see all the options.

## Example output
![image](https://user-images.githubusercontent.com/964245/130408874-28b8896f-7e92-42e2-8d06-92938cd44ac2.png)
