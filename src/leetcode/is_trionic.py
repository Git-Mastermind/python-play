def isTrionic(nums) -> bool:
    index = 0
    increase = 0
    decrease = 0
    again_increases = False
    while index < len(nums) - 1:
        if decrease != 0 and nums[index] < nums[index + 1]:
            return True
            index+=1
        elif nums[index] < nums[index + 1]:
            increase += 1
            index+=1
        elif nums[index] > nums[index + 1]:
            decrease += 1
            index+=1
        if increase == 0 and decrease != 0:
            return False
    
        
    return again_increases

print(isTrionic([1,3,5,4,2,6])) 