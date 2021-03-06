# Analysis of DAI collateralized debt position (CDP) transitions

## Setup

Clone this repo:

    `git clone https://github.com/vic007207/dai_markov_chains.git`

cd into the directory:

    `cd dai_markov_chain`

Install Python3:
  If you do not have homebrew, first install homebrew:

    `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
  
  If you do have homebrew:

    `brew install python3`

To reproduce results, run the following commands:
    `python3 markov_chain_part1.py`
    `python3 markov_chain_part2.py`

If you receive an error because you do not have pandas or numpy installed, run the following commands:
    `pip3 install pandas`
    `pip3 install numpy`
    If you receive a permissions error while attempting to install, re-run as follows:
        `sudo pip3 install pandas`
        `sudo pip3 install numpy`
        You will be prompted to enter your computer login password, do so and hit enter.
    
# Description:

## Pre-processing:
markov_chain_part1.py processes the raw data, labeling each transition with a simplified state transition, ie from ['born','open','shut,'wipe,'bite','safe','unsafe'] to just ['safe','open','unsafe','bite','wipe']. 

This is the 'simple_transition' field. It also adds the time_spent value, which is a simple subtraction of the timestamp of the state being transitioned to minus the timestamp of the state being transitioned from. 

This output is the 'intermediate_markov_output.csv'.
    
## The magic:
markov_chain_part2.py uses pandas and numpy. 
It first reads and parses the intermediate output file, then cross-tabulates the count of transitions in each from-to state pair. 
It then sums the time spent in each 'from' state (ie 'safe' and 'unsafe'). 
Lastly, it divides the # of transitions for each state pair by the total time spent in the 'from' state to produce the final output.

### A little backfground on states:
    bite = debt-tranche that has been liquidated
    wipe/shut = debt-tranche that has been voluntarily closed by owner
    unsafe = CDP is below 150% collateralization ratio
    safe = CDP is not below 150% collateralization ratio
    open = CDP is safe and is still open, these are present to properly acount for CDPs still open at the end of the observation period (UNIX 1549495867). They contribute to the time spent in 'safe' state, but not to the number of transitions from the 'safe' state.

# The Code and the Output

## Step 1

### Reads the File
df = pd.read_csv("intermediate_markov_output.csv")
df.head()

### output: none

## Step 2

### Produces a matrix of the number of transitions between each 'from' and 'to' state
transition_count = pd.crosstab(index=df.simple_from, columns=df.simple_to)

### output:
Number of Transitions
-----------------------------------------------
| simple_to   | bite | open | safe | unsafe | wipe |
| ----------- |:----:|:----:|:----:|:------:| ----:|
| simple_from |      |      |      |        |      |
| safe        | 0    | 4287 | 0    | 4617   | 17702| 
| unsafe      | 3922 | 5    | 346  | 0      | 344  | 

## Step 3

### Produces a matrix of the time spent in each state (still broken-out by the transition 'from'/'to)
time_spent = pd.crosstab(values=df.time_spent,aggfunc=np.sum,index=df.simple_from, columns=df.simple_to)

### output:
Time Spent
-----------------------------------------------
| simple_to   | bite | open | safe | unsafe | wipe |
| ----------- |:----:|:----:|:----:|:------:| ----:|
| simple_from |         |               |         |              |              |
|safe         |NaN      |   1.814051e+10|   NaN   |  1.955786e+10|  3.472525e+10|
|unsafe       |4120329.0|7.524720e+05|1058672.0|NaN           |  4.609800e+04|

## Step 4

### Multiplies the first two matrices, to get draw-seconds spent in each state (still broken-out by 'from'/'to')
draw_seconds = transition_count * time_spent

### output: 
Draw Seconds (Number of Draws x Time Spent)
-----------------------------------------------
| simple_to   | bite | open | safe | unsafe | wipe |
| ----------- |:----:|:----:|:----:|:------:| ----:|
| simple_from |      |      |      |        |      |               
|safe         | NaN | 7.765534e+13  | NaN  | 9.029862e+13 | 6.147064e+14|
|unsafe       |1.615993e+10| 3.762360e+06  | 366300512.0 | NaN | 1.585771e+07|

## Step 5

### Collapses the break-out to just draw-seconds in 'safe' vs. 'unsafe' (ie by 'from' state)
total_draw_seconds_spent = draw_seconds.sum(axis=1)

### output:
Total Draw Seconds in 'from' state
-----------------------------------------------
|simple_from | draw-time |
| -- | -- |
|safe|7.827734e+14|
|unsafe|1.654585e+10|

## Step 6

### Adds a column for time-spent in 'from' state to the 1st transition count matrix
merged_transition_count = pd.concat([transition_count,total_draw_seconds_spent],axis=1)

### output:
Concatenated Matrix
-----------------------------------------------
| simple_to   | bite | open | safe | unsafe | wipe | total_draw_seconds_spent |
| ----------- |:----:|:----:|:----:|:------:|:------:| ----:|
| simple_from |      |      |      |        |        |      |                                                     
|safe    |        0|     4284|     0|    4617|  17702|             7.827734e+14|
|unsafe   |    3922|     0|   346 |      0 |   344 |             1.654585e+10|

## Step 7 (not really a step)

### Beautification (renaming columns)
merged_transition_count.columns = ["bite","open","safe","unsafe","wipe","total_draw_seconds_spent"]

### output: none

## Step 8

### Simple division of transition count for each state pair by total draw-seconds spent in 'from' state ('safe' vs 'unsafe') across all draws
equilibrium = merged_transition_count[["bite","safe","unsafe","wipe"]].div(merged_transition_count["total_draw_seconds_spent"],axis=0)

### output:
Equilibrium Probabilities (Number of Transitions / Total Draw Seconds in 'from' state, excluding 'open')
-----------------------------------------------
| simple_to   | bite | safe | unsafe | wipe |
| ----------- |:----:|:----:|:------:| ----:|
| simple_from |      |      |        |      |
|safe   |      0.000000e+00|  0.000000e+00 | 5.898259e-12 | 2.261446e-11|
|unsafe|       2.370383e-07 |2.091159e-08 | 0.000000e+00 | 2.079071e-08|
