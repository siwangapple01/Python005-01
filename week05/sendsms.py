import redis
import os
from datetime import datetime

datetime_string = datetime.now().strftime("%Y%m%d-%H%M")

client = redis.Redis(host=os.getenv("NASIP"), port=6379, decode_responses=True)
client.flushdb()

def counter(id: int):
    client.incr(id)

    return client.get(id)

def sender(key_string, times, split = False):
    
    origin_times = times + 1 if split == True else times
    if client.get(key_string) is None or int(client.get(key_string)) < times:
        print("信息已经发送")
        counter(key_string)
    else:
        print("发送失败，一分钟只能发送{}次小于70字符短信，超过70个字符会被拆分成两条短信".format(origin_times))



def send_times(times):
    def wrapper(f):
        def wrapper_function(telephone_number, content, times = times , key=None):
            key_string = str(telephone_number) + "-" + datetime_string
            if len(content) <= 70:
                sender(key_string, times)
            else:
                sender(key_string, times - 1, True)

            return f(telephone_number, content)
        return wrapper_function
    return wrapper


@send_times(times = 5)
def sendsms(telephone_number: int, content: str, key= None):
    key_string = str(telephone_number) + "-" + datetime_string
    print("号码{}本分钟已经发送 {} 次".format(telephone_number,client.get(key_string)))


def main():
    for _ in range(5):
        sendsms(134234234234324324, "hello world"*20, times = 4)


if __name__ == "__main__":
    main()
