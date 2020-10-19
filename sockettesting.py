import threading
import time
import socket

class myThread (threading.Thread):
    def __init__(self, threadID, name, sock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.sock = sock
    def run(self):
        print ("Starting " + self.name)
        # Get lock to synchronize threads
        print("Reading from sock")
        # Free lock to release next thread
        line = conn.recv(512).decode("utf-8")
        print(line)


threads = []


server_address = "127.0.0.1"
port = 5100
sock =  socket.socket(socket.AF_INET,  socket.SOCK_STREAM) 
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((server_address, port))
sock.listen(5)

for i in range(1) :
    #Accept port
    conn,addr =  sock.accept()
   # Create new threads
    print("Accepted a Connection")
    thread = myThread(i, "Thread-"+str(i), conn)
    # Start new Threads
    thread.start()
    # Add threads to thread list
    threads.append(thread)

# Wait for all threads to complete
for t in threads:
    t.join()

sock.close()
print ("Exiting Main Thread")