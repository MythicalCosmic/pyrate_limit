from limitless_py import ratelimit
import time

@ratelimit(calls=3, per=2)
def greet():
    print("Hello!", time.time())

if __name__ == "__main__":
    for _ in range(5):
        greet()
        time.sleep(0.3)