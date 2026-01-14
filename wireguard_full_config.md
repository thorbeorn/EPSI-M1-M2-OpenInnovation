```conf
[Interface]
PrivateKey = <server-private-key>
Address = 10.0.0.1/24
SaveConfig = true

[Peer]
PublicKey = <client-public-key>
PresharedKey = <preshared-key>
AllowedIPs = 10.0.0.2/32
Endpoint = vpn.example.com:51820
PersistentKeepalive = 3600
```