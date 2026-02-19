def shuffle(nums, n):
    first_half = nums[0 : n]
    second_half = nums[n : len(nums)]
    shuffled = []
    for i in range(n):
        shuffled.append(first_half[i])
        shuffled.append(second_half[i])
    return shuffled

print(shuffle(nums=[2,5,1,3,4,7], n=3))