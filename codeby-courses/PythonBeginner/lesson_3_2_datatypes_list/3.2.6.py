digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

test_list = [digits[-1]*2, digits[0] + symbols[4], digits[-3] + symbols[2],
             symbols[0] + digits[0], symbols[2] + digits[-3]]

print(':'.join(test_list))