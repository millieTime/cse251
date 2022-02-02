"""
CSE251
Program to create final video from images
"""

import os
import platform

def stitch_video():
    # the folder "resources/processed" must exist
    if not os.path.exists('resources/processed'):
        print('\nERROR: the folder "resources/processed" doesn\'t exist\n')
        return 

    if platform.system() == 'Windows':
        command = r'ffmpeg -y -i resources/processed/image%3d.png final.mp4'
    else:
        command = r'./ffmpeg -y -i resources/processed/image%3d.png final.mp4'

    os.system(command)

    print('\nThe video file final.mp4 has been created\n')
    print('Do NOT submit this video for your assignment!!')

stitch_video()
