import time
from limitless_py import ratelimit

# ---- limitless_py -------------------------------------------------
@ratelimit(calls=100, per=1)
def limited():
    pass

def bench_pyratelimit():
    start = time.time()
    for _ in range(10_000):
        limited()
    return time.time() - start

# ---- manual sleep -------------------------------------------------
def make_manual_limiter():
    calls = []
    def call():
        now = time.time()
        if calls and len(calls) >= 100:
            oldest = calls[-100]
            if now - oldest < 1.0:
                time.sleep(1.0 - (now - oldest))
        calls.append(now)
        if len(calls) > 100:
            calls.pop(0)
    return call

manual_call = make_manual_limiter()

def bench_manual():
    start = time.time()
    for _ in range(10_000):
        manual_call()
    return time.time() - start

# ---- ratelimit lib (safe) ----------------------------------------
try:
    from ratelimit import limits, RateLimitException

    @limits(calls=100, period=1)
    def external():
        pass

    def bench_external():
        start = time.time()
        count = 0
        while count < 10_000:
            try:
                external()
                count += 1
            except RateLimitException:
                time.sleep(0.01)
        return time.time() - start
except Exception as e:
    bench_external = lambda: "N/A"

# ---- run ---------------------------------------------------------
if __name__ == "__main__":
    print("10,000 calls @ 100/sec limit")
    print("┌────────────────────┬──────────────┐")
    print(f"│ {'limitless_py':18} │ {bench_pyratelimit():6.2f} s │")
    print(f"│ {'Manual sleep()':18} │ {bench_manual():6.2f} s │")
    t = bench_external()
    status = t if isinstance(t, str) else f"{t:6.2f} s"
    print(f"│ {'ratelimit lib':18} │ {status} │")
    print("└────────────────────┴──────────────┘")