"""
Experimenting with the multiprocessing module in attempt to
speed up the processing time of video frames by utilizing
multiple hardware threads.

Creates blended interstitial frames between existing frames
of video that have already been split.  Since frames are black
and white and simply an alpha channel, the average grayscale
value for each pixel is taken from adjacent frames to make the
new frame.

"""
# Relevant libary imports
from PIL import Image
from clouds_common import suffix_creator
import os, time, multiprocessing


# Set output directory and file prefix
out_dir = ''
out_file_prefix = 'cloud_frame_blends'

# Make output directory or skip if it exists
try:
    os.mkdir(out_dir)
except FileExistsError: pass

# Specify source directory and populate list of frames from source to process
source_dir = ''
source_list = os.listdir(source_dir)

# Declare global variable for total duration
duration = None

# Initialize global index so that multiple processes can coordinate
global_index = 0


# Define class that inherits from multiprocessing.Process class
class ImgProcProcess(multiprocessing.Process):
    # Override the "run" method from the multiprocessing "Process" class
    def run(self):
        global global_index, duration

        # Set width and height in pixels from first frame in source directory
        reference_img = Image.open(source_dir + source_list[0])
        reference_px = reference_img.load()
        img_w = reference_img.size[0]
        img_h = reference_img.size[1]
        
        # Loop through all the frames in the source list
        for source_index in range(len(source_list)):
            source_index = global_index
            global_index += 1
            
            if source_index == 0:
                # Get first frame and load pixels
                curr_img = Image.open(source_dir + source_list[source_index])
                curr_px = curr_img.load()

                # Save first frame without further processing
                curr_img.save(out_dir + out_file_prefix + '00000.jpg')
            elif source_index == 200:
                duration = time.time() - start_time
                break
            elif source_index > 200:
                break
            else:
                # Get the previous image and pixels for interpolation
                prev_img = Image.open(source_dir + source_list[source_index - 1])
                prev_px = prev_img.load()
                
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
            print('new frame ' + str(source_index) + ' completed via ' + self.name)


# Set the total number of processes and populate list of ImgProcProcess objects
no_processes = 4 
process_list = [ImgProcProcess() for i in range(no_processes)]

# Start the processes
start_time = time.time()
for img_process in process_list:
    if __name__ == '__main__':
        img_process.start()
