def batched_list(orig_list, batch_size):
    """ split list into batches
[in]    a = [1,2,3,4,5,6,7,8,9,0,1,2,3]
        for i in batched_list(a,4):
            print(i)

[out]   [1, 2, 3, 4]
        [5, 6, 7, 8]
        [9, 0, 1, 2]
        [3]


    Args:
        orig_list (list): list
        batch_size (int): batch size

    Yields:
        _type_: list batch
    """
    for i in range(0, len(orig_list), batch_size): 
        yield orig_list[i:i + batch_size]