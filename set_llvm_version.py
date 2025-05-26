from datetime import datetime

now = datetime.now()
date = f"__version__ = \"{now.year}{now.month:02}{now.day:02}{now.hour:02}\""

with open("llvm_version.txt", "w") as file:
    print(date, file=file, sep="")
