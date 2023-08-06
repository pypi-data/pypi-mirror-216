# What is speedracer?

Speedracer is an asyncio enabled python library for interacting with Autobahn.
Speedracer enables users to

- Subscribe to datasets available in Autobahn
- Authenticate to Autobahn APIs

# Installation

<span style="color:red;">Requires Python3.8+</span>

```
pip install speedracer
```

# Quickstart

<span style="color:red;">
  See <a href="#important-notes">Important Notes</a> for all SSL/TLS errors.
</span>

## Subscribe to a dataset

To subscribe to a dataset on the MDB
  1. Modify the string 'PUT-DATASET-HERE' with the dataset slug
  1. Modify the certificate paths to poin to your certificates [(about certificates)](#providing-client-certificates)
  1. Download the CA Bundle from the table [here](#providing-a-certificate-authority-sslcertverificationerror), and update the `ca_bundle` path to point to it

Put the following code block in a file, and run it.

```python
import asyncio
from speedracer import Connection

async def main():
    conn = Connection('https://mdb-account-server/',
              cert=('/path/to/mycert.crt', '/path/to/mycert.key'),
              ca_bundle='/path/to/ca.cer')
    sub = await conn.subscribe('PUT-DATASET-HERE')
    async for msg in sub:
        print(msg.data.decode())

if __name__ == '__main__':
    asyncio.run(main())
```

## Authenticate to Autobahn APIs

Autobahn uses JWT credentials for authorization. These tokens are put into the `Authorization`
header for all HTTPs requests. 

JWTs are obtained by exchanging private keys with the API Gateway server and
must be periodically refreshed.

`speedracer` automates the process of fetching JWTs and refreshing them when they expire.

```python
manager = JWTManager('https://api-gateway/getjwt',
              cert=('/path/to/mycert.crt', '/path/to/mycert.key'),
              verify='/path/to/ca.cer')
auth_headers = manager.get_headers()
requests.get('https://autobahn-service/', headers=auth_headers)
```

# Advanced Usage

## Dataset Subscriptions

### Callback

Instead of iterating over a `Subscription`, you can provide a callback that
takes a message as an argument.

```python
def cb(msg):
    print(msg.data.decode())

conn = Connection('https://mdb-account-server.com')
sub = await conn.subscribe('mydataset', callback=cb)
await sub.wait(messages=10) # exit after 10 messages received
```

### Seek

Autobahn maintains a short history of messages (by default 7 days) for each 
dataset. To navigate to different points in the stream use the `seek` method.
Seek accepts a message sequence number or a datetime object.

```python
# seek to message sequence 1
await sub.seek(1)

# seek to 5 minutes ago
await sub.seek(datetime.datetime.utcnow() - datetime.timedelta(minutes=5))
```

### Offset

By default, `subscribe` starts at the current time; to start at the beginning
of the stream use `Offset.BEGIN`

```python
sub = await conn.subscribe('mydataset', offset=Offset.BEGIN)
```

### Low Latency

By default, each `Subscription` fetches messages in batches of 10. If the
server has fewer than 10 messages to send, it will wait up to 10 seconds
for new messages before returning the messages it does have. For low-latency
applications set the `batch` size to 1.

```python
sub = await conn.subscribe('mydataset', batch=1)
```

# Important Notes

## SSL/TLS Errors

SSL/TLS errors occur for 2 reasons
  1. Invalid or missing client certificates
  2. No certificate authority configured

### Providing Client Certificates

By default, speedracer uses PEM formatted X.509 certificates for user
authentication. By default speedracer will use certificates placed in
the users `$HOME/.ssh` directory. The certificate and key files should be named
`$HOME/.ssh/cert.crt` and `$HOME/.ssh/cert.key`, respectively.

To specify a different path, pass a tuple containing the path to the certificate
and key files to the `cert` argument.

```python
conn = Connection('https://mdb-account-server.com',
          cert=('./mycert.crt', './mycert.key'))
```

To create PEM formatted `.crt` and `.key` certificate files from a PKCS `.p12`
**signing_cert** file, run the following OpenSSL commands.

```
openssl pkcs12 -in INFILE.p12 -out OUTFILE.key -nodes -nocerts
openssl pkcs12 -in INFILE.p12 -out OUTFILE.crt -nokeys
```

### Providing a Certificate Authority (SSLCertVerificationError)

Certificate Authorities establish a chain of trust. This is usually configured globally
as part of the operating system. There are cases where the OS does not have the proper
certificate authority configured.

In these instances, users may specify a cabundle as a X.509 PEM file via the argument `ca_bundle`.

```python
conn = Connection('https://mdb-account-server.com', ca_bundle='ca.cer')
```

Download the appropiate CA Bundle.

| Autobahn Environment | Link to CA Bundle |
| --- | --- |
|||

## Subscription not starting at specified offset

Subscriptions to datasets are **durable**. This means that once you have subscribed to a
dataset, message delivery restarts where you left off--even if your program restarts.

To change where your subscription starts, use
<a href="#Connection.Subscription.seek">`seek`</a>.

Subscriptions will expire after 1-week if not used.
