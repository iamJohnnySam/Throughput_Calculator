import os

path = ""


def prepare_log_file(log_file):
    global path

    if ".json" in log_file:
        log_file = log_file.replace(".json", "")

    if log_file == "":
        return

    path = "log/" + log_file + ".txt"

    if os.path.isfile(path):
        os.remove(path)


def log(item):
    global path

    f = open(path, "a")
    f.write("\n" + item)
    # print(item)
    f.close()
