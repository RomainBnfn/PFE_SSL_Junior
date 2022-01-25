import sys 
from model import DDPG
from utils import *
from socker_environment import *

env = SockerEnvironement('blue')

agent = DDPG(env)
batch_size = 128
rewards = []
avg_rewards = []

for episode in range(50):
    env.reset()
    # env.render()
    state = env.obs('blue')
    state = np.concatenate(np.array(state), axis=None)
    episode_reward = 0

    done = False
    while not done:
        action = agent.get_action(state)
        new_state, reward, done, _ = env.step(action)
        new_state = torch.flatten(torch.tensor(new_state))
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