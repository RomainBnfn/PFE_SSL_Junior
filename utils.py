import numpy as np
from collections import deque, namedtuple
import random
import torch

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class OUNoise(object):
    pass

class Memory():
    '''Replay buffer to save experience tuples'''

    def __init__(self, batch_size, buffer_size=1000000, seed=1):
        # action_size : dimension of each action
        # buffer_size : max size of buffer
        random.seed(seed)
        np.random.seed(seed)
        # Deque is preferred over a list in the cases 
        # where we need quicker append and pop operations
        self.memory = deque(maxlen=buffer_size)
        self.batch_size = batch_size
        self.experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])

    
    def add(self, state, action, reward, next_state, done):
        '''Add new experience to memory'''
        e = self.experience(state, action, reward, next_state, done)
        self.memory.append(e)

    def sample(self):
        '''Take a random sample of saved experiences'''
        experiences = random.sample(self.memory, k=self.batch_size)
        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).float().to(device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(device)
        next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(device)
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(device)
        return (states, actions, rewards, next_states, dones)

    def __len__(self):
        # size of memory
        return len(self.memory)