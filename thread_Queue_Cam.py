from queue import Queue
from threading import Thread
import time
import cv2

get_stop = False
show_stop = False

sentinel = object()       #  se usa para salir limpiamente de los Threads
n = 0


def get_video(out_q):
    global get_stop, show_stop
    stream = cv2.VideoCapture(0)
    while not get_stop:
        (grabbed, frame) = stream.read()
        if not grabbed:
            get_stop = True
            show_stop = True
        out_q.put(frame)
        
    out_q.put(sentinel)

def show_video (in_q):
    global show_stop, get_stop
    while not show_stop:
        frame = in_q.get()
        if frame is sentinel:
            in_q.put(sentinel)
            break
        cv2.imshow("Window",frame)
        if cv2.waitKey(1) == ord("q"):
            show_stop = True
            get_stop = True




if __name__ == '__main__':
    q = Queue()
    Thread(target = get_video, args=(q,)).start()
    Thread(target = show_video, args=(q,)).start()
    while not show_stop and not get_stop:
        n +=1
        print(n)
        time.sleep(1)
        



