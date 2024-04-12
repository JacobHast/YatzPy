# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 14:33:36 2022

@author: Jacob
"""

import numpy as np
import dice
import scoring
import scoreboard
import time
import pickle


def best_score(outcome, board, board_EV, score_lists, return_priority=False):
    points = np.empty(board.num_categories)
    points[:] = -np.inf
    if board.bonussum != None:
        maxsum = board.max_bonussum_remaining()
        minsum = board.min_bonussum_remaining()
        
    for category in range(board.num_categories):
        if board.state[category] == 1:
            category_points = score_lists[outcome.index][category]
            new_index = board.index - 2**category
            if board.bonussum != None:
                if category > 5:
                    new_bonussum = board.bonussum
                elif board.bonussum == 'bonus':
                    new_bonussum = 'bonus'
                elif board.bonussum == 'nobonus':
                    new_bonussum = 'nobonus'
                else:
                    new_bonussum = board.bonussum + category_points
                    new_maxsum = maxsum - (category + 1)*2
                    new_minsum = minsum + (category + 1)*3
                    if new_bonussum + new_maxsum < 0:
                        new_bonussum = 'nobonus'
                    elif new_bonussum + new_minsum >= 0:
                        new_bonussum = 'bonus'   
                # print(board, scoreboard.index_to_state(board.index, 15), board.index)
                board_points = board_EV[new_index][new_bonussum] 
            else:
                board_points = board_EV[new_index]
            points[category] = category_points + board_points
    if return_priority:
        isorted = np.argsort(-points)
        points_sorted = points[isorted]
        isorted = isorted[points_sorted != -np.inf]
        points_sorted = points_sorted[points_sorted != -np.inf]
        return points_sorted, isorted
    else:
        return max(points)


def best_roll(outcomes, outcome_probabilities, board, board_EV, score_lists, M_reroll_list, num_rolls, current_dice=None):
    best_scores = []
    best_scores.append([best_score(outcome, board, board_EV, score_lists) for outcome in outcomes])

    for rolls_remaining in range(1, num_rolls):
        best_scores.append([max(M_reroll@best_scores[rolls_remaining - 1]) for M_reroll in M_reroll_list])
    
    if current_dice==None:
        # best_scores.append([max(M_reroll@best_scores[-1]) for M_reroll in M_reroll_list])
        expected_score = best_scores[-1]@outcome_probabilities
        return expected_score
    else:
        reroll_scores = M_reroll_list[current_dice.index]@best_scores[-1]
        isorted = np.argsort(-reroll_scores)

        expected_scores = reroll_scores[isorted]
        dice_keep = np.array(current_dice.find_subsets())[isorted]
        return expected_scores, dice_keep


def make_board_EV(num_dice, num_rolls, num_categories, filename):
    tic = time.perf_counter()
    total_board_states = 2**num_categories
    board_states_done = 0
    
    M_reroll_list = dice.get_reroll_matrices(num_dice)  
    outcomes = dice.all_outcomes(num_dice)
    board_EV = np.zeros(total_board_states)
    outcome_probabilities = np.array([outcome.probability() for outcome in outcomes])
    
    score_lists = [[scoring.calculate_score(outcome, category)  for category in range(num_categories)] for outcome in outcomes]
    
    for turns_remaining in range(1, num_categories + 1):
        states = scoreboard.all_states(turns_remaining, num_categories)
        
        for state in states:
            board = scoreboard.Scoreboard(state) 
            
            board_EV[board.index] = best_roll(outcomes, outcome_probabilities, board, board_EV, 
                                                    score_lists, M_reroll_list, num_rolls)
        board_states_done += len(states)
        board_states_remaining = total_board_states - board_states_done
        toc = time.perf_counter()
        elapsed = toc - tic
        rate = board_states_done/elapsed
        expected_time_remaining = board_states_remaining/rate
        expected_finish = time.time() + expected_time_remaining
        time_string = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(expected_finish))
        
        print(f"# states done: {board_states_done} out of {total_board_states} (rate: {len(states)/elapsed:.2g}/s) \
              \nExpected finished: {time_string}")
    
    toc = time.perf_counter()
    elapsed_total = toc - tic
    print(f"Total elapsed time: {elapsed_total:.2g}s. ({num_categories} categories)")
    np.save(f"expected_values/{filename}", board_EV)


def make_board_EV_bonus(num_dice, num_rolls, num_categories, filename):
    tic = time.perf_counter()
    total_board_states = 2**num_categories
    board_states_done = 0
    
    M_reroll_list = dice.get_reroll_matrices(num_dice)  
    outcomes = dice.all_outcomes(num_dice)

    board_EV = [{} for _ in range(total_board_states)]
    board_EV[0] = {'bonus': 50, 'nobonus': 0}
    outcome_probabilities = np.array([outcome.probability() for outcome in outcomes])
    
    score_lists = [[scoring.calculate_score(outcome, category)  for category in range(num_categories)] for outcome in outcomes]
    
    for turns_remaining in range(1, num_categories + 1):
        states = scoreboard.all_states(turns_remaining, num_categories)
        
        for state in states:
            bonussums = scoreboard.Scoreboard(state).possible_bonussum()
            for bonussum in bonussums:
                board = scoreboard.Scoreboard(state, bonussum) 
                board_EV[board.index].update({bonussum: best_roll(outcomes, outcome_probabilities, board, board_EV, 
                                                        score_lists, M_reroll_list, num_rolls)})
        board_states_done += len(states)
        board_states_remaining = total_board_states - board_states_done
        toc = time.perf_counter()
        elapsed = toc - tic
        rate = board_states_done/elapsed
        expected_time_remaining = board_states_remaining/rate
        expected_finish = time.time() + expected_time_remaining
        time_string = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(expected_finish))
        
        print(f"# states done: {board_states_done} out of {total_board_states} (rate: {len(states)/elapsed:.2g}/s) \
              \nExpected finished: {time_string}")
    
    toc = time.perf_counter()
    elapsed_total = toc - tic
    print(f"Total elapsed time: {elapsed_total:.2g}s. ({num_categories} categories)")
    
    
    pickle_out = open(f"{filename}", "wb")
    pickle.dump(board_EV, pickle_out)
    pickle_out.close()
    
#%%

if __name__ == "__main__":
    NUM_DICE_TOTAL = 5
    NUM_ROLLS_TOTAL = 3
    NUM_CATEGORIES = 15
    # filename = "EV_nobonus"
    # make_board_EV(NUM_DICE_TOTAL, NUM_ROLLS_TOTAL, NUM_CATEGORIES, filename)
    #%%
    filename = f"expected_values/EV_bonus.npy"
    
    make_board_EV_bonus(NUM_DICE_TOTAL, NUM_ROLLS_TOTAL, NUM_CATEGORIES, filename)
    
    
    # filehandler = open(filename, 'rb') 
    # U = pickle.load(filehandler)
    # board_EV = np.load(filename, allow_pickle=True)
    
    # M_reroll_list = dice.get_reroll_matrices(NUM_DICE_TOTAL)  
    # outcomes = dice.all_outcomes(NUM_DICE_TOTAL)
    # outcome_probabilities = np.array([outcome.probability() for outcome in outcomes])
    # state = np.ones(NUM_CATEGORIES)
     
    # board = scoreboard.Scoreboard(state)
    # score_lists = [[scoring.calculate_score(outcome, category)  for category in range(NUM_CATEGORIES)] for outcome in outcomes]
    
    
    # d = dice.Dice(cumlist=[2,0,0,1,1,1])
    # expected_scores, dice_keep = best_roll(outcomes, outcome_probabilities, board, 
    #                                        board_EV, score_lists, M_reroll_list, 2, current_dice=d)
    
    
    
    
    
