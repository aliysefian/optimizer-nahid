def compare_lists(list1, list2):
    if len(list1) != len(list2):
        return False

    for item1, item2 in zip(list1, list2):
        if item1 > item2:
            return False

    return True
