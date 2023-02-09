import zipfile
import sys
import argparse
import threading

def extract_zip(zfile, password):
    try:
        zfile.extractall(pwd=password.encode('utf-8'))
        print("[+] Password found: " + password)
        return password
    except:
        pass

def run_thread(zfile, password_list):
    for password in password_list:
        password = password.strip()
        if extract_zip(zfile, password):
            return

def main(zip_file, password_list, num_threads):
    zfile = zipfile.ZipFile(zip_file)
    chunk_size = len(password_list) 
    threads = []
    
    for i in range(num_threads):
        start = chunk_size * i
        end = chunk_size * (i + 1)
        if i == num_threads - 1:
            end = len(password_list)
        chunk = password_list[start:end]
        t = threading.Thread(target=run_thread, args=(zfile, chunk,))
        threads.append(t)
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Brute-force password protected zip file using multithreading')
    parser.add_argument('zip_file', help='Name of the zip file')
    parser.add_argument('password_list', help='Name of the password list file')
    parser.add_argument('num_threads', type=int, help='Number of threads to use')
    args = parser.parse_args()

    with open(args.password_list, 'r') as f:
        password_list = f.readlines()

    main(args.zip_file, password_list, args.num_threads)
