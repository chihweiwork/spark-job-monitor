import threading
import signal
import functools
import time
        
from typing import Callable, Any

def function_daemonize(sleep_time: int = 1) -> Callable:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        exit_event = threading.Event()
        def handle_signal(signum: int, frame: Any) -> None:
            print(f"Received signal {signum}, shutting down gracefully...")
            exit_event.set()  # Signal the thread to exit

        def wrapper(*args: Any, **kwargs: Any) -> None:
            def run_in_thread(exit_event: threading.Event) -> None:
                while not exit_event.is_set():
                    try:
                        func(*args, **kwargs)
                    except Exception as e:
                        print(f"Error occurred: {e}")
                    time.sleep(sleep_time)  # Sleep for a short period to prevent a tight loop

            # Registering the signal handlers
            signal.signal(signal.SIGINT, handle_signal)  # Signal from keyboard interruption Ctrl+C
            signal.signal(signal.SIGTERM, handle_signal)  # Termination signal from system

            thread = threading.Thread(target=run_in_thread, args=(exit_event,))
            thread.daemon = True  # Set thread as a daemon so it will end when the main program exits
            thread.start()
            thread.join()  # Wait for the thread to complete execution

        return functools.update_wrapper(wrapper, func)
    return decorator
