from queue import Queue
import threading



# Publisher function
def send_message(queue):
    while True:
        message = input("Enter a message (or 'quit' to exit): ")
        queue.put(message)
        if message == 'quit':
            break

# Main function
def main():
    # Create a shared queue for communication
    message_queue = Queue()
    
    # Start the subscriber thread

    
    # Start the publisher thread
    publisher_thread = threading.Thread(target=send_message, args=(message_queue,))
    publisher_thread.start()

    while True:
        message = message_queue.get()
        if message == 'quit':
            break
        print(f"Received message: {message}")
        print("hello")
    
    # Wait for both threads to finish
    publisher_thread.join()

if __name__ == "__main__":
    main()
