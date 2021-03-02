PyTube Video Downloader

Windows setup:

1. Extract into "C:\Users\Public\Documents\PTD".
2. Copy "PTD.lnk" (shortcut) and paste wherever is convenient for you; personally, I prefer to "Pin to Taskbar" on the "PTD.lnk".

Linux or OSX setup:

1. Either execute the PTD.py script in the Terminal directly, make an executable shortcut, or some other method allowed by your OS.

Usage:

1. Copy the YouTube URL of a video to be downloaded.
2. Run the program with the included shortcut, the .exe in "/scripts" directly, or however best suits you for your given OS.
3. It will download the video to "C:\Users\\[username]\Videos" as separate audio and video files, then muxes them together in MKV Video format using FFMPEG (which you'll also need to install if you haven't already).

   Note (Windows): if you add ".LNK;" to the end of the Environment Variable "PATHEXT" and then paste the shortcut into a directory in "PATH", you can run this from from any console or from the Run dialog by entering PTD.

Created by Alaester Nikolai Modern.

.exe compiled with BAT To EXE Converter; .bat included as source code for inquiring minds.

Licensed under MIT License.
