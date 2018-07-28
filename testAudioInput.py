import os,sys
import caffe
import cv2
import numpy as np
from caffe import layers as L,params as P, to_proto
import sounddevice as sd
import matplotlib.pyplot as plt

caffe.set_mode_gpu()
net=caffe.Net(sys.argv[1],caffe.TEST)
net.forward()
data=net.blobs['data'].data
label=net.blobs['label'].data
plt.ion()
plt.show(block=False)
for n in range(data.shape[0]):
    print label[n]
    print 'play audio signal...'
    audioSig=data[n,0,0,...]
    scaled=np.int16(audioSig/np.max(np.abs(audioSig))*32767)
    plt.clf()
    plt.plot(audioSig)
    plt.draw()
    plt.pause(0.001)
    print scaled.shape
    sd.play(scaled,44100,blocking=True)
print 'finish'
