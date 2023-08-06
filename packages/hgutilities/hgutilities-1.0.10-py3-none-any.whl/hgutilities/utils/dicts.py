def remove_none_values(dictionary):
    filtered_dictionary = {key: value for key, value in dictionary.items()
                           if value is not None}
    return filtered_dictionary

def transpose_list(my_list):
    transposed_list = list(map(list, zip(*my_list)))
    return transposed_list
