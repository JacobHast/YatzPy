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
    filename = f"expected_values/EV_nobonus.npy"
    
    board_EV = np.load(filename, allow_pickle=True)
    
    M_reroll_list = dice.get_reroll_matrices(NUM_DICE_TOTAL)  
    outcomes = dice.all_outcomes(NUM_DICE_TOTAL)
    outcome_probabilities = np.array([outcome.probability() for outcome in outcomes])
    state = get_current_state()
     
    board = scoreboard.Scoreboard(state)
    score_lists = [[scoring.calculate_score(outcome, category)  for category in range(NUM_CATEGORIES)] for outcome in outcomes]
    
    expected_scores, dice_keep = training.best_roll(outcomes, outcome_probabilities, board, 
                                            board_EV, score_lists, M_reroll_list, 2, current_dice=get_current_dice())
    return dice_keep

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
    i = selected_player.get()
    s = 0
       
    for score in scores[i]:
        try:
            s += float(score.get())
        except:
            pass
    
    # sums[i].delete(0 tk.END)
    sums[i]["text"] = int(s)


def best_action():
    keepers = get_best_keep()
    outputtext.delete("1.0", "end")
    outputtext.insert(tk.INSERT, keepers)
    # outputtext.insert()

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

selected_player = tk.IntVar(master=window)


# Player name fields
for j in range(NUM_PLAYERS):
    frame = tk.Frame(master=window)
    frame.grid(row=0, column=j + 1)
    entry = tk.Entry(master=frame, width=8)
    entry.pack()

# Category name fields
for i in range(NUM_CATEGORIES):
    frame = tk.Frame(master=window)
    frame.grid(row=i+1, column=0)
    label = tk.Label(master=frame, text=categories[i])
    label.pack()
frame = tk.Frame(master=window)
frame.grid(row=NUM_CATEGORIES+1, column=0)
label = tk.Label(master=frame, text='sum')
label.pack()    

# Scoring fields
scores = []
sums = [[]]*NUM_PLAYERS
for j in range(NUM_PLAYERS):
    scores.append([])
    for i in range(NUM_CATEGORIES):
        frame = tk.Frame(master=window)
        frame.grid(row=i + 1, column=j + 1)
        entry = tk.Entry(master=frame, width=width)
        scores[j].append(entry)
        entry.pack()
    frame = tk.Frame(master=window)
    frame.grid(row=NUM_CATEGORIES+1, column=j + 1)
    label = tk.Label(master=frame, text='0')
    label.pack() 
    sums[j] = label

# Summing buttons
for j in range(NUM_PLAYERS):
    frame = tk.Frame(master=window)
    frame.grid(row=NUM_CATEGORIES+2, column=j + 1)
    
    rbtn = tk.Radiobutton(master=frame, variable=selected_player, value=j, command=calculate_score)
    rbtn.pack()
    
current_dice_list = []
# Dice buttons
for i in range(NUM_DICE_TOTAL):
    frame = tk.Frame(master=window)
    frame.grid(row=1, column=NUM_PLAYERS + 3 + i)
    entry = tk.Entry(master=frame, width=width)
    current_dice_list.append(entry)
    entry.pack()
    
# Remaining roll
rolls_remaining = tk.IntVar(master=window)
rolls_remaining.set(3) # default value
frame = tk.Frame(master=window)
frame.grid(row=1, column=NUM_PLAYERS + 4 + NUM_DICE_TOTAL)
dropdown = tk.OptionMenu(frame, rolls_remaining, 0, 1, 2, 3)
dropdown.pack()

# Output text
frame = tk.Frame(master=window)
frame.grid(row=2, column=NUM_PLAYERS + 3)
outputtext = tk.Text(frame, height = 5, width = 52)
outputtext.pack()


# Output text
frame = tk.Frame(master=window)
frame.grid(row=2, column=NUM_PLAYERS + 4)
helpbutton = tk.Button(frame, text="best actions", command=best_action)
helpbutton.pack()

window.mainloop()















