
import queue
import threading
import time
import random


class DiningPhilosophers(threading.Thread):
    def __init__(self, philosopher, leftFork, rightFork, queue, eatTimes):
        super().__init__()
        self.philosopher = philosopher
        self.leftFork = leftFork
        self.rightFork = rightFork
        self.queue = queue
        self.eatTimes = eatTimes

    def eat(self):
        time.sleep(0.01)
        self.queue.put([self.philosopher, 0, 3])

    def think(self):
        time.sleep(random.random())

    def pickLeftFork(self):
        self.queue.put([self.philosopher, 1, 1])

    def pickRightFork(self):
        self.queue.put([self.philosopher, 2, 1])

    def putLeftFork(self):
        self.leftFork.release()
        self.queue.put([self.philosopher, 1, 2])

    def putRightFork(self):
        self.rightFork.release()
        self.queue.put([self.philosopher, 2, 2])

    def run(self):
        while True:
            left = self.leftFork.acquire(blocking=False)
            right = self.rightFork.acquire(blocking=False)
            if left and right:
                self.pickLeftFork()
                self.pickRightFork()
                self.eat()
                self.putLeftFork()
                self.putRightFork()
                break
            elif left and not right:
                self.leftFork.release()
            elif right and not left:
                self.rightFork.release()
            else:
                time.sleep(1)
        print(f"哲学家{self.philosopher}号吃了{self.eatTimes}次\n")


if __name__ == '__main__':
    queue = queue.Queue()
    fork1 = threading.Lock()
    fork2 = threading.Lock()
    fork3 = threading.Lock()
    fork4 = threading.Lock()
    fork5 = threading.Lock()
    n = 3
    for i in range(n+1)[1:]:
        philosopher0 = DiningPhilosophers(0, fork5, fork1, queue, i)
        philosopher0.start()
        philosopher1 = DiningPhilosophers(1, fork1, fork2, queue, i)
        philosopher1.start()
        philosopher2 = DiningPhilosophers(2, fork2, fork3, queue, i)
        philosopher2.start()
        philosopher3 = DiningPhilosophers(3, fork3, fork4, queue, i)
        philosopher3.start()
        philosopher4 = DiningPhilosophers(4, fork4, fork5, queue, i)
        philosopher4.start()

    action_list = [queue.get() for _ in range(25*n)]
    print(action_list)
