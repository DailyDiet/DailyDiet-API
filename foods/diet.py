import random

def sevade(list1, list2, list3, calorie):
    i = 0
    j = 0
    k = len(list3)-1
    rand = random.randint(1,10)
    while i < len(list1):
        while j < len(list2) and k >= 0:
            if list1[i].get_calorie() + list2[j].get_calorie() + list3[k].get_calorie() in range(n-rand, n+rand, 1):
                return list1[i], list2[j], list3[k], list1[i].get_calorie() + list2[j].get_calorie() + list3[k].get_calorie()
            elif list1[i].get_calorie() + list2[j].get_calorie() + list3[k].get_calorie() < n-10:
                j += 1
            else:
                k -=1
        i +=1
    return None
