import king
import queen
import tqdm
import queen_update_weight
# print("\n------------------Queen's---------------------\n")
# broken = 0
# for _ in tqdm.tqdm(range(1000)):
#     result = queen.weighted_byzantine_queen(20)
#     if(result[0]==False and result[1]==False): 
#         print(f"queen {result}")
#         broken+=1

# print(f"{broken}/1000 Broken x x")

# print("\n------------------King's---------------------\n")
# broken = 0
# for _ in tqdm.tqdm(range(2000)):
#     a1,a0,attribute = king.weighted_byzantine_king(20)
    
#     if(a1==False and a0==False): 
#         print(f"king {attribute}")
#         broken += 1

# print(f"{broken}/1000 Broken x x")
queen_update_weight.queen_update_weight(10)
