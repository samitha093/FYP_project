def convert_last_two_digits(num):
    integer_part = int(num) 
    fractional_part = num - integer_part 
    converted_fractional = int(fractional_part * 100)
    converted_num = float(f"{integer_part}.{converted_fractional:02d}")
    return converted_num

input_num = 123.45678
converted_num = convert_last_two_digits(input_num)
print(converted_num)
