import subprocess
import time


def main():
    for port in range(8001, 8004 + 1):
        subprocess.Popen(
            ['python3.7', '/home/sanyash/TKP/app.py', '--port', str(port)]
        )

    while True:
        time.sleep(1000000)


if __name__ == '__main__':
    main()
