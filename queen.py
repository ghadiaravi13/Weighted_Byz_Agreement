import numpy as np
import pandas as pd
import config
import copy

def weighted_byzantine_queen(total_procs, faulty_weight, user_overwrite=None, proposed_values=None):
    # Check if weights_file is provided and load weights
    
    if user_overwrite is None:
        weights, fault_flag, alpha_rho = config.init(total_procs, "Queen", faulty_weight)
    else:
        weights, fault_flag, alpha_rho = user_overwrite # Load weights from the specified file
    
    faultySets = {}
    V = np.random.randint(2,size=(total_procs,total_procs))
    if proposed_values is not None:
        np.fill_diagonal(V,copy.deepcopy(proposed_values))
    myvalue = copy.deepcopy(V.diagonal())#np.random.randint(2,size=total_procs)
    myweight = np.zeros(total_procs)

    for round in range(alpha_rho):
        # print(f"\n-----------Round: {round}-----------\n")
        #first phase
        
        #send own value to others
        for proc_id in range(total_procs):
            if weights[proc_id]>0:
                # send my value to all
                if(fault_flag[proc_id]=='C'): V[:,proc_id] = myvalue[proc_id] # if good process, send correct value
                else: 
                    V[:,proc_id] = np.random.choice([0,1])
                    V[proc_id,proc_id] = myvalue[proc_id]                     # if byzantine, send random value
        
        for proc_id in range(total_procs):
            s1 = np.dot(V[proc_id],weights)
            s0 = weights.sum() - s1
            if(s1>0.5):
                myvalue[proc_id] = 1
                myweight[proc_id] = s1
            else:
                myvalue[proc_id] = 0
                myweight[proc_id] = s0
        
        #Second Phase
        for proc_id in range(total_procs):
            if proc_id not in faultySets:
                faultySet = set()
            else:
                faultySet = faultySets[proc_id]
            queen_value = myvalue[round] if fault_flag[round]=='C' else np.random.choice([0,1]) 
            if(myweight[proc_id]>3/4): 
                V[proc_id,proc_id] = myvalue[proc_id]
                if queen_value != myvalue[proc_id] and round!=proc_id:
                    faultySet.add(round)
                    #print("found byzantine queen")
            else: 
                V[proc_id,proc_id] = queen_value # queen value
            faultySets[proc_id] = faultySet
                # if(fault_flag[round]=='F'): print("Accepting Byzantine Queen :(")
        # print(f"\nAgreed on 1: {np.all(V.diagonal()==1)}\t Agreed on 0: {np.all(V.diagonal()==0)}\n")
    #     print("\n--------------------------------------\n")
    # print(f"\nAgreed on 1: {np.all(V.diagonal()==1)}\t Agreed on 0: {np.all(V.diagonal()==0)}\n")
    # print("\n")

    # At the end of the function, save the final weights array
    #np.save('queen_final_weights.npy', weights)  # Save final weights as a numpy object
    return (np.all(V.diagonal()==1),np.all(V.diagonal()==0),faultySets,weights,fault_flag,alpha_rho)
    
