import os,sys,caffe

#caffe.set_mode_gpu()
#solver=caffe.SGDSolver(sys.argv[1])
solver=caffe.get_solver(sys.argv[1])
solver.solve()