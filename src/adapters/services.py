import os
from flask import json
import requests
from ports.order_service import OrderServicePort


class OrderServiceAdapter(OrderServicePort):

    def __init__(self):
        self.order_service_api = os.environ.get("ORDER_SERVICE_API")

    def update_status_order(self, order_id: int, status: str):
        url = f"{self.order_service_api}/api/v1/orders/{order_id}/status"
        data = json.dumps({"status": status})
        headers = {"Content-Type": "application/json"}
        response = requests.patch(url=url, data=data, headers=headers)
        return response
