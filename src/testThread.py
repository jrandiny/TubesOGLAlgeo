from queue import Queue
import threading
import time

q = Queue()

def worker(qu):   
    while(True):
        while(not qu.empty()):
            pass
        in2 = input("type = ")
        hehe(in2)
        qu.put(in2,False)

def hehe(in3):
    print(in3)

threads = []
t = threading.Thread(target=worker,args=(q,))
t.start()

while True:
    time.sleep(3)
    if(q.empty()):
        pass
    else:
        print("queue")
        while not q.empty():
            isi = q.get()
            q.task_done()
            print(isi)