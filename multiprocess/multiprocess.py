import multiprocessing


def make_data(queue, num, work_nums ):
    for j in range(num):
        queue.put(j)
    for j in range(work_nums):
        queue.put(None)


def handle_data(queue, share_value, lock):
    while True:
        data = queue.get()
        if data is None:
            break
        lock.acquire()
        share_value.value = share_value.value + data
        lock.release()


if __name__ == "__main__":
    queue = multiprocessing.Queue()
    share_value = multiprocessing.Value("i", 0)
    lock = multiprocessing.Lock()
    num = 10000
    work_nums = 5
    sub_process = []
    master_process = multiprocessing.Process(target=make_data, args=(queue, num, work_nums,))
    master_process.start()

    for i in range(work_nums):
        sub_process1 = multiprocessing.Process(target=handle_data,args=(queue,share_value,lock, ))
        sub_process.append(sub_process1)
    for p in sub_process:
        p.start()

    master_process.join()
    for p in sub_process:
        p.join()
    result = 0
    for i in range(num):
        result = result + i
    print str(result)
    print str(share_value.value )