class Settings(object):
    
    def __init__(self):
        self.default()

    def default(self):
        self.load_buffer=True
        self.gpu=True

        # learning parameters
        self.gamma=0.99 # discount factor
        self.critic_learning_rate=1e-3
        self.actor_learning_rate=1e-4
        self.tau=1e-3
        self.l2_penalty=1e-5
        self.max_buffer=1e+5
        self.batch_size=64
        self.max_step=1e+3
        self.max_episode=1e+4
        self.max_epoch=1e+7
        
        # dimension setup
        self.observation_dim={
            'lidar':[36],
            'proximity':[4],
            'control':[3],
            'depth':[96,128,3],
            'goal':[2]
        }
        self.state_dim=[50]
        self.action_dim=[3]        
        self.action_bounds=[[0.2,0.2,0.5],[-0.2,-0.2,-0.5]] # [max,min]

        # loss
        self.c_srl = 0.25
        self.c_rew = 0.5
        self.c_slow = 1.0
        self.c_div = 1.0
        self.c_inv = 0.5
        self.c_fwd = 1.0


        # layer setup
        self.observation_networks={
            'lidar':[
                {
                    'type':'dense',
                    'activation':'softplus',
                    'shape':[self.observation_dim['lidar'][0],200]
                },
                {
                    'type':'dense',
                    'activation':'softplus',
                    'shape':[200,self.state_dim[0]]
                }
            ],
            'proximity':[
                {
                    'type':'dense',
                    'activation':'softplus',
                    'shape':[self.observation_dim['proximity'][0],200]
                },
                {
                    'type':'dense',
                    'activation':'softplus',
                    'shape':[200,self.state_dim[0]]
                }
            ],
            'control':[
                {
                    'type':'dense',
                    'activation':'softplus',
                    'shape':[self.observation_dim['control'][0],200]
                },
                {
                    'type':'dense',
                    'activation':'softplus',
                    'shape':[200,self.state_dim[0]]
                }
            ],
            'depth':[
                {
                    'type':'conv2d',
                    'activation':'softplus',
                    'shape':[5,5,self.observation_dim['depth'][3],8],
                    'strides':[1,1,1,1],
                    'pool':[1,2,2,1]
                },
                {
                    'type':'conv2d',
                    'activation':'softplus',
                    'shape':[3,3,8,9],
                    'strides':[1,1,1,1],
                    'pool':[1,2,2,1]
                },
                {
                    'type':'conv2d',
                    'activation':'softplus',
                    'shape':[3,3,9,10],
                    'strides':[1,1,1,1],
                    'pool':[1,2,2,1]
                },
                {
                    'type':'flatten',
                    'shape':[-1,self.state_dim[0]]
                }
            ],
            'goal':[
                {
                    'type':'dense',
                    'activation':'None',
                    'shape':[self.observation_dim['goal'][0],3]
                }
            ]
        }
        self.prediction_networks={
            'reward':[
                {
                    'type':'dense',
                    'activation':'softplus',
                    'shape':[self.state_dim[0]+self.action_dim[0],60]
                },
                {
                    'type':'dense',
                    'activation':'softplus',
                    'shape':[60,1]
                }
            ],
            'state':[
                {
                    'type':'dense',
                    'activation':'softplus',
                    'shape':[self.state_dim[0]+self.action_dim[0],100]
                },
                {
                    'type':'dense',
                    'activation':'softplus',
                    'shape':[100,self.state_dim[0]]
                }
            ]
        }
        self.rl_networks={
            'actor':[
                {
                    'type':'dense',
                    'activation':'softplus',
                    'shape':[self.state_dim[0],50]
                },
                {
                    'type':'dense',
                    'activation':'softplus',
                    'shape':[50,40]
                },
                {
                    'type':'decision',
                    'shape':[40,self.action_dim[0]],
                    'bounds':self.action_bounds,
                    'epsilon':self.epsilon
                }
            ],
            'critic':[
                {
                    'type':'dense',
                    'activation':'softplus',
                    'shape':[self.state_dim[0]+self.action_dim,60]
                },
                {
                    'type':'dense',
                    'activation':'softplus',
                    'shape':[60,40]
                },
                {
                    'type':'dense',
                    'activation':'None',
                    'shape':[40,1]
                }
            ]
        }

config=Settings()
