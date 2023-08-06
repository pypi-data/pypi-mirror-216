import loky
from concurrent.futures import ProcessPoolExecutor

if __name__ == "__main__":
    loky.freeze_support()
    e = loky.get_reusable_executor(max_workers=2)
    # e = ProcessPoolExecutor(max_workers=2)
    print(sum(e.map(int, range(10))))
