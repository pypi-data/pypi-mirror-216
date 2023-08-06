import argparse
import time
from loky import get_reusable_executor, freeze_support


def main():
    arguments_parser = argparse.ArgumentParser()
    arguments_parser.add_argument("-n", default=None, type=int)
    flags, _ = arguments_parser.parse_known_args()

    # safe guard otherwise new processes are spawned forever
    if flags.n is None:
        raise RuntimeError("main() was called again.")

    exc = get_reusable_executor(2)
    f = [exc.submit(time.sleep, 0.1) for _ in range(10)]
    [r.result() for r in f]
    print("Correct end!!!!")


if __name__ == "__main__":
    freeze_support()
    main()
