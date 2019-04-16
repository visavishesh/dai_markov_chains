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
markov_chain_part1.py processes the raw data, labeling each transition with a simplified state transition, ie from ['born','shut,'wipe,'bite','safe','unsafe'] to just ['safe','unsafe','bite','wipe']. 

This is the 'simple_transition' field. It also adds the time_spent value, which is a simple subtraction of the timestamp of the state being transitioned to minus the timestamp of the state being transitioned from. 

This output is the 'intermediate_markov_output.csv'.
    
## The magic:
markov_chains_part2.py uses pandas and numpy. 
It first reads and parses the intermediate output file, then cross-tabulates the count of transitions in each from-to state pair. 
It then sums the time spent in each 'from' state (ie 'safe' and 'unsafe'). 
Lastly, it divides the # of transitions for each state pair by the total time spent in the 'from' state to produce the final output.

# The Code

### Reads the File
df = pd.read_csv("intermediate_markov_output.csv")
df.head()

### Produces a matrix of the number of transitions between each 'from' and 'to' state
transition_count = pd.crosstab(index=df.simple_from, columns=df.simple_to)

### Produces a matrix of the time spent in each state (still broken out by the transition 'from')
time_spent = pd.crosstab(values=df.time_spent,aggfunc=np.sum,index=df.simple_from, columns=df.simple_to)

### Multiplies the first two matrices, to get draw-seconds spent in each state (still broken out by the transition 'from')
draw_seconds = transition_count * time_spent

### Collapses the break out for transition 'from', to just draw-seconds in 'safe' vs. 'unsafe'
total_draw_seconds_spent = draw_seconds.sum(axis=1)

### Adds a time-spent in 'from' state column to the 1st transition count matrix
merged_transition_count = pd.concat([transition_count,total_draw_seconds_spent],axis=1)

### Beautification (renaming columns)
merged_transition_count.columns = ["bite","safe","unsafe","wipe","total_draw_seconds_spent"]

### Simple division of transition count for each state pair by total draw-seconds spent in 'from' state ('safe' vs 'unsafe') across all draws
equilibrium = merged_transition_count[["bite","safe","unsafe","wipe"]].div(merged_transition_count["total_draw_seconds_spent"],axis=0)
