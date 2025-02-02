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
        if not os.path.exists('resources/rickroll.mp4'):
            print('No rickroll file found, download one from https://ir.stonybrook.edu/xmlui/bitstream/handle/11401/9656/rickroll.mp4')
            print("Then run the following command: ffmpeg -i rickroll.mp4 -vf scale=1280:720 rickroll.mp4")
            return
        else:
            create_dir('resources/rickroll')
            create_images('resources/rickroll.mp4', 'resources/rickroll')
    else:
        create_dir('resources/elephant')
        create_images('resources/elephants.mp4', 'resources/elephant')
    # Create sub folders 
    create_dir('resources/green')
    create_dir('resources/processed')

    # Create the image files
    create_images('resources/green.mp4', 'resources/green')

main()
