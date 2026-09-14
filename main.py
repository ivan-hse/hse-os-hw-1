import mmap
import time
from multiprocessing import Process

# размер буфера = 64 байта
BUFFER_SIZE = 64
# индекс байта флага
FLAG = 0
# индекс байта, с которого начинаются данные
DATA = 1

# производитель
def producer(buffer):
    message = "Hello consumer!"
    data = message.encode("utf-8") + b"\0"

    # записываем данные в буфер и устанавливаем флаг
    buffer[DATA:DATA + len(data)] = data
    buffer[FLAG] = 1

# потребитель
def consumer(buffer):
    # ждем, пока флаг не установлен
    while buffer[FLAG] == 0:
        time.sleep(0.01)

    # читаем данные из буфера и декодируем их
    data = buffer[DATA:BUFFER_SIZE]
    message = data.split(b"\0", 1)[0].decode("utf-8")

    print(f"Получено сообщение: {message}")

def main():
    # выделяем память под буфер
    buffer = mmap.mmap(-1, BUFFER_SIZE)

    # создаем процессы производителя и потребителя
    producer_process = Process(target=producer, args=(buffer,))
    consumer_process = Process(target=consumer, args=(buffer,))
    producer_process.start()
    consumer_process.start()

    # присоединяем дочерние процессы к родительскому
    producer_process.join()
    consumer_process.join()
    buffer.close()

if __name__ == "__main__":
    main()
