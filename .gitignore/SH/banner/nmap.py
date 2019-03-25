from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
import json

def  report_parser(NameFile):
    report = NmapParser.parse_fromfile(NameFile)

    BD_Nmap = []

    for host in report.hosts:
        ip = host.address
        if host.is_up():
            hostname = 'N/A'
            if len(host.hostnames) != 0:
                hostname = host.hostnames[0]
            IpChild = {'IP':'',
            'hostname':'',
            'services': []
            }
            IpChild['IP'] = ip
            IpChild['hostname'] = hostname
            servises = []
            for s in host.services:
                if s.open():
                    ServChild = {'port': 0,
                    'service': '',
                    'ban': ''
                    }                 
                    ServChild['port'] = s.port
                    ServChild['service'] = s.service
                    ServChild['ban'] = s.banner
                    servises.append(ServChild)
            IpChild['services'] = servises
            BD_Nmap.append(IpChild)
    return BD_Nmap
