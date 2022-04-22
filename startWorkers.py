import sys
from subprocess import Popen
try:
    WORKERS = 100
    PORT = 8000

    for i in range(WORKERS):
        port = PORT + i
        Popen(["python3", "Worker.py", str(port)])
except Exception as err:
    print("Error: %s" % err)
    sys.exit(1)


#SOURCES
#https://stackoverflow.com/questions/12605498/how-to-use-subprocess-popen-python