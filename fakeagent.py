#!/usr/bin/python
# Copyright (c) 2014 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import yaml

# debug = False
debug = True
def debug_print(*args):
    if debug == True:
        print("FPGAENT:" + "".join(map(str, args)))
# List available fpga devices
def fpga_device_list():
    #with open("device.yml") as ymlfile:
    with open("fpgainfo.yml") as ymlfile:
        cfg = yaml.load(ymlfile)
    devlist = {}
    for section in cfg:
        devlist[section] = {}
        devlist[section]["name"] = cfg[section]["name"]
        devlist[section]["path"] = cfg[section]["path"]
        devlist[section]["id"] = cfg[section]["id"]
    return devlist

# Given the fpga device, show detailed info
def fpga_device_info(devicename):
    with open("fpgainfo.yml") as ymlfile:
        cfg = yaml.load(ymlfile)
    devinfo = {}
    for section in cfg:
        if section == devicename:
            debug_print(devicename)
            devinfo = cfg[section]
            break
    return devinfo

# List the supported Accelerator types
def fpga_acc_list(fpgatype):
    with open(fpgatype+"acclist.yml") as ymlfile:
        cfg = yaml.load(ymlfile)
    acclist = []
    for acc in cfg:
        acclist.append(acc)
    return acclist

def _get_idle_slot_with_acc(device, acctype):
    for s in device["slots"]:
        slot = device["slots"][s]
        if slot["status"] == "idle" and slot["acc_type"] == acctype:
            return slot
    return None

def _get_free_slot(device):
    for s in device["slots"]:
        slot = device["slots"][s]
        if slot["status"] == "empty":
            return slot
    return None

# Program fpga slot with specific accelerator type
def fpga_program(device, slot, acc_type):
    slot["acc_type"] = acc_type
    slot["vfpath"] = device + device[id] + "fakedVFpathslot" + slot[slotid]
    slot["status"] = "idle"
    return

def fpga_acc_free(device, slot):
    if slot["status"] == "inuse":
        slot["status"] = "idle"
    return

def fpga_erase(device, slot):
    slot["status"] = "empty"
    return

def _save_status(cfg):
    ymlfile = open("fpgainfo.yml", 'w')
    yaml.dump(cfg, ymlfile, default_flow_style=False, default_style='')
    return

# Allocate one slot with acctype and return the slot struct
def fpga_acc_alloc(acctype):
    # 1). find idle with the acctype
    # 2). program empty if not found
    with open("fpgainfo.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    d = {}
    for device in cfg:
        d = cfg[device]
        slot = _get_idle_slot_with_acc(d, acctype)
        if slot != None:
            slot["status"] = "inuse"
            _save_status(cfg)
            return slot
    for device in cfg:
        d = cfg[device]
        slot = _get_free_slot(d)
        if slot != None:
            fpga_program(device, slot, acctype)
            print slot
            slot["status"] = "inuse"
            _save_status(cfg)
            return slot
    return None
def fpga_free_all():
    ymlfile = open("fpgainfo.yml", 'r')
    cfg = yaml.load(ymlfile)
    d = {}
    for device in cfg:
        d = cfg[device]
        for slot in d[slots]:
            if d[slots][slot][status] == "inuse":
                fpga_acc_free(d, d[slots][slot])
    _save_status(cfg)
    return
def fpga_erase_all():
    ymlfile = open("fpgainfo.yml", 'r')
    cfg = yaml.load(ymlfile)
    d = {}
    for device in cfg:
        d = cfg[device]
        for slot in d[slots]:
            if d[slots][slot][status] == "idle":
                fpga_erase(d, d[slots][slot])
    _save_status(cfg)
    return

def main():
    dev = fpga_device_list()
    print yaml.dump(dev, default_flow_style=False, default_style='')
    di = fpga_device_info("device2")
    print yaml.dump(di, default_flow_style=False, default_style='')
    acclist = fpga_acc_list("intel-mcp")
    print acclist
    #slot = fpga_acc_alloc("intel-mcp-echo")

if __name__ == "__main__":
    main()
