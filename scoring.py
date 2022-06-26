# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 13:38:36 2022

@author: Jacob
"""

import numpy as np


def calculate_score(outcome, category):
    if category == 0:
        score = score_type(outcome, 1)
    elif category == 1:
        score = score_type(outcome, 2)
    elif category == 2:
        score = score_type(outcome, 3)
    elif category == 3:
        score = score_type(outcome, 4)
    elif category == 4:
        score = score_type(outcome, 5)
    elif category == 5:
        score = score_type(outcome, 6)
    elif category == 6:
        score = score_pair(outcome)
    elif category == 7:
        score = score_two_pairs(outcome)
    elif category == 8:
        score = score_three_of_a_kind(outcome)
    elif category == 9:
        score = score_four_of_a_kind(outcome)
    elif category == 10:
        score = score_small_straight(outcome)
    elif category == 11:
        score = score_large_straight(outcome)
    elif category == 12:
        score = score_house(outcome)
    elif category == 13:
        score = score_chance(outcome)
    elif category == 14:
        score = score_yatzy(outcome)
    return score


def score_type(outcome, n):
    return n*outcome.cumlist[n - 1] - 3*n


def score_pair(outcome):
    return score_n_of_a_kind(outcome, 2)


def score_two_pairs(outcome):
    score = 0
    first_pair_found = False
    score_first_pair = 0
    for i, x in reversed(list(enumerate(outcome.cumlist))):
        if x >= 2:
            if first_pair_found:
                score = 2*(i + 1) + score_first_pair
                break
            else:
                first_pair_found = True
                score_first_pair = 2*(i + 1)
    return score


def score_three_of_a_kind(outcome):
    return score_n_of_a_kind(outcome, 3)


def score_four_of_a_kind(outcome):
    return score_n_of_a_kind(outcome, 4)


def score_small_straight(outcome):
    if all(np.array(outcome.cumlist[:5]) > 0):
        return 15
    else:
        return 0


def score_large_straight(outcome):
    if all(np.array(outcome.cumlist[1:6]) > 0):
        return 20
    else:
        return 0


def score_house(outcome):
    pair_found = False
    triple_found = False
    score = 0
    score_pair = 0
    score_triple = 0
    for i, x in reversed(list(enumerate(outcome.cumlist))):
        if x >= 3 and not triple_found:
            if pair_found:
                score = 3*(i + 1) + score_pair
                break
            else:
                triple_found = True
                score_triple = 3*(i + 1)
        elif x >= 2 and not pair_found:
            if triple_found:
                score = 2*(i + 1) + score_triple
                break
            else:
                pair_found = True
                score_pair = 2*(i + 1)
    return score


def score_chance(outcome):
    score = 0
    for i, x in enumerate(outcome.cumlist):
        score += (i + 1)*x
    return score


def score_yatzy(outcome):
    if score_n_of_a_kind(outcome, 5) > 0:
        return score_n_of_a_kind(outcome, 5) + 50
    else:
        return 0


def score_n_of_a_kind(outcome, n):
    score = 0
    for i, x in reversed(list(enumerate(outcome.cumlist))):
        if x >= n:
            score = n*(i + 1)
            break
    return score
