targets = ('192.168.0.1', '10.10.1.1', '127.0.0.1')
ports = (80, 8080, 22)

for ips, elem in zip(targets, ports):
    print(ips, elem, sep='\t'*4)

print()

for elem in range(len(targets)):
    print(targets[elem], ports[elem], sep='\t'*4)