import king
import queen
import tqdm
import queen_update_weight
print("\n------------------Queen's---------------------\n")
broken = 0
for _ in tqdm.tqdm(range(100)):
    result = queen.weighted_byzantine_queen(100)
    if(result[0]==False and result[1]==False): broken+=1

print(f"{broken}/100 Broken x x")

print("\n------------------King's---------------------\n")
broken = 0
for _ in tqdm.tqdm(range(100)):
    a1,a0,attribute = king.weighted_byzantine_king(100)
    
    if(a1==False and a0==False): 
        broken += 1

print(f"{broken}/100 Broken x x")

