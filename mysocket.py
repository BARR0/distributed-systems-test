import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
chunks = {}
STORE = b'CHUNK:'         # CHUNK:$num:$msg
REQ = b'REQ:'             # REQ:$num
ERASE = b'ERASE'
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data: break
                print('Message:', data)
                if data.startswith(STORE):
                    data = data.split(b':')
                    chunk_n, messg = int(data[1]), data[2]
                    print('chunks[%d] = %s' % (chunk_n, messg))
                    chunks[chunk_n] = messg
                    conn.sendall(b'200 OK')
                elif data.startswith(REQ):
                    data = data.split(b':')
                    chunk_n = int(data[1])
                    messg = chunks.get(chunk_n, b'')
                    if not messg:
                        conn.sendall(b'404')
                    else:
                        print('sending... chunks[%d] = %s' % (chunk_n, messg))
                        conn.sendall(messg)
                    print('sent')
                elif data.startswith(ERASE):
                    chunks = {}
                    conn.sendall(b'200 OK')
