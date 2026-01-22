def max_consecutive_ones(nums):
    counter = 0
    storage = []
    for i in range(len(nums)):
        if nums[i] == 1:
                counter += 1
        else:
                storage.append(counter)
                counter = 0
    storage.append(counter)
                
    return max(storage)

print(max_consecutive_ones(nums=[1,1,0,1,1,1]))
       
              
            