import config
import numpy as np
from fractions import Fraction

def weighted_byzantine_king(total_procs, faulty_weight):
    weights, fault_flag, alpha_rho = config.init(total_procs,"King", faulty_weight)

    V = np.random.randint(2,size=(total_procs,total_procs))
    myvalue = np.random.randint(2,size=total_procs)
    myweight = np.zeros(total_procs)

    for round in range(alpha_rho):
        #first phase

        #send own value to others
        for procs_id in range(total_procs):
            if weights[procs_id]>0:
                # send my value to all
                if(fault_flag[procs_id]=='C'): V[:,procs_id] = myvalue[procs_id] # if good procsess, send correct value
                else: 
                    V[:,procs_id] = np.random.choice([0,1])                     # if byzantine, send random value
                    V[procs_id,procs_id] = myvalue[procs_id]
        
        for procs_id in range(total_procs):
            s1 = np.dot(V[procs_id],weights)
            s0 = weights.sum() - s1
            if(s0>=Fraction(2/3)):
                myvalue[procs_id] = 0
            elif(s1>=Fraction(2/3)):
                myvalue[procs_id] = 1
            else:
                myvalue[procs_id] = 2
        
        #Second Phase
        for procs_id in range(total_procs):
            if(weights[procs_id]>0): 
                V[:,procs_id] = myvalue[procs_id]
        for procs_id in range(total_procs):
            s0, s1, su = 0.0,0.0,0.0
            for j in range(total_procs):
                if weights[j]>0:
                    if V[procs_id,j]== 1:
                        s1 += weights[j]
                    elif V[procs_id,j]==0:
                        s0 += weights[j]
                    else:
                        su += weights[j]
            if s0>Fraction(1/3):
                myvalue[procs_id],myweight[procs_id] = 0,s0
            elif s1>Fraction(1/3):
                myvalue[procs_id],myweight[procs_id] = 1,s1
            elif su >Fraction(1/3):
                myvalue[procs_id],myweight[procs_id] = 2,su
            
        #third phase

        for procs_id in range(total_procs):
            if round== procs_id:
                if(fault_flag[procs_id]=='C'): V[:,procs_id] = myvalue[procs_id] # if good procsess, send correct value
                else: 
                    V[:,procs_id] = np.random.choice([0,1])                     # if byzantine, send random value
                    V[procs_id,procs_id] = myvalue[procs_id]
        
        for procs_id in range(total_procs):
            king_value = V[procs_id,round]
            if myvalue[procs_id] == 2 or myweight[procs_id]<Fraction(2/3):
                if king_value == 2: myvalue[procs_id] = 1
                else: myvalue[procs_id] = king_value
            V[procs_id,procs_id] = myvalue[procs_id]

    return (np.all(myvalue==1), np.all(myvalue==0),(weights, fault_flag, alpha_rho))