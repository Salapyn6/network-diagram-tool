# -*- coding: utf-8 -*-
from enum import Enum
from dataclasses import dataclass

class LinkType(Enum):
    """Types of connections between devices"""
    ETHERNET = "ethernet"
    WIFI = "wifi"
    UPLINK = "uplink"
    TRUNK = "trunk"
    SERIAL = "serial"
    USB = "usb"
    FIBER = "fiber"

@dataclass
class Link:
    """Represents a connection between two devices"""
    link_id: str
    from_device_id: str
    to_device_id: str
    link_type: LinkType = LinkType.ETHERNET
    from_port: str = ""
    to_port: str = ""
    vlan: str = ""
    bandwidth: str = ""
    status: str = "active"
    notes: str = ""
    
    def to_dict(self):
        return {
            'link_id': self.link_id,
            'from_device_id': self.from_device_id,
            'to_device_id': self.to_device_id,
            'link_type': self.link_type.value,
            'from_port': self.from_port,
            'to_port': self.to_port,
            'vlan': self.vlan,
            'bandwidth': self.bandwidth,
            'status': self.status,
            'notes': self.notes,
        }
    
    @staticmethod
    def from_dict(data):
        data['link_type'] = LinkType(data['link_type'])
        return Link(**data)
