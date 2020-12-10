"""
Creates blended interstitial frames between existing frames
of video that have already been split.  Since frames are black
and white and simply an alpha channel, the average grayscale
value for each pixel is taken from adjacent frames to make the
new frame.

"""
# Relevant libary imports
from PIL import Image
from clouds_common import suffix_creator
import os


# Set output directory and file prefix
out_dir = '../results/interim/frames/blends_1'
out_file_prefix = 'cloud_frame_blends'

# Make output directory or skip if it exists
try:
    os.mkdir(out_dir)
except FileExistsError: pass

# Get all the files in the output directory to skip frames already processed
out_list = os.listdir(out_dir)

# Specify source directory and populate list of frames from source to process
source_dir = '../results/interim/frames/from_source'
source_list = os.listdir(source_dir)

# Keep track of whether frames have been skipped due to already having been processed
skipped = False
# Keep track of whether processing has resumed after having skipped
resumed = False

for source_index in range(len(source_list)):
    test_suffix = suffix_creator(source_index * 2)

    # Check whether frame has already been processed
    if (out_file_prefix + test_suffix) in out_list:
        # Set skipped to true first time
        if not skipped:
            skipped = True
        continue # Skip rest of loop and start next iteration

    # Get height and width in number of pixels and save first frame if out_list is empty
    if source_index == 0:
        # Get current frame
        curr_img = Image.open(source_dir + source_list[source_index])
        curr_px = curr_img.load()
        
        # Obtain width and height of video (frame) in pixels
        img_w = curr_img.size[0]
        img_h = curr_img.size[1]

        curr_img.save(out_dir + out_file_prefix + '00000.jpg')
    # Any itertion of loop after first
    else:
        # First frame after resuming frame processing
        if skipped and not resumed:
            prev_img = Image.open(source_dir + source_list[source_index - 1])
            img_w = prev_img.size[0]
            img_h = prev_img.size[1]
            prev_px = prev_img.load()
            resumed = True
        # Any subsequent frames after first after resuming frame processing
        else:
            prev_px = curr_px
        
        # Get current image and pixels
        curr_img = Image.open(source_dir + source_list[source_index])
        curr_px = curr_img.load()

        # Create new frame from original source frame and load new pixels
        new_img = curr_img
        new_px = new_img.load()

        # loop over pixels and average "prev" and "curr" for "new" values
        h_count = 0
        while h_count < img_h:
            # Loop over each pixel along width
            w_count = 0
            while w_count < img_w:
                # Interpolate new grayscale value and apply to pixel
                new_alpha = int((prev_px[w_count, h_count][0] + curr_px[w_count, h_count][0]) / 2)
                new_px.__setitem__((w_count, h_count), (new_alpha, new_alpha, new_alpha))
                # Increment width count
                w_count += 1
            # Increment height count
            h_count += 1
        
        # Properly set file suffix for newly created interstitial frame
        new_new_index = source_index * 2 - 1
        new_new_suffix = suffix_creator(new_new_index)

        # Properly set file suffix for original frame
        new_curr_index = source_index * 2
        new_curr_suffix = suffix_creator(new_curr_index)
        
        # Save newly created frame and original frame in succession
        new_img.save(out_dir + out_file_prefix + new_new_suffix)
        curr_img.save(out_dir + out_file_prefix + new_curr_suffix)

    print('new frame ' + str(source_index) + ' complete') # Provide user feedback      
