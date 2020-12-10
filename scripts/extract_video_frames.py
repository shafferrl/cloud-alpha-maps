"""
Splits a video into is respective frames and
save each frame to image file.

"""
# Relevant library imports
import cv2
from clouds_common import suffix_creator


# Split video file into frames
def frame_capture(in_path, out_path):
    # Path to video file
    vid_obj = cv2.VideoCapture(in_path)
    # Loop counter
    count = 0
    # Variable for checking whether frames are extracted
    success = 1

    # Loop until frames are extracted
    while success:
        success, image = vid_obj.read()
        frame_suffix = suffix_creator(count)
        try:
            cv2.imwrite(out_path +'/frame'+ frame_suffix, image)
            count += 1
        except: break

# Source directory and file
vid_dir = '../sources/video'
vid_file = 'earthcloudvideo.mp4'

# Output directory
out_dir = '../results/interim/frames/from_source'

if __name__ == '__main__':
    frame_capture(vid_dir + '/' + vid_file, out_dir)
