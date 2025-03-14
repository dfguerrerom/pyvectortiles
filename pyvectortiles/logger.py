import sys
import logging
from pathlib import Path
import colorlog  # Install via: pip install colorlog
import io

# ANSI background color codes
BLUE_BG = "\033[44m"
PURPLE_BG = "\033[45m"
YELLOW_BG = "\033[43m"
RESET = "\033[0m"


class InMemoryLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_buffer = io.StringIO()

    def emit(self, record):
        msg = self.format(record)
        self.log_buffer.write(msg + "\n")

    def get_logs(self):
        return self.log_buffer.getvalue()


class CustomLogger:
    def __init__(
        self, name: str, level: int = logging.DEBUG, module_color: str = YELLOW_BG
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create a colored console handler.
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Build the format string using the module_color for the logger's name.
        format_str = f"%(log_color)s%(asctime)s - {module_color}%(name)s{RESET} - %(levelname)s - %(message)s"
        console_formatter = colorlog.ColoredFormatter(
            format_str,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def message_to_string(self, *messages: str) -> str:
        return " ".join(str(msg) for msg in messages)

    def debug(self, *messages: str):
        self.logger.debug(self.message_to_string(*messages))

    def info(self, *messages: str):
        self.logger.info(self.message_to_string(*messages))

    def warning(self, *messages: str):
        self.logger.warning(self.message_to_string(*messages))

    def error(self, *messages: str):
        self.logger.error(self.message_to_string(*messages))

    def critical(self, *messages: str):
        self.logger.critical(self.message_to_string(*messages))


logger = CustomLogger("VECTORTILES", module_color=PURPLE_BG)
in_memory_handler = InMemoryLogHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
in_memory_handler.setFormatter(formatter)
logger.logger.addHandler(InMemoryLogHandler())
