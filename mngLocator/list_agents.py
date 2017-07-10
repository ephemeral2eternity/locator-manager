from azure.common.credentials import UserPassCredentials
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
# from azure.mgmt.compute import ComputeManagementClient, ComputeManagementClientConfiguration
from azure.mgmt.network import NetworkManagementClient
# from azure.mgmt.network import NetworkManagementClient, NetworkManagementClientConfiguration
import json
import os
import pprint
import boto.ec2

def azure_list_agents(rg_name, prefix):
    info_dict = json.load(open(os.path.dirname(__file__) + "/azure_info.json"))
    location_dict = json.load(open(os.path.dirname(__file__) + "/azure_locations.json"))
    # info_dict = json.load(open(os.getcwd() + "/info.json"))
    # location_dict = json.load(open(os.getcwd() + "/azure_locations.json"))
    subscription_id = info_dict["subscription_id"]
    # TODO: See above how to get a Credentials instance

    '''
    credentials = UserPassCredentials(
        info_dict["user"],    # Your new user
        info_dict["password"],  # Your password, Woku5113
    )'''

    credentials = ServicePrincipalCredentials(
        client_id=info_dict["client_id"],
        secret=info_dict["secret"],
        tenant=info_dict["tenant"]
    )

    #compute_client = ComputeManagementClient(ComputeManagementClientConfiguration(
    #        credentials,
    #        subscription_id
    #    )
    #)

    compute_client = ComputeManagementClient(credentials, subscription_id)

    #network_client = NetworkManagementClient(NetworkManagementClientConfiguration(
    #        credentials,
    #        subscription_id
    #    )
    #)

    network_client = NetworkManagementClient(credentials, subscription_id)

    locators = []

    vms = compute_client.virtual_machines.list(rg_name)
    for vm in vms:
        vm_name = vm.name
        print(vm_name)
        if prefix in vm_name:
            try:
                 vm_ip = network_client.public_ip_addresses.get(rg_name, vm_name + "-ip").ip_address
            except:
                 vm_ip = network_client.public_ip_addresses.get(rg_name, vm_name).ip_address
            vm_location = vm.location
            vm_coordinates = location_dict[vm_location]
            # print vm_name, vm_ip, vm_location
            cur_locator = {"name" : vm_name, "ip" : vm_ip, "location" : vm_location,
                           "latitude" : vm_coordinates["latitude"], "longitude" : vm_coordinates["longitude"]}
            locators.append(cur_locator)


    return locators


def aws_list_agents():
    info_dict = json.load(open(os.path.dirname(__file__) + "/aws_info.json"))
    agents = json.load(open(os.path.dirname(__file__) + "/aws_cloud_agents.json"))

    agent_ips = []
    for agent in agents:
        conn = boto.ec2.connect_to_region(agent["location"])
        reservations = conn.get_all_instances(instance_ids=[agent["id"]])
        vm = reservations[0].instances[0]
        agent["ip"] = vm.ip_address
        agent["type"] = vm.instance_type
        agent["name"] = vm.tags["Name"]

        agent_ips.append(agent)

    return agent_ips



if __name__ == '__main__':
    # locators = azure_list_agents("agens", "locator-")
    # caches = azure_list_agents("QRank", "cache-")
    # print(caches)
    locators = aws_list_agents()
    print(locators)