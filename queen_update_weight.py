import queen
import numpy as np
def queen_update_weight(total_procs, faulty_weight):
    a1,a0,faultySets,weights,faulty_flag,alpha_rho = queen.weighted_byzantine_queen(total_procs,faulty_weight)

    print(f"initial weight: {weights}\n fault flag: {faulty_flag}")
    suspectWeight = np.zeros((total_procs,total_procs))
    consensusFaulty = set()
    proposed_matrix = np.zeros((total_procs,total_procs))
    
    for proc_id in range(total_procs):
        #phase 1
        faultySet = faultySets[proc_id]
        if weights[proc_id] <= 0:
            continue
        for j in range(total_procs):
            for k in faultySets[j]:
                suspectWeight[proc_id][k] = suspectWeight[proc_id,k] + weights[j]
        for j in range(total_procs):
            if suspectWeight[proc_id][j] >= 0.25 and j!=proc_id:
                faultySet.add(j)
        
        proposed_matrix[proc_id,list(faultySet)] = 1
        

    #phase 2
    for j in range(total_procs):
        # if j in faultySet:
        #     value = queen.weighted_byzantine_queen(total_procs, (weights,faulty_flag,alpha_rho),proposed_matrix[:,j])
        # else:
        value = queen.weighted_byzantine_queen(total_procs,(weights,faulty_flag,alpha_rho),proposed_matrix[:,j])
        if value[0] == True:
            consensusFaulty.add(j)
        
    #phase 3
    totalWeight = 1.0
    for j in consensusFaulty:
        totalWeight = totalWeight - weights[j]
        weights[j] = 0
    
    for j in range(total_procs):
        weights[j] = weights[j]/totalWeight
    #return final weight
    print(f"proposed Matrix: {proposed_matrix}")
    print(f"consensusFaulty: {consensusFaulty}")
    print(f"finial weights: {weights}")
    
    return weights