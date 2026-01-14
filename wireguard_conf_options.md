# Wireguard Configuration File Format
WireGuard uses simple text files for configuration, utilizing key-value pairs organized under specific sections. The two primary sections are [Interface] and [Peer]. The configuration is minimalistic yet powerful, allowing for straightforward setup and management.

General Structure of the Configuration File
The configuration file is divided into sections, each beginning with a header enclosed in square brackets, such as [Interface] or [Peer]. Under each section, configuration options are specified as Key = Value pairs.

## Example Structure:
```conf
[Interface]
# Interface-specific options

[Peer]
# Peer-specific options
```

# [Interface] Section Options
This section defines settings for the local WireGuard interface, including network configurations and cryptographic keys.

## Options:

- PrivateKey (required):
Description: The private key of the local interface, encoded in base64. This key must remain secret.
Purpose: Essential for establishing encrypted communication. Must be kept confidential.
Generation: Can be generated using wg genkey.
Usage: This key is specific to the local machine and should not be shared.
Example:
```conf
PrivateKey = 6vAaW2V5EnpNi5AqfZ57EKbQq8+OXPxJ1qpAh+yOcQw=
```

- Address (required):
Description: IP address(es) assigned to the interface. Supports both IPv4 and IPv6, and multiple addresses can be specified, separated by commas.
Purpose: Assigns IP addresses to the interface. These are the IPs that will be used within the VPN.
Multiple Addresses: Supports multiple addresses for dual-stack IPv4/IPv6 setups.
Example:
```conf
Address = 10.0.0.2/24, fd86:ea04:1115::1/64
```

- ListenPort (optional):
Description: The port on which the interface will listen for incoming WireGuard traffic. This is typically specified on servers.
Purpose: Defines the port for incoming WireGuard traffic.
Default Behavior: If not specified, WireGuard selects a random port.
Firewall Considerations: Ensure this port is allowed through any firewalls.
Example:
```conf
ListenPort = 51820
```

- DNS (optional):
Description: Specifies DNS server(s) to be used while the interface is up. Multiple DNS servers are separated by commas.
Purpose: Sets DNS servers for name resolution while the interface is active.
Client Configuration: Particularly useful for clients to resolve domain names over the VPN.
Example:
```conf
DNS = 1.1.1.1, 8.8.8.8
```

- MTU (optional):
Description: Sets the Maximum Transmission Unit (MTU) for the interface. If not specified, WireGuard attempts to calculate an appropriate MTU.
Purpose: Optimizes packet size to prevent fragmentation.
Default Behavior: WireGuard auto-detects MTU, but manual setting can improve performance in some cases.
Example:
```conf
MTU = 1420
```

- Table (optional):
Description: Controls whether WireGuard modifies the system's routing table. Setting off prevents automatic route configuration.
Purpose: Controls route table modifications.
Options:
Auto (default): WireGuard adds routes based on AllowedIPs.
off: Disables automatic route configuration.
Custom Table Number: Specify a table number for advanced routing.
Example:
```conf
Table = off
```

- PreUp, PostUp, PreDown, PostDown (optional):
Description: Commands or scripts to execute before or after the interface is brought up or down. Useful for custom firewall rules or logging.
Purpose: Automate tasks like configuring firewall rules or logging.
Placeholders: %i can be used as a placeholder for the interface name.
Example:
```conf
PostUp = iptables -A FORWARD -i %i -j ACCEPT
PostDown = iptables -D FORWARD -i %i -j ACCEPT
```

- SaveConfig (optional):
Description: If set to true, the current configuration is saved on shutdown. This can overwrite the configuration file.
Purpose: Automatically saves runtime configuration to the config file on shutdown.
Caution: Can overwrite manual changes to the configuration file.
Example:
```conf
SaveConfig = true
```

# [Peer] Section Options
This section defines configuration for remote peers (other WireGuard interfaces you are connecting to). Multiple [Peer] sections can be included to define multiple peers.

## Options:

- PublicKey (required):
Description: The public key of the remote peer, encoded in base64. Used for encrypting traffic to that peer.
Purpose: Identifies the remote peer and encrypts data sent to it.
Obtaining the Key: Should be securely shared by the remote peer.
Example:
```conf
PublicKey = Ae4TbZPdsXPUrbIjkItC3aJ7bDtx4OCDfz7eS5Nh9ho=
```

- PresharedKey (optional):
Description: An additional layer of symmetric encryption using a pre-shared key. Must be the same on both peers.
Purpose: Adds an extra layer of symmetric encryption.
Generation: Can be generated using wg genpsk.
Usage: Must be shared securely and set identically on both peers.
Example:
```conf
PresharedKey = 6vqAaV2V5EnpNi5AqfZ57EKbQq8+OXRa5gAh+yOcRw=
````

- AllowedIPs (required):
Description: Specifies which IP addresses are allowed through this peer. Acts as a routing table and access control list.
Purpose: Acts as both a routing rule and an access control mechanism.
Common Configurations:
Full Tunnel: 0.0.0.0/0, ::/0 routes all traffic through the VPN.
Split Tunnel: Specify only the subnets that should be routed through the VPN.
Example:
```conf
AllowedIPs = 0.0.0.0/0, ::/0
```

- Endpoint (optional):
Description: The hostname or IP address and port of the remote peer. Required for peers that are not initiating connections.
Purpose: Specifies where to send encrypted packets.
Dynamic IPs: If the remote peer has a dynamic IP, consider using a dynamic DNS service.
Example:
```conf
Endpoint = vpn.example.com:51820
```

- PersistentKeepalive (optional):
Description: Sends keepalive packets at the specified interval (in seconds) to maintain NAT mappings. Useful for peers behind NAT.
Purpose: Maintains NAT mappings on routers/firewalls that may drop idle connections.
Recommended Value: 25 seconds is commonly used.
Example:
```conf
PersistentKeepalive = 25
```

# Generating Keys and Configuration Steps
Generating a Private and Public Key Pair
Use the following commands to generate a key pair:

## Generate a private key
```bash
wg genkey > privatekey
```

## Generate a public key from the private key
```bash
wg pubkey < privatekey > publickey
```

## Generating a Pre-shared Key
```bash
wg genpsk > presharedkey
```

# Sample Configuration for a Client
```conf
[Interface]
PrivateKey = <client-private-key>
Address = 10.0.0.2/32
DNS = 1.1.1.1

[Peer]
PublicKey = <server-public-key>
PresharedKey = <preshared-key>
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = your.server.com:51820
PersistentKeepalive = 25
```

# Sample Configuration for a Server
```conf
[Interface]
PrivateKey = <server-private-key>
Address = 10.0.0.1/24
ListenPort = 51820

[Peer]
PublicKey = <client-public-key>
PresharedKey = <preshared-key>
AllowedIPs = 10.0.0.2/32
```

# Explanation of PresharedKey

PresharedKey in WireGuard is an optional parameter that adds an extra layer of symmetric encryption to the already secure WireGuard connection. Both peers must have the same PresharedKey configured for it to be effective.

Security Enhancement: Increases resistance against certain types of cryptographic attacks.
Usage Scenario: Recommended when maximum security is desired.
Generation: Use wg genpsk to generate a new pre-shared key.

## Example Usage:
```conf
[Peer]
PublicKey = <peer-public-key>
PresharedKey = <base64-encoded-preshared-key>
AllowedIPs = 10.0.0.0/24
Endpoint = vpn.example.com:51820
```

# Conclusion
For more information and updates, please refer to the official WireGuard Documentation.