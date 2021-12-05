from time import sleep
import datetime
from typing import Tuple

import requests

FILE_PATH = "requests_history.txt"


def write_to_file(file_name, content):
    print("{} -> {}".format(content, file_name).replace("\n", ""))
    f = open(file_name, 'a')
    f.write(content)
    f.close()

def requestors_monitoring(node_url: str, auth: Tuple[str], period: int):
    node_ids = []
    while True:
        date = datetime.datetime.time(datetime.datetime.now())
        try:
            pega_resp = requests.get(f"{node_url}/prweb/api/v1/nodes/all/requestors",
                                     auth=auth
                                     ).json()
            nodes = pega_resp["data"]["result"]

            if len(node_ids) == 0:
                node_ids = [node["nodeId"] for node in nodes]
                write_to_file(FILE_PATH, "Date," + ",".join([node_id for node_id in node_ids]) + "\n")

            stats = {}
            for node in nodes:
                node_id = node["nodeId"]
                stats[node_id] = 0

                for requestor in node["requestors"]:
                    if requestor["requestor_type"] == "BROWSER" and requestor["disconnected"] == "false":
                        stats[node_id] += 1

            for node_id in node_ids:
                if node_id not in stats.keys():
                    stats[node_id] = 0

            write_to_file(FILE_PATH, str(date) + "," + ",".join([str(stats[node_id]) for node_id in node_ids]) + "\n")
        except Exception as e:
            print('Exception occurred: {};'.format(e))
            write_to_file(FILE_PATH, str(date) + "," + ",".join(["0" for node_id in node_ids]) + "\n")

        sleep(period)

if __name__ == "__main__":
    # Seconds to sleep between checks
    PERIOD = 600
    
    NODE_URL = "http://pega:1111"
    AUTH = ("login", "password")

    requestors_monitoring(NODE_URL, AUTH, PERIOD)
