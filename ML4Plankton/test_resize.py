from aspect_resize import *
import os

path1 = "/Users/Apple/Desktop/testims" #insert path directory
path2 = '/Users/Apple/Desktop/resims' #insert path directory

listing = os.listdir(path1)
spe = len(listing)
print(listing)
print(spe)

for file in listing:
    img = Image.open(path1 + "/" + file)
    rese = aspect_resize(img, 227)
    imge = Image.fromarray(rese)
    imge.save(path2 + "/" + file)