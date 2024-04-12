# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 14:36:01 2022

@author: Jacob
"""

import numpy as np


class Scoreboard():
    def __init__(self, state, bonussum=None):
        self.state = np.array(state, 'int')
        self.num_categories = len(state)
        self.index = sum(2**np.arange(self.num_categories) * self.state)
        self.bonussum = bonussum

    def __repr__(self):
        return f"board state: {self.state}, bonus-sum: {self.bonussum}"

    def max_bonussum_remaining(self, num_dice=5):
        state = self.state
        s = 0
        for i in range(6):
            if state[i] == 1:
                s += 2*(i + 1)
        return s

    def min_bonussum_remaining(self, num_dice=5):
        state = self.state
        s = 0
        for i in range(6):
            if state[i] == 1:
                s -= (num_dice - 2)*(i + 1)
        return s

    def possible_bonussum(self, num_dice=5):
        def _append_unique(array, x):
            if x not in array:
                array.append(x)
            return array
        
        def _possible_recursion(possible, state_eyes, i, s):
            if i == 6:
                return _append_unique(possible, s)
            elif state_eyes[i] == 0:
                for j in range(num_dice + 1):
                    possible = _possible_recursion(possible, state_eyes, i + 1, s + (i + 1)*(j - (num_dice - 2)))
            else:
                return _possible_recursion(possible, state_eyes, i + 1, s)
            return possible

        state_eyes = self.state[:6]
        possible = _possible_recursion([], state_eyes, 0, 0)
        possible.sort()
        possible_reduced = []
        maxsum = self.max_bonussum_remaining()
        minsum = self.min_bonussum_remaining()
        for i, s in enumerate(possible):
            if s + minsum >= 0:
                if 'bonus' not in possible_reduced:
                    possible_reduced.append('bonus')
            elif s + maxsum < 0:
                if 'nobonus' not in possible_reduced:
                    possible_reduced.append('nobonus')
            else:
                possible_reduced.append(s)

        return possible_reduced

    def reduce_bonussum(self):
        maxsum = self.max_bonussum_remaining()
        minsum = self.min_bonussum_remaining()
        b = self.bonussum
        if b != 'bonus' and b != 'nobonus':
            if b + minsum >= 0:
                b = 'bonus'
            elif b + maxsum < 0:
                b = 'nobonus'
        self.bonussum = b

    def fill_category(self, category, points):
        if self.state[category] == 0:
            raise ValueError('Category is already taken!')
        self.state[category] = 0
        self.index -= 2**category
        if category < 6 and self.bonussum != 'bonus' and self.bonussum != 'nobonus':
            self.bonussum += points
            self.reduce_bonussum()


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
    

def total_boardstates_bonus(num_categories, num_dice):
    num_other_states = 2**(num_categories - 6)
    num_total_states = 0
    for i in range(2**6):
        eye_state = np.array(list(np.binary_repr(i, 6)), 'int')
        num_total_states += len(Scoreboard(eye_state).possible_bonussum(num_dice))*num_other_states
    return num_total_states
        
    


def index_to_state(index, NUM_CATEGORIES):
    state = [int(x) for x in np.binary_repr(index, NUM_CATEGORIES)]
    state.reverse()
    return state
    


if __name__ == '__main__':    
    
    print(total_boardstates_bonus(15, 5))

    
    
    
    
    
    