import king
import queen
import tqdm
import matplotlib.pyplot as plt
import numpy as np

def test_failure_rate(type_algorithm):
    broken = 0
    faulty_weights = (np.arange(0.0,0.9,0.1))
    failure_rate = []
    sizes = (range(30,81,10))
    print(f"type: {type_algorithm}\n")
    for size in sizes: 
        for faulty_weight in faulty_weights:
            for _ in tqdm.tqdm(range(500), disable=True):
                if type_algorithm == "queen":
                    result = queen.weighted_byzantine_queen(size, faulty_weight)
                    if(result[0]==False and result[1]==False): 
                        broken+=1
                else:
                    result = king.weighted_byzantine_king(size, faulty_weight)
                    if(result[0]==False and result[1]==False): 
                        broken+=1
            failure_rate.append(broken/500)
            broken = 0
        plt.plot(faulty_weights, failure_rate, label=f"Weighted {type_algorithm} Byzantine Algorithm with size {size}")
        print(f"size: {size} failure rate for faulty weight {faulty_weights}: {failure_rate}")
        failure_rate = []
    
    plt.xlabel('Total Faulty Weight')
    plt.ylabel('Failure Rate')
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()
test_failure_rate("queen")
test_failure_rate("king")