import pygame
import Queue
import time
from car import Car
import os
from threading import Thread
import random
import math as m
from sensordata import get_data as sdata
from sensordata import circleMatrix2
from network import Dqn
import torch
import numpy as np

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

MouseMotionQ = Queue.Queue()
quit_game = False

mycar = Car(15,30,(200,200),screen)
clock = pygame.time.Clock()


def EventDispatcher():
    while True:
        Events = pygame.event.get()
        for event in Events:
            if(event.type == pygame.MOUSEMOTION):
                buttons = pygame.mouse.get_pressed()
                if(buttons[0]):
                    MouseMotionQ.put(pygame.mouse.get_pos())
            if(event.type == pygame.QUIT):
                os._exit(0)


def cross_bounds():
    v1,v2,v3 = mycar.get_car()
    X = v1[0]
    Y = v1[1]
    if(X<0 or X>1000 or Y<0 or Y>1000):
        return True
    else:
        return False


def draw():
    map_data = []
    while True:
        if(not MouseMotionQ.empty()):
            pos = MouseMotionQ._get()
            pygame.draw.circle(screen,(255,255,255),pos,3,3)
            map_data.append(pos)


def reset():
    global mycar
    erase()
    mycar = Car(20, 30, (200, 200),screen)


def erase():
    points = mycar.get_car()

    x, y = int(mycar.sensor1.x), int(mycar.sensor1.y)
    pygame.draw.circle(screen, (0,0,0), (x, y), 1, 0)

    x, y = int(mycar.sensor2.x), int(mycar.sensor2.y)
    pygame.draw.circle(screen, (0,0,0), (x, y), 1, 0)

    x, y = int(mycar.sensor3.x), int(mycar.sensor3.y)
    pygame.draw.circle(screen, (0,0,0), (x, y), 1, 0)

    pygame.draw.polygon(screen, (0, 0, 0), points)


def sign(p1,p2,p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])


def PointInTriangle(point):
    d1 = sign(point,(mycar.v1_x,mycar.v1_y),(mycar.v2_x,mycar.v2_y))
    d2 = sign(point, (mycar.v2_x, mycar.v2_y), (mycar.v3_x, mycar.v3_y))
    d3 = sign(point, (mycar.v3_x, mycar.v3_y), (mycar.v1_x, mycar.v1_y))

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not(has_neg and has_pos)


def collision():
    white = (255,255,255)
    for point in environment:
        try:
            color = screen.get_at(point)
            if color == white:
                if PointInTriangle(point):
                    return True
        except IndexError:
            pass
    return False


def turn_car(direction):
    car = mycar
    angle = direction*60
    car.rotate(180/m.pi * angle)
    points = mycar.get_car()
    pygame.draw.polygon(screen, (255, 69, 0), points)

    x,y = int(car.sensor1.x) , int(car.sensor1.y)
    pygame.draw.circle(screen,(155,155,200),(x,y),1,0)

    x, y = int(car.sensor2.x), int(car.sensor2.y)
    pygame.draw.circle(screen, (0, 155, 200), (x, y), 1, 0)

    x, y = int(car.sensor3.x), int(car.sensor3.y)
    pygame.draw.circle(screen, (155, 0, 200), (x, y), 1, 0)

    pygame.display.update()

def move_car():
    global mycar
    car = mycar
    Vx = car.v1_x-car.x
    Vy = car.v1_y-car.y

    car.move(Vx,Vy)
    points = mycar.get_car()

    pygame.draw.polygon(screen, (255, 69, 0), points)

    x, y = int(car.sensor1.x), int(car.sensor1.y)
    pygame.draw.circle(screen, (155, 155, 200), (x, y), 1, 0)

    x, y = int(car.sensor2.x), int(car.sensor2.y)
    pygame.draw.circle(screen, (0, 155, 200), (x, y), 1, 0)

    x, y = int(car.sensor3.x), int(car.sensor3.y)
    pygame.draw.circle(screen, (155, 0, 200), (x, y), 1, 0)

    pygame.display.update()

def get_env():
    while not quit_game:
        x = int(mycar.x)
        y = int(mycar.y)
        global environment
        environment = circleMatrix2(x,y,20)

def get_reward():
    reward = 0
    global distance
    global col
    global cb
    global reached
    d = (goal[0]-mycar.x)**2+(goal[1]-mycar.y)**2
    if d > distance:
        reward-=1
    if d < distance:
        reward+=1
    if cross_bounds():
        cb = True
        reward-=5
    if collision():
        col = True
        reward-=5
    if PointInTriangle(goal):
        reward+=20
        reached = True
    distance = d
    return reward


goal = (900,900)
distance = (goal[0]-mycar.x)**2+(goal[1]-mycar.y)**2
brain = Dqn()
points = mycar.get_car()
cb = False
col = False
reached = False
Thread(target=EventDispatcher,args=()).start()
Thread(target=draw,args=()).start()
Thread(target=get_env,args=()).start()

environment = []
# left,right,forward

first = True
size = 0

torch.set_default_tensor_type('torch.cuda.FloatTensor')
brain.model.to('cuda')

while not quit_game:
    if first:
        s1 = sdata(screen, (int(mycar.sensor1.x), int(mycar.sensor1.y)), 10)
        s2 = sdata(screen, (int(mycar.sensor2.x), int(mycar.sensor2.y)), 10)
        s3 = sdata(screen, (int(mycar.sensor3.x), int(mycar.sensor3.y)), 10)
        st = torch.tensor([s1, s2, s3])
        first = False
    else:
        st = torch.tensor([s1, s2, s3])
    action = brain.forward(st).max(0)[1].item()
    if action == 0:
        turn_car(-1)
    elif action == 1:
        turn_car(1)
    else:
        move_car()
    reward = get_reward()
    s1 = sdata(screen, (int(mycar.sensor1.x), int(mycar.sensor1.y)), 10)
    s2 = sdata(screen, (int(mycar.sensor2.x), int(mycar.sensor2.y)), 10)
    s3 = sdata(screen, (int(mycar.sensor3.x), int(mycar.sensor3.y)), 10)
    ST = torch.tensor([s1, s2, s3])
    brain.Memory.push([st, ST, reward, action])
    size += 1
    if size > 16:
        size = 16
        batch_state = brain.Memory.sample(16)
        brain.step(batch_state[:,0],batch_state[:,1],batch_state[:,2],batch_state[:,3])
    if cb or col or reached:
        cb = False
        col = False
        reached = False
        reset()
    else:
        erase()

