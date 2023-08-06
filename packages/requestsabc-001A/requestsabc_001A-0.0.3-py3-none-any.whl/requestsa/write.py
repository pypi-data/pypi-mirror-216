import time

def mwrite():
    while True:
        with open('D:\\Users\\1.txt','a') as f:
            f.write(str(int(time.time())) + '\n')
        time.sleep(5)