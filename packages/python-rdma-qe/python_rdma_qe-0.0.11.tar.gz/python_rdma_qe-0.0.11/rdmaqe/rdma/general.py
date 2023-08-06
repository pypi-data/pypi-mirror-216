#!/usr/bin/env python

"""roce.py: Module to check or configure RDMA. """

__author__ = "Zhaojuan Guo"
__copyright__ = "Copyright (c) 2023 Red Hat, Inc. All rights reserved."

import os
import json
import re
from libsan.host.cmdline import run

RDMA_BASE = '/sys/class/infiniband'
DEV_INFO_JSON = "/tmp/devinfo.json"


class HCA:
    def __init__(self, hca_id):
        self.hca_id = hca_id
        if ibv_devinfo_2_json(dev=hca_id) == 0:
            self.devinfo_json = DEV_INFO_JSON
        else:
            print("Error: Generating to json file failed.")
            return 1

    def get_port_num(self):
        """
        @return: how many physical ports?
        """
        with open(DEV_INFO_JSON, "r") as info:
            return json.load(info)[self.hca_id]["phys_port_cnt"]

    def get_state(self, port):
        with open(DEV_INFO_JSON, "r") as info:
            return json.load(info)[self.hca_id][port]["state"]

    def get_transport(self):
        with open(DEV_INFO_JSON, "r") as info:
            return json.load(info)[self.hca_id]["transport"]

    def get_link_layer(self, port):
        with open(DEV_INFO_JSON, "r") as info:
            return json.load(info)[self.hca_id][port]["link_layer"]

    def get_protocol(self, port=1):
        """
        @param port: port number, the default is 1.
        @return: the protocol of the specified port, it is iWARP, RoCE or InfiniBand.
        """
        transport = self.get_transport()
        link_layer = self.get_link_layer(port)
        if re.search("iWARP", transport, re.I) and re.search("Ethernet", link_layer, re.I):
            protocol = "iWARP"
        elif re.search("InfiniBand", transport, re.I) and re.search("Ethernet", link_layer, re.I):
            protocol = "RoCE"
        elif re.search("InfiniBand", transport, re.I) and re.search("InfiniBand", link_layer, re.I):
            protocol = "InfiniBand"

        return protocol


def is_rdma_device() -> bool:
    """
    Check if it contains RDMA devices
    @return: True if yes; False if no
    """
    return os.path.exists(RDMA_BASE)


def is_opa_device() -> bool:
    """
    Check if it contains OPA device
    :return:
    True: if yes
    False: if no
    """
    if is_rdma_device():
        for _ in os.listdir("/sys/class/infiniband"):
            if "hfi" in _:
                return True
            else:
                continue

    return False


def get_ibdev():
    # return: ['mlx5_1', 'mlx5_0']
    _ibdev = []
    for dev in os.listdir(RDMA_BASE):
        _ibdev.append(dev)

    return _ibdev


def get_netdev(dev):
    """
    :param dev: ibdev, like mlx5_0
    :return: netdev list, like ['mlx5_roce']
    """
    if not dev:
        return None
    _netdev = []
    _dir = '/sys/class/infiniband/{}/device/net/'.format(dev)
    for dev in os.listdir(_dir):
        _netdev.append(dev)

    return _netdev


def ibv_devinfo_2_json(dev=None, port=None):
    """
    Convert the output of utility ibv_devinfo to json
    @param dev: hca_id, like mlx5_0
    @param port: the port number, 1 is the first port
    @return:
    """
    if dev is not None and port is not None:
        _cmd = "ibv_devinfo -d " + dev + " -i " + port
    elif dev is None and port is not None:
        _cmd = "ibv_devinfo -i " + port
    elif dev is not None and port is None:
        _cmd = "ibv_devinfo -d " + dev
    else:
        _cmd = "ibv_devinfo"

    retcode, devinfo = run(_cmd, return_output=True)
    if retcode == 0:
        data = {}
        pre_hca_id_list = []
        current_hca_id = None
        current_port = None

        for line in devinfo.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('hca_id:'):
                current_hca_id = line.split('hca_id:')[1].strip()
                data[current_hca_id] = {}
            elif line.startswith('port:'):
                current_port = line.split('port:')[1].strip()
                data[current_hca_id][current_port] = {}
            else:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if current_hca_id not in pre_hca_id_list:
                    current_port = None
                    pre_hca_id_list.append(current_hca_id)
                if current_port is None:
                    data[current_hca_id][key] = value.strip()
                else:
                    data[current_hca_id][current_port][key] = value.strip()

        with open(DEV_INFO_JSON, 'w') as f:
            json.dump(data, f, indent=4)

    return retcode


def create_bond(con_name=None, ifname=None, options=None, **kwargs):
    """
    Create network bond
    @param con_name: connection name
    @param ifname: interface name
    @param options: bond options, like options="mode=active-backup,miimon=1000"
    @param kwargs: interfaces that will be attached to the bonding device
    @return: True if creating bond succeeded.
    """
    if con_name is None:
        con_name = "bond0"
    if ifname is None:
        ifname = "bond0"
    _cmd = f'nmcli connection add type bond con-name {con_name} ifname {ifname}'
    if options is not None:
        _cmd = _cmd + f' bond.options {options}'
    if run(_cmd) != 0:
        return False
    # add slave
    for i in kwargs.values():
        _cmd = f"ifenslave {ifname} {i}"
        if run(_cmd) != 0:
            return False
    _cmd = f"nmcli connection up {con_name}"
    if run(_cmd) != 0:
        return False
    return True


def delete_connection(con_name):
    """
    Delete NetworkManager connection using nmcli
    @param con_name: conncetion name
    @return: True if deleting connection succeeds
    """
    _cmd = "nmcli connection delete %s" % con_name
    retcode, output = run(_cmd, return_output=True, verbose=False)
    if retcode != 0:
        print("FAIL: Unable to delete the conn %s" % con_name)
        return False
    print(output)
    return True
