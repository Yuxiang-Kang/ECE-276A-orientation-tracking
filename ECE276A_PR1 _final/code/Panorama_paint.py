from parameters import dataset
import math


import Quaternion_calculation as qt
import transforms3d as ts3d
import matplotlib.pyplot as plt
import Funcs as F
import autograd
import autograd.numpy as np1
from PIL import Image, ImageDraw




#load data from panorama result
trainset= dataset
print("Dataset:",trainset)
cam_file="../code/mid_data/panorama_cood/cam_mod_dataset_"+trainset+".npy"
cam=np1.load(cam_file)
cyl_s_file="../code/mid_data/panorama_cood/cyl_s_dataset_"+trainset+".npy"
cyl_s=np1.load(cyl_s_file)
T_file="../code/mid_data/panorama_cood/T_dataset_"+trainset+".npy"
T=np1.load(T_file)
print("Data loaded")




#define canvas RGB
canvas=np1.zeros((960,1920,3))
canvas=canvas.astype('int')
i=0
while(i<T):
    j=0
    while(j<240):
        k=0
        while(k<320):
            #print(cam[j,k,0,i])
            canvas[cyl_s[j,k,1,i],cyl_s[j,k,0,i],0]=int(cam[j,k,0,i])
            canvas[cyl_s[j,k,1,i],cyl_s[j,k,0,i],1]=int(cam[j,k,1,i])
            canvas[cyl_s[j,k,1,i],cyl_s[j,k,0,i],2]=int(cam[j,k,2,i])
            #print(canvas[cyl_s[j,k,1,i],cyl_s[j,k,0,i],:])
            k=k+1
            
            
        
        j=j+1
        
    
    i=i+1
    
    print("t=",i-1)
#print(canvas)
pic_file="../code/mid_data/panorama_cood/pic_dataset_"+trainset+".npy"
np1.save(pic_file,canvas)


fig = plt.figure()
im1=plt.imshow(canvas)
plt.show()
#print(canvas.shape)
