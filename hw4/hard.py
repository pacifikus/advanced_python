import codecs
import logging
import time
from multiprocessing import Process, Queue, Pipe

logging.basicConfig(
    format='%(asctime)s  %(message)s',
    datefmt='%H:%M:%S %d-%m-%y',
    filename='artifacts/hard_logging.txt',
    level=logging.INFO,
    filemode='a',
)


def process_A(input_queue, conn):
    while True:
        msg = input_queue.get()
        if msg is not None:
            logging.info(f'Process A get {msg} from main')
            msg = msg.lower()
            conn.send(msg)
            logging.info(f'Process A send {msg} to process B')
            time.sleep(5)
        else:
            conn.send(msg)
            break


def process_B(input_conn, output_queue):
    while True:
        msg = input_conn.recv()
        if msg is not None:
            logging.info(f'Process B get {msg} from process A')
            msg = codecs.encode(msg, 'rot_13')
            output_queue.put(msg)
            logging.info(f'Process B send {msg} to main')
        else:
            break


in_queue = Queue()
out_queue = Queue()
conn_a, conn_b = Pipe()

a = Process(target=process_A, args=(in_queue, conn_b))
b = Process(target=process_B, args=(conn_a, out_queue))

a.start()
b.start()

while True:
    text = input()
    in_queue.put(text)
    logging.info(f'Main send {text} to process A')
    result = out_queue.get()
    print(result)

a.join()
b.join()
