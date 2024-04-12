# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 10:35:09 2022

@author: Jacob
"""

import numpy as np
import scipy
import time
import os
import scipy.special

class Dice:
    def __init__(self, **kwargs):
        if len(kwargs) < 1:
            raise ValueError('One keyword argument is required: index, eyelist or cumlist')
        if len(kwargs) > 1:
            raise ValueError('Only one keyword must be input')

        dicetype, dicevalue = next(iter((kwargs.items())))
        if dicetype == 'cumlist':
            if isinstance(dicevalue, (list, np.ndarray)) and len(dicevalue) == 6:
                self.cumlist = np.array(dicevalue)
                self._cumlist_to_eyelist()
                self.num_dice = int(sum(self.cumlist))
                self._eyelist_to_index()
            else:
                raise ValueError('cumlist must be length 6 list or numpy array')

        elif dicetype == 'eyelist':
            if (isinstance(dicevalue, (list, np.ndarray)) and
                    all([dice in [1, 2, 3, 4, 5, 6] for dice in dicevalue])):
                self.eyelist = np.array(dicevalue, int)
                self._eyelist_to_cumlist()
                self.num_dice = len(self.eyelist)
                self._eyelist_to_index()
            else:
                raise ValueError('eyelist must be list or numpy array of integers between 1 and 6')

        elif dicetype == 'index':
            if isinstance(dicevalue, tuple) and len(dicevalue) == 2:
                self.index = dicevalue[0]
                self.num_dice = int(dicevalue[1])
                if self.index >= num_unique(self.num_dice):
                    raise ValueError('index must be smaller than nchoosek(num_dice + 5, 5)')
                self._index_to_eyelist()
                self._eyelist_to_cumlist()
            else:
                raise ValueError('index-type must be 2-element tuple: (index, num_dice)')
        else:
            raise ValueError('kwarg must be one of the following: index, eyelist')

    def __repr__(self):
        return f"cumulative list: {self.cumlist}, # of dice: {self.num_dice}, index: {self.index}"

    def __add__(self, outcome2):
        sum_cumlist = self.cumlist + outcome2.cumlist
        return Dice(cumlist=sum_cumlist)

    def _cumlist_to_eyelist(self):
        self.eyelist = []
        for i in range(6):
            self.eyelist.extend([i + 1]*self.cumlist[i])

    def _eyelist_to_cumlist(self):
        self.cumlist = np.zeros(6, 'int')
        for i in range(6):
            self.cumlist[i] = sum(self.eyelist == i + 1)

    def _eyelist_to_index(self):
        def pascal(column, row):
            return scipy.special.comb(column + row - 1, column, exact=True)

        def back_cum(column, n):
            x = 0
            for i in range(n):
                x += pascal(column, 6-i)
            return x

        sorted_list = np.flip(np.sort(self.eyelist))
        index = 0
        for i in range(self.num_dice):
            if i < (self.num_dice - 1):
                index += back_cum(i, sorted_list[i] - 1) - back_cum(i, sorted_list[i + 1] - 1)
            else:
                index += back_cum(i, sorted_list[i] - 1)
        self.index = index

    def _index_to_eyelist(self):
        def increase(sorted_list):
            sorted_list = set_value(sorted_list, 0)
            return sorted_list

        def set_value(sorted_list, i):
            if sorted_list[i] < 6:
                sorted_list[i] += 1
            else:
                if i + 1 < len(sorted_list):
                    sorted_list = set_value(sorted_list, i + 1)
                    sorted_list[i] = sorted_list[i + 1]
            return sorted_list

        self.eyelist = np.ones(self.num_dice, 'int')
        for i in range(self.index):
            self.eyelist = increase(self.eyelist)

    def multiplicity(self):
        m = np.math.factorial(self.num_dice)
        for i in range(6):
            m /= np.math.factorial(self.cumlist[i])
        return int(m)

    def probability(self):
        return self.multiplicity()/6**self.num_dice

    def find_subsets(self):
        subsets = []
        return self._find_subsets_recursion(subsets)

    def _find_subsets_recursion(self, subsets, start=0):
        subsets.append(self)
        for i in range(start, 6):
            if self.cumlist[i] > 0:
                new_cumlist = self.cumlist.copy()
                new_cumlist[i] -= 1
                new_dice = Dice(cumlist=new_cumlist)
                subsets = new_dice._find_subsets_recursion(subsets, start=i)
        return subsets

    def outcome_probabilities(self, num_dice_total):
        num_dice_roll = num_dice_total - self.num_dice
        new_outcomes = all_outcomes(num_dice_roll)
        total_outcomes = [self + outcome for outcome in new_outcomes]

        p = np.zeros(num_unique(num_dice_total))
        for total_outcome, new_outcome in zip(total_outcomes, new_outcomes):
            p[total_outcome.index] = new_outcome.probability()

        return p

    def generate_reroll_matrix(self):
        M = [sub.outcome_probabilities(self.num_dice) for sub in self.find_subsets()]
        return np.array(M)



def num_unique(num_dice):
    return int(scipy.special.comb(num_dice + 5, 5))

def all_outcomes(num_dice):
    return [Dice(index=(i, num_dice)) for i in range(num_unique(num_dice))]

def get_reroll_matrices(num_dice, from_npy=True):
    if from_npy:
        filename = f"reroll_matrices/reroll_matrix_{num_dice}.npy"
        if os.path.exists(filename):
            M_list = np.load(filename, allow_pickle=True)
        else:
            M_list = [d.generate_reroll_matrix() for d in all_outcomes(num_dice)]
            np.save(filename, M_list)
    else:
        M_list = [d.generate_reroll_matrix() for d in all_outcomes(num_dice)]
    return M_list

def random(num_dice):
    eyelist = np.random.randint(1, 7, size=num_dice)
    return Dice(eyelist=eyelist)
    
    
    
if __name__ == '__main__':
    d = random(5)
    print(d)
    
    
    