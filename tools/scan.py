from threading import Thread, activeCount
import socket
import time


def test_port(dst, port):
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli_sock.settimeout(2)
    try:
        indicator = cli_sock.connect_ex((dst, port))
        if indicator == 0:
            print(dst, port)
        cli_sock.close()
    except:
        pass


if __name__ == '__main__':
    for i in range(1, 255):
        if activeCount() <= 255:
            Thread(target=test_port, args=('172.16.16.%s' % i, 5900)).start()
            time.sleep(0.001)

    while True:
        if activeCount() < 2:
            break

    print 'Finished scanning.'
