# frozen lake

# actions
# 0 - left
# 1 - down
# 2 - right
# 3 - up

# done = hit the hole or hit the end

# observations
# 0 1 2 3
# 4 5 6 7
# 8 9 ...

# info always yields {'prob' : 0.33}
# which prob means sprite has 2/3 probability of moving according to action

# reward - 1.0 if G, 0 otherwise

# ideal logic should be:
# - don't try to go past the edge
# - don't choose any known holes
# - don't choose to go anywhere we've already been on this trip

import gym
import random

env = gym.make('FrozenLake-v0')

dir_map = [
        'left',
        'down',
        'right',
        'up',
        'no_change']

action_dict = {
        'up': 3,
        'down': 1,
        'left': 0,
        'right': 2
        }

dir_changes = [
        -1, # left
        4,  # down
        1,  # right
        -4, # up
        0   # no change
        ]

def is_hole(reward, done):
    if reward == 0 and done == 1:
        return True
    return False

def is_goal(reward, done):
    if reward == 1 and done == 1:
        return True
    return False

def viable_actions(current_pos):
    # top - 0-3
    # bottom - 12-15
    # left - 0, 4, 8, 12 (p % 4 == 0)
    # right - 3, 7, 11, 15 (p % 4 == 3)
    dir_no_go = []
    if current_pos < 4:
        dir_no_go.append(action_dict['up'])
    if current_pos > 11:
        dir_no_go.append(action_dict['down'])
    if current_pos % 4 == 0:
        dir_no_go.append(action_dict['left'])
    if current_pos % 4 == 3:
        dir_no_go.append(action_dict['right'])

    return set(range(4)) - set(dir_no_go)


def actual_change(pos_i, pos_f):
    # determine change that actually happened
    diff = pos_f - pos_i

    if diff == -1:      # left
        return 0
    elif diff == 1:     # right
        return 2
    elif diff == -4:    # up
        return 3
    elif diff == 4:     # down
        return 1
    else:               # didn't move
        return 4

def next_pos(current_pos, direction):

    if direction in viable_actions(current_pos):
        return current_pos + dir_changes[direction]
    return current_pos

def choose_next_move(current_pos, visited, known_holes):

    print current_pos, visited, known_holes

    dir_options = viable_actions(current_pos)
    #print 'dir options', dir_options

    next_pos_options = [next_pos(current_pos, d) for d in dir_options]
    #print 'next pos options', next_pos_options

    good_options = set(next_pos_options) - set(visited) - set(known_holes)
    #print 'good options', good_options

    if len(good_options) > 0:
        new_pos = random.choice(list(good_options))
    else:
        new_pos = random.choice(list(set(next_pos_options) - set(known_holes)))

    return actual_change(current_pos, new_pos)


known_holes = []
found = False
i_episode = 0
#for i_episode in xrange(100):
#    if found is False:
while not found:
    observation= env.reset()
    visited = [observation]
    for t in xrange(100):
        #action = env.action_space.sample()
        action = choose_next_move(observation, visited, known_holes)
        print '------------'
        print 'attempted action:', dir_map[action]
        initial_pos = observation
        observation, reward, done, info = env.step(action)
        visited = list(set(visited) | set([observation]))
        print 'actual action:', dir_map[actual_change(initial_pos, observation)]
        env.render()
        print visited
        print 'holes:', known_holes
        if is_hole(reward, done):
            known_holes = list(set(known_holes) | set([observation]))
            print '*************************'
            print 'hole found! restarting.', i_episode
            print '*************************'
            break
        elif is_goal(reward, done):
            print '*************************'
            print 'woooooooooooooo!', i_episode
            print '*************************'
            found = True
            break
    i_episode += 1
















