# cloud-alpha-maps
Scripts used to convert time-lapse video of cloud cover on Earth into time-lapse alpha maps of clouds (with frame interpolation).

## Scripts Description ##

The scripts in this repository were used to convert a time-lapse video of cloud cover over a whole-Earth map into black-and-white maps purely of cloud cover, which are also slowed down using a basic frame interpolation technique and were intended to be used as an alpha map to apply a video cloud texture onto a 3D representation of the Earth.

Due to the heavy computational load of analyzing each pixel of each frame during frame interpolation, Python's multiprocessing module was also experimented with in an attempt to speed up processing time.

## Other Files ##

The source video and some results have also been included in the repository, but extracted frames and some output videos have been excluded due to their large size.  These files can also be reproduced from the source video and the scripts herein.

The original video output files were too large to upload to Github and have been compressed using clideo.com, which has applied a watermark to each that has been compressed.
