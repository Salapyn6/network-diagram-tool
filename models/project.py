# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from .device import Device
from .link import Link

@dataclass
class Project:
    """Represents a complete network diagram project"""
    name: str
    description: str = ""
    devices: List[Device] = field(default_factory=list)
    links: List[Link] = field(default_factory=list)
    created_at: str = ""
    modified_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.modified_at:
            self.modified_at = datetime.now().isoformat()
    
    def add_device(self, device: Device):
        self.devices.append(device)
        self.modified_at = datetime.now().isoformat()
    
    def remove_device(self, device_id: str):
        self.devices = [d for d in self.devices if d.device_id != device_id]
        self.links = [l for l in self.links 
                      if l.from_device_id != device_id and l.to_device_id != device_id]
        self.modified_at = datetime.now().isoformat()
    
    def add_link(self, link: Link):
        self.links.append(link)
        self.modified_at = datetime.now().isoformat()
    
    def remove_link(self, link_id: str):
        self.links = [l for l in self.links if l.link_id != link_id]
        self.modified_at = datetime.now().isoformat()
    
    def get_device(self, device_id: str):
        for device in self.devices:
            if device.device_id == device_id:
                return device
        return None
    
    def get_link(self, link_id: str):
        for link in self.links:
            if link.link_id == link_id:
                return link
        return None
    
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'devices': [d.to_dict() for d in self.devices],
            'links': [l.to_dict() for l in self.links],
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }
    
    @staticmethod
    def from_dict(data):
        project = Project(
            name=data['name'],
            description=data.get('description', ''),
            created_at=data.get('created_at', ''),
            modified_at=data.get('modified_at', ''),
        )
        project.devices = [Device.from_dict(d) for d in data.get('devices', [])]
        project.links = [Link.from_dict(l) for l in data.get('links', [])]
        return project
