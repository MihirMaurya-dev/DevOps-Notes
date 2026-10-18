---
tags: [interview, networking, azure]
source: devopsinsiders/batch-18
created: 2026-06-08
level: intermediate
---

# 🎯 Networking Fundamentals: Interview Questions

These questions test your understanding of core networking concepts including the OSI model, TCP/IP, IP addressing, CIDR, subnetting, DNS, HTTP/HTTPS, TCP vs UDP, ports, NAT, routing, and VPN basics.

---

## Part 1: Basics

### Question 1: What is the OSI model?
**Question:** Explain what the OSI model is and why it is useful in networking.
<details>
<summary><b>Show Answer</b></summary>
<br>
The OSI model is a theoretical framework used to understand how networks operate. It breaks down network communication into 7 distinct layers (Physical, Data Link, Network, Transport, Session, Presentation, Application). It is useful for standardizing communication and troubleshooting network issues step-by-step.
</details>

### Question 2: What is an IP address?
**Question:** Define an IP address in simple terms.
<details>
<summary><b>Show Answer</b></summary>
<br>
An IP address is a unique numerical label assigned to every device connected to a computer network. It acts like a home address, allowing devices to find and communicate with each other over the network.
</details>

### Question 3: What is the difference between IPv4 and IPv6?
**Question:** Why do we have both IPv4 and IPv6, and what is the main difference?
<details>
<summary><b>Show Answer</b></summary>
<br>
IPv4 uses 32-bit addresses, meaning it can only support about 4.3 billion unique devices. Because we ran out of IPv4 addresses, IPv6 was created using 128-bit addresses, offering a practically limitless number of unique IP addresses.
</details>

### Question 4: What is DNS?
**Question:** Explain DNS (Domain Name System) as if you were talking to a beginner.
<details>
<summary><b>Show Answer</b></summary>
<br>
DNS is like the phonebook of the internet. Humans use domain names (like google.com) to visit websites, but computers use IP addresses. DNS translates the readable domain name into the IP address so your browser can load the webpage.
</details>

### Question 5: HTTP vs HTTPS
**Question:** What is the main difference between HTTP and HTTPS?
<details>
<summary><b>Show Answer</b></summary>
<br>
The main difference is security. HTTPS is the secure version of HTTP. It uses encryption (TLS/SSL) to scramble the data sent between the browser and the website, preventing hackers from reading sensitive information like passwords.
</details>

### Question 6: TCP vs UDP
**Question:** In simple terms, how do TCP and UDP differ?
<details>
<summary><b>Show Answer</b></summary>
<br>
TCP is reliable. It guarantees that data arrives in order without errors (like a certified mail delivery). UDP is fast but unreliable; it just throws data at the destination without checking if it arrived (like a live video or voice call where missing a split second is fine).
</details>

### Question 7: What are network ports?
**Question:** What is a port and why is it needed?
<details>
<summary><b>Show Answer</b></summary>
<br>
While an IP address directs traffic to a specific computer, a port directs traffic to a specific application or service on that computer. It's like the apartment number in a large building address.
</details>

### Question 8: What is NAT?
**Question:** What does NAT (Network Address Translation) do?
<details>
<summary><b>Show Answer</b></summary>
<br>
NAT allows multiple devices on a private network (like your home Wi-Fi) to share a single public IP address to access the internet. The router translates the private IPs of your devices into the one public IP when sending traffic out.
</details>

### Question 9: What is a Subnet Mask?
**Question:** What is the purpose of a subnet mask?
<details>
<summary><b>Show Answer</b></summary>
<br>
A subnet mask is used to divide an IP address into two parts: the network address (which network the device is on) and the host address (the specific device). It tells computers whether they can talk directly to another device or if they need to send traffic through a router.
</details>

### Question 10: What is a VPN?
**Question:** What is a VPN and what is its primary use?
<details>
<summary><b>Show Answer</b></summary>
<br>
A VPN (Virtual Private Network) creates a secure, encrypted tunnel over the public internet. It is primarily used to allow remote users to safely access private corporate networks and hide their internet activity.
</details>

---

## Part 2: Advanced

### Question 11: The TCP/IP Model
**Question:** How does the TCP/IP model differ from the 7-layer OSI model?
<details>
<summary><b>Show Answer</b></summary>
<br>
The TCP/IP model is a more practical, simplified version of the OSI model. It uses only 4 layers (Network Access, Internet, Transport, and Application). It condenses the top three OSI layers into one Application layer, and the bottom two OSI layers into the Network Access layer.
</details>

### Question 12: Understanding CIDR
**Question:** What is CIDR and what problem does it solve?
<details>
<summary><b>Show Answer</b></summary>
<br>
CIDR (Classless Inter-Domain Routing) is a method for allocating IP addresses and routing them efficiently. It replaces the old Class A, B, and C system, which wasted millions of IPs, by allowing flexible subnet sizes using a slash notation (like /24).
</details>

### Question 13: Private vs Public IPs
**Question:** What are Private IP ranges and why can't they access the internet directly?
<details>
<summary><b>Show Answer</b></summary>
<br>
Private IP addresses (like 10.x.x.x, 172.16.x.x, 192.168.x.x) are reserved for internal networks. Internet routers are configured to drop traffic from these addresses. To access the internet, Private IPs must be translated to a Public IP using NAT.
</details>

### Question 14: Default Gateway
**Question:** What is a default gateway and when does a device use it?
<details>
<summary><b>Show Answer</b></summary>
<br>
A default gateway is the router that connects your local network to other networks (like the internet). A device uses it whenever it wants to send data to an IP address that is not on its own local subnet.
</details>

### Question 15: Step-by-Step DNS
**Question:** What happens when you type a URL into your browser regarding DNS resolution?
<details>
<summary><b>Show Answer</b></summary>
<br>
First, the browser checks its local cache. If not found, it queries the OS cache, then the configured DNS resolver (like your ISP). The resolver queries the Root DNS servers, then the TLD (like .com) servers, and finally the Authoritative name server for that domain to get the IP address.
</details>

### Question 16: The 3-Way Handshake
**Question:** Explain the TCP 3-way handshake.
<details>
<summary><b>Show Answer</b></summary>
<br>
It is the process TCP uses to establish a connection. Step 1: The client sends a SYN (synchronize) packet. Step 2: The server responds with a SYN-ACK (synchronize-acknowledge). Step 3: The client replies with an ACK (acknowledge). The connection is now open.
</details>

### Question 17: Common Ports
**Question:** List the standard port numbers for HTTP, HTTPS, SSH, DNS, and RDP.
<details>
<summary><b>Show Answer</b></summary>
<br>
HTTP: 80<br>
HTTPS: 443<br>
SSH: 22<br>
DNS: 53<br>
RDP: 3389
</details>

### Question 18: SNAT vs DNAT
**Question:** What is the difference between Source NAT (SNAT) and Destination NAT (DNAT)?
<details>
<summary><b>Show Answer</b></summary>
<br>
SNAT changes the source IP address of outbound traffic (e.g., hiding private IPs behind one public IP). DNAT changes the destination IP address of inbound traffic (e.g., forwarding traffic from a public IP to a specific internal private server).
</details>

### Question 19: How Routing Works
**Question:** How does a router decide where to send a packet?
<details>
<summary><b>Show Answer</b></summary>
<br>
A router looks at the destination IP address of a packet and compares it against its routing table. It finds the longest prefix match (the most specific route) and forwards the packet out the corresponding interface.
</details>

### Question 20: Subnetting Math
**Question:** If you have a /24 subnet, how many IP addresses are in the network, and how many are usable by hosts (assuming standard networking, not Azure)?
<details>
<summary><b>Show Answer</b></summary>
<br>
A /24 subnet has 256 total IP addresses. In standard networking, 2 are reserved (the network address and the broadcast address), leaving 254 usable IPs for hosts.
</details>

---

## Part 3: Scenario-Based

### Question 21: The Missing Website
**Scenario:** A user says they can access `http://192.168.1.50` but they cannot access `http://mycompany.local`. 
**Question:** What is the most likely cause of this issue?
<details>
<summary><b>Show Answer</b></summary>
<br>
Since the application loads perfectly via IP address but fails with a hostname, this is purely a DNS issue. The user's computer cannot resolve the hostname `mycompany.local` to the IP `192.168.1.50`.
</details>

### Question 22: HTTPS Failure
**Scenario:** Users complain that when they go to your secure website, the browser displays a giant red warning saying "Your connection is not private."
**Question:** What networking or security component has failed?
<details>
<summary><b>Show Answer</b></summary>
<br>
The SSL/TLS certificate used for HTTPS has likely expired, is self-signed, or the domain name on the certificate doesn't match the website URL. The browser blocks it to protect the user.
</details>

### Question 23: The Fast but Flawed Transfer
**Scenario:** A developer built an app to transfer critical financial database records using UDP to make it as fast as possible. 
**Question:** Why is this a terrible design choice?
<details>
<summary><b>Show Answer</b></summary>
<br>
UDP is connectionless and does not guarantee delivery or packet order. Using UDP for critical financial data means packets could be dropped silently over the network, leading to corrupted or missing database records. They should use TCP.
</details>

### Question 24: Cloud VPN Needs
**Scenario:** Your company has an office in New York and an Azure cloud environment. You need servers in Azure to talk to on-premises servers securely over private IPs.
**Question:** How do you solve this using VPN basics?
<details>
<summary><b>Show Answer</b></summary>
<br>
You would deploy a Site-to-Site VPN. An Azure VPN Gateway would connect securely over the public internet to the VPN appliance in the New York office, encrypting traffic and routing the private subnets between the two locations.
</details>

### Question 25: Unreachable Database
**Scenario:** A Web server (10.0.1.5) and a DB server (10.0.2.5) are on different subnets. The Web server cannot ping the DB server, but it can ping other web servers.
**Question:** What is missing?
<details>
<summary><b>Show Answer</b></summary>
<br>
Because they are on different subnets, a router is required to pass traffic between them. Either the router is missing, the routing tables are incorrect, or a firewall rule (like an NSG in Azure) is blocking the traffic between the subnets.
</details>

### Question 26: Port Forwarding
**Scenario:** You are hosting a Minecraft server on a computer in your home (Private IP: 192.168.1.100). Your friends on the internet cannot connect to your home's Public IP.
**Question:** What NAT concept must you configure on your home router?
<details>
<summary><b>Show Answer</b></summary>
<br>
You must configure Port Forwarding (a form of DNAT). You tell your home router to take any traffic hitting its public IP on the specific Minecraft port (default 25565) and forward it directly to 192.168.1.100.
</details>

### Question 27: Layer 7 Firewall Inspection
**Scenario:** A company installs a Next-Generation Firewall. It blocks a user from accessing Facebook, even though the user is allowed to use standard HTTPS (port 443).
**Question:** How does the firewall know the traffic is going to Facebook?
<details>
<summary><b>Show Answer</b></summary>
<br>
The firewall is operating at Layer 7 (Application Layer) of the OSI model. Instead of just looking at IPs and ports, it inspects the actual application data and domain names (via SNI or packet inspection) to determine what service the user is trying to access.
</details>

### Question 28: CIDR Overlap Disaster
**Scenario:** You have a local data center using the network `10.0.0.0/16`. You create a new cloud network using `10.0.0.0/24` and connect them with a VPN. Nobody can communicate across the VPN.
**Question:** Why did this fail?
<details>
<summary><b>Show Answer</b></summary>
<br>
This failed due to IP Address Overlap. The cloud network (`10.0.0.0/24`) is completely contained inside the local data center's network (`10.0.0.0/16`). Routers get confused because the destination IP ranges exist on both sides of the VPN, causing traffic to drop or loop.
</details>
