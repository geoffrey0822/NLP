import os,sys
from shutil import copyfile

if not os.path.isdir(sys.argv[2]):
    os.mkdir(sys.argv[2])
    
print 'Converting...',
for file in os.listdir(sys.argv[1]):
    fname,ext=os.path.splitext(file)
    if ext=='.ldb':
        new_name=os.path.join(sys.argv[2],'%s.sst'%fname)
        copyfile(os.path.join(sys.argv[1],file),new_name)
    else:
        copyfile(os.path.join(sys.argv[1],file),os.path.join(sys.argv[2],file))
        
print 'Done'