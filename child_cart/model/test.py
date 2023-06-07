import threading

# Define a function that will be executed in the thread
def thread_function():
    
    for i in range(20):
        print("This is the child thread.")

# Create a new thread
thread = threading.Thread(target=thread_function)

# Start the thread
thread.start()

# Main thread continues executing
for i in range(20):
    print("This is the main thread.")    