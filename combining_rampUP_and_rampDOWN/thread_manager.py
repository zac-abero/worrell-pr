import threading

class ThreadManager:
    def __init__(self):
        self.threads = []

    def create_thread(self, target, args=()):
        """Create a new thread and add it to the manager."""
        thread = threading.Thread(target=target, args=args)
        self.threads.append(thread)
        print(f"Thread {thread.name} created.")
        return thread

    def start_all(self):
        """Start all threads managed by this instance."""
        for thread in self.threads:
            thread.start()
            print(f"Thread {thread.name} started.")

    def join_all(self):
        """Join all threads managed by this instance."""
        for thread in self.threads:
            thread.join()

    def terminate_all(self, end_event):
        """Signal all threads to terminate."""
        end_event.set()
        for thread in self.threads:
            if thread.is_alive():
                thread.join()  # Wait for the thread to finish if it's still running
                print(f"Thread {thread.name} terminated.")

    def clear(self):
        """Clear the thread list."""
        self.threads.clear()
