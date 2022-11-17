import copy


lst1 = [[3,4],2,3]
print('The original list is', lst1)


lst2 = copy.deepcopy(lst1)
lst2[0].append(5)
print('The copied list is ',lst2)
print('The original list is not changed: ', lst1)
print('---')


lst3 = copy.copy(lst1)
lst3[0].append(6)
print('List 3:', lst3)

print('THe orignial list is changed, ',lst1)