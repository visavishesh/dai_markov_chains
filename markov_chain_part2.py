import csv
import pandas as pd
import numpy as np

df = pd.read_csv("intermediate_markov_output.csv")

df.head()

df["simple_transition"] = df["simple_from"]+"_to_"+df["simple_to"]

transition_count = pd.crosstab(index=df.simple_from, columns=df.simple_to)
print("Number of Transitions")
print("-----------------------------------------------")
print(transition_count)
print()

time_spent = pd.crosstab(values=df.time_spent,aggfunc=np.sum,index=df.simple_from, columns=df.simple_to)
print("Time Spent")
print("-----------------------------------------------")
print(time_spent)
print()

draw_seconds = transition_count * time_spent
print("Draw Seconds (Number of Draws x Time Spent)")
print("-----------------------------------------------")
print(draw_seconds)
print()

total_draw_seconds_spent = draw_seconds.sum(axis=1)
print("Total Draw Seconds in 'from state'")
print("-----------------------------------------------")
print(total_draw_seconds_spent)
print()

merged_transition_count = pd.concat([transition_count,total_draw_seconds_spent],axis=1)
merged_transition_count.columns = ["bite","safe","unsafe","wipe","total_draw_seconds_spent"]
print("Concatenated Matrix")
print("-----------------------------------------------")
print(merged_transition_count)
print()

equilibrium = merged_transition_count[["bite","safe","unsafe","wipe"]].div(merged_transition_count["total_draw_seconds_spent"],axis=0)
print("Equilibrium Probabilities (Number of Transitions / Total Draw Seconds in 'from state')")
print("-----------------------------------------------")
print(equilibrium)
print()