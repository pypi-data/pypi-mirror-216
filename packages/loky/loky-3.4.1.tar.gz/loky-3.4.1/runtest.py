import time

from loky.backend import resource_tracker

resource_tracker.ensure_running()
time.sleep(1)
resource_tracker.ensure_running()
print("all good")
