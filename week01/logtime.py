import logging
from pathlib import Path
import time


def timeLogger(func):
    currDate = time.strftime("%Y-%m-%d", time.localtime())
    currTime = time.strftime("%H-%M-%S", time.localtime())
    Path(f"/var/log/ownlog/python-{currDate}/").mkdir(parents=True, exist_ok=True)
    outputPath = f"/var/log/ownlog/python-{currDate}/{currTime}.log"


    logging.basicConfig(filename=outputPath,
                        level=logging.DEBUG,
                        datefmt="%Y-%m-%d %H:%M:%S",
                        format="time function called by %(message)s at %(asctime)s"
                        )
    logging.info(f'{func} {func.__name__}')
    return func

@timeLogger
def func():
    print('done')

if __name__ == '__main__':
    func()