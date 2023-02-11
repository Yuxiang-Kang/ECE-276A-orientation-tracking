
import math
import transforms3d as ts3d
import autograd
import autograd.numpy as np1
#定义Quaenion multiply函数，输入两个1*4矩阵，输出一个1*4矩阵
def mult(Q,P):
    qs=np1.array(Q[0])
    ps=np1.array(P[0])
    qv=np1.array((Q[1:4]))
    pv=np1.array((P[1:4]))
    #print(qv)
    Ms=np1.array(qs*ps-(qv.T)@pv)
    Mv=np1.multiply(pv,qs)+np1.multiply(ps,qv)+np1.cross(qv,pv)
    #print(Mv)


    M=np1.array([Ms])

    M2=np1.concatenate((M,Mv))

    #M.extend(Mv)
    #print(M)
    return M2


#定义exponential函数，输入一个1*4矩阵，输出一个1*4矩阵
def exp(Q):
    qs=np1.array(Q[0])
    qv=np1.array((Q[1:4]))
    E=np1.array([math.cos(np1.linalg.norm(qv))])
    
    Ev=np1.multiply(qv,(math.sin(np1.linalg.norm(qv))/np1.linalg.norm(qv)))
    #print(Ev)
    E1=np1.concatenate((E,Ev))
    #E.extend(np1.multiply(qv,(math.sin(np1.linalg.norm(qv))/np1.linalg.norm(qv))))
    E_final=np1.multiply(E1,(math.exp(qs)))
    return E_final


#定义inverse函数，输入一个1*4矩阵，输出一个1*4矩阵
def inv(Q):
    qs=np1.array(Q[0])
    qv=np1.array((Q[1:4]))
    qc=np1.array([qs])
    qv1=np1.multiply(qv,-1)
    qc1=np1.concatenate((qc,qv1))
    #qc.extend(np1.multiply(qv,-1))
    iv=np1.multiply(qc1,1/((np1.linalg.norm(Q))*(np1.linalg.norm(Q))))
    return iv

def conj(Q):
    qs=np1.array(Q[0])
    qv=np1.array((Q[1:4]))
    qc=np1.array([qs])
    qc1=np1.concatenate((qc,np1.multiply(qv,-1)))
    #qc.extend(np1.multiply(qv,-1))
    return qc1

def log(Q):
    qs=np1.array(Q[0])
    qv=np1.array((Q[1:4]))
    K=np1.linalg.norm(Q)
    #print(type(K))
    Kv=np1.linalg.norm(qv)
    Ls=np1.log(K)
    lv=np1.multiply(qv,(1/Kv*np1.arccos(qs/K)))
    L=np1.array([Ls])
    L1=np1.concatenate((L,lv))
    #L.extend(lv)
    return L1
'''
eul=np1.zeros((3,3))
q1=np1.array([1.,2.,3.,4.])
q2=np1.array([5.,6.,7.,8.])
q3=np1.array([(math.sqrt(3))/2,1/2, 0., 0.])
q4=np1.array([1.,0., 0., 0.])
R=ts3d.quaternions.quat2mat(q3)
eul[1]=ts3d.euler.quat2euler(q3)
print(mult(q1,q2))
'''
#q1=np1.array([1.,2.,3.,4.])
#q2=np1.array([5.,6.,7.,8.])
#print(mult(q1,q2))
#q4=np1.array([1.,2., 3., 4.])
#q5=np1.array([0., 0., 0., -1.])

#print(log(q1))
#print(eul[1])
#print(inv(q1))
#print(ts3d.quaternions.qexp(q1))

