import cv2
import numpy as np
from time import time
from math import sin, cos, pi, sqrt

n = 10

m = []
radius = []
x = []
y = []
vx = []
vy = []
color = []
ring = []

for i in range(n):
    m.append(0)
    radius.append(0)
    x.append(-10000)
    y.append(-10000)
    vx.append(0)
    vy.append(0)
    color.append((0, 255, 0))
    ring.append(False)

m[0] = 10**(37)
radius[0] = 30
x[0] = 600
y[0] = 350
# vx[0] = -cos(pi/3)*2*10**(12)
# vy[0] = sin(pi/3)*2*10**(12)
vx[0] = 0
vy[0] = 0
color[0] = (0, 255, 255)

m[1] = 10**(37)
radius[1] = 30
x[1] = 400
y[1] = 350
vx[1] = 2*10**(12)
vy[1] = 0
# vx[1] = -cos(pi/3)*2*10**(12)
# vy[1] = -sin(pi/3)*2*10**(12)
color[1] = (0, 255, 255)

# m[2] = 10**(37)
# radius[2] = 30
# x[2] = 500
# y[2] = 350-100*sqrt(3)
# vx[2] = 2*10**(12)
# vy[2] = 0
# color[2] = (0, 255, 255)

G = 6.67*10**(-11)
dt = 3*10**(-13)


base = np.zeros(shape=(700, 1000, 3), dtype=np.uint8)
rastro = []

while True:
    initial_time = time()    
    img = base.copy()
    
    for j in range(len(m)):
        if not (x[j] == -10000 and y[j] == -10000):
            for i in range(len(m)):
                if i != j:
                    if ((x[i]-x[j])**2 + (y[i]-y[j])**2)**(1/2) < radius[i]+radius[j]:
                        x[j] = (x[j] + x[i])/2
                        y[j] = (y[j] + y[i])/2
                        x[i] = -10000
                        y[i] = -10000
                        ring[j] = True
                        radius[j] = (radius[i]**3 + radius[j]**3)**(1/3)
                        vx[j] = (vx[i]*m[i] + vx[j]*m[j])/(m[i]+m[j])
                        vy[j] = (vy[i]*m[i] + vy[j]*m[j])/(m[i]+m[j])
                    else:
                        vx[j] += - G*m[i]*(x[j]-x[i])*dt/((x[j]-x[i])**2+(y[j]-y[i])**2)**(3/2)
                        vy[j] += - G*m[i]*(y[j]-y[i])*dt/((x[j]-x[i])**2+(y[j]-y[i])**2)**(3/2)
        
            x[j] = x[j] + vx[j]*dt
            y[j] = y[j] + vy[j]*dt

    if len(rastro) > 8000:
        for i in range(len(m)):
            rastro = rastro[1:] + [(int(x[i]), int(y[i]), color[i])]
    else:
        for i in range(len(m)):
            rastro.append((int(x[i]), int(y[i]), color[i]))

    for i in range(len(rastro)):
        point = rastro[i][:2]
        c = rastro[i][2]
        cv2.circle(img, point, 1, (int(0.6*c[0]*i/len(rastro)), int(0.6*c[1]*i/len(rastro)), int(0.6*c[2]*i/len(rastro))), 1)

    for i in range(len(m)):
        if not (x[i] == -10000 and y[i] == -10000):
            cv2.putText(img, str(i), (int(radius[i]+x[i]), int(radius[i]+y[i])), cv2.FONT_HERSHEY_SIMPLEX, 1, color[i])
            cv2.circle(img, (int(x[i]), int(y[i])), int(radius[i]), color[i], 2)
            if ring[i]:
                cv2.ellipse(img, (int(x[i]), int(y[i])), (int(radius[i]*1.5), int(radius[i]*0.5)), 0, 0, 360, color[i])

    cv2.imshow("image", img)
    while time()-initial_time < 7*10**(-4):
        print("waiting..")
    if cv2.waitKey(1) == 27:
            exit(0)
