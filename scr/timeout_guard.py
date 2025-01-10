import threading

def timeout_guard(func, timeout=60, *args, **kwargs):
    result = [None]
    exception = [None]
    finished = threading.Event()

    def wrapper():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exception[0] = e
        finally:
            finished.set()

    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join(timeout)  # Đợi tối đa `timeout` giây

    if not finished.is_set():  # Nếu không hoàn thành trong thời gian cho phép
        raise TimeoutError("Quá thời gian chờ! Đang khởi động lại chương trình...")

    if exception[0]:  # Nếu xảy ra lỗi trong hàm
        raise exception[0]

    return result[0]