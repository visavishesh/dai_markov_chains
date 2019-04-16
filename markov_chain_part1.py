import csv
import json

output = []

last_time = 1549548199

with open("debt_lives_processed.csv","r") as csvfile:
	reader = csv.DictReader(csvfile)		
	for row in reader:
		cup = int(row["\ufeffcup"])
		born = int(row["born"])
		transitions = sorted([k for k in reader.fieldnames if "transition" in k and "time" not in k])
		transition_times = sorted([k for k in reader.fieldnames if "transition" in k and "time" in k])
		transition_array = [(-1,"born",born,"safe")]

		weight = float(row["start_val"])		

		for i in range(len(transitions)):
			transition = row[transitions[i]]
			transition_time = row[transition_times[i]]
			if transition_time!='': 
				transition_array+=[(int(transitions[i].replace("transition","")),transition,int(transition_time))]

		if row["transition0"]=='' and row["safe"]=='TRUE': 
			transition_array+=[(0, 'open', 1549548199, 'safe')]

		for i in range(1,len(transition_array)):
			transition_name = transition_array[i-1][1]+"->"+transition_array[i][1]
			time_spent = transition_array[i][2]-transition_array[i-1][2]

			if transition_array[i][0]<transition_array[i-1][0]: print("OUT OF ORDER")

			if transition_name=="born->wipe": simple_transition=("safe","wipe")
			elif transition_name=="born->shut": simple_transition=("safe","wipe")
			elif transition_name=="born->bite": simple_transition=("safe","bite")
			elif transition_name=="born->open": simple_transition=("safe","open")
			elif transition_name=="born->FALSE": simple_transition=("safe","unsafe")
			elif transition_name=="TRUE->FALSE": simple_transition=("safe","unsafe")
			elif transition_name=="TRUE->bite": simple_transition=("safe","bite")
			elif transition_name=="TRUE->shut": simple_transition=("safe","wipe")
			elif transition_name=="TRUE->wipe": simple_transition=("safe","wipe")
			elif transition_name=="FALSE->TRUE": simple_transition=("unsafe","safe")
			elif transition_name=="FALSE->bite": simple_transition=("unsafe","bite")
			elif transition_name=="FALSE->wipe": simple_transition=("unsafe","wipe")
			elif transition_name=="FALSE->shut": simple_transition=("unsafe","wipe")
			else: print(transition_name)

			#safe to unsafe
			#safe to bitten
			#safe to wiped
			#unsafe to safe
			#unsafe to bitten
			#unsafe to wiped
			
			if simple_transition==("safe","bite"):
				output_dict1 = dict(cdp = cup,initial_size = weight,transition = transition_name+"_part1", time_spent = time_spent,simple_from=simple_transition[0],simple_to="unsafe") 
				output_dict2 = dict(cdp = cup,initial_size = weight,transition = transition_name+"_part2", time_spent = 0,simple_from="unsafe",simple_to="bite") 
				output+=[output_dict1]
				output+=[output_dict2]
			else:
				output_dict = dict(cdp = cup,initial_size = weight,transition = transition_name, time_spent = time_spent,simple_from=simple_transition[0],simple_to=simple_transition[1]) 
				output+=[output_dict]

out_fieldnames = list(output[0].keys())
with open("intermediate_markov_output.csv","w") as outfile:
	 writer = csv.DictWriter(outfile, fieldnames=out_fieldnames)

	 writer.writeheader()
	 for o in output:
	 	writer.writerow(o)
