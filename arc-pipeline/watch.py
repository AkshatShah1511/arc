import time
from run_pipeline import run

POLL_INTERVAL_SECONDS = 30

if __name__ == "__main__":
    print("ARC watcher started. Waiting for NEW rows...")

    while True:
        try:
            run()
        except Exception as e:
            print("Watcher error:", e)

        time.sleep(POLL_INTERVAL_SECONDS)
