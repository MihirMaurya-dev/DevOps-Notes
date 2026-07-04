---
tags: [networking, architecture, hub-spoke, fundamentals]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🎡 Hub and Spoke Architecture Theory

> "Hub and Spoke is the ultimate networking design for the cloud. It is the digital equivalent of an airport terminal."

---

## 📖 Before You Read
Before you dive into Hub and Spoke, make sure you understand:
- What a **Virtual Network (VNet)** is — see [[VNet]]
- How **VNet Peering** connects networks together.

---

## 🤔 What is it?

The **Hub and Spoke** network topology is the absolute gold standard for building enterprise environments in the cloud. Almost every Landing Zone uses it.

> 🚲 **Real-World Analogy:**
> Look at the wheel of a bicycle. 
> In the exact center is the central metal ring (**The Hub**). 
> Radiating outward from the center are the metal rods (**The Spokes**).
> 
> In Azure:
> - **The Hub** is a central Virtual Network (VNet). It acts as the grand central station for all network traffic.
> - **The Spokes** are multiple other VNets. They represent your different applications (e.g., HR App VNet, Finance App VNet). Every Spoke is connected directly to the Hub via a digital cable called *VNet Peering*.

---

## 🧠 Why do we need it?

If a company has 50 different applications, and each application needs a Firewall ($1000/month) and a VPN connection to the physical office ($200/month), the company would go bankrupt buying 50 firewalls!

**The Hub and Spoke solution saves massive amounts of money:**
1. **Centralized Costs:** You buy exactly ONE massive Firewall and ONE VPN Gateway. You put them in the central Hub VNet.
2. **Shared Services:** You connect all 50 Application Spokes to the Hub. Because they are connected, all 50 apps can share that single Firewall and single VPN!

It also improves **Security**. Because all traffic must flow through the central Hub to get to the internet or back to the office, the security team only has to monitor one massive chokepoint.

---

## ⚙️ How does it work? (The Transitivity Trap)

Connecting the Spokes to the Hub is easy. But there is a massive networking "gotcha" you must understand: **Transitivity.**

**VNet Peering is NOT transitive by default.**
- If Spoke A (HR App) connects to the Hub.
- And Spoke B (Finance App) connects to the Hub.
- **Spoke A CANNOT talk directly to Spoke B.** Azure drops the traffic! The Hub does not act as an automatic bridge.

**How to fix it:**
If you actually want the HR App to talk to the Finance App, you must:
1. Place a network router (usually an **Azure Firewall**) inside the Hub VNet.
2. Create a **Route Table (UDR)** in Spoke A that says: "To reach Spoke B, send the traffic to the Firewall's IP Address." (And do the same in Spoke B).
3. The Firewall will receive the traffic, inspect it for viruses, and then forward it to Spoke B!

---

## 💡 Real Example (The Landing Zone Network)

When you deploy a Landing Zone, the networking team builds the following:

- **Hub VNet (`10.0.0.0/16`)**: Contains the Azure Firewall, the VPN back to the London office, and the central Custom DNS servers.
- **Prod Spoke VNet (`10.1.0.0/16`)**: Contains the Virtual Machines for the Production website. It is peered to the Hub.
- **Dev Spoke VNet (`10.2.0.0/16`)**: Contains the Virtual Machines for the Development testing website. It is peered to the Hub.

If a developer in the London office wants to test their code, their laptop sends traffic through the VPN into the Hub. The Hub Firewall checks their identity, and then safely routes their traffic down into the Dev Spoke VNet!

---

## ⚠️ Common Mistakes Beginners Make

1. **Creating a Full Mesh:** Beginners often try to connect Spoke A directly to Spoke B, and Spoke B directly to Spoke C (A Full Mesh network). This is a nightmare to manage. If you have 50 VNets, you would need 1,225 peering connections! Always route traffic through the Hub instead.
2. **Overlapping IP Addresses:** If Spoke A uses `10.1.0.0/16` and Spoke B uses `10.1.0.0/16`, you cannot connect them to the Hub. Azure will block the peering because the IP addresses overlap and the Firewall wouldn't know which VNet to send the traffic to.

---

## 🎯 Key Takeaway
The Hub and Spoke topology centralizes expensive security and connectivity resources (like Firewalls and VPNs) into a single Hub VNet, allowing dozens of isolated Spoke VNets to share them securely.

---

## ❓ Beginner FAQ

**Q1: What is "Azure Virtual WAN"?**
> Azure Virtual WAN (vWAN) is Microsoft's "Hub and Spoke as a Service." Instead of you manually building the Hub VNet and configuring the complex Firewall routing tables yourself, Microsoft builds a massive managed Hub for you and handles all the routing automatically!

**Q2: Can I have more than one Hub?**
> Yes! Massive global companies usually have one Hub per geographical region (e.g., an East US Hub and a West Europe Hub). All the European Spokes connect to the Europe Hub, and the US Spokes connect to the US Hub. Then, you connect the two Hubs together!
