import glob
import os
from os import system
from platform import system as plsys

op_sys = plsys()
if 'Windows' in str(op_sys) or 'Linux' in str(op_sys):
    from getpass import getuser as _getuser
elif 'Darwin' in str(op_sys):
    import pwd

import re
from pathlib import Path

import ffmpeg
import pyperclip
from pytube.cli import on_progress
import pytube

# def clear(): 
#     if name == 'nt': 
#         _ = system('cls') 
#     else: 
#         _ = system('clear')
global base_path

base_path = "0"
if op_sys == 'Windows':
    base_path = str(f"C:\\Users\\{_getuser()}\\Videos")
elif op_sys == 'Linux':
    base_path = str(f"/home/{_getuser()}/Videos")
elif op_sys == 'Darwin':
    base_path = str(f"/Users/{pwd.getpwuid( os.getuid() )[ 0 ]}/Movies")
else:
    print("""I am very sorry for the inconvenience, but I haven't added support for your operating system yet,
    as I don't know the proper method of finding the active user's username using Python in your given OS.
    
    If you'd like to modify this script to include your OS for your personal use, please feel free to do so.""")
    print(input("Press Enter to exit."))
    exit()

Path(f'{base_path}').mkdir(parents=True, exist_ok=True)

def find_files(filename, search_path):
    os.chdir(f"{search_path}")
    for file in glob.glob(f"{filename}"):
        return file

def cleanup(filename, search_path):
    os.chdir(f"{search_path}")
    for file in glob.glob(f"{filename}"):
        os.remove(file)

url_one = pyperclip.paste()
str(url_one)

def good_format():
    try:
        if "https://www.youtube.com/" in url_one:
            return True
    except:
            return False

def clean_filename_windows(filename):
    
    illegal_start_names = "CON, PRN, AUX, NUL, COM1, COM2, COM3, COM4, COM5, COM6, COM7, COM8, COM9, LPT1, LPT2, LPT3, LPT4, LPT5, LPT6, LPT7, LPT8, LPT9".replace(" ","").split(",")
    illegal_chars = "\<\>\[\]\{\}\:\"\/\\\|\?\*"
    
    filename = str(filename)
    clean_name = ""
    
    for char in filename:
        if char in illegal_chars:
            clean_name+="-"
        else:
            clean_name+=str(char)
    
    for illegal_name in illegal_start_names:
        if clean_name.startswith(illegal_name):
            clean_name = "_"+clean_name
            break
    
    return clean_name

def STREAM_V():
    for v in video.streams.filter(adaptive=True, only_video=True).order_by("resolution").desc():
        if 'type="video"' in str(v) and ('res="1080p"' in str(v) or 'res="720p"' in str(v) or 'res="480p"' in str(v) or 'res="360p"' in str(v) or 'res="240p"' in str(v) or 'res="144p"' in str(v)) and 'res="None"' not in str(v):
            print(str(v))
            my_string = f"{v}"
            itag = re.search(r'itag=\"(\d+)\"', my_string)
            v = video.streams.get_by_itag(itag.group(1))
            break
    os.chdir(f"{base_path}")
    print(f'Downloading "{title}" (video)('+my_string+')...')
    v.download(filename=f"{title}_video")
    print('Done downloading video.')

def STREAM_A():
    for a in audio.streams.filter(adaptive=True, only_audio=True).order_by("abr").desc():
        if 'type="audio"' in str(a):
            my_string = f"{a}"
            result = re.search(r'itag=\"(\d+)\"', my_string)
            a = audio.streams.get_by_itag(result.group(1))
            break
    os.chdir(f"{base_path}")
    print(f'Downloading "{title}" (audio)('+my_string+')...')
    a.download(filename=f"{title}_audio")
    print('Done downloading audio.')

def COMBINE():
    os.chdir(f"{base_path}")
    print('Beginning combining video and audio sources.')
    vid = ffmpeg.input(f'{v_ext}')
    aud = ffmpeg.input(f'{a_ext}')
    out = ffmpeg.output(vid, aud, f'{title}.mkv', vcodec='copy', acodec='copy', strict='experimental')
    overwrite = ffmpeg.overwrite_output(out)
    overwrite.run()
    print('Finished combining video and audio sources.')

if good_format():
    video = pytube.YouTube(url_one, on_progress_callback=on_progress)
    audio = pytube.YouTube(url_one, on_progress_callback=on_progress)
    title = f'{clean_filename_windows(video.title)}'
    print(str(title))
    if f"{title}.mkv" not in str(f'{find_files(f"{title}.mkv", f"{base_path}")}'):
        STREAM_V()
        STREAM_A()
        v_ext = f'{find_files(f"{title}_video.*", f"{base_path}")}'
        a_ext = f'{find_files(f"{title}_audio.*", f"{base_path}")}'
        COMBINE()
        cleanup(f"{v_ext}", f"{base_path}")
        cleanup(f"{a_ext}", f"{base_path}")
    else:
        print('Error: combined video file already exists; Exiting.')
        exit()
else:
    print('Error: Not good URL format; Exiting.')
exit()
