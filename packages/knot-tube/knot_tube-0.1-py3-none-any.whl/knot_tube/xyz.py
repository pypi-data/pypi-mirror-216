import numpy as np
import os

# 定义读取xyz格式的函数，返回迭代器
def read_xyz(file):
    with open(file) as f:
        while True:
            try:
                n_atoms = int(f.readline())
            except ValueError:
                break
            if not n_atoms:
                break
            f.readline()
            
            # 将坐标保存为narray
            coords = []
            for i in range(n_atoms):
                line = f.readline().split()
                coords.append([float(x) for x in line[1:]])
            yield coords

def read_xyz_single(filename):
    with open(filename,'r') as f:
        N=int(f.readline())
        f.readline()
        data=np.zeros((N,3))
        for i in range(N):
            line=f.readline().split()
            data[i,0]=float(line[1])
            data[i,1]=float(line[2])
            data[i,2]=float(line[3])
    return data

# def read_xyz_single(filename):
#     """Read xyz file and return a list of atoms. return numpy array"""
#     with open(filename, 'r') as f:
#         lines = f.readlines()
#         lines = lines[2:]
#         atoms = []
#         for line in lines:
#             line = line.split()
#             atom = [ float(line[1]), float(line[2]), float(line[3])]
#             atoms.append(atom)
#     return np.array(atoms)

def save_xyz(file, X:np.ndarray, title:str, dir=None, append=False):
    # 如果dir不存在则创建
    if dir and not os.path.exists(dir):
        os.makedirs(dir)
    
    if(append):
        with open(dir+'/'+file, 'a') as f:
            f.write(str(X.shape[0]) + '\n')
            f.write(title + '\n')
            for x in X:
                f.write('1\t{:f} {:f} {:f}'.format(x[0], x[1], x[2]) + '\n')
    else:
        with open(dir+'/'+file, 'w') as f:
            f.write(str(X.shape[0]) + '\n')
            f.write(title + '\n')
            for x in X:
                f.write('1\t{:f} {:f} {:f}'.format(x[0], x[1], x[2]) + '\n')