"""
Takes an image that shows the Earth without any clouds--which was 
generated from a timelapse video of cloud cover on Earth, from which
the frames were also obtained--and compares the relative total 
R + G + B values of each pixel from the map showing Earth's surface to 
the map in each frame to ascertain the amount of cloud cover and therefore 
appropriate alpha (grayscale) value for an Earth cloud texture.

"""
# Relevant libary imports
from PIL import Image
import os


# Target directory and file prefix
target_dir = ''
target_file_prefix = 'cloud_alpha_frame'

# Make target directory if it doesn't exist
try:
    os.mkdir(target_dir)
except FileExistsError: pass

# Specify Earth surface map
surface_file = '/earth_without_clouds.jpg'

# Source directory for frames and list of their file names
frames_dir = ''
frame_images = os.listdir(frames_dir)

# Open surface image and get pixels
surface_img = Image.open(surface_file)
surface_px = surface_img.load()

# Get height and width of image in pixels
img_w = surface_img.size[0]
img_h = surface_img.size[1]

# Highest possible R+G+B value (fully opaque pixel)
opaque_total = 255 * 3

# Loop through each frame in source directory and extract clouds
frame_count = 0
for frame in frame_images:
    # Check whether file is correct format
    if frame.endswith('.jpg'):
        # Open frame as Image object and load pixels
        img_obj = Image.open(frames_dir + frame)
        img_px = img_obj.load()

        # Create a new image object from frame and also load pixels of new image
        new_img = img_obj
        new_px = new_img.load()
        
        # Loop through the number of lines of pixels along image height
        h_count = 0
        while h_count < img_h:
            # Loop through each pixel along image width in a line of pixels
            w_count = 0
            while w_count < img_w:
                # Get the RGB values of the frame's pixel and add together
                px_rgb = img_px[w_count, h_count]
                rgb_total = px_rgb[0] + px_rgb[1] + px_rgb[2]

                # Get the RGB values of the surface map pixel and add together
                surface_rgb = surface_px[w_count, h_count]
                surface_total = surface_rgb[0] + surface_rgb[1] + surface_rgb[2]

                # Find the difference in R+G+B between completely white and the Earth surface map
                transparent_difference = opaque_total - surface_total
                relative_transparency = (rgb_total - surface_total)/transparent_difference

                # Set the alpha (grayscale) to apply to the pixel
                alpha_rgb = int(relative_transparency * 255)

                # Set alpha (grayscale) of new pixel
                new_px.__setitem__((w_count, h_count), (alpha_rgb, alpha_rgb, alpha_rgb))

                # Increment pixel index in line  
                w_count += 1

            # Increment pixel line index along height
            h_count += 1

        # Save new image to target directory and with index suffix
        new_img.save(target_dir + target_file_prefix + frame[-7:])
    
    # Increment frame count and provide user feedback
    frame_count += 1
    print('frame ' + str(frame_count) + ' complete')                
