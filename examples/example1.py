from multiprocessing import Process


def print_from_child():
    print("Hello from child Process")


if __name__ == "__main__":
    print("Hello from main Process")

    child_process = Process(target=print_from_child)
    child_process.start()
    child_process.join()  # Ожидаем завершения дочернего процесса
