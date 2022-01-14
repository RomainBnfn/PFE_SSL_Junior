import sys 
from model import DDPG
from utils import *
from socker_environment import *

env = SockerEnvironement()

agent = DDPG(env)
batch_size = 128
rewards = []
avg_rewards = []

for episode in range(50):
    state = env.reset()
    episode_reward = 0

    for step in range(500):
        action = agent.get_action(state)
        new_state, reward, done, _ = env.step(action)
        agent.memory.add(state, action, reward, new_state, done)

        if len(agent.memory) > batch_size:
            agent.update(batch_size)
        
        state = new_state
        episode_reward += reward

        if done:
            sys.stdout.write("episode: {}, reward: {}, average reward: {} \n". format(episode, np.round(episode_reward, decimals=2), np.mean(rewards[-10:])))
            break

        rewards.append(episode_reward)
        avg_rewards.append(np.mean(rewards[-10:]))