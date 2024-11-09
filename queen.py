import numpy as np
import pandas as pd
import config
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

def weighted_byzantine_queen(total_procs):
    weights, fault_flag, alpha_rho = config.init(total_procs,"Queen")

    V = np.random.randint(2,size=(total_procs,total_procs))
    myvalue = np.zeros(total_procs)
    myweight = np.zeros(total_procs)

    for round in range(alpha_rho):
        #first phase

        #send own value to others
        for proc_id in range(total_procs):
            if weights[proc_id]>0:
                # send my value to all
                if(fault_flag[proc_id]=='C'): V[:,proc_id] = V[proc_id,proc_id] # if good process, send correct value
                else: V[:,proc_id] = np.random.choice([0,1])                     # if byzantine, send random value
        
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
        queen_value = myvalue[round] if fault_flag[round]=='C' else np.random.choice([0,1])

        for proc_id in range(total_procs):
            if(myweight[proc_id]>3/4): V[proc_id,proc_id] = myvalue[proc_id]
            else: V[proc_id,proc_id] = queen_value

    print(np.all(V.diagonal()==1),np.all(V.diagonal()==0))
    print("\n")

    
