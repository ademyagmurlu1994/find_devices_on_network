import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import socket
import threading

count = 0

def is_exist(text, word):
    try:
        if text.index(word) >= 0:
            return True
    except ValueError:
        return False

def split_thread_ip_address(split_size, ip_address):
    threads=[]
    division_size = 255//split_size
    remainder = 255 % split_size
    for i in range(0, split_size):
        threads.append(threading.Thread(target=ping, args=(ip_address, (division_size * i + 1, division_size * (i+1)))))
    threads.append(threading.Thread(target=ping, args=(ip_address, (division_size * split_size + 1 , division_size * (split_size) + remainder))))

    for thread in threads:
        thread.start()

def find_device_on_network(card=0): #card=0 ise ethernet, card=1 ise wifi
    ip_address = socket.gethostbyname_ex(socket.gethostname())[2][card]
    index = ip_address.rfind(".", 0)
    ip_address = ip_address[0:index + 1]

    split_thread_ip_address(20, ip_address)

def ping(ip_address, range_of_ip=(1, 255)):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    for ping in range(range_of_ip[0], range_of_ip[1] + 1):
        address = ip_address + str(ping)
        process = subprocess.Popen(['ping', param, '1', address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        if is_exist(str(out), "bytes="):
            print("Device: ", address, "OK")
        """else:
            print("Device: ", address, "failed!")"""

        global count
        count = count + 1
        if count == 255:
            print("device sacanning is finished :-)")
            break

if __name__ == "__main__":
    find_device_on_network(1)
