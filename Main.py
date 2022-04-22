import xmlrpc.client
import sys
import time
import threading


WORKERS = 100
PORT = 8000

workers = []
for i in range(WORKERS):
    try:
        worker = { 
            "name": "worker-%s" % i,
            "proxy": xmlrpc.client.ServerProxy("http://localhost:%s" % (PORT + i))
        }
        workers.append(worker)
    except Exception as err:
        print("Error: %s" % err)
        sys.exit(1)

class LINK:
    def __init__(self, title, depth):
        self.title = title
        self.parent = None
        self.checked = False
        self.depth = depth

        
try:
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    def menu():
        print("""
        1. Search for a page
        2. Exit
        """)
        choice = input("Your choice: ")
        return choice

    def search(worker, link):
        try:
            links = worker["proxy"].get_links(link.title)
            if links == False:
                return
            for title in links:
                if("Category:" not in title) and ("Wikipedia:" not in title) and ("Template:" not in title) and ("Template talk:" not in title) and ("Help:" not in title):
                    new_link = LINK(title, link.depth+1)
                    list.append(new_link)
                    second_list.append(title)
        except Exception as err:
            print("Error: %s" % err)
            sys.exit(1)

    list = []
    second_list = []

    depth = 0
    while True:
        choice = menu()
        if choice == "1":
            list = []
            second_list = []
            start = input("Enter your starting page: ")
            destination = input("Enter your destination page: ")
            links = proxy.get_links(start)
            print("Searching..")
            for title in links:
                if("Category:" not in title) and ("Wikipedia:" not in title) and ("Template:" not in title) and ("Template talk:" not in title) and ("Help:" not in title):
                    depth = 1
                    link = LINK(title, depth)
                    link.parent = start
                    list.append(link)

            i = 0
            while True:

                if destination in second_list:
                    for link in list:
                        if link.title == destination:
                            print("You can get to %s from %s" % (destination, start))
                            print("It takes %d step/s" % (link.depth))
                            break;
                    break

                for link in list:
                    if link.checked == False:
                        link.checked = True
                        worker = workers[i%WORKERS]
                        i += 1
                        thread = threading.Thread(target=search, args=(worker, link,))
                        thread.start()
                        break
                time.sleep(0.05)
        if choice == "2":
            print("Thank you for using the program.")
            sys.exit(1)

except Exception as err:
    print("Error: %s" % err)
    sys.exit(1)

#SOURCES
#https://www.mediawiki.org/wiki/API:Main_page
#https://www.pythontutorial.net/advanced-python/python-threading/
#https://stackoverflow.com/questions/15990639/find-shortest-path-between-two-articles-in-english-wikipedia-in-python