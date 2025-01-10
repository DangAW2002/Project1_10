import logging
from datetime import datetime

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"log/app/app_{current_date}.log"),  # Ghi log vào file với ngày hiện tại
        logging.StreamHandler()         # Hiển thị log trên console
    ],
)

# Tạo một logger riêng cho lỗi
error_logger = logging.getLogger("error_logger")
# Tạo một logger riêng cho state
state_logger = logging.getLogger("state_logger")
def configure_logger():
    error_logger.setLevel(logging.ERROR)

    # Cấu hình handler cho error_logger
    error_handler = logging.FileHandler(f"log/error/error_{current_date}.log")  # Ghi log lỗi vào file riêng với ngày hiện tại
    error_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    error_logger.addHandler(error_handler)
    error_logger.propagate = False  # Prevent propagation to avoid duplicate logs


    state_logger.setLevel(logging.INFO)

    # Cấu hình handler cho state_logger
    state_handler = logging.FileHandler(f"log/state/state_{current_date}.log")  # Ghi log state vào file riêng với ngày hiện tại
    state_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    state_logger.addHandler(state_handler)
    state_logger.propagate = False  # Prevent propagation to avoid duplicate logs

# Suppress specific log messages from appearing in the console
class SuppressConsoleFilter(logging.Filter):
    def filter(self, record):
        if "Setting `pad_token_id` to `eos_token_id`" in record.getMessage():
            return False
        return True

for handler in logging.getLogger().handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.addFilter(SuppressConsoleFilter())



