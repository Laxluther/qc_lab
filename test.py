
def threeSum(nums):
    nums.sort()
    l = []
    k = len(nums)-1
    for i in range(len(nums)):       
        for j in range(i+1,len(nums)):
            if nums[i]+nums[j]+nums[k] == 0:
                l.append([nums[i],nums[j],nums[k]])
    return l

print(threeSum([-1,0,1,2,-1,-4]))