import pandas as pd
import numpy as np

ny = 4
nx = 5
nt = 4

Txy = np.random.rand(nt,ny,nx)

for j in range(nt):
    for i in range(ny):
        Txy[j][i][1:nx-1]= 273
        Txy[j][i][0] = 348
        Txy[j][i][nx-1] = 373
        Txy[j][ny-1] = 323
        Txy[j][0] = 573
        Txy[j][0][0] = (573+348)/2
        Txy[j][ny-1][0] = (348+323)/2
        Txy[j][0][nx-1] = (573+373)/2
        Txy[j][ny-1][nx-1] = (323+373)/2
