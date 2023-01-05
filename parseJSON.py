import json
import datetime as dt

def UTC_time(timezone_date: str) -> dt.datetime:
    """Convert timezone date to UTC timestamp."""
    utc_tz = dt.timezone.utc
    date = dt.datetime.fromisoformat(timezone_date)
    return date.astimezone(utc_tz)

def load_json(filename: str) -> dict:
    """Load json file."""
    with open(filename, "r", encoding="utf-8") as f:
        json_data = f.read()
    return json.loads(json_data)

def print_info_data(json_data: list[dict]) -> None:
    """From json data print name, cpu, memory usage, created_at, status, IP addresses."""
    
    for container in json_data:
        
        try:
            print("name:",container["name"])
            print("cpu usage:", container["state"]["cpu"]["usage"])
            print("memory usage:", container["state"]["memory"]["usage"] )
            
            print("created_at:", UTC_time(container["created_at"]))
            print("status:", container["status"])
            # print("list of IP addresses:", container["state"]["network"]["lo"]["addresses"])
        except TypeError as err: 
            print(err) # name: docker-at 
            # 'NoneType' object is not subscriptable
            
        print("")

def search_for_addresses(container: dict):
    network = container["state"]["network"]
    for key, value in network.items():
        print(key, value)

def main():
    filename = "sample-data.json"
    data = load_json(filename)
    # print_info_data(data)

if __name__ == "__main__":
    main()