import config
import numpy as np
from fractions import Fraction

def weighted_byzantine_king(total_proc):
    weights, fault_flag, alpha_rho = config.init(total_proc,"King")

    V = np.random.randint(2,size=(total_proc,total_proc))
    myvalue = np.random.randint(2,size=total_proc)
    myweight = np.zeros(total_proc)

    for round in range(alpha_rho):
        #first phase

        #send own value to others
        for proc_id in range(total_proc):
            if weights[proc_id]>0:
                # send my value to all
                if(fault_flag[proc_id]=='C'): V[:,proc_id] = myvalue[proc_id] # if good process, send correct value
                else: 
                    V[:,proc_id] = np.random.choice([0,1])                     # if byzantine, send random value
                    V[proc_id,proc_id] = myvalue[proc_id]
        
        for proc_id in range(total_proc):
            if weights[proc_id]>0:
                s1 = np.dot(V[proc_id],weights)
                s0 = weights.sum() - s1
                if(s0>=Fraction(2/3)):
                    myvalue[proc_id] = 0
                elif(s1>=Fraction(2/3)):
                    myvalue[proc_id] = 1
                else:
                    myvalue[proc_id] = 2
        
        #Second Phase
        for proc_id in range(total_proc):
            if(weights[proc_id]>0): 
                V[:,proc_id] = myvalue[proc_id]
        for proc_id in range(total_proc):
            s0, s1, su = 0.0,0.0,0.0
            for j in range(len(weights)):
                if weights[proc_id]>0:
                    if V[proc_id,j]== 1:
                        s1 += weights[j]
                    elif V[proc_id,j]==0:
                        s0 += weights[j]
                    else:
                        su += weights[j]
            if s0>Fraction(1/3):
                myvalue[proc_id],myweight[proc_id] = 0,s0
            elif s1>Fraction(1/3):
                myvalue[proc_id],myweight[proc_id] = 1,s1
            elif su >Fraction(1/3):
                myvalue[proc_id],myweight[proc_id] = 2,su
            
        #third phase

        for proc_id in range(total_proc):
            if round== proc_id:
                if(fault_flag[proc_id]=='C'): V[:,proc_id] = myvalue[proc_id] # if good process, send correct value
                else: 
                    V[:,proc_id] = np.random.choice([0,1])                     # if byzantine, send random value
                    V[proc_id,proc_id] = myvalue[proc_id]
        for proc_id in range(total_proc):
            if myvalue[proc_id] == 2 or myweight[proc_id]<Fraction(2/3):
                if myvalue[round] == 2: myvalue[proc_id] = 1
                else: myvalue[proc_id] = myvalue[round]

    print(np.all(myvalue==1), np.all(myvalue==0))