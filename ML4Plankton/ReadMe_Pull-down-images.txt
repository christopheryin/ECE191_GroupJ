For downloading images from the website, we run 'pull_unlabled_spcdata2_1.py'.
The code should be run under Python 2 (doesn't work under Python 3).
For running 'pull_unlabled_spcdata2_1.py', we need to create a TXT file which includes the parameters of the images that we are looking for from the website.
The TXT file should be saved in the same directory of 'pull_unlabled_spcdata2_1.py'.
The information of the TXT file should be like this:
e.g. 2016-05-16 09:00:00 2016-05-16 12:59:59 0.04 5 SPCP2 Any (For downloading all the images)
e.g. 2016-05-16 09:00:00 2016-05-16 12:59:59 0.04 5 SPCP2 Sand (For downloading just sand images)
For downloading the images of another time slot, just change the date & time, but keep the format.

And when we run the code, the command should be like this:
python 'full name of the TXT file' 'full path of the folder that contains the downloaded images'