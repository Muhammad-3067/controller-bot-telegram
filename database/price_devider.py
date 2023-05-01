def sort_price(price):
    updated_price = ''
    cut_to = 0
    if len(price) % 3 == 1:
        cut_to = 1
    elif len(price) % 3 == 2:
        cut_to = 2
        
    skum = price[cut_to:]
    new_i = 0
    str_data = ''
    array = []
    for i in skum:
        new_i += 1
        str_data += i
        if new_i == 3:
            array.append(str_data)
            new_i = 0
            str_data = ''
    sum_str = ' '.join(array)
    updated_price = f'{price[:cut_to]} {sum_str}'

    return updated_price
