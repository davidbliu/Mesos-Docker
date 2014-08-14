import etcd

etcd_client = etcd.Client()
etcd_client.write('/test', 1)

