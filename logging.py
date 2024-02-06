from datetime import datetime

file_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
file = open(file_name, "w")


def log(item):
    f = open(file_name, "a")
    f.write("\n" + item)
    print(item)
    f.close()
