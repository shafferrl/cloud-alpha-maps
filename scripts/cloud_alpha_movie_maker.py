"""
Makes an MP4 video file by stitching individual
frames together.

"""
# Relevant libary imports
import cv2
import os


# Target directory and file
target_dir = '../results/final/video'
target_file = 'cloud_alpha_multi_blended.mp4'

# Source directory list of frame files
source_dir = ''
source_list = os.listdir(source_dir)

frame_rate = 28 #fps

# Loop through each frame and add to video
for source_index in range(len(source_list)):
    vid_jpg = cv2.imread(source_dir + source_list[source_index])

    # Set size of video on first loop iteration
    if source_index == 0:
        height, width, layers = vid_jpg.shape
        size = (width, height)
        cloud_alpha_video = cv2.VideoWriter(target_dir + target_file, 0, frame_rate, size)
    
    # Write frame to video and provide user feedback
    cloud_alpha_video.write(vid_jpg)
    print('Frame ' + str(source_index + 1) + ' written')

# Tie up loose ends
cloud_alpha_video.release()
cv2.destroyAllWindows()
