#!/usr/bin/env python3
# rewards: [golden_fish, jellyfish_1, jellyfish_2, ... , step]
rewards = [50, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -1]

# Q learning learning rate
#If alpha > 0.4, too much variance, doesn't converge. If alpha < 0.1, we learn too slow.
# we set alpha=0.4 so that we learn fast but still converge
alpha = 0.4

# Q learning discount rate
# finds solution with gamma 0.2-1.0. If gamma < 0.2, we don't value future reward high enough compared to present reward.
gamma = 0.8

# Epsilon initial
# varying epsilon doesn't seem to effect learning much in this scenario
epsilon_initial = 1

# Epsilon final
epsilon_final = 1

# Annealing timesteps
annealing_timesteps = 1

# threshold
threshold = 1e-6
