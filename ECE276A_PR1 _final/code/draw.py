
import math



import matplotlib.pyplot as plt

import autograd
import autograd.numpy as np1
from PIL import Image, ImageDraw

trainset="2"
pic_file="../code/mid_data/panorama_cood/pic_dataset_"+trainset+".npy"
canvas=np1.load(pic_file)
print(canvas)

fig = plt.figure()
im1=plt.imshow(canvas)
plt.show()
