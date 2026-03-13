def duplicates(nums):
    unique_values = []

    for i in range(len(nums)):
        if nums[i] not in unique_values:
            unique_values.append(nums[i])
        else:
            return nums[i]

def findErrorNums(nums):
    duplicate = duplicates(nums)
    nums.remove(duplicate)
    duplicate_and_missing_number = [duplicate]
    i = 0

    if len(nums) == 1 and nums[0] == 1:
        duplicate_and_missing_number.append(nums[0] + 1)
        return duplicate_and_missing_number
    elif len(nums) == 1 and nums[0] != 1:
        duplicate_and_missing_number.append(nums[0] - 1)
        return duplicate_and_missing_number

    while nums[i] != duplicate:
        i += 1
    if nums[i] > nums[i - 1]:
        duplicate_and_missing_number.append(nums[i + 1] - 1)
    else:
        duplicate_and_missing_number.append(nums[i] - 1)
    
    return duplicate_and_missing_number

print(findErrorNums([3,2,2]))