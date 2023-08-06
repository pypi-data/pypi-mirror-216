import logging

# 简单定义日志对象
log = logging.getLogger('aniya')
log.setLevel(logging.WARNING)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('[%(name)s] %(levelname)s %(message)s')  # noqa
console_handler.setFormatter(formatter)
log.addHandler(console_handler)
