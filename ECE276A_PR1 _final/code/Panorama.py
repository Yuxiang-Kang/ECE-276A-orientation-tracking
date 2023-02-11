#imu数据包含2个类'vals'和'ts'
#vicd数据包含两个类'rots'和'ts'
#camd数据包含两个类'cam'和'ts'，前者为240*320*3*T矩阵
from parameters import dataset
import math

from load_data import camd, imud, vicd
import Quaternion_calculation as qt
import transforms3d as ts3d
import matplotlib.pyplot as plt
import Funcs as F
import autograd
import autograd.numpy as np1
#import autograd.numpy
#import numpy as np1
from PIL import Image, ImageDraw




#load optimized orientation data
trainset=dataset
generation="100"
q_optfile="../code/mid_data/optimized_q_dataset_"+trainset+"/qop_gen_"+generation+"dataset_"+trainset+".npy"
q_opt=np1.load(q_optfile)



print("Dataset:",dataset)
#match imud and q with camd
len_imu=len(imud['ts'][0])
len_cam=len(camd['ts'][0])
match_seq=np1.arange(len_cam)
i=0
j=0
while(i<len_imu and j<len_cam):
    if(imud['ts'][0,i]<camd['ts'][0,j]):
        if(i==0):
            cam_start=j           
        i=i+1
    else:
        match_seq[j]=i
        j=j+1
    if(i==0):
        print("cam starts early")
    if(i==len_imu):
        print("cam ends late")
        cam_end=j-1
    else:
        cam_end=len_cam-1
match_seq_modified=match_seq[cam_start:(cam_end+1)]
q_opt_modified=q_opt[match_seq_modified,:]
T=len(match_seq_modified)

T_file="../code/mid_data/panorama_cood/T_dataset_"+trainset+".npy"
np1.save(T_file,T)



#modify camd data in range of imud      
camd_modified=camd['cam'][:,:,:,cam_start:(cam_end+1)]
print("camd_modified shape:",camd_modified.shape)




#create rotation matrix sequence
R=np1.zeros((T,3,3))
k=0
while(k<T):
    R[k,:,:]=ts3d.quaternions.quat2mat(q_opt_modified[k,:])
    k=k+1
k=0




#reset sphere coordinate(lamda phi 1)
sphere_b=np1.zeros((240,320,3));
i=0
while(i<240):
    j=0
    while (j<320):
        sphere_b[i,j,:]=np1.array([(-math.pi/6+math.pi/960*(0.5+j)),(math.pi/8+math.pi/960*(-0.5-i)) ,1.])
        j=j+1
    i=i+1




#convert sphere coordinate to cartisian
cart_b=np1.zeros((240,320,3));
i=0
while(i<240):
    j=0
    while (j<320):
        cart_b[i,j,:]=np1.array([(math.cos(sphere_b[i,j,1])*math.cos(sphere_b[i,j,0])), (math.cos(sphere_b[i,j,1])*math.sin(sphere_b[i,j,0])), math.sin(sphere_b[i,j,1])])
        j=j+1
    i=i+1


#print("R="R)

#for each Rt,calculate R@cart_b, to get 240*320*3*T (x,y,z)s
i=0
cart_s=[]
while(i<T):
    cart_b_mult=cart_b.reshape(240,320,3,1)
    cart_s_0=np1.matmul(R[i,:,:],cart_b_mult)
    cart_s_1=cart_s_0.reshape(240,320,3)
    cart_s.append(cart_s_1)
    i=i+1
cart_s=np1.stack(cart_s,axis=-1)

    

#print(cart_s)


#convert the (x,y,z)in world frame to sphere,then convert to cylinder coordinates
canvas=np1.arange(960*1920*3).reshape(960,1920,3)
sph_s=np1.arange(240*320*3*T).reshape(240,320,3,T)
sph_s=sph_s.astype('float32')
cyl_s=np1.arange(240*320*2*T).reshape(240,320,2,T)
cyl_s=cyl_s.astype('int')
i=0
while(i<T):
    j=0
    while(j<240):
        k=0
        while(k<320):
            if(cart_s[j,k,0,i]>0):                          #x>0
                if(cart_s[j,k,1,i]==0):
                    sph_s[j,k,0,i]=0
                elif(cart_s[j,k,1,i]>0):                    #y>0
                    sph_s[j,k,0,i]=math.atan((cart_s[j,k,1,i]/cart_s[j,k,0,i]))
                else:                                       #y<0
                    sph_s[j,k,0,i]=math.atan((cart_s[j,k,1,i]/cart_s[j,k,0,i]))+2*math.pi   
            else:                                           #x<=0
                if(cart_s[j,k,1,i]==0):
                    sph_s[j,k,0,i]=math.pi
                else:
                    sph_s[j,k,0,i]=math.atan((cart_s[j,k,1,i]/cart_s[j,k,0,i]))+math.pi
            sph_s[j,k,1,i]=math.acos(cart_s[j,k,2,i])
            sph_s[j,k,2,i]=1.
                                                            #convert to cylinder
            cyl_s[j,k,0,i]=math.floor(sph_s[j,k,0,i]/(2*math.pi)*1919)
            cyl_s[j,k,1,i]=math.floor(sph_s[j,k,1,i]/(math.pi)*959)

            k=k+1
        j=j+1
    i=i+1
    print("t=:",i-1)
    
#print(cyl_s[0,0,0,0])
#print(camd_modified[0,0,:,0])

cam_mod_file="../code/mid_data/panorama_cood/cam_mod_dataset_"+trainset+".npy"
np1.save(cam_mod_file,camd_modified)
cyl_s_file="../code/mid_data/panorama_cood/cyl_s_dataset_"+trainset+".npy"
np1.save(cyl_s_file,cyl_s)


