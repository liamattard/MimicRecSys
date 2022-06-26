
def get_list_dimension(myList):

    x = len(myList)
    y = 0

    for i in myList:
        if (len(i) > y):
            y = len(i)
    return x, y


def generate_med_ids(mySet):
    myList = list(mySet)
    myDict = {}

    for i, med in enumerate(myList):
        myDict[med] = i

    return myDict
