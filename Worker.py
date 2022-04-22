from xmlrpc.server import SimpleXMLRPCServer
import sys
import requests
server = SimpleXMLRPCServer(("localhost", int(sys.argv[1])))
print("Listening on port", sys.argv[1])

URL = "https://en.wikipedia.org/w/api.php"
S = requests.Session()

def get_links(title):
    try:
        PARAMS = {
            "action": "parse",
            "format": "json",
            "page": title,
            "prop": "links"
        }
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        pageData = DATA.get("parse")
        links = pageData.get("links")
        print(title)
        list = []
        #file = open('links.txt', 'w', encoding="utf-8")
        for link in links:
            list.append(link["*"])
            #file.write(link["*"] + '\n')
        return list
    except:
        print("Error")
        return False

server.register_function(get_links, "get_links")
server.serve_forever()