var_1, var_2, var_3 = 29, 138, 7005

var_1_st = str(var_1)
var_2_st = str(var_2)
var_3_st = str(var_3)

print('Число', 'Через строку', 'Через деление', sep='\t')
print(var_1, '\t'.expandtabs(4), var_1_st[1], '\t'.expandtabs(13),
      var_1 % 10)
print(var_2, '\t'.expandtabs(3), var_2_st[1], '\t'.expandtabs(13),
      var_2 % 100//10)
print(var_3, '\t'.expandtabs(2), var_3_st[0], '\t'.expandtabs(13),
      var_3//1000)