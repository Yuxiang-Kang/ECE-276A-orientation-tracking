
import math

import autograd
import Quaternion_calculation as qt
import autograd.numpy as np1


def quat2acc(Q):
    G=autograd.numpy.array([0., 0., 0., 1.])
    G=qt.mult(G,Q)
    
    J=qt.inv(Q)
    
    G=qt.mult(J,G)
    return G


def quat2next(Q,ts,w):
    A=np1.array([0.])
    B=np1.multiply(w,ts/2)
    #A.extend(autograd.numpy.multiply(w,ts/2))
    C=np1.concatenate((A,B))
    Q1=qt.mult(Q,qt.exp(C))
    return Q1

'''
def cost(q,a,ts,w,T):
    q1=autograd.numpy.zeros(T)
    #print (q1[0])
    q2=autograd.numpy.zeros(T)
    i=0
    #print(T)
    #print(math.pow(np.linalg.norm(np.multiply(qt.log(qt.mult((qt.inv(q[i+1])),quat2next(q[i],ts[i],w[i]))),2)),2))
    while(i<T-1):
        
        q1[i]=1
        q1[i]=math.pow(autograd.numpy.linalg.norm(autograd.numpy.multiply(qt.log(qt.mult((qt.inv(q[i+1])),quat2next(q[i],ts[i],w[i]))),2)),2)
        #print(q1[i])
        #print('i=',i)
        #q1[i]=math.pow(np.linalg.norm(np.multiply(qt.log(qt.mult((qt.inv(q[i+1])),quat2next(q[i],ts[i],w[i]))),2)),2)
        i= i+1
    i=1
    
    while(i<T):
        ht=quat2acc(q[i])[1:4]
        #print(ht)
        q2[i-1]=math.pow(np1.linalg.norm(np1.subtract(a[i],ht)),2.)
        i=i+1
    A=1/2*sum(q1)+1/2*sum(q2)
    return A
'''
