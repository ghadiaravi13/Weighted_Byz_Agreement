import numpy as np
import pandas as pd
import config
import copy
# trusted_procs = []
# untrusted_procs = []

# total_procs = total_procs

# trusted_proc_frac = 0.1
# untrusted_proc_frac = 1 - trusted_proc_frac

# trusted_proc_count = total_procs * trusted_proc_frac
# untrusted_proc_count = total_procs * untrusted_proc_frac

# proc_idx = np.arange(total_procs)

# trusted_proc_failure_rate = 0.1
# untrusted_proc_failure_rate = 0.5

# fault_flag = np.array([np.random.choice(['F','C'],p=[untrusted_proc_failure_rate,1-untrusted_proc_failure_rate]) if i < untrusted_proc_count else np.random.choice(['F','C'],p=[trusted_proc_failure_rate,1-trusted_proc_failure_rate]) for i in proc_idx])
# print(np.unique(fault_flag[:int(untrusted_proc_count)],return_counts=True),np.unique(fault_flag[int(untrusted_proc_count):],return_counts=True))
# print("\n")

# #RHO < 1/4 for Queen's
# faulty_weight = 0.20
# correct_weight = 1 - faulty_weight
# weights = np.random.randint(low=500,size=total_procs)
# weights = weights.astype(np.float64)
# weights[fault_flag=='F'] *= faulty_weight/weights[fault_flag=='F'].sum()
# weights[fault_flag=='C'] *= correct_weight/weights[fault_flag=='C'].sum()
# # print(pd.Series(weights[fault_flag=='F']).describe())

# # shuffle the process IDs
# np.random.shuffle(proc_idx)

# fault_flag = fault_flag[proc_idx]
# weights = weights[proc_idx]
# # print(weights[fault_flag=='C'].sum())

# # alpha_rho
# k = 1
# while(1):
#     top_k_indices = np.argpartition(weights, -k)[-k:]
#     if(weights[top_k_indices].sum()>faulty_weight):
#         print(f"\n--------------------{k} Queens:\n\n",top_k_indices,"\n---------------------\n")
#         alpha_rho = k
#         # queens = top_k_indices
#         break
#     else: k+=1

# init vector matrix

def weighted_byzantine_queen(total_procs, user_overwrite=None, proposed_values=None):
    # Check if weights_file is provided and load weights
    
    if user_overwrite is None:
        weights, fault_flag, alpha_rho = config.init(total_procs, "Queen")
    else:
        weights, fault_flag, alpha_rho = user_overwrite # Load weights from the specified file
    
    faultySets = {}
    V = np.random.randint(2,size=(total_procs,total_procs))
    if proposed_values is not None:
        np.fill_diagonal(V,copy.deepcopy(proposed_values))
    myvalue = np.random.randint(2,size=total_procs)
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
                if queen_value != myvalue[proc_id]:
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
    
