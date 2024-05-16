from tqdm import tqdm
import time


class Color:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"


class ProgressBar:
    def __init__(self, total, description="Processing", color="green"):
        self.total = total
        self.description = description
        self.color = color
        self.bar = tqdm(total=self.total, desc=self.description, colour=self.color)
        self.start_time = time.time()
        self.end_time = None

    def update(self, increment=1):
        self.bar.update(increment)

    def complete(self):
        self.bar.close()
        self.bar = None
        self.end_time = time.time()
        execution_time = self.end_time - self.start_time
        print(
            f"{self.description} finished in:",
            end=" ",
        )
        print(
            f"{Color.GREEN if execution_time < 50 else Color.YELLOW}",
            execution_time,
            "seconds" + Color.RESET,
        )
