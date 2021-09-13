import copy
def filter_simple(collection: list[int]) -> list[int]:
    # Iterate over all the elements in the collection
    for i in copy(collection):
        # If the element matches a certain 
        if i > 0:
            collection.remove(i)
        elif i % 2 == 0:
            collection.remove(i)
        elif i < 45:
            collection.remove(i)
    return collection