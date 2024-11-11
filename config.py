import numpy as np
import pandas as pd

def init(num_processes, algorithm_type):
    trusted_procs = []
    untrusted_procs = []

    total_procs = num_processes

    trusted_proc_frac = 0.1
    untrusted_proc_frac = 1 - trusted_proc_frac

    trusted_proc_count = total_procs * trusted_proc_frac
    untrusted_proc_count = total_procs * untrusted_proc_frac

    proc_idx = np.arange(total_procs)

    trusted_proc_failure_rate = 0.1
    untrusted_proc_failure_rate = 0.5

    fault_flag = np.array([np.random.choice(['F','C'],p=[untrusted_proc_failure_rate,1-untrusted_proc_failure_rate]) if i < untrusted_proc_count else np.random.choice(['F','C'],p=[trusted_proc_failure_rate,1-trusted_proc_failure_rate]) for i in proc_idx])
    # print(np.unique(fault_flag[:int(untrusted_proc_count)],return_counts=True),np.unique(fault_flag[int(untrusted_proc_count):],return_counts=True))
    # print("\n")

    if algorithm_type == "Queen":
        #RHO < 1/4 for Queen's
        faulty_weight = np.random.uniform(0,0.25)
        correct_weight = 1 - faulty_weight
    elif algorithm_type == "King":
        faulty_weight = np.random.uniform(0, 0.33)
        correct_weight = 1 - faulty_weight
    weights = np.random.randint(low=1,high=num_processes,size=num_processes)
    weights = weights.astype(np.float64)
    if(faulty_weight==0):
        weights[fault_flag=='F'] == 0.0
    else:
        weights[fault_flag=='F'] *= faulty_weight/weights[fault_flag=='F'].sum()
    weights[fault_flag=='C'] *= correct_weight/weights[fault_flag=='C'].sum()
    # print(pd.Series(weights[fault_flag=='F']).describe())
    # print(f"faulty weight: {faulty_weight} type {algorithm_type}")
    # shuffle the process IDs
    np.random.shuffle(proc_idx)

    fault_flag = fault_flag[proc_idx]
    weights = weights[proc_idx]
    # print(weights[fault_flag=='C'].sum())

    # alpha_rho
    k = 1
    while(1):
        if k==len(weights): 
            alpha_rho = k
            break
        top_k_indices = np.argpartition(weights, k)[:k]
        if(weights[top_k_indices].sum()>faulty_weight):
            # print(f"\n--------------------{k} {algorithm_type}s:\n\n",top_k_indices,"\n---------------------\n")
            alpha_rho = k
            # queens = top_k_indices
            break
        else: k+=1
    return weights, fault_flag, alpha_rho