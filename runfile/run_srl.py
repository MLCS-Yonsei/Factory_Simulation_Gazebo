#!/usr/bin/env python
import time
import gym
import RL_mlcs
import numpy
import random

from env_reset import env_reset
from module import srl, replay, liveplot

from srl_config import config


def render():
    render_skip = 0 #Skip first X episodes.
    render_interval = 50 #Show render Every Y episodes.
    render_episodes = 10 #Show Z episodes every rendering.

    if (x%render_interval == 0) and (x != 0) and (x > render_skip):
        env.render()
    elif ((x-render_episodes)%render_interval == 0) and (x != 0) and (x > render_skip) and (render_episodes < x):
        env.render(close=True)

if __name__ == '__main__':

    env = gym.make('srl-v0')

    #env_reset().gazebo_warmup()

    outdir = '/tmp/gazebo_gym_experiments'
    # env = gym.wrappers.Monitor(env, outdir, force=True)
    env.action_space = 3
    # plotter = liveplot.LivePlot(outdir)

    last_time_steps = numpy.ndarray(0)

    srl = srl.SRL(config)
    if config.load_weight:
        try:
            srl.load(numpy.load('srl_weights.npy').item())
            print ('weight loaded.')
        except:
            print ('weight does not exist')

    memory = replay.Replay(
        config.max_buffer,
        config.batch_size,
        observations=config.observation_networks.keys()
    )
    if config.load_buffer:
        try:
            memory.load(numpy.load('srl_buffer.npy').item())
            print ('replay memory loaded.')
        except:
            print ('replay memory does not exist')

    initial_epsilon = srl.epsilon

    epsilon_discount = 0.9986

    start_time = time.time()
    highest_reward = 0
    reward_summary = []

    for x in range(int(config.max_episode)):
        done = False

        cumulated_reward = 0 #Should going forward give more reward then L/R ?

        state0 = env.reset()

        if srl.epsilon > 0.05:
            srl.epsilon *= epsilon_discount

        for i in range(int(config.max_step)):

            # Pick an action based on the current state
            action = srl.chooseAction(state0)

            # Execute the action and get feedback
            state1,reward,done,info = env.step(action)
            # print('action:',action,'  Done:',done)
            experience={
                'lidar_0':state0['lidar'],
                'depth_0':state0['depth'],
                'proximity_0':state0['proximity'],
                'control_0':state0['control'],
                'goal_0':state0['goal'],
                'lidar_1':state1['lidar'],
                'depth_1':state1['depth'],
                'proximity_1':state1['proximity'],
                'control_1':state1['control'],
                'goal_1':state1['goal'],
                'action':action,
                'reward':reward,
                'done':done
            }

            memory.add(experience)

            cumulated_reward += reward

            if highest_reward < cumulated_reward/(i+1):
                highest_reward = cumulated_reward/(i+1)

            #nextState = ''.join(map(str, observation))

            if memory.buffersize > config.batch_size:
                batch=memory.batch()
                srl.learn(memory.batch())
                batch.clear()

            # env._flush(force=True)

            if not(done):
                state0 = state1
            else:
                last_time_steps = numpy.append(last_time_steps, [int(i+1)])
                break

        if (x+1)%10==0:
            # plotter.plot(env)
            numpy.save('srl_weights.npy', srl.return_variables())
            numpy.save('srl_buffer.npy', memory.buffer)
        
        m, s = divmod(int(time.time() - start_time), 60)
        h, m = divmod(m, 60)
        print ("\nEP: "+str(x+1)+" - Avg. reward: "+str(cumulated_reward/(i+1))+"     Time: %d:%02d:%02d" % (h, m, s))
        reward_summary.append(cumulated_reward/(i+1))
        numpy.save('reward_summary.npy', reward_summary)

    #Github table content
    # print ("\n|"+str(int(config.max_episode))+"|"+str(highest_reward)+"| PICTURE |")

    l = last_time_steps.tolist()
    l.sort()

    #print("Parameters: a="+str)
    # print ("Overall score: {:0.2f}".format(last_time_steps.mean()))
    # print ("Best 100 score: {:0.2f}".format(reduce(lambda x, y: x + y, l[-100:]) / len(l[-100:])))

    env.close()
