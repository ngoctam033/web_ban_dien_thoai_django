import logging

# Tạo một logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Tạo một FileHandler để ghi log vào file
file_handler = logging.FileHandler('app.txt', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Tạo một StreamHandler để ghi log ra console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Thêm các handler vào logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Now the logger is configured, you can use it in your code
logger.info('This is an info message')