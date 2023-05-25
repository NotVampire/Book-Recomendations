import time


class Program:
    start_time = time.time()

    def start_timer(self):
        self.start_time = time.time()

    def finish_timer(self):
        end_time = time.time()
        time_taken = end_time - self.start_time
        print(f"Time taken overall: {time_taken}")

class Timer:
    start_time = time.time()

    def start_timer(self):
        self.start_time = time.time()

    def finish_timer(self, message):
        end_time = time.time()
        time_taken = int(end_time - self.start_time)
        print(f"{message}, time taken: {time_taken}s")