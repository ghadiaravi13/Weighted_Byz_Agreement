import concurrent.futures
import numpy as np
import tqdm
import king, queen  # Add this import

def test_failure_rate(type_algorithm):
    broken = 0
    faulty_weights = list(np.arange(0,0.9,0.1))+[0.25,0.33]
    failure_rate = []
    sizes = (range(20,121,10))
    print(f"type: {type_algorithm}\n")

    def run_test(size, faulty_weight):
        nonlocal broken  # Use nonlocal to modify the outer broken variable
        for _ in tqdm.tqdm(range(1000), disable=True):
            if type_algorithm == "queen":
                result = queen.weighted_byzantine_queen(size, faulty_weight)
                if(result[0]==False and result[1]==False): 
                    broken += 1
            else:
                result = king.weighted_byzantine_king(size, faulty_weight)
                if(result[0]==False and result[1]==False): 
                    broken += 1
        return broken / 1000

    for size in sizes: 
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(run_test, size, faulty_weight): faulty_weight for faulty_weight in faulty_weights}
            for future in concurrent.futures.as_completed(futures):
                failure_rate.append(future.result())
        print(f"size: {size} failure rates for faulty weights {faulty_weights}: {failure_rate}")
        failure_rate = []

test_failure_rate("queen")
test_failure_rate("king")