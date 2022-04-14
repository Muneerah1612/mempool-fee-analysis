from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import authentication, permissions,status
from .serializers import TxSerializer
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
# from decimal import Decimal
import json

from rest_framework.response import Response

# Create your views here.
class GetTxDetails(APIView):
    def post(self,request):
        rpc_user=request.data['rpc-user']
        rpc_pwd=request.data['rpc-pass']
        rpc_connection = AuthServiceProxy("http://%s:%s@localhost:18443"%(rpc_user, rpc_pwd))
        mempool_list = rpc_connection.getrawmempool()
        # print(mempool_list==True)
        txid=request.data['txid']
        if txid in mempool_list:
            txinfo=rpc_connection.getmempoolentry(txid)
            print(txinfo['fees']['base'])
            return Response({'status':status.HTTP_302_FOUND, 'message':txinfo})
        else:
            return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Transaction not in mempool'})

## restructure the code to take in the rpc user,rpc password and network type (mainnet,signet,testnet)
class ListFeesView(APIView):
    def post(self,request):
        rpc_user=request.data['rpc-user']
        rpc_pwd=request.data['rpc-pass']
        rpc_connection = AuthServiceProxy("http://%s:%s@localhost:18443"%(rpc_user, rpc_pwd))
        mempool_list = rpc_connection.getrawmempool()
        details=[{i:rpc_connection.getmempoolentry(i)['fees']['base']} for i in mempool_list]
        
        
        return Response({'status':status.HTTP_302_FOUND, 'message':details})


class HighLowFeesView(APIView):
    def post(self,request):
        rpc_user=request.data['rpc-user']
        rpc_pwd=request.data['rpc-pass']
        rpc_connection = AuthServiceProxy("http://%s:%s@localhost:18443"%(rpc_user, rpc_pwd))
        mempool_list = rpc_connection.getrawmempool()
        details=[{rpc_connection.getmempoolentry(i)['fees']['base']} for i in mempool_list]
        highlow= [{'lowest fee':min(details)},{'highest fee':max(details)}]
        return Response({'status':status.HTTP_302_FOUND, 'message':highlow})
        

