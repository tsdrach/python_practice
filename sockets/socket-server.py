import socket


def fibGenerator():
    a, b = 0, 1
    yield 0
    while True:
        a, b = b, a + b
        yield a


def fibReturn(n):
    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b
    return a


sock = socket.socket()
sock.bind(('', 9090))
sock.listen()
conn, addr = sock.accept()

print('connected:', addr)

while True:
    conn.send(b'Enter number: ')
    data = conn.recv(1024)
    if not data:
        break
    try:
        ddata = int(data.decode())
        if 0 <= ddata < 100:
            fibonaccinumbers = []
            fib = fibGenerator()
            for n in range(ddata):
                next(fib)
            edata = str(next(fib)).encode()
            print(edata)
            conn.send(b'Answer: ' + edata + b'\r\n')
        else:
            conn.send(b'Please enter number from 0 to 100\r\n')
    except ValueError:
        conn.send(b'Please enter digit\r\n')

conn.close()
