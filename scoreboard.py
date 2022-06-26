# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 14:36:01 2022

@author: Jacob
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy

class Scoreboard():
    def __init__(self, state):
        self.state = np.array(state, 'int')
        self.num_categories = len(state)
        self.index = sum(2**np.arange(self.num_categories) * self.state)



def all_states(num_missing, num_categories):
    def _all_states_recursion(num_missing, num_categories, ongoing, finished):
        if num_missing == num_categories:
            # final = ongoing.copy()''
            ongoing.extend([1]*num_categories)
            finished.append(ongoing)
        elif num_missing == 0:
            ongoing.extend([0]*num_categories)
            finished.append(ongoing)
        else:
            ongoing0 = ongoing.copy()
            ongoing0.append(0)
            finished = _all_states_recursion(num_missing, num_categories-1, ongoing0, finished)
            
            ongoing1 = ongoing.copy()
            ongoing1.append(1)
            finished = _all_states_recursion(num_missing-1, num_categories-1, ongoing1, finished)
        return finished

    return _all_states_recursion(num_missing, num_categories, [], [])
    
    

if __name__ == '__main__':    
    
    num_missing = 0
    num_categories = 15
    
    states = all_states(num_missing, num_categories)
    print(states)
    print(scipy.special.comb(num_categories, num_missing), len(states))
    
