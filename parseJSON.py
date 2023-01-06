import json
import datetime as dt

from glom import glom # deep property access
from collections import namedtuple

from saveToDatabase import *

def UTC_time(timezone_date: str):
    """Convert timezone date to UTC timestamp."""
    utc_tz = dt.timezone.utc
    date = dt.datetime.fromisoformat(timezone_date)
    date = date.astimezone(utc_tz)
    return date.strftime("%Y-%m-%d %H:%M:%S")

def load_json(filename: str) -> dict:
    """Load json file."""
    with open(filename, "r", encoding="utf-8") as f:
        json_data = f.read()
    return json.loads(json_data)


def print_info_data(json_data: list[dict]) -> None:
    """From json data print name, cpu, memory usage, created_at, status, list of IP addresses."""
    
    for container in json_data:
        print("name:",container["name"])
        print("cpu usage:", glom(container, "state.cpu.usage", default = ""))
        print("memory usage:", glom(container, "state.memory.usage", default = ""))
        
        print("created_at:", UTC_time(container["created_at"]))
        print("status:", container["status"])
        
        network = glom(container, "state.network", default = {})
        addresses = []
        for net in network.values():
            for addr in net["addresses"]:
                addresses.append(addr["address"])
        
        print("; ".join(addresses))
        print("")


# namedtuple funguje podobně jako structs
# namedtuple(název, attributes oddělené mezerami)
LXC_Container = namedtuple("LXC_Container", "name cpu memory created_at status addresses")
        
def create_containers_from_json(json_data: list[dict]) -> list[LXC_Container]:
    containers = []
    for container in json_data:
        # search for all addresses
        network = glom(container, "state.network", default = {})
        addresses = []
        for net in network.values():
            for addr in net["addresses"]:
                addresses.append(addr["address"])
        
        # create a new container
        x = LXC_Container(
            name = container["name"],
            cpu = glom(container, "state.cpu.usage", default = None),
            memory=glom(container, "state.memory.usage", default = None),
            created_at=UTC_time(container["created_at"]),
            status =container["status"],
            addresses=addresses
        )
        containers.append(x)
        
    return containers
        

def main():
    filename = "sample-data.json"
    data = load_json(filename)
    # print_info_data(data)
    # print(create_containers_from_json(data))
    
    db = initialize_MySQL()
    save_to_database(db, create_containers_from_json(data))

if __name__ == "__main__":
    main()