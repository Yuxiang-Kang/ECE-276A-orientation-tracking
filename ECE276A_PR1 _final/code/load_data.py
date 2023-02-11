import pickle
import sys
import time 
import numpy as np
from parameters import dataset
def tic():
  return time.time()
def toc(tstart, nm=""):
  print('%s took: %s sec.\n' % (nm,(time.time() - tstart)))

def read_data(fname):
  d = []
  with open(fname, 'rb') as f:
    if sys.version_info[0] < 3:
      d = pickle.load(f)
    else:
      d = pickle.load(f, encoding='latin1')  # need for python 3
  return d

#dataset="1"
if(dataset=="1" or dataset=="2" or dataset=="8" or dataset=="9" or dataset=="10" or dataset=="11"):
  cfile = "../data/cam/cam" + dataset + ".p"
  camd = read_data(cfile)
else:
  camd=0

ifile = "../data/imu/imuRaw" + dataset + ".p"
vfile = "../data/vicon/viconRot" + dataset + ".p"


if(dataset=="10" or dataset=="11"  ):
  vicd=np.array([0])
else:
  vicd = read_data(vfile)
  

ts = tic()

imud = read_data(ifile)

toc(ts,"Data import")

#print(vicd['ts'].shape)
