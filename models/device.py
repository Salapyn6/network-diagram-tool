# -*- coding: utf-8 -*-
from enum import Enum
from dataclasses import dataclass

class DeviceType(Enum):
    """All supported network device types"""
    ROUTER = "router"
    SWITCH = "switch"
    FIREWALL = "firewall"
    ACCESS_POINT = "access_point"
    SERVER = "server"
    DESKTOP = "desktop"
    LAPTOP = "laptop"
    PRINTER = "printer"
    IP_CAMERA = "ip_camera"
    MODEM = "modem"
    UPS = "ups"
    NAS = "nas"
    LOAD_BALANCER = "load_balancer"
    GATEWAY = "gateway"
    PHONE = "phone"
    TABLET = "tablet"

DEVICE_COLORS = {
    DeviceType.ROUTER: "#FF6B6B",
    DeviceType.SWITCH: "#4ECDC4",
    DeviceType.FIREWALL: "#FFE66D",
    DeviceType.ACCESS_POINT: "#95E1D3",
    DeviceType.SERVER: "#C44569",
    DeviceType.DESKTOP: "#A8DADC",
    DeviceType.LAPTOP: "#F1FAEE",
    DeviceType.PRINTER: "#E8D1F0",
    DeviceType.IP_CAMERA: "#F4A460",
    DeviceType.MODEM: "#DDA0DD",
    DeviceType.UPS: "#F0E68C",
    DeviceType.NAS: "#CD5C5C",
    DeviceType.LOAD_BALANCER: "#20B2AA",
    DeviceType.GATEWAY: "#FF8C00",
    DeviceType.PHONE: "#98D8C8",
    DeviceType.TABLET: "#F7DC6F",
}

DEVICE_LABELS = {
    DeviceType.ROUTER: "Router",
    DeviceType.SWITCH: "Switch",
    DeviceType.FIREWALL: "Firewall",
    DeviceType.ACCESS_POINT: "Access Point",
    DeviceType.SERVER: "Server",
    DeviceType.DESKTOP: "Desktop PC",
    DeviceType.LAPTOP: "Laptop",
    DeviceType.PRINTER: "Printer",
    DeviceType.IP_CAMERA: "IP Camera",
    DeviceType.MODEM: "Modem",
    DeviceType.UPS: "UPS",
    DeviceType.NAS: "NAS",
    DeviceType.LOAD_BALANCER: "Load Balancer",
    DeviceType.GATEWAY: "Gateway",
    DeviceType.PHONE: "Phone",
    DeviceType.TABLET: "Tablet",
}

@dataclass
class Device:
    """Represents a network device on the diagram"""
    device_id: str
    device_type: DeviceType
    x: float
    y: float
    label: str = ""
    ip_address: str = ""
    mac_address: str = ""
    vlan: str = ""
    role: str = ""
    notes: str = ""
    
    def get_color(self) -> str:
        return DEVICE_COLORS.get(self.device_type, "#CCCCCC")
    
    def get_type_label(self) -> str:
        return DEVICE_LABELS.get(self.device_type, self.device_type.value)
    
    def to_dict(self):
        return {
            'device_id': self.device_id,
            'device_type': self.device_type.value,
            'x': self.x,
            'y': self.y,
            'label': self.label,
            'ip_address': self.ip_address,
            'mac_address': self.mac_address,
            'vlan': self.vlan,
            'role': self.role,
            'notes': self.notes,
        }
    
    @staticmethod
    def from_dict(data):
        data['device_type'] = DeviceType(data['device_type'])
        return Device(**data)
