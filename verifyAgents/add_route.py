from .models import Session, Node, Network, Hop, Subnetwork, Edge

def add(client_info, isVideoPath):
    server_info = client_info['server']
    src_ip = client_info['ip']
    dst_ip = server_info['ip']
    ## Add a new session
    try:
        session = Session.objects.get(src_ip=src_ip, dst_ip=dst_ip)
        session.isVideoSession = (session.isVideoSession or isVideoPath)
    except:
        session = Session(src_ip=src_ip, dst_ip=dst_ip, isVideoSession=isVideoPath)
    session.save()

    if isVideoPath:
        src_type = 'client'
        src_net_type = 'access'
        dst_type = 'server'
        dst_net_type = 'cloud'
    else:
        src_type = 'agent'
        dst_type = 'agent'
        src_net_type = 'access'
        dst_net_type = 'access'

    ## Add src and dst networks.
    try:
        src_net = Network.objects.get(ASNumber=client_info['AS'], latitude=client_info['latitude'], longitude=client_info['longitude'])
        src_net.isVideoPath = (isVideoPath or src_net.isVideoPath)
    except:
        src_net = Network(ASNumber=client_info['AS'], name=client_info['ISP'], type=src_net_type,
                          latitude=client_info['latitude'], longitude=client_info['longitude'],
                          city=client_info['city'], region=client_info['region'], country=client_info['country'], isVideoPath=isVideoPath)
    src_net.save()
    try:
        src_subnet = Subnetwork.objects.get(session=session, network=src_net)
    except:
        src_subnet = Subnetwork(session=session, network=src_net)
    src_subnet.save()

    try:
        dst_net = Network.objects.get(ASNumber=server_info['AS'], latitude=server_info['latitude'], longitude=server_info['longitude'])
        dst_net.isVideoPath = (isVideoPath or dst_net.isVideoPath)
    except:
        dst_net = Network(ASNumber=server_info['AS'], name=server_info['ISP'], type=dst_net_type,
                          latitude=server_info['latitude'], longitude=server_info['longitude'],
                          city=server_info['city'], region=server_info['region'], country=server_info['country'], isVideoPath=isVideoPath)
    dst_net.save()

    ## Add src and dst nodes
    try:
        src_node = Node.objects.get(ip=src_ip)
    except:
        src_node = Node(ip=src_ip, type=src_type, network_id=src_net.id, name=client_info['name'])
    src_node.save()

    try:
        dst_node = Node.objects.get(ip=dst_ip)
    except:
        dst_node = Node(ip=dst_ip, type=dst_type, network_id=dst_net.id, name=server_info['name'])
    dst_node.save()

    ## Add hops and their network
    hopID = 0
    try:
        preHop = Hop.objects.get(session=session, node=src_node, hopID=hopID)
    except:
        preHop = Hop(session=session, node=src_node, hopID=hopID)
    preHop.save()

    if src_node not in src_net.nodes.all():
        src_net.nodes.add(src_node)
        src_net.save()

    hasServer = False

    for i, node_info in enumerate(client_info['route']):
        node_ip = node_info['ip']
        hopID += 1
        if isVideoPath:
            if node_ip == src_ip:
                node_type = "client"
            elif node_ip == dst_ip:
                node_type = "server"
                hasServer = True
            else:
                node_type = "router"
        else:
            if (node_ip == src_ip) or (node_ip == dst_ip):
                node_type = "agent"
            else:
                node_type = "router"

        if node_info['AS'] == src_net.ASNumber:
            node_net_type = src_net.type
            node_net_id = src_net.id
        elif node_info['AS'] == dst_net.ASNumber:
            node_net_type = dst_net.type
            node_net_id = dst_net.id
        else:
            node_net_type = "transit"

        try:
            node_net = Network.objects.get(ASNumber=node_info['AS'], latitude=node_info['latitude'], longitude=node_info['longitude'])
            node_net.isVideoPath = (isVideoPath or node_net.isVideoPath)
        except:
            node_net = Network(ASNumber=node_info['AS'], name=node_info['ISP'], type=node_net_type,
                    latitude=node_info['latitude'], longitude=node_info['longitude'],
                    city=node_info['city'], region=node_info['region'], country=node_info['country'],
                    isVideoPath=isVideoPath)
        node_net.save()

        try:
            node_subnet = Subnetwork.objects.get(session=session, network=node_net)
        except:
            node_subnet = Subnetwork(session=session, network=node_net)
        node_subnet.save()
        node_net_id = node_net.id

        try:
            node = Node.objects.get(ip=node_ip)
        except:
            node = Node(ip=node_ip, type=node_type, network_id=node_net_id, name=node_info['name'])
        node.save()

        if (node not in node_net.nodes.all()):
            node_net.nodes.add(node)
            node_net.save()

        try:
            curHop = Hop.objects.get(session=session, hopID=hopID, node=node)
        except:
            curHop = Hop(session=session, hopID=hopID, node=node)
        curHop.save()

        #### Add Edge Information
        try:
            curEdge = Edge.objects.get(src=preHop.node, dst=curHop.node)
        except:
            curEdge = Edge(src=preHop.node, dst=curHop.node)
        curEdge.save()
        preHop = curHop

    if not hasServer:
        try:
            lastEdge = Edge.objects.get(src=preHop.node, dst=dst_node)
        except:
            lastEdge = Edge(src=preHop.node, dst=dst_node)
        lastEdge.save()