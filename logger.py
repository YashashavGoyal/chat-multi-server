## Importing Modules
from pathlib import Path
import time
## .......


class Logger:

    def __init__(self, filename_without_extension):
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)  # ensure logs/ exists
        self.log_file = log_dir / f"{filename_without_extension}"
        
    def _write(self, level, msg):
        timeStamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a+") as file:
            file.write(f"[{timeStamp}] [{level}] {msg}\n")
    
    def log(self,msg):
        self._write("MSG", msg)

    def info(self, msg):
        self._write("INFO", msg)

    def warn(self, msg):
        self._write("WARNING", msg)

    def error(self, msg):
        self._write("ERROR", msg)


