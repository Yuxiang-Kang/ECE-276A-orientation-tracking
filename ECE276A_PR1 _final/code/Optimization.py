from parameters import dataset
import math

from load_data import camd, imud, vicd
import Quaternion_calculation as qt
import transforms3d as ts3d
import matplotlib.pyplot as plt
import Funcs as F
import autograd
import autograd.numpy as np1


def cost_f(qk):
    q_ry=np1.reshape(qk,(len_imu,4))
    #ft=F.quat2next(q[:len_imu-2],tau_imu[:-1],ang_vel[:len_imu-2])

    #q1=np1.zeros(len_imu)
    #print (q1[0])
    #q2=np1.zeros(len_imu)
    i=0
    #print(T)
    #print(math.pow(np.linalg.norm(np.multiply(qt.log(qt.mult((qt.inv(q[i+1])),quat2next(q[i],ts[i],w[i]))),2)),2))
    while(i<len_imu-1):
        
        #q1[i]=1
        #print(type(q1[i]))

        #q1[i]=np1.linalg.norm(np1.multiply(qt.log(qt.mult((qt.inv(q_ry[i+1])),F.quat2next(q[i],tau_imu[i],ang_vel[i]))),2))
        #q1[i]=q1[i]*q1[i]
        q1=np1.linalg.norm(np1.multiply(qt.log(qt.mult((qt.inv(q_ry[i+1])),F.quat2next(q[i],tau_imu[i],ang_vel[i]))),2))
        q1_sq= np1.multiply(q1,q1)
        if (i==0):
            q1_seq=np1.array([q1_sq])
        else:
            q1_seq=np1.hstack((q1_seq,np1.array([q1_sq])))
        #print(q1[i])
        #print('i=',i)
        
        i= i+1
    i=1
    
    while(i<len_imu):
        ht=F.quat2acc(q_ry[i])[1:4]
        #print(ht)
        #q2[i-1]=np1.linalg.norm(np1.subtract(acc_imu[i],ht))
        #q2[i-1]=q2[i-1]*q2[i-1]
        q2=np1.linalg.norm(np1.subtract(acc_imu[i],ht))
        q2_sq= np1.multiply(q2,q2)
        if (i==1):
            q2_seq=np1.array([q2_sq])
        else:
            q2_seq=np1.hstack((q2_seq,np1.array([q2_sq])))
        
        i=i+1
    A=1./2*np1.sum(q1_seq)+1./2*np1.sum(q2_seq)
    #print(q1_seq)
    #print(q2_seq)
    #print(q2_seq.shape)
    #print(q1_seq.shape)
    return A





#load data from main
qfile="../code/mid_data/q_"+dataset+"_unoptimized.npy"
taufile="../code/mid_data/tau_"+dataset+".npy"
angfile="../code/mid_data/ang_vel_"+dataset+".npy"
lenfile="../code/mid_data/len_imu_"+dataset+".npy"
accfile="../code/mid_data/acc_imu_"+dataset+".npy"
q=np1.load(qfile)
tau_imu=np1.load(taufile)
ang_vel=np1.load(angfile)
len_imu=np1.load(lenfile)
acc_imu=np1.load(accfile)



print("Optimization dataset:",dataset)
# calculate cost funct and grad
q_pl=np1.reshape(q,4*len_imu)
print(q_pl.shape)
q_pl=q_pl+1e-4
print(q_pl.shape)
cst=cost_f(q_pl)
grad_cost=autograd.grad(cost_f)
#print(type(q_pl))
print(cst)
#print(grad_cost(q_pl))
j=0
q_opt=np1.copy(q_pl)
q_doc=np1.copy(q_pl)
while(j<50):
    q_opt_ary=np1.reshape(q_opt,(len_imu,4))
    grad_cost=autograd.grad(cost_f)
    grad_q=grad_cost(q_opt)
    grad_q_ary=np1.reshape(grad_q,(len_imu,4))
    step=np1.multiply(grad_q_ary,-0.1)
    #step length is defined
    no_c_q=np1.add(q_opt_ary,step)
    norm_ary=np1.sqrt(np1.sum(no_c_q*no_c_q,axis=1)).reshape((len_imu,1))
    c_q=no_c_q/norm_ary
    q_opt=np1.reshape(c_q,(4*len_imu))
    print(cost_f(q_opt))
    print("gen=",j)
    q_op_file="../code/mid_data/qop_gen_"+str(j)+"dataset_"+dataset+".npy"
    np1.save(q_op_file,c_q)
    j=j+1

