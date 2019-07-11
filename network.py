import torch
import torch.nn.functional as f
import torch.nn as nn
import numpy as np
import torch.optim as optim
from torch.autograd import Variable
import random


class memory:
    def __init__(self,size):
        self.memory = np.array([])
        self.size = size

    def push(self,event):
        if(len(self.memory) > self.size):
            np.delete(self.memory,0)
        self.memory = np.append(self.memory,[event],axis=0)

    def sample(self,batch_size):
        st = np.random.randint(0,self.memory.shape[0]-batch_size)
        sam = self.memory[st:st+batch_size,:]
        return sam

class Network(nn.Module):

    def __init__(self,input_size,actions):
        super(Network,self).__init__()
        self.input_size = input_size
        self.actions = actions
        self.fc1 = nn.Linear(input_size,30)
        self.fc2 = nn.Linear(30,actions)

    def forward(self, input_batch):
        x = self.fc1(input_batch)
        x = f.relu(x)
        batch_output = self.fc2(x)
        return batch_output

class Dqn:
    def __init__(self):
        self.model = Network(3,4)
        self.optim = optim.Adam(self.model.parameters(),lr=0.001)
        self.gamma = 0.01
        self.Memory = memory(10000)

    def forward(self,input_batch):
        return self.model.forward(input_batch)

    def step(self,current_states,next_states,rewards,actions):
        output = self.forward(current_states)
        current_Q = output.gather(1,actions)
        Next_Q = self.forward(next_states)
        Next_Qmax = Next_Q.max(1)[0]
        targets = rewards + self.gamma*Next_Qmax
        td_loss = f.smooth_l1_loss(current_Q,targets)
        self.optim.zero_grad()
        td_loss.backwards(retain_vaiables=True)
        self.optim.step()

    

