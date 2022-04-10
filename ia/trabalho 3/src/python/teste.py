import numpy as np

a=[10,20,30]
v=np.asarray(a)
i=0
while True:
    if i==v.size:
        break
    if i==0:
        v=np.append(v,40)
    print(v[i])
    i+=1