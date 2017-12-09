# /usr/bin/env python
# -*- coding:utf8 -*-
from unittest import TestCase
import shopee
import json

class TestOrder(TestCase):

    def get_client(self):
        client = shopee.Client(8526804, 10007, "80fb2727b950aa3e754cd8f7f9d2716cc056f00f1e8cd334c9fc61746bb2d4b1")
        return client

    def test_shopee_get_order_by_status(self):
        client = self.get_client()
        try:
            resp = client.order.get_order_by_status(order_status="READY_TO_SHIP")
        except Exception as e:
            print(e)



    def test_shopee_get_order_detail(self):
        client = self.get_client()
        # resp = client.order.query(create_time_from = 1512117303, create_time_to=1512635703)
        # if resp.status_code == 200:
        #     print(resp.text)

        #17113023414VVJF
        #171128143941R5V
        #17112917104CHF4
        #17112715084T7MG

        # ordersn_list = [
        #     "171209092707FHK",
        #
        # ]
        #
        # resp = client.logistic.get_tracking_no(ordersn_list=ordersn_list)
        #
        #
        # print(resp)
        #
        # for o in ordersn_list:
        #     resp = client.order.get_order_escrow_detail(ordersn=o)
        #     print(resp)
        resp = client.order.get_order_detail(ordersn_list = ["17120501004SGEF"])
        print(resp)
        #
        #
        # #PH174660492724H
        # resp = client.logistic.get_parameter_for_init(ordersn = "171209085506N5D")
        # print(resp)
        # b = {'dropoff': [], "ordersn": "171209085506N5D"}
        #PH175869963295V  //PH175869963295V
        #resp = client.logistic.init(ordersn="171209085506N5D", dropoff={})
        #print(resp)
