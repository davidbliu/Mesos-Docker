"""from twisted.internet import defer
import etcd

etcd_client = etcd.Client()
df = defer.Deferred()

def watch_key():
    df = etcd_client.read('/test', recursive=True, wait=True, timeout=0)
    df.addCallback(_someData, response)
    return df

def _transform(rows):
    # rows here is now the returned data
    return [my_object(row) for row in rows]

def _someData(rows, response):
    response.render(rows)
    response.finish()

watch_key()"""

#Nevermind