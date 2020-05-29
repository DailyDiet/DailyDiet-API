import random

def yevade(list1, calorie):
    i = 0
    rand = random.randint(1,30)
    while i < len(list1):
        if float(list1[i].get_calorie()) in range (calorie-rand, calorie+rand, 1):
            return list1[i], float(list1[i].get_calorie())
        i += 1
    return None

def dovade(list1, list2, calorie):
    i = 0
    j = len(list2) - 1
    rand = random.randint(1,30)
    while i < len(list1) and j>=0:
        if float(list1[i].get_calorie()) + float(list2[j].get_calorie()) in range(calorie-rand, calorie+rand, 1):
            return list1[i], list2[j], float(list1[i].get_calorie()) + float(list2[j].get_calorie())
        elif float(list1[i].get_calorie()) + float(list2[j].get_calorie()) < calorie - 10:
            j -= 1
        i += 1
    return None


def sevade(list1, list2, list3, calorie):
    i = 0
    j = 0
    k = len(list3) - 1
    rand = random.randint(1,30)
    while i < len(list1):
        while j < len(list2) and k >= 0:
            if float(list1[i].get_calorie()) + float(list2[j].get_calorie()) + float(list3[k].get_calorie()) in range(calorie-rand, calorie+rand, 1):
                return list1[i], list2[j], list3[k], float(list1[i].get_calorie()) + float(list2[j].get_calorie()) + float(list3[k].get_calorie())
            elif float(list1[i].get_calorie()) + float(list2[j].get_calorie()) + float(list3[k].get_calorie()) < calorie-10:
                j += 1
            else:
                k -= 1
        i += 1
    return None
