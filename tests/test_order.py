# /usr/bin/env python
# -*- coding:utf8 -*-
from unittest import TestCase
import shopee
import json

class TestOrder(TestCase):

    def get_client(self):
        client = shopee.Client(34535, 345554, "343")
        return client

    def test_shopee_get_order_by_status(self):
        client = self.get_client()
        resp = client.order.get_order_by_status(order_status="CANCELLED")

        body = json.loads(resp.text)

        for o in body["orders"]:
            print("%s : %s"% (o["ordersn"], o["order_status"]))


    def test_shopee_get_order_detail(self):
        client = self.get_client()
        # resp = client.order.query(create_time_from = 1512117303, create_time_to=1512635703)
        # if resp.status_code == 200:
        #     print(resp.text)

        #17113023414VVJF
        #171128143941R5V
        #17112917104CHF4
        #17112715084T7MG

        ordersn_list = [
            "17113023414VVJF", "171128143941R5V",
            "17112917104CHF4", "17112715084T7MG",
            "17111418244FMFA", "17120213344PUUQ",
            "17120501004SGEF", "17120316264UJNX"
        ]

        resp = client.logistic.get_tracking_no(ordersn_list=ordersn_list)

        body = json.loads(resp.text)
        print(body)

        for o in ordersn_list:
            resp = client.order.get_order_escrow_detail(ordersn=o)
            body = json.loads(resp.text)
            print(body)
        resp = client.order.get_order_detail(ordersn_list = ordersn_list)

        body = json.loads(resp.text)

        for o in body["orders"]:
            print(o)
