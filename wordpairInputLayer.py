import os,sys,leveldb,caffe

class WordPairInputLayer(caffe.Layer):
    def setup(self,bottom,top):
        if len(top)!=2:
            raise Exception('the number of output must be 2')
        
        params=eval(self.param_str)
        self.batchsize=1
        self.dataset=''
        self.wordDim=2
        self.total=0
        
        if 'batch_size' in params:
            self.batchsize=int(params['batch_siize'])
        if 'dataset' in params:
            self.dataset=params['dataset']
        if 'dim' in params:
            self.wordDim=int(params['dim'])
        if 'total' in params:
            self.total=int(params['total'])
            
        if self.total==0:
            print 'scanning dataset'
            ds=leveldb.LevelDB(self.dataset)
            for key,value in ds.RangeIter():
                self.total+=1
        self.currentIdx=0
    
    def reshape(self,bottom,top):
        top[0].reshape(*(self.batchsize))
        top[1].reshape(*(self.batchsize))
    
    def forward(self,bottom, top):
        ds=leveldb.LevelDB(self.dataset)
        i=0
        while i<self.batchsize:
            if self.currentIdx>=self.total:
                self.currentIdx=0
            pairs_str=ds.Get(self.currentIdx,default=None)
            pairs=pairs_str.split(';')
            top[0].data[i,...]=[int(pairs[0])]
            top[0].data[i,...]=[int(pairs[1])]
            i+=1
            self.currentIdx+=1
    
    def backward(self,top,propagate_down,bottom):
        pass