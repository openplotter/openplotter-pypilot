import os


path='/boot/config.txt'
with open(path, 'r') as file:
    while True:
        line = file.readline()
        if not line:
            with open(path, 'a') as file:
                file.write('dtoverlay=disable-bt\n')
            break
        if 'dtoverlay=disable-bt' in line:
            break
            
path='/boot/cmdline.txt'
write = False
lines = ''
with open(path, 'r') as file:
    while True:
        line = file.readline()
        if not line:
            break
        params = line.split()
        line = ''
        for p in params:
            if p[:7] == 'console':
                write = True
            else:
                line += p + ' '
        lines += line + '\n'

if write:
    print('detected console in cmdline.txt, rewriting cmdline.txt')
    with open(path, 'w') as file:
        file.write(lines)

if not os.system('systemctl is-active hciuart'):
    os.system('systemctl disable hciuart')
    os.system('systemctl stop hciuart')
