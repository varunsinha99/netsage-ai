#!/usr/bin/env python3
"""Deterministic network checks for the NetSage AI project.
The checker is intentionally independent of an AI model.
"""
from ipaddress import ip_address, ip_network

def check_network(data):
    findings=[]
    # 1. Duplicate IP addresses across interfaces.
    seen={}
    for iface in data.get("interfaces",[]):
        ip=iface.get("ip")
        if ip:
            if ip in seen: findings.append(f"DUPLICATE_IP: {ip} on {seen[ip]} and {iface['name']}")
            else: seen[ip]=iface['name']
    # 2. Mismatched masks within each VLAN.
    for vlan, members in data.get("vlan_hosts",{}).items():
        masks={m.get("mask") for m in members}
        if len(masks)>1: findings.append(f"MASK_MISMATCH: VLAN {vlan} has masks {sorted(masks)}")
    # 3. Gateway mismatch.
    svi=data.get("vlan_gateways",{})
    for host in data.get("hosts",[]):
        expected=svi.get(str(host.get("vlan")))
        if expected and host.get("gateway") != expected:
            findings.append(f"GATEWAY_MISMATCH: {host['name']} uses {host.get('gateway')}; expected {expected}")
    # 4. Interface not up/up.
    for iface in data.get("interfaces",[]):
        if iface.get("status") != "up" or iface.get("protocol") != "up":
            findings.append(f"INTERFACE_DOWN: {iface['name']} is {iface.get('status')}/{iface.get('protocol')}")
    # 5. Referenced VLAN absent from VLAN table.
    present={str(v) for v in data.get("vlan_table",[])}
    for iface in data.get("switch_ports",[]):
        vlan=str(iface.get("vlan"))
        if vlan not in present: findings.append(f"MISSING_VLAN: {iface['name']} references VLAN {vlan}")
    # 6. Destination network absent from routing table.
    routes=[ip_network(r, strict=False) for r in data.get("routes",[])]
    for dest in data.get("required_routes",[]):
        network=ip_network(dest, strict=False)
        if not any(network == r or network.subnet_of(r) for r in routes):
            findings.append(f"MISSING_ROUTE: {dest} is absent from the routing table")
    return findings

SAMPLE_DATA={
    "interfaces":[
        {"name":"Gi0/0","ip":"172.16.1.1","status":"up","protocol":"up"},
        {"name":"Gi0/1","ip":"172.16.1.1","status":"down","protocol":"down"},
    ],
    "vlan_hosts":{"10":[{"name":"PC1","mask":"255.255.255.0"},{"name":"PC2","mask":"255.255.0.0"}]},
    "vlan_gateways":{"10":"192.168.10.1"},
    "hosts":[{"name":"PC1","vlan":10,"gateway":"192.168.10.254"}],
    "vlan_table":[1,10,20],
    "switch_ports":[{"name":"Fa0/1","vlan":10},{"name":"Fa0/2","vlan":50}],
    "routes":["192.168.10.0/24","172.16.1.0/30"],
    "required_routes":["10.50.0.0/16"],
}

if __name__ == "__main__":
    for finding in check_network(SAMPLE_DATA):
        print(finding)
