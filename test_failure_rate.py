import king
import queen
import tqdm
import queen_update_weight


def test_failure_rate(type_algorithm):
    broken = 0
    faulty_weights = list(range(1,10,1)) + [2.5,3.3]
    faulty_weights = [w/10 for w in faulty_weights]
    failure_rate = []
    sizes = (range(20,121,10))
    print(f"type: {type_algorithm}\n")
    for size in sizes: 
        for faulty_weight in faulty_weights:
            for _ in tqdm.tqdm(range(1000), disable=True):
                if type_algorithm == "queen":
                    result = queen.weighted_byzantine_queen(size, faulty_weight)
                    if(result[0]==False and result[1]==False): 
                        broken+=1
                else:
                    result = king.weighted_byzantine_king(size, faulty_weight)
                    if(result[0]==False):# and result[1]==False): 
                        broken+=1
            failure_rate.append(broken/1000)
            broken = 0
        print(f"size: {size} failure rate for faulty weight {faulty_weights}: {failure_rate}")
        failure_rate = []

test_failure_rate("queen") 
# test_failure_rate("king")