import json
import socket
import time
import pandas as pd


def real_time_transmit(file_path, host='spark-master', port=9999, chunk_size=2):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"Listening for connections on {host}:{port}")

    last_sent_index = 0
    while True:
        conn, addr = s.accept()
        print(f"Connection from {addr}")
        try:
            with open(file_path, 'r') as file:
                # Skip lines that were already sent
                for _ in range(last_sent_index):
                    next(file)

                records = []
                for line in file:
                    records.append(json.loads(line))
                    if len(records) == chunk_size:
                        chunk = pd.DataFrame(records)
                        print(chunk)
                        for record in chunk.to_dict(orient='records'):
                            serialized_data = json.dumps(record).encode('utf-8')
                            conn.send(serialized_data + b'\n')  # Send each record followed by a newline
                            time.sleep(5)
                            last_sent_index += 1
                        records = []
        except (BrokenPipeError, ConnectionResetError):
            print("Client disconnected.")
        finally:
            conn.close()
            print("Waiting for a new connection...")


if __name__ == "__main__":
    real_time_transmit("./dataset/archive/output.json")
