# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 20:54:54 2022

@author: Jacob
"""

import numpy as np
import tkinter as tk
import dice
import scoreboard
import training
import scoring



def get_best_keep():
    if rolls_remaining.get() < 1:
        raise ValueError("Rolls remaining must be at least 1")
        
    state = get_current_state()
    if use_bonus:
        bonussum = get_bonus()
    else:
        bonussum = None
    
    M_reroll_list = dice.get_reroll_matrices(NUM_DICE_TOTAL)  
    outcomes = dice.all_outcomes(NUM_DICE_TOTAL)
    outcome_probabilities = np.array([outcome.probability() for outcome in outcomes])
    
    
    board = scoreboard.Scoreboard(state, bonussum)
    score_lists = [[scoring.calculate_score(outcome, category) for category in range(NUM_CATEGORIES)] for outcome in outcomes]
    
    expected_scores, dice_keep = training.best_roll(outcomes, outcome_probabilities, board, 
                                                    board_EV, score_lists, M_reroll_list, rolls_remaining.get(), current_dice=get_current_dice())
    return expected_scores, dice_keep

def get_best_pick():
    state = get_current_state()
    if use_bonus:
        bonussum = get_bonus()
    else:
        bonussum = None
    
    M_reroll_list = dice.get_reroll_matrices(NUM_DICE_TOTAL)  
    outcomes = dice.all_outcomes(NUM_DICE_TOTAL)
    outcome_probabilities = np.array([outcome.probability() for outcome in outcomes])
    board = scoreboard.Scoreboard(state, bonussum)
    score_lists = [[scoring.calculate_score(outcome, category)  for category in range(NUM_CATEGORIES)] for outcome in outcomes]
    # (outcome, board, board_EV, score_lists, return_priority=False):
    return training.best_score(get_current_dice(), board, board_EV, score_lists, return_priority=True)


def get_current_state():
    player = selected_player.get()
    state = np.ones(NUM_CATEGORIES)
    for i, score in enumerate(scores[player]):
        if score.get() != "":
            state[i] = 0
    return state


def get_current_dice():
    eyelist = []
    for current_dice in current_dice_list:
        eyelist.append(int(current_dice.get()))
    return dice.Dice(eyelist=eyelist)


def calculate_score():
    player = selected_player.get()
    s = 0
    bonussum = 0
    for category, score in enumerate(scores[player]):
        try:
            s += int(score.get())
            if category < 6:
                bonussum += int(score.get())
        except:
            pass
    bonussums[player]["text"] = bonussum
    bonus = get_bonus()
    sbonus = 0
    if bonus == "bonus":
        bonuses[player]["text"] = 50
        sbonus = 50
    elif bonus == "nobonus":
        bonuses[player]["text"] = 0
    if use_bonus:
        state = scoreboard.Scoreboard(get_current_state(), bonus)
    else:
        state = scoreboard.Scoreboard(get_current_state())
    # board_index = sum(2**np.arange(self.num_categories) * state)
    EV = board_EV[state.index][state.bonussum] + s
    sums[player]["text"] = f"{s + sbonus} ({EV:.0f})"


def best_action():
    outputtext.delete("1.0", "end")
    outputtext.insert(tk.INSERT, "Best choices:\n")
    if rolls_remaining.get() > 0:
        expected_scores, keepers = get_best_keep()
        for d, s in zip(keepers, expected_scores):
            outputtext.insert(tk.INSERT, f"{d.eyelist} ({s - expected_scores[0]:.2f})\n")
    elif rolls_remaining.get() == 0:
        expected_scores, pick = get_best_pick()
        for i, s in zip(pick, expected_scores):
            outputtext.insert(tk.INSERT, f"{categories[i]}: {scoring.calculate_score(get_current_dice(), i)} ({s - expected_scores[0]:.2f})\n")


def get_bonus():
    player = selected_player.get()
    bonussum = 0
    for i, score in enumerate(scores[player][:6]):
        if score.get() != "":
            bonussum += int(score.get())
    board = scoreboard.Scoreboard(get_current_state(), bonussum)
    board.reduce_bonussum()
    return board.bonussum

NUM_PLAYERS = 5
categories = [
    "1'ere",
    "2'ere",
    "3'ere",
    "4'ere",
    "5'ere",
    "6'ere",
    "1 par",
    "2 par",
    "3 ens",
    "4 ens",
    "Lille straight",
    "Stor straight",
    "Fuldt hus",
    "Chance",
    "YATZY!"]

NUM_CATEGORIES = len(categories)
NUM_DICE_TOTAL = 5
window = tk.Tk()

width = 5

frame_scores = tk.Frame(master=window)
frame_scores.grid(row=0, column=0)
frame_interface = tk.Frame(master=window)
frame_interface.grid(row=0, column=1, sticky="n")

# Player name fields
for j in range(NUM_PLAYERS):
    # frame = tk.Frame(master=window)
    # frame.grid(row=0, column=j + 1)
    entry = tk.Entry(master=frame_scores, width=8)
    entry.grid(row=0, column=j+1)

# Category name fields
for i in range(NUM_CATEGORIES):
    bonus_spacing = 2*(i > 5)
    label = tk.Label(master=frame_scores, text=categories[i])
    label.grid(row=i+1+bonus_spacing, column=0)
label = tk.Label(master=frame_scores, text='SUM')
label.grid(row=NUM_CATEGORIES+3, column=0)

# Scoring fields
scores = []
sums = [[]]*NUM_PLAYERS
for j in range(NUM_PLAYERS):
    scores.append([])
    for i in range(NUM_CATEGORIES):
        bonus_spacing = 2*(i > 5)
        entry = tk.Entry(master=frame_scores, width=width)
        entry.grid(row=i+1+bonus_spacing, column=j+1)
        scores[j].append(entry)
    label = tk.Label(master=frame_scores)
    label.grid(row=NUM_CATEGORIES+3, column=j + 1)
    sums[j] = label

# Bonus 
label = tk.Label(master=frame_scores, text='SUM')
label.grid(row=7, column=0)
label = tk.Label(master=frame_scores, text='Bonus')
label.grid(row=8, column=0)
bonussums = [[]]*NUM_PLAYERS
bonuses = [[]]*NUM_PLAYERS
for j in range(NUM_PLAYERS):
    label = tk.Label(master=frame_scores)
    label.grid(row=7, column=j+1)
    bonussums[j] = label
    label = tk.Label(master=frame_scores)
    label.grid(row=8, column=j+1) 
    bonuses[j] = label
        

# Player select buttons
selected_player = tk.IntVar(master=window)
for j in range(NUM_PLAYERS):
    rbtn = tk.Radiobutton(master=frame_scores, variable=selected_player, value=j, command=calculate_score)
    rbtn.grid(row=NUM_CATEGORIES+4, column=j+1)
    
# # EV buttons
# for player in range(NUM_PLAYERS):  
#     btn = tk.Button(frame_rolls, text="show EV", command=show_EV)
#     helpbutton.grid(row=NUM_CATEGORIES+5, column=player + 1)

# Dice buttons
current_dice_list = []
frame_dice = tk.Frame(master=frame_interface)
frame_dice.grid(row=1, column=0)
for i in range(NUM_DICE_TOTAL):
    # frame.grid(row=1, column=NUM_PLAYERS + 3 + i)
    entry = tk.Entry(master=frame_dice, width=width)
    current_dice_list.append(entry)
    entry.grid(row=0, column=i)

    
# Remaining roll
frame_rolls = tk.Frame(master=frame_interface)
frame_rolls.grid(row=2, column=0)
rolls_remaining = tk.IntVar(master=window)
rolls_remaining.set(2) # default value

# frame = tk.Frame(master=window)
# frame.grid(row=1, column=NUM_PLAYERS + 4 + NUM_DICE_TOTAL)
dropdown = tk.OptionMenu(frame_rolls, rolls_remaining, 0, 1, 2)
dropdown.grid(row=0, column=0)

# help button
helpbutton = tk.Button(frame_rolls, text="best actions", command=best_action)
helpbutton.grid(row=0, column=1)

# Output text
outputtext = tk.Text(frame_interface, height = 21, width = 26)
outputtext.grid(row=3, column=0)

use_bonus = True

# if use_bonus:
# filename = "expected_values/EV_bonus.npy"
# else:
#     filename = f"expected_values/EV_nobonus.npy"

filename = f"standard_5dice_bonusTrue_blockyatzyTrue"
# filename = f"standard_5dice_bonusTrue_blockyatzyFalse"

board_EV = np.load(filename, allow_pickle=True)

window.mainloop()















