tool = 'Super-Puper MainTool /v2*'
tool = tool[:5] + tool[-9:].replace('/v2*', 'v1')

print(''.center(20, '*'))
print(tool.center(20, '-'))
print(''.center(20, '*'))