from New_Tags import Main_Elements_1

# image complexity recognition
def getComplexity():

    global complexity
    complexity = []

    sum_1 = len(Main_Elements_1.nb_classId)
    sum_2 = len(Main_Elements_1.nb_classId_deduplicate)
    if sum_1 <= 3 and sum_2 <=1:
        complexity.append("isolated")
    elif sum_1 >= 5 and sum_2 >= 3:
        complexity.append("multiple")

    return complexity
