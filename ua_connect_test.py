"""
OPC-UAテスト
No.2：不正接続

"""
import sys
import argparse
from opcua import Client, ua
from opcua.crypto import security_policies
from time import sleep

secPolicy = ""
policies = ["", "Basic128Rsa15", "Basic256", "Basic256Sha256"]

setCert = ""
certs = ["anonymous", "user", "certificate"]
#引数定義
def get_args():
    # 準備
    parser = argparse.ArgumentParser()
    # 標準入力以外の場合
    #if sys.stdin.isatty():
    parser.add_argument("policy", help="0:none, 1:basic128rsa15, 2:basic256", type=int)
    parser.add_argument("cert", help="0:anonymous, 1:user, 2:certificate", type=int)
    # 結果を受ける
    args = parser.parse_args()
    return(args)

def set_args():
    global secPolicy, setCert
    args = get_args()
    print("args.policy: "+str(args.policy))
    print("args.cert: "+str(args.cert))
    secPolicy = policies[args.policy]
    setCert = certs[args.cert]

def conn_opc():
    # OPCサーバに接続
    cl = Client("opc.tcp://192.168.10.5:51110/CogentDataHub/DataAccess")
    # クライアント証明書のapplication_uri
    cl.application_uri = "urn:desktop-i50i89m:Cogent DataHub"
    # policy設定
    print("secPolicy: "+str(secPolicy))
    if secPolicy != policies[0]: # None以外の場合SecurityPolicyを設定
        mode = ua.MessageSecurityMode.SignAndEncrypt
        pc = getattr(security_policies, 'SecurityPolicy' + secPolicy)
        # 第二引数：クライアント証明書
        cl.set_security(pc, "/Users/watarium/PycharmProjects/opcua/OPCUA_CL.der", "/Users/watarium/PycharmProjects/opcua/OPCUAClient.pem", "/Users/watarium/PycharmProjects/opcua/OPCUAServer.der", mode)
        
    # 認証設定
    if setCert == certs[1]: # user/pass
        cl.set_user("admin")
        cl.set_password("1234")
    elif setCert == certs[2]: # certificate
        cl.load_private_key("/Users/watarium/PycharmProjects/opcua/OPCUAClient.pem")
        cl.load_client_certificate("/Users/watarium/PycharmProjects/opcua/OPCUA_CL.der")
    try:
        # 接続
        print("Policy: {0}, Certificate: {1}".format(secPolicy, setCert))
        print("---------------------Connection start-----------------------")
        cl.connect()
        sleep(5)
        # 情報取得
        ep = cl.get_endpoints()
        print(ep[0].Server.ApplicationUri)

        root = cl.get_root_node()
        print("Objects node is: ", root)


        print(cl.get_namespace_array())
        print(cl.get_namespace_index('urn:win-9hi38ajrojd:Cogent DataHub'))

        #これがうまくいかなかった（2019/06/27）
        #node = cl.get_node('ns=1;s=xxxxx')
        #print(node.get_value())

        #node.set_attribute(ua.AttributeIds.Value, 1)

        # 切断
        cl.disconnect()
        print("-------------------Connection Success!!!--------------------")

    except Exception as e:
        print("---------------------Connection Faild!!---------------------")
        print(e)
        cl.disconnect()
if __name__ == "__main__":
    set_args()
    conn_opc()
