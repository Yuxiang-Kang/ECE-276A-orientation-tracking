#imu数据包含2个类'vals'和'ts'
#vicd数据包含两个类'rots'和'ts'
from parameters import dataset
import math

from load_data import camd, imud, vicd
import Quaternion_calculation as qt
import transforms3d as ts3d
import matplotlib.pyplot as plt
import Funcs as F
import autograd
import autograd.numpy as np1



print("current dataset:",dataset)
len_imu=len(imud['ts'][0])
ang_vel=np1.zeros((len_imu,3),dtype=float)
q=np1.zeros(((len_imu),4))
tau_imu=np1.zeros(len_imu-1,dtype=float)
eul_imu_ang=np1.zeros(((len_imu),3),dtype=float)
acc_imu=np1.zeros((len_imu,3),dtype=float)
h=np1.zeros((len_imu,3),dtype=float)

#len_vic=len(vicd['ts'][0])
#eul_vic_ang=np1.zeros(((len_vic),3))

sc_ft_ang=3300/1023*(math.pi)/180/3.33
sc_ft_acc=3300/1023/300

q[0][0]=1.








#定义角速度ω，共t项,定义时间间隔tau_imu，共t-1项，并进行前处理
i=0
while(i<len_imu):
    ang_vel[i,0]=imud['vals'][4,i]*sc_ft_ang
    ang_vel[i,1]=imud['vals'][5,i]*sc_ft_ang
    ang_vel[i,2]=imud['vals'][3,i]*sc_ft_ang
    acc_imu[i,0:2]=imud['vals'][0:2,i]*sc_ft_acc*(-1)
    acc_imu[i,2]=imud['vals'][2,i]*sc_ft_acc
    if(i<(len_imu-1)):
        tau_imu[i]=(imud['ts'][0,i+1]-imud['ts'][0,i])
    i=i+1

#对前100项取平均计算bias

bias_ang_x=np1.average(ang_vel[0:100,0])
bias_ang_y=np1.average(ang_vel[0:100,1])
bias_ang_z=np1.average(ang_vel[0:100,2])
bias_acc_x=np1.average(acc_imu[0:100,0])
bias_acc_y=np1.average(acc_imu[0:100,1])
bias_acc_z=np1.average(acc_imu[0:100,2])
print(bias_ang_x)
print(bias_ang_y)
print(bias_ang_z)


#对ang_vel减去bias

i=0
while(i<len_imu):
    ang_vel[i,0]=ang_vel[i,0]-bias_ang_x
    ang_vel[i,1]=ang_vel[i,1]-bias_ang_y
    ang_vel[i,2]=ang_vel[i,2]-bias_ang_z
    acc_imu[i,0]=acc_imu[i,0]-bias_acc_x
    acc_imu[i,1]=acc_imu[i,1]-bias_acc_y
    acc_imu[i,2]=acc_imu[i,2]-bias_acc_z+1
    i=i+1

#通过quaenion计算pitch, roll, yaw,eul_imu_ang[i]=[pitch, roll, yaw]

i=0
while(i<len_imu-1):

    q[i+1]=F.quat2next(q[i],tau_imu[i],ang_vel[i])
    eul_imu_ang[i+1]=ts3d.euler.quat2euler(q[i+1])
    i=i+1



#使用vicd数据计算pitch, roll, yaw
#print(imud['vals'])
'''
i=0
while(i<len_vic):
    eul_vic_ang[i]=ts3d.euler.mat2euler(vicd['rots'][:,:,i])
    i=i+1
'''
#使用quaternion计算h(t)
i=0
while(i<len_imu):
    h[i]=F.quat2acc(q[i])[1:4]
    i = i+1

#save q ,tau, ang_vel,len_imu

qfile="../code/mid_data/q_"+dataset+"_unoptimized.npy"
taufile="../code/mid_data/tau_"+dataset+".npy"
angfile="../code/mid_data/ang_vel_"+dataset+".npy"
lenfile="../code/mid_data/len_imu_"+dataset+".npy"
accfile="../code/mid_data/acc_imu_"+dataset+".npy"
vicangfile="../code/mid_data/ang_vic_"+dataset+".npy"
len_vicfile="../code/mid_data/len_vic_"+dataset+".npy"
len_imufile="../code/mid_data/len_imu_"+dataset+".npy"
qangfile="../code/mid_data/qang_"+dataset+".npy"
np1.save(qfile,q)
np1.save(taufile,tau_imu)
np1.save(angfile,ang_vel)
np1.save(lenfile,len_imu)
np1.save(accfile,acc_imu)
#np1.save(vicangfile,eul_vic_ang)
#np1.save(len_vicfile,len_vic)
np1.save(len_imufile,len_imu)
np1.save(qangfile,eul_imu_ang)


