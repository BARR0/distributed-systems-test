import socket
import textwrap

CHUNK = 'CHUNK:'
REQ = 'REQ:'
ERASE = 'ERASE'

IPS = [
    'ips'
]

def send_chunk(HOST, msg):
    PORT = 50007              # The same port as used by the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(msg.encode('utf-8'))
        data = s.recv(1024)
    response = repr(data)#.decode('utf-8')
    print('Received', response, ' from IP: ', HOST)
    return response[2:-1]

def send_data(fname, ips, dupf = 3):
    f = open(fname)
    text = f.read()
    chnum = len(ips)
    chsize = len(text) // chnum
    chunks = textwrap.wrap(text, width = chsize)
    if len(chunks) > chnum:
        chunks[-2] += chunks[-1]
        chunks.pop()
    print(chunks)
    for i, ip in enumerate(ips):
        for j in range(dupf):
            if j > 0 and (i + j) % len(chunks) == i:
                break
            print(CHUNK + str((i + j) % len(chunks)) + ':' + chunks[(i + j) % len(chunks)])
            # send_chunk(ip, CHUNK + str((i + j) % chnum) + ':' + text[chsize * ((i + j) % chnum) : chsize * ((i + j + 1) % chnum)])
            send_chunk(ip, CHUNK + str((i + j) % chnum) + ':' + chunks[(i + j) % len(chunks)])
        print()
    f.close()
    return chnum

def clean(ips):
    for ip in ips:
        send_chunk(ip, ERASE)

def rebuild(chnum, ips):
    text = ''
    for i in range(chnum):
        for ip in ips:
            try:
                tmp = send_chunk(ip, REQ + str(i))
                if tmp != '404' and tmp != '':
                    text += tmp
                    break
            except:
                continue
    return text

if __name__ == '__main__':
    clean(IPS)
    chnum = send_data('distributed_data.txt', IPS, dupf = 3)
    while input('Press enter to rebuild, something else to exit: ') == '':
        print('Rebuilding...')
        print(rebuild(chnum, IPS))
