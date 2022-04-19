from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def CheckNodeConnection(network,rpc_user,rpc_pwd):
    try:
        if network == 'mainnet':
            rpc_connection = AuthServiceProxy("http://%s:%s@localhost:8332"%(rpc_user, rpc_pwd))
        elif network == "signet":
            rpc_connection = AuthServiceProxy("http://%s:%s@localhost:38332"%(rpc_user, rpc_pwd))
        elif network == 'regtest':
            rpc_connection = AuthServiceProxy("http://%s:%s@localhost:18443"%(rpc_user, rpc_pwd))
        return rpc_connection

    except JSONRPCException:
        return "Check your rpc username/password, and ensure bitcon core is running"

