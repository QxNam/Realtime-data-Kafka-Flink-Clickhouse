from datetime import datetime
import json
from pyflink.common import Row

def parse_data(data: str) -> Row:
    data = json.loads(data)
    customer_id = int(data["customer_id"])
    shop_id = int(data["shop_id"])
    product_id = int(data["product_id"])
    action = data["action"]
    event_timestamp = datetime.strptime(data["event_timestamp"], "%Y-%m-%d %H:%M:%S")
    additional_info = json.dumps(data["additional_info"])
    return Row(customer_id, shop_id, product_id, action, event_timestamp, additional_info)


