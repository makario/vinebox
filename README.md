VineBox
=======

Watch a constant, real-time stream of videos from Vine on your Raspberry Pi!

Instructions
------------
Download all files to a folder on your Raspberry Pi.
Here's a description of what the files do:

* **vine.py** - This file searches Twitter for Vine videos and downloads them to ~/.vine
* **vinelooper.py** - This folder searches ~/.vine for .mp4 videos and plays them with omxplayer
* **update_vine.py** - Add this file to your crontab if you want vine to download periodically. See **crontab.example** for an example.
* **vinelooper.desktop** - Put this file in ~/.config/autostart if you want to loop videos on boot.
* **filelock.py** This prevents omxplayer from hiccuping if an .mp4 is being overwritten while omxplayer is playing it. This file is actually from [here](http://www.evanfosmark.com/2009/01/cross-platform-file-locking-support-in-python/).