#imports dependencies
import csv
import pandas as pd
import numpy as np

#reads the csv file into a dataframe
df = pd.read_csv("intermediate_markov_output.csv")
df.head()

#cross-tabulates the dataframe, crossing the simple_from and simple_to columns
#this produces a matrix of the number of transitions between each 'from' and 'to' state
transition_count = pd.crosstab(index=df.simple_from, columns=df.simple_to)
print("Number of Transitions")
print("-----------------------------------------------")
print(transition_count)
print()

#creates a 2nd matrix
#cross-tabulates the 'from' and 'to' states, same as the previous line, but this time sums the 'time_spent' column instead of a simple count of the number of matching rows
time_spent = pd.crosstab(values=df.time_spent,aggfunc=np.sum,index=df.simple_from, columns=df.simple_to)
print("Time Spent")
print("-----------------------------------------------")
print(time_spent)
print()

#this multiples the two matrices together
#produces a 3rd matrix of the number of draw-seconds spent in 'safe' vs. 'unsafe', broken out into sections for all of the 'from'/'to' states
draw_seconds = transition_count * time_spent
print("Draw Seconds (Number of Draws x Time Spent)")
print("-----------------------------------------------")
print(draw_seconds)
print()

#produces a 4th matrix
#this condenses the above 3rd matrix, collapsing all of the broken out sections, into just draw-seconds spent in 'safe' vs. 'unsafe'
total_draw_seconds_spent = draw_seconds.sum(axis=1)
print("Total Draw Seconds in 'from state'")
print("-----------------------------------------------")
print(total_draw_seconds_spent)
print()

#produces the 5th matrix
#this concatenates the 1st matrix of transition counts with the 4th matrix of draw-time spent in 'safe' vs. 'unsafe' 
#effectively, this simply adds a column to the 1st matrix for the total draw-seconds spent in each row (ie 'safe' and 'unsafe')
merged_transition_count = pd.concat([transition_count,total_draw_seconds_spent],axis=1)
merged_transition_count.columns = ["bite","safe","unsafe","wipe","total_draw_seconds_spent"]
print("Concatenated Matrix")
print("-----------------------------------------------")
print(merged_transition_count)
print()

#this produces the 6th and final matrix
#this performans a division operation, dividing the number of transitions for each 'from-to' pair of states by the total draw-seconds spent in the 'from' state
equilibrium = merged_transition_count[["bite","safe","unsafe","wipe"]].div(merged_transition_count["total_draw_seconds_spent"],axis=0)
print("Equilibrium Probabilities (Number of Transitions / Total Draw Seconds in 'from state')")
print("-----------------------------------------------")
print(equilibrium)
print()