from multiprocessing import Pool, Lock
import socket
from netaddr import IPRange
from itertools import product


def port_scan(scan_data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect(('%s' % scan_data[0], scan_data[1]))
        print(scan_data[0], 'Port:', scan_data[1], 'is open')
    except socket.error:
        pass
    finally:
        s.close()


def user_data():
    ip_start, ip_end = input('Введите IP-IP: ').split('-')
    ip_range = IPRange(ip_start, ip_end)
    port_range = (43, 80, 109, 110, 115, 118, 119, 143, 194, 220, 443, 540,
                  585, 591, 1112, 1433, 1443, 3128, 3197, 3306, 3899, 4224,
                  4444, 5000, 5432, 6379, 8000, 8080, 10000)
    return ip_range, port_range


if __name__ == '__main__':
    ip_range, ports = user_data()
    data = product(ip_range, ports)
    print('Scan started...')
    with Pool(5) as pool:
        pool.map(port_scan, data)

    print('Scan completed...')

# 52.89.18.0-52.89.18.255
# 192.0.0.1-192.0.0.100