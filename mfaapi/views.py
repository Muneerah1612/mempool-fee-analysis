from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import authentication, permissions,status
from .serializers import TxSerializer
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

from rest_framework.response import Response

# Create your views here.
class GetTxDetails(APIView):
    def post(self,request):
        rpc_user=request.data['rpc-user']
        rpc_pwd=request.data['rpc-pass']
        rpc_connection = AuthServiceProxy("http://%s:%s@localhost:18443"%(rpc_user, rpc_pwd))
        mempool_list = rpc_connection.getrawmempool()
        # print(mempool_list)
        txid=request.data['txid']
        if txid in mempool_list:
            txinfo=rpc_connection.getmempoolentry(txid)
            print(txinfo)
            return Response({'status':status.HTTP_302_FOUND, 'message':txinfo})
        else:
            return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Transaction not in mempool'})

## restructure the code to take in the rpc user,rpc password and network type (mainnet,signet,testnet)
class ListFeesView(APIView):
    def post(self,request):
        pass
        

