# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 14:36:50 2022

@author: Jacob
"""

import numpy as np
import scoring


def standard_rules(num_dice, use_bonus, block_yatzy):
    if num_dice not in [5, 6]:
        raise ValueError("Standard rules must use 5 or 6 dice")
        
    name = f"standard_{num_dice}dice_bonus{use_bonus}_blockyatzy{block_yatzy}"
    ruleset = scoring.Ruleset(name, num_dice, num_rolls=3, use_bonus=use_bonus, bonus_points=50, block_yatzy=block_yatzy)
    # 1-6 categories
    ruleset.add_categories(eye_categories(num_dice))

    # 1 par
    category_1par = scoring.Category("1 par", score_pair)
    ruleset.add_category(category_1par)

    # 2 par
    category_2par = scoring.Category("2 par", score_two_pairs)
    ruleset.add_category(category_2par)
    
    if num_dice == 6:
        # 3 par
        category_2par = scoring.Category("3 par", score_three_pairs)
        ruleset.add_category(category_2par)   

    # 3 ens
    category_3ens = scoring.Category("3 ens", score_three_of_a_kind)
    ruleset.add_category(category_3ens)

    # 4 ens
    category_4ens = scoring.Category("4 ens", score_four_of_a_kind)
    ruleset.add_category(category_4ens)
    
    if num_dice == 6:
        # 2 x 3 ens
        category_2par = scoring.Category("2x3 ens", score_two_x_three)
        ruleset.add_category(category_2par)           
    
    # lille straight
    category_lille = scoring.Category("Lille straight", score_small_straight)
    ruleset.add_category(category_lille)

    # stor straight
    category_stor = scoring.Category("Stor straight", score_large_straight)
    ruleset.add_category(category_stor)
    
    if num_dice == 6:
        # royal straight
        category_2par = scoring.Category("Royal straight", score_royal_straight)
        ruleset.add_category(category_2par)          

    # hus
    category_hus = scoring.Category("Hus", score_house)
    ruleset.add_category(category_hus)

    # chance
    category_chance = scoring.Category("Chance", score_chance)
    ruleset.add_category(category_chance)

    # YATZY
    category_yatzy = scoring.Category("YATZY!", lambda outcome: score_yatzy(outcome, num_dice, 50))
    ruleset.add_category(category_yatzy)
    return ruleset


def standard_5dice():
    return standard_rules(5, True, False)
    
    # num_dice = 5
    # num_rolls = 3
    # ruleset = scoring.Ruleset("5dice_standard", num_dice, num_rolls, use_bonus=True, bonus_points=50)

    # # 1-6 categories
    # ruleset.add_categories(eye_categories(num_dice))

    # # 1 pair
    # category_1par = scoring.Category("1 par", lambda outcome, scoreboard: score_pair(outcome))
    # ruleset.add_category(category_1par)

    # # 2 pairs
    # category_2par = scoring.Category("2 par", lambda outcome, scoreboard: score_two_pairs(outcome))
    # ruleset.add_category(category_2par)

    # # 3 ens
    # category_3ens = scoring.Category("3 ens", lambda outcome, scoreboard: score_three_of_a_kind(outcome))
    # ruleset.add_category(category_3ens)

    # # 4 ens
    # category_4ens = scoring.Category("4 ens", lambda outcome, scoreboard: score_four_of_a_kind(outcome))
    # ruleset.add_category(category_4ens)

    # # lille straight
    # category_lille = scoring.Category("Lille straight", lambda outcome, scoreboard: score_small_straight(outcome))
    # ruleset.add_category(category_lille)

    # # stor straight
    # category_stor = scoring.Category("Stor straight", lambda outcome, scoreboard: score_large_straight(outcome))
    # ruleset.add_category(category_stor)

    # # hus
    # category_hus = scoring.Category("Hus", lambda outcome, scoreboard: score_house(outcome))
    # ruleset.add_category(category_hus)

    # # chance
    # category_chance = scoring.Category("Chance", lambda outcome, scoreboard: score_chance(outcome))
    # ruleset.add_category(category_chance)

    # # YATZY
    # category_yatzy = scoring.Category("YATZY!", lambda outcome, scoreboard: score_yatzy(outcome, num_dice, 50))
    # ruleset.add_category(category_yatzy)
    # return ruleset
 

def nobonus_5dice():
    num_dice = 5
    num_rolls = 3
    ruleset = scoring.Ruleset("nobonus_5dice", num_dice, num_rolls, use_bonus=False)

    # 1-6 categories
    ruleset.add_categories(eye_categories(num_dice))

    # 1 pair
    category_1par = scoring.Category("1 par", lambda outcome, scoreboard: score_pair(outcome))
    ruleset.add_category(category_1par)

    # 2 pairs
    category_2par = scoring.Category("2 par", lambda outcome, scoreboard: score_two_pairs(outcome))
    ruleset.add_category(category_2par)

    # 3 ens
    category_3ens = scoring.Category("3 ens", lambda outcome, scoreboard: score_three_of_a_kind(outcome))
    ruleset.add_category(category_3ens)

    # 4 ens
    category_4ens = scoring.Category("4 ens", lambda outcome, scoreboard: score_four_of_a_kind(outcome))
    ruleset.add_category(category_4ens)

    # lille straight
    category_lille = scoring.Category("Lille straight", lambda outcome, scoreboard: score_small_straight(outcome))
    ruleset.add_category(category_lille)

    # stor straight
    category_stor = scoring.Category("Stor straight", lambda outcome, scoreboard: score_large_straight(outcome))
    ruleset.add_category(category_stor)

    # hus
    category_hus = scoring.Category("Hus", lambda outcome, scoreboard: score_house(outcome))
    ruleset.add_category(category_hus)

    # chance
    category_chance = scoring.Category("Chance", lambda outcome, scoreboard: score_chance(outcome))
    ruleset.add_category(category_chance)

    # YATZY
    category_yatzy = scoring.Category("YATZY!", lambda outcome, scoreboard: score_yatzy(outcome, num_dice, 50))
    ruleset.add_category(category_yatzy)
    return ruleset


def gentleman_5dice():
    num_dice = 5
    num_rolls = 3
    ruleset = scoring.Ruleset("5dice_standard", num_dice, num_rolls, use_bonus=True, bonus_points=50)

    # 1-6 categories
    ruleset.add_categories(eye_categories(num_dice))

    # 1 pair
    category_1par = scoring.Category("1 par", lambda outcome, scoreboard: score_pair(outcome))
    ruleset.add_category(category_1par)

    # 2 pairs
    category_2par = scoring.Category("2 par", lambda outcome, scoreboard: score_two_pairs(outcome))
    ruleset.add_category(category_2par)

    # 3 ens
    category_3ens = scoring.Category("3 ens", lambda outcome, scoreboard: score_three_of_a_kind(outcome))
    ruleset.add_category(category_3ens)

    # 4 ens
    category_4ens = scoring.Category("4 ens", lambda outcome, scoreboard: score_four_of_a_kind(outcome))
    ruleset.add_category(category_4ens)

    # lille straight
    category_lille = scoring.Category("Lille straight", lambda outcome, scoreboard: score_small_straight(outcome))
    ruleset.add_category(category_lille)

    # stor straight
    category_stor = scoring.Category("Stor straight", lambda outcome, scoreboard: score_large_straight(outcome))
    ruleset.add_category(category_stor)

    # hus
    category_hus = scoring.Category("Hus", lambda outcome, scoreboard: score_house(outcome))
    ruleset.add_category(category_hus)

    # chance
    category_chance = scoring.Category("Chance", lambda outcome, scoreboard: score_chance(outcome))
    ruleset.add_category(category_chance)

    # YATZY
    category_yatzy = scoring.Category("YATZY!", lambda outcome, scoreboard: score_yatzy_gentleman(outcome, num_dice, 50, scoreboard))
    ruleset.add_category(category_yatzy)
    return ruleset
   
    
def eye_categories(num_dice):
    categories = []
    name = f"1'ere"
    score_fnc = lambda outcome: score_type(outcome, 1, num_dice)
    categories.append(scoring.Category(name, score_fnc))
    name = f"2'ere"
    score_fnc = lambda outcome: score_type(outcome, 2, num_dice)
    categories.append(scoring.Category(name, score_fnc))    
    name = f"3'ere"
    score_fnc = lambda outcome: score_type(outcome, 3, num_dice)
    categories.append(scoring.Category(name, score_fnc))
    name = f"4'ere"
    score_fnc = lambda outcome: score_type(outcome, 4, num_dice)
    categories.append(scoring.Category(name, score_fnc))
    name = f"5'ere"
    score_fnc = lambda outcome: score_type(outcome, 5, num_dice)
    categories.append(scoring.Category(name, score_fnc))
    name = f"6'ere"
    score_fnc = lambda outcome: score_type(outcome, 6, num_dice)
    categories.append(scoring.Category(name, score_fnc))
    

        
    # print([category.score_fnc(outcome) for category in categories])
    return categories

def generate_score_type_fnc(outcome, eye, num_dice):
    f = score_type(outcome, eye, num_dice)
    return f

def score_type(outcome, eye, num_dice):
    return eye*outcome.cumlist[eye - 1] - (num_dice - 2)*eye


def score_pair(outcome):
    return score_n_of_a_kind(outcome, 2)


def score_sets(outcome, set_size, num_sets):
    score = 0
    sets_found = 0
    for i, x in reversed(list(enumerate(outcome.cumlist))):
        if x >= set_size:
            score += set_size*(i + 1)
            sets_found += 1
        if sets_found == num_sets:
            break

    if sets_found < num_sets:
        score = 0
    return score


def score_two_pairs(outcome):
    return score_sets(outcome, set_size=2, num_sets=2)


def score_three_pairs(outcome):
    return score_sets(outcome, set_size=2, num_sets=3)


def score_two_x_three(outcome):
    return score_sets(outcome, set_size=3, num_sets=2)
    

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


def score_royal_straight(outcome):
    if all(np.array(outcome.cumlist) > 0):
        return 30
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


def score_yatzy(outcome, num_dice, yatzy_points):
    if score_n_of_a_kind(outcome, num_dice) > 0:
        return score_n_of_a_kind(outcome, num_dice) + yatzy_points
    else:
        return 0


def score_yatzy_blocked(outcome, num_dice, yatzy_points):
    points = score_yatzy(outcome, num_dice, yatzy_points)
    if points == 0:
        points = -np.inf
    return points


def score_n_of_a_kind(outcome, n):
    score = 0
    for i, x in reversed(list(enumerate(outcome.cumlist))):
        if x >= n:
            score = n*(i + 1)
            break
    return score


if __name__ == "__main__":
    import dice
    
    r = standard_5dice()
