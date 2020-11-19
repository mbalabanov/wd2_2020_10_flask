shopping_list = ["bread", "butter", "salt", "bread"]


def uniquify(something_list):
    return list(set(something_list))


unique_list = uniquify(shopping_list)

print(shopping_list)
print(unique_list)
