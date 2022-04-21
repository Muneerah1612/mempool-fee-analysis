from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .utils import CheckNodeConnection
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from rest_framework.response import Response


class GetTxDetails(APIView):
    def post(self, request):
        rpc_user = request.data["rpc_user"]
        rpc_pwd = request.data["rpc_pwd"]
        network = request.data["rpc_port"]
        rpc_connect = CheckNodeConnection(network, rpc_user, rpc_pwd)
        mempool_list = rpc_connect.getrawmempool()

        txid = request.data["txid"]
        if txid in mempool_list:
            txinfo = rpc_connect.getmempoolentry(txid)
            return Response({"status": status.HTTP_302_FOUND, "message": txinfo})
        else:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Transaction not in mempool",
                }
            )


class ListFeesView(APIView):
    def post(self, request):
        rpc_user = request.data["rpc_user"]
        rpc_pwd = request.data["rpc_pwd"]
        network = request.data["rpc_port"]
        try:
            rpc_connect = CheckNodeConnection(network, rpc_user, rpc_pwd)
            mempool_list = rpc_connect.getrawmempool(True)
            details = [{i: str(mempool_list[i]["fees"]["base"])} for i in mempool_list]
            return Response({"status": status.HTTP_302_FOUND, "message": details})
        except ConnectionRefusedError:
            return Response(
                {
                    "message": "Check your rpc username/password, and ensure bitcon core is running"
                }
            )


class HighLowFeesView(APIView):
    def post(self, request):
        rpc_user = request.data["rpc_user"]
        rpc_pwd = request.data["rpc_pwd"]
        network = request.data["rpc_port"]
        try:
            rpc_connect = CheckNodeConnection(network, rpc_user, rpc_pwd)
            mempool_list = rpc_connect.getrawmempool(True)
            details = [mempool_list(i)["fees"]["base"] for i in mempool_list]
            highlow = [
                {"lowest fee": str(min(details))},
                {"highest fee": str(max(details))},
            ]
            return Response({"status": status.HTTP_302_FOUND, "message": highlow})
        except ConnectionRefusedError:
            return Response(
                {
                    "message": "Check your rpc username/password, and ensure bitcon core is running"
                }
            )


class GetMempoolLastTransaction(APIView):
    def post(self, request):
        rpc_user = request.data["rpc_user"]
        rpc_pwd = request.data["rpc_pwd"]
        network = request.data["rpc_port"]
        try:
            rpc_connection = CheckNodeConnection(network, rpc_user, rpc_pwd)
            mempool_list = rpc_connection.getrawmempool(True)
            details = [mempool_list[i]["time"] for i in mempool_list]
            lasttxinfo = [
                {
                    i: {
                        "time": mempool_list[i]["time"],
                        "fees": str(mempool_list[i]["fees"]["base"]),
                        "vsize": mempool_list[i]["vsize"],
                    }
                }
                for i in mempool_list
                if mempool_list[i]["time"] == max(details)
            ]
            return Response({"status": status.HTTP_302_FOUND, "message": lasttxinfo})
        except ConnectionRefusedError:
            return Response(
                {
                    "message": "Check your rpc username/password, and ensure bitcon core is running"
                }
            )
