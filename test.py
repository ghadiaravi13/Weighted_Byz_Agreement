import king
import queen
import tqdm

# print("\n------------------Queen's---------------------\n")
# broken = 0
# for _ in tqdm.tqdm(range(100000)):
#     a1,a0 = queen.weighted_byzantine_queen(100)
#     if(a1==False and a0==False): broken+=1

# print(f"{broken}/100000 Broken x x")

print("\n------------------King's---------------------\n")
broken = 0
for _ in tqdm.tqdm(range(100)):
    a1,a0 = king.weighted_byzantine_king(100)
    if(a1==False and a0==False): broken+=1

print(f"{broken}/100000 Broken x x")