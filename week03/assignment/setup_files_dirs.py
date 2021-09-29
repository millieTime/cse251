"""
CSE251
Program to split videos into individual files
"""

import os
import platform

def create_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def create_images(video_file, folder):
    # limit the number of frames to 300
    if platform.system() == 'Windows':
        command = rf'ffmpeg -i {video_file} -vframes 300 {folder}/image%3d.png'
    else:
        command = rf'./ffmpeg -i {video_file} -vframes 300 {folder}/image%3d.png'
    os.system(command)

def main():
    do_rickroll = input("Do Rickroll? (y/n): ")
    if do_rickroll == 'y':
        if not os.path.exists('rickroll.mp4'):
            print('No rickroll file found, download one from https://ir.stonybrook.edu/xmlui/bitstream/handle/11401/9656/rickroll.mp4')
            print("Then run the following command: ./ffmpeg -i rickroll.mp4 -vf scale=1280:720 rickroll.mp4")
            return
        else:
            create_dir('rickroll')
            create_images('rickroll.mp4', 'rickroll')
    else:
        create_dir('elephant')
        create_images('elephants.mp4', 'elephant')
    # Create sub folders 
    create_dir('green')
    create_dir('processed')

    # Create the image files
    create_images('green.mp4', 'green')

main()
