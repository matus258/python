#!/usr/bin/python3

import iptc
import json

chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "DOCKER")
discovery = {}
data = []
for rule in chain.rules:
  for match in rule.matches:
    (packets, bytes) = rule.get_counters()
    data.append({"{#PORTA}":match.dport})
    #print(packets, bytes, match.name, match.dport)

discovery = {"data":data}
print(json.dumps(discovery, indent=2))

