#from parameters import dataset
import math

from load_data import camd, imud, vicd
import Quaternion_calculation as qt
import transforms3d as ts3d
import matplotlib.pyplot as plt
import Funcs as F
import autograd
import autograd.numpy as np1





#load data from main
trainset="6"
generation="49"
qfile="../code/mid_data/q_"+trainset+"_unoptimized.npy"
taufile="../code/mid_data/tau_"+trainset+".npy"
angfile="../code/mid_data/ang_vel_"+trainset+".npy"
lenfile="../code/mid_data/len_imu_"+trainset+".npy"
accfile="../code/mid_data/acc_imu_"+trainset+".npy"
q_optfile="../code/mid_data/optimized_q_dataset_"+trainset+"/qop_gen_"+generation+"dataset_"+trainset+".npy"
ang_vicfile="../code/mid_data/ang_vic_"+trainset+".npy"
len_vicfile="../code/mid_data/len_vic_"+trainset+".npy"
#len_imufile="../code/mid_data/len_imu_"+trainset+".npy"
qangfile="../code/mid_data/qang_"+trainset+".npy"

q=np1.load(qfile)
tau_imu=np1.load(taufile)
ang_vel=np1.load(angfile)
len_imu=np1.load(lenfile)
acc_imu=np1.load(accfile)
q_opt=np1.load(q_optfile)
eul_vic_ang=np1.load(ang_vicfile)
len_vic=np1.load(len_vicfile)
#len_imu=np1.load(len_imufile)
eul_imu_ang=np1.load(qangfile)
#print(q_optfile)
print(len_imu)
optimized_q_ang=np1.zeros(((len_imu),3),dtype=float)

print(eul_vic_ang)
#use q to calculate angel
i=0

while(i<len_imu):

    
    optimized_q_ang[i]=ts3d.euler.quat2euler(q_opt[i])
    i=i+1





#plot x-axis angle
n1= np1.arange(0,len_imu ,1)
n2= np1.arange(0,len_vic ,1)
plt.figure(figsize=(10,20))
plt.subplots_adjust(wspace=0, hspace=0.5)
a1=plt.subplot(3, 1, 1)
linesList1=plt.plot(n1, eul_imu_ang.T[0])
linesList2=plt.plot(n2, eul_vic_ang.T[0])
linesList3=plt.plot(n1, optimized_q_ang.T[0])
plt.setp(linesList1, color='r')
plt.setp(linesList2, color='b')
plt.setp(linesList3, color='g')
a1.set_title("roll")

a2=plt.subplot(3, 1, 2)
linesList1=plt.plot(n1, eul_imu_ang.T[1])
linesList2=plt.plot(n2, eul_vic_ang.T[1])
linesList3=plt.plot(n1, optimized_q_ang.T[1])
plt.setp(linesList1, color='r')
plt.setp(linesList2, color='b')
plt.setp(linesList3, color='g')
a2.set_title("pitch")

a3=plt.subplot(3, 1, 3)
linesList1=plt.plot(n1, eul_imu_ang.T[2])
linesList2=plt.plot(n2, eul_vic_ang.T[2])
linesList3=plt.plot(n1, optimized_q_ang.T[2])
plt.setp(linesList1, color='r')
plt.setp(linesList2, color='b')
plt.setp(linesList3, color='g')
a3.set_title("yaw")

plt.legend()
plt.show()
