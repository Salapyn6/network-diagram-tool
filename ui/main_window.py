# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QMessageBox, QFileDialog, QDialog,
    QSplitter, QStatusBar
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from models.device import DeviceType, DEVICE_LABELS
from models.project import Project
from utils.file_manager import FileManager
from utils.icons import IconGenerator
from ui.canvas import NetworkCanvas
from ui.dialogs import NewProjectDialog, DevicePropertiesDialog, LinkPropertiesDialog

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Diagram Tool v1.0")
        self.setGeometry(50, 50, 1600, 1000)
        
        self.project = None
        self.canvas = None
        self.status_bar = self.statusBar()
        
        self.init_ui()
        self.new_project()
    
    def init_ui(self):
        """Initialize the user interface"""
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        
        # Left panel - Device palette
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        title = QLabel("<b>DEVICES</b>")
        title.setFont(QFont("Arial", 10, QFont.Bold))
        left_layout.addWidget(title)
        
        self.device_list = QListWidget()
        self.device_list.itemClicked.connect(self.on_device_selected)
        self.device_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #CCC;
                background-color: #F9F9F9;
            }
            QListWidget::item:selected {
                background-color: #4ECDC4;
                color: white;
            }
        """)
        
        for device_type in DeviceType:
            item = QListWidgetItem(DEVICE_LABELS.get(device_type, device_type.value))
            item.setData(Qt.UserRole, device_type)
            icon = IconGenerator.generate_icon(device_type)
            item.setIcon(QIcon(icon))
            item.setToolTip(f"Click to select, then click canvas to place")
            self.device_list.addItem(item)
        
        left_layout.addWidget(self.device_list)
        
        # Control buttons
        btn_style = """
            QPushButton {
                background-color: #4ECDC4;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3CB5AD;
            }
            QPushButton:pressed {
                background-color: #2A9D96;
            }
        """
        
        self.btn_new = QPushButton("📄 New")
        self.btn_new.setStyleSheet(btn_style)
        self.btn_new.clicked.connect(self.new_project)
        left_layout.addWidget(self.btn_new)
        
        self.btn_open = QPushButton("📂 Open")
        self.btn_open.setStyleSheet(btn_style)
        self.btn_open.clicked.connect(self.open_project)
        left_layout.addWidget(self.btn_open)
        
        self.btn_save = QPushButton("💾 Save")
        self.btn_save.setStyleSheet(btn_style)
        self.btn_save.clicked.connect(self.save_project)
        left_layout.addWidget(self.btn_save)
        
        self.btn_export_png = QPushButton("🖼️  PNG")
        self.btn_export_png.setStyleSheet(btn_style)
        self.btn_export_png.clicked.connect(self.export_png)
        left_layout.addWidget(self.btn_export_png)
        
        self.btn_export_svg = QPushButton("📊 SVG")
        self.btn_export_svg.setStyleSheet(btn_style)
        self.btn_export_svg.clicked.connect(self.export_svg)
        left_layout.addWidget(self.btn_export_svg)
        
        self.btn_delete = QPushButton("🗑️  Delete")
        self.btn_delete.setStyleSheet(btn_style)
        self.btn_delete.clicked.connect(self.delete_selected)
        left_layout.addWidget(self.btn_delete)
        
        self.btn_clear = QPushButton("🧹 Clear All")
        self.btn_clear.setStyleSheet(btn_style)
        self.btn_clear.clicked.connect(self.clear_canvas)
        left_layout.addWidget(self.btn_clear)
        
        left_layout.addStretch()
        
        info = QLabel(
            "<small><b>HOW TO USE:</b><br>"
            "1. Select device<br>"
            "2. Click canvas<br>"
            "3. Right-click to connect<br>"
            "4. Double-click to edit<br>"
            "5. Save & Export</small>"
        )
        info.setStyleSheet("background-color: #FFF9E6; padding: 8px; border-radius: 4px;")
        left_layout.addWidget(info)
        
        left_widget.setMaximumWidth(220)
        left_widget.setMinimumWidth(180)
        
        # Center - Canvas
        self.canvas = NetworkCanvas(self)
        
        # Add to main layout
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.canvas, 1)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        self.create_menu_bar()
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet("QMenuBar { background-color: #F5F5F5; }")
        
        file_menu = menubar.addMenu("📁 File")
        file_menu.addAction("New Project", self.new_project, "Ctrl+N")
        file_menu.addAction("Open Project", self.open_project, "Ctrl+O")
        file_menu.addAction("Save Project", self.save_project, "Ctrl+S")
        file_menu.addSeparator()
        file_menu.addAction("Export PNG", self.export_png)
        file_menu.addAction("Export SVG", self.export_svg)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close, "Ctrl+Q")
        
        edit_menu = menubar.addMenu("✏️  Edit")
        edit_menu.addAction("Delete Selected", self.delete_selected, "Delete")
        edit_menu.addAction("Clear All", self.clear_canvas)
        
        help_menu = menubar.addMenu("❓ Help")
        help_menu.addAction("About", self.show_about)
    
    def on_device_selected(self, item: QListWidgetItem):
        """Handle device selection from list"""
        device_type = item.data(Qt.UserRole)
        self.canvas.set_drawing_mode(device_type)
        self.status_bar.showMessage(f"Selected {DEVICE_LABELS.get(device_type)} - Click canvas to place")
    
    def new_project(self):
        """Create new project"""
        dialog = NewProjectDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.project = Project(
                name=dialog.project_name,
                description=dialog.description
            )
            self.canvas.set_project(self.project)
            self.setWindowTitle(f"Network Diagram Tool - {self.project.name}")
            self.status_bar.showMessage(f"New project: {self.project.name}")
    
    def open_project(self):
        """Open existing project"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            FileManager.PROJECT_DIR,
            "Network Diagrams (*.ndt);;All Files (*)"
        )
        
        if filepath:
            project = FileManager.load_project(filepath)
            if project:
                self.project = project
                self.canvas.set_project(self.project)
                self.setWindowTitle(f"Network Diagram Tool - {self.project.name}")
                self.status_bar.showMessage(f"Loaded: {project.name} ({len(project.devices)} devices, {len(project.links)} links)")
            else:
                QMessageBox.warning(self, "Error", "Failed to load project")
    
    def save_project(self):
        """Save current project"""
        if self.project is None:
            QMessageBox.warning(self, "Warning", "No project to save")
            return
        
        try:
            FileManager.save_project(self.project)
            self.status_bar.showMessage(f"Saved: {self.project.name}")
            QMessageBox.information(self, "Success", f"Project '{self.project.name}' saved!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
    
    def export_png(self):
        """Export diagram as PNG"""
        from utils.export import Exporter
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Export as PNG",
            f"{self.project.name if self.project else 'diagram'}.png",
            "PNG Images (*.png);;All Files (*)"
        )
        
        if filepath:
            if Exporter.export_to_png(self.canvas.scene(), filepath):
                self.status_bar.showMessage(f"Exported to PNG: {filepath}")
                QMessageBox.information(self, "Success", f"Exported to:\n{filepath}")
            else:
                QMessageBox.warning(self, "Error", "Failed to export PNG")
    
    def export_svg(self):
        """Export diagram as SVG"""
        from utils.export import Exporter
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Export as SVG",
            f"{self.project.name if self.project else 'diagram'}.svg",
            "SVG Images (*.svg);;All Files (*)"
        )
        
        if filepath:
            if Exporter.export_to_svg(self.canvas.scene(), filepath):
                self.status_bar.showMessage(f"Exported to SVG: {filepath}")
                QMessageBox.information(self, "Success", f"Exported to:\n{filepath}")
            else:
                QMessageBox.warning(self, "Error", "Failed to export SVG")
    
    def delete_selected(self):
        """Delete selected item on canvas"""
        count = self.canvas.delete_selected()
        if count > 0:
            self.status_bar.showMessage(f"Deleted {count} item(s)")
    
    def clear_canvas(self):
        """Clear all devices from canvas"""
        if len(self.project.devices) == 0:
            QMessageBox.information(self, "Info", "Canvas is already empty")
            return
        
        reply = QMessageBox.question(
            self,
            "Clear All?",
            f"Delete all {len(self.project.devices)} devices and {len(self.project.links)} connections?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.project.devices.clear()
            self.project.links.clear()
            self.canvas.set_project(self.project)
            self.status_bar.showMessage("Canvas cleared")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Network Diagram Tool",
            "<b>Network Diagram Tool v1.0</b><br><br>"
            "A simple drag-and-drop network topology designer for Ubuntu.<br><br>"
            "<b>Features:</b><br>"
            "✓ 16 device types<br>"
            "✓ Drag & drop placement<br>"
            "✓ Connect devices<br>"
            "✓ Edit properties (IP, VLAN, etc)<br>"
            "✓ Save/Load projects<br>"
            "✓ Export PNG/SVG<br><br>"
            "<small>© 2024 - Made for personal network design</small>"
        )
