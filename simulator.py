import cv2
import numpy as np
from time import time
from math import sin, cos, pi, sqrt

n = 10

m = [500]
radius = [30]
x = [-3]
y = [5]
vx = [30000]
vy = [30000]
color = [4]
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

m[0] = 2*10**(37)
radius[0] = 30
x[0] = 200
y[0] = 350
vx[0] = 0
vy[0] = -1*10**(12)
color[0] = (0, 255, 255)

m[1] = 10**(37)
radius[1] = 30
x[1] = 700
y[1] = 350
vx[1] = 0
vy[1] = 10**(12)+2*10**(12)
color[1] = (0, 255, 255)

m[2] = 10**(37)
radius[2] = 30
x[2] = 800
y[2] = 350
vx[2] = 0
vy[2] = 10**(12)-2*10**(12)
color[2] = (0, 255, 255)

G = 6.67*10**(-11)
dt = 3*10**(-13)

base = np.zeros(shape=(700, 1000, 3), dtype=np.uint8)
rastro = []

initial_point = [0, 0]
last_origin = [0, 0]
origin = [0, 0]
pressed = False

def dragAndDropCamera(event,x,y,flags,param):
    global initial_point, pressed, origin, last_origin
    if event == cv2.EVENT_LBUTTONDOWN:
        pressed = True
        initial_point = [x, y]
        last_origin = [origin[0], origin[1]]
    if event == cv2.EVENT_MOUSEMOVE and pressed:
        origin[0] = last_origin[0] + x - initial_point[0]
        origin[1] = last_origin[1] + y - initial_point[1]
    if event == cv2.EVENT_LBUTTONUP:
        initial_point = [0, 0]
        pressed = False

cv2.namedWindow("image")
cv2.setMouseCallback("image", dragAndDropCamera)

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
        xr, yr = rastro[i][:2]
        c = rastro[i][2]
        cv2.circle(img, (origin[0] + xr, origin[1] + yr), 1, (int(0.6*c[0]*i/len(rastro)), int(0.6*c[1]*i/len(rastro)), int(0.6*c[2]*i/len(rastro))), 1)

    for i in range(len(m)):
        if not (x[i] == -10000 and y[i] == -10000):
            cv2.putText(img, str(i), (origin[0] + int(radius[i]+x[i]), origin[1] + int(radius[i]+y[i])), cv2.FONT_HERSHEY_SIMPLEX, 1, color[i])
            cv2.circle(img, (origin[0] + int(x[i]), origin[1] + int(y[i])), int(radius[i]), color[i], 2)
            if ring[i]:
                cv2.ellipse(img, (origin[0] + int(x[i]), origin[1] + int(y[i])), (int(radius[i]*1.5), int(radius[i]*0.5)), 0, 0, 360, color[i])

    cv2.imshow("image", img)
    while time()-initial_time < 7*10**(-4):
        print("waiting..")
    if cv2.waitKey(1) == 27:
            exit(0)
