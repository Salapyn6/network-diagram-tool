# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QComboBox, QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from models.device import Device, DeviceType, DEVICE_LABELS
from models.link import Link, LinkType

class NewProjectDialog(QDialog):
    """Dialog to create a new project"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Project")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.project_name = ""
        self.description = ""
        
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout()
        
        title = QLabel("<b>New Network Diagram</b>")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addRow(title)
        
        self.name_input = QLineEdit()
        self.name_input.setText("My Network")
        self.name_input.selectAll()
        layout.addRow("Project Name:", self.name_input)
        
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        self.desc_input.setPlaceholderText("e.g., Main office network topology...")
        layout.addRow("Description:", self.desc_input)
        
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("✅ Create")
        btn_ok.setStyleSheet("""
            QPushButton {
                background-color: #4ECDC4;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("❌ Cancel")
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #CCCCCC;
                padding: 8px 16px;
                border-radius: 4px;
            }
        """)
        btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addRow(btn_layout)
        
        self.setLayout(layout)
    
    def accept(self):
        self.project_name = self.name_input.text().strip()
        self.description = self.desc_input.toPlainText().strip()
        
        if not self.project_name:
            QMessageBox.warning(self, "Error", "Project name cannot be empty")
            return
        
        super().accept()

class DevicePropertiesDialog(QDialog):
    """Dialog to edit device properties"""
    
    def __init__(self, parent=None, device=None):
        super().__init__(parent)
        self.device = device
        self.setWindowTitle(f"Edit {device.get_type_label()}")
        self.setModal(True)
        self.setMinimumWidth(450)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout()
        
        title = QLabel(f"<b>Device Properties: {self.device.get_type_label()}</b>")
        title.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addRow(title)
        
        self.label_input = QLineEdit()
        self.label_input.setText(self.device.label)
        self.label_input.setPlaceholderText("e.g., Core Router 1")
        layout.addRow("Label:", self.label_input)
        
        self.ip_input = QLineEdit()
        self.ip_input.setText(self.device.ip_address)
        self.ip_input.setPlaceholderText("192.168.1.1")
        layout.addRow("IP Address:", self.ip_input)
        
        self.mac_input = QLineEdit()
        self.mac_input.setText(self.device.mac_address)
        self.mac_input.setPlaceholderText("00:11:22:33:44:55")
        layout.addRow("MAC Address:", self.mac_input)
        
        self.vlan_input = QLineEdit()
        self.vlan_input.setText(self.device.vlan)
        self.vlan_input.setPlaceholderText("VLAN100, 1,10,20 or trunk")
        layout.addRow("VLAN(s):", self.vlan_input)
        
        self.role_input = QLineEdit()
        self.role_input.setText(self.device.role)
        self.role_input.setPlaceholderText("Core / Distribution / Access / User")
        layout.addRow("Role:", self.role_input)
        
        self.notes_input = QTextEdit()
        self.notes_input.setText(self.device.notes)
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setPlaceholderText("Any additional notes...")
        layout.addRow("Notes:", self.notes_input)
        
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("✅ OK")
        btn_ok.setStyleSheet("""
            QPushButton {
                background-color: #4ECDC4;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("❌ Cancel")
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #CCCCCC;
                padding: 6px 12px;
                border-radius: 4px;
            }
        """)
        btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addRow(btn_layout)
        
        self.setLayout(layout)
    
    def accept(self):
        self.device.label = self.label_input.text().strip()
        self.device.ip_address = self.ip_input.text().strip()
        self.device.mac_address = self.mac_input.text().strip()
        self.device.vlan = self.vlan_input.text().strip()
        self.device.role = self.role_input.text().strip()
        self.device.notes = self.notes_input.toPlainText().strip()
        
        super().accept()

class LinkPropertiesDialog(QDialog):
    """Dialog to edit link properties"""
    
    def __init__(self, parent=None, link=None):
        super().__init__(parent)
        self.link = link
        self.setWindowTitle("Edit Connection")
        self.setModal(True)
        self.setMinimumWidth(450)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout()
        
        title = QLabel("<b>Connection Properties</b>")
        title.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addRow(title)
        
        self.type_combo = QComboBox()
        for link_type in LinkType:
            self.type_combo.addItem(link_type.value.upper(), link_type)
        self.type_combo.setCurrentText(self.link.link_type.value.upper())
        layout.addRow("Link Type:", self.type_combo)
        
        self.from_port_input = QLineEdit()
        self.from_port_input.setText(self.link.from_port)
        self.from_port_input.setPlaceholderText("Eth0/1, Gi0/0/1, etc")
        layout.addRow("From Port:", self.from_port_input)
        
        self.to_port_input = QLineEdit()
        self.to_port_input.setText(self.link.to_port)
        self.to_port_input.setPlaceholderText("Eth0/2, Gi0/0/2, etc")
        layout.addRow("To Port:", self.to_port_input)
        
        self.vlan_input = QLineEdit()
        self.vlan_input.setText(self.link.vlan)
        self.vlan_input.setPlaceholderText("1,10,20 or trunk")
        layout.addRow("VLAN(s):", self.vlan_input)
        
        self.bandwidth_input = QLineEdit()
        self.bandwidth_input.setText(self.link.bandwidth)
        self.bandwidth_input.setPlaceholderText("1Gbps, 10Gbps, etc")
        layout.addRow("Bandwidth:", self.bandwidth_input)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["active", "inactive", "backup"])
        self.status_combo.setCurrentText(self.link.status)
        layout.addRow("Status:", self.status_combo)
        
        self.notes_input = QTextEdit()
        self.notes_input.setText(self.link.notes)
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setPlaceholderText("Any additional notes...")
        layout.addRow("Notes:", self.notes_input)
        
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("✅ OK")
        btn_ok.setStyleSheet("""
            QPushButton {
                background-color: #4ECDC4;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("❌ Cancel")
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #CCCCCC;
                padding: 6px 12px;
                border-radius: 4px;
            }
        """)
        btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addRow(btn_layout)
        
        self.setLayout(layout)
    
    def accept(self):
        self.link.link_type = self.type_combo.currentData()
        self.link.from_port = self.from_port_input.text().strip()
        self.link.to_port = self.to_port_input.text().strip()
        self.link.vlan = self.vlan_input.text().strip()
        self.link.bandwidth = self.bandwidth_input.text().strip()
        self.link.status = self.status_combo.currentText()
        self.link.notes = self.notes_input.toPlainText().strip()
        
        super().accept()
