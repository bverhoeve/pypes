import copy


def filter_simple(collection: list[int]) -> list[int]:
    # Iterate over all the elements in the collection
    for i in copy.copy(collection):
        # If the element matches a certain
        if i < 0:
            collection.remove(i)
        elif i % 2 == 0:
            collection.remove(i)
    return collection


def main():
    collection = list(range(-20, 20))
    print(f"Original collection: {collection}")
    filtered_collection = filter_simple(collection)
    print(f"Filtered collection: {filtered_collection}")


if __name__ == "__main__":
    main()
