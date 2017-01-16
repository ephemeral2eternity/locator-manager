import requests
import json

def get_ipinfo(ip):
    rsp = requests.get("http://ipinfo.io/" + ip)
    node_info = json.loads(rsp.text)

    if 'org' in node_info.keys():
        node_org = node_info['org']
        node_org_items = node_org.split()
        node_info['AS'] = int(node_org_items[0][2:])
        node_info['ISP'] = " ".join(node_org_items[1:])
    else:
        node_info['AS'] = -1
        node_info['ISP'] = "unknown"

    if 'loc' in node_info.keys():
        locations = node_info['loc'].split(',')
        node_info['latitude'] = float(locations[0])
        node_info['longitude'] = float(locations[1])
    else:
        node_info['latitude'] = 0.0
        node_info['longitude'] = 0.0

    if ('city' not in node_info.keys()):
        node_info['city'] = ''

    if ('region' not in node_info.keys()):
        node_info['region'] = ''

    if ('country' not in node_info.keys()):
        node_info['country'] = ''

    if ('hostname' not in node_info.keys()):
        node_info['hostname'] = ip
    elif ('No' in node_info['hostname']):
        node_info['hostname'] = ip

    node_info['name'] = node_info['hostname']

    return node_info