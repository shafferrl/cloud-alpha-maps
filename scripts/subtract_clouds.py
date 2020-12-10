"""
Produces an image of the Earth after subtracting clouds to the
greatest extent possible by finding the pixels with the lowest 
R + G + B value in a series of frames.  The white or near-white
color of clouds will always add to the frame's R + G + B value
and make it possible to find the frame with the least cloud
cover over each pixel.

"""
# Relevant libary imports
from PIL import Image
import os


# Target directory and file
target_dir = '../results/interim/img'
target_file = 'earth_without_clouds.jpg'

# Make target directory unless it already exists
try:
    os.mkdir(target_dir)
except FileExistsError: pass

# Specify directory from which to gather frames
frames_dir = '../results/interim/frames/from_source'
frame_images = os.listdir(frames_dir)

# Open first frame as Image object and load pixels
base_img = Image.open(frames_dir + '/' + frame_images[0])
base_px = base_img.load()

# Get width and height of image in pixels
img_w = base_img.size[0]
img_h = base_img.size[1]

# Loop through each frame in source directory
frame_count = 0
for frame in frame_images:
    # Make sure image is right file type
    if frame.endswith('.jpg'):
        # Create Image object from frame image and load pixels
        img_obj = Image.open(frames_dir + '/' + frame)
        img_px = img_obj.load()
        
        # Loop through the number of lines of pixels along image height
        h_count = 0
        while h_count < img_h:
            # Loop through each pixel along image width in a line of pixels
            w_count = 0
            while w_count < img_w:
                # Get pixel RGB values and add together
                px_rgb = img_px[w_count, h_count]
                rgb_total = px_rgb[0] + px_rgb[1] + px_rgb[2]

                # Get the RGB values of the base image and add together
                base_rgb = base_px[w_count, h_count]
                base_total = base_rgb[0] + base_rgb[1] + base_rgb[2]

                # Save pixel RGB to base image pixel if the R + G + B value is lowest thus far
                if rgb_total < base_total:
                    base_px.__setitem__((w_count, h_count), (px_rgb[0], px_rgb[1], px_rgb[2]))
                    
                # Increment pixel index in line 
                w_count += 1
                
            # Increment pixel line index along height
            h_count += 1

    # Increment frame count and provide user feedback
    frame_count += 1
    print('frame ' + str(frame_count) + ' complete')

# Save resulting image
base_img.save(target_dir + '/' + target_file)
