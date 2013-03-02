#!/usr/bin/python

import sys
import subprocess
import os

LOG_DIR = os.getenv('HOME') + os.sep + ".vine"

while 1:
    for filename in sorted(os.listdir(LOG_DIR)):
        if filename.endswith(".mp4"):
            if not os.path.exists(filename.replace(".mp4", ".lock")):
                subprocess.call(["omxplayer", LOG_DIR + os.sep + filename])
