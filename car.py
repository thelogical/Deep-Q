import numpy as np
import math as m


class sensor:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.value = 0


class Car:

    def setup(self):
        self.v1_x = self.x
        self.v1_y = self.y - float((self.length / m.sqrt(3)))

        mid_x = self.x
        mid_y = self.v1_y + float(m.sqrt(5) / 2 * self.length)

        self.v2_x = mid_x + float(self.length / 2)
        self.v2_y = mid_y

        self.v3_x = mid_x - float(self.length / 2)
        self.v3_y = mid_y

        self.sensor1.x = (self.v1_x+self.v2_x)/2
        self.sensor1.y = (self.v1_y+self.v2_y)/2

        self.sensor2.x = (self.v1_x+self.v3_x)/2
        self.sensor2.y = (self.v1_y+self.v3_y)/2

        self.sensor3.x = self.v1_x
        self.sensor3.y = self.v1_y

    def rotate(self,angle):
        t_x = self.v1_x - self.x
        t_y = self.v1_y - self.y
        rotationMatrix = np.array([[m.cos(angle),m.sin(angle)],
                                   [-m.sin(angle),m.cos(angle)]])
        t_x,t_y = np.matmul(rotationMatrix,np.array([t_x,t_y]))
        self.v1_x = t_x + self.x
        self.v1_y = t_y + self.y

        t_x = self.v2_x - self.x
        t_y = self.v2_y - self.y
        rotationMatrix = np.array([[m.cos(angle), m.sin(angle)],
                                   [-m.sin(angle), m.cos(angle)]])
        t_x, t_y = np.matmul(rotationMatrix, np.array([t_x, t_y]))
        self.v2_x = t_x + self.x
        self.v2_y = t_y + self.y

        t_x = self.v3_x - self.x
        t_y = self.v3_y - self.y
        rotationMatrix = np.array([[m.cos(angle), m.sin(angle)],
                                   [-m.sin(angle), m.cos(angle)]])
        t_x, t_y = np.matmul(rotationMatrix, np.array([t_x, t_y]))
        self.v3_x = t_x + self.x
        self.v3_y = t_y + self.y

        t_x = self.sensor1.x - self.x
        t_y = self.sensor1.y - self.y
        rotationMatrix = np.array([[m.cos(angle), m.sin(angle)],
                                   [-m.sin(angle), m.cos(angle)]])
        t_x, t_y = np.matmul(rotationMatrix, np.array([t_x, t_y]))
        self.sensor1.x = t_x + self.x
        self.sensor1.y = t_y + self.y

        t_x = self.sensor2.x - self.x
        t_y = self.sensor2.y - self.y
        rotationMatrix = np.array([[m.cos(angle), m.sin(angle)],
                                   [-m.sin(angle), m.cos(angle)]])
        t_x, t_y = np.matmul(rotationMatrix, np.array([t_x, t_y]))
        self.sensor2.x = t_x + self.x
        self.sensor2.y = t_y + self.y

        t_x = self.sensor3.x - self.x
        t_y = self.sensor3.y - self.y
        rotationMatrix = np.array([[m.cos(angle), m.sin(angle)],
                                   [-m.sin(angle), m.cos(angle)]])
        t_x, t_y = np.matmul(rotationMatrix, np.array([t_x, t_y]))
        self.sensor3.x = t_x + self.x
        self.sensor3.y = t_y + self.y

    def get_car(self):
        v1 = (int(self.v1_x),int(self.v1_y))
        v2 = (int(self.v2_x),int(self.v2_y))
        v3 = (int(self.v3_x),int(self.v3_y))
        return v1,v2,v3

    def __init__(self,length,angle,pos,screen):
        self.length=length
        self.x = pos[0]
        self.y = pos[1]
        self.sensor1 = sensor()
        self.sensor2 = sensor()
        self.sensor3 = sensor()
        self.setup()
        self.rotate(angle)

    def move(self,Vx,Vy):
        self.x += Vx
        self.y += Vy

        self.v1_x += Vx
        self.v1_y += Vy

        self.v2_x += Vx
        self.v2_y += Vy

        self.v3_x += Vx
        self.v3_y += Vy

        self.sensor1.x += Vx
        self.sensor1.y += Vy

        self.sensor2.x += Vx
        self.sensor2.y += Vy

        self.sensor3.x += Vx
        self.sensor3.y += Vy