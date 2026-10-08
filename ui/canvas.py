# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QMenu
from PyQt5.QtCore import Qt, QPointF, QLineF, QTimer
from PyQt5.QtGui import QColor, QPen, QBrush, QFont, QCursor, QPolygonF, QPainter
from models.device import DeviceType, Device, DEVICE_COLORS, DEVICE_LABELS
from models.link import Link
from models.project import Project
from ui.dialogs import DevicePropertiesDialog, LinkPropertiesDialog
import uuid

class DeviceItem(QGraphicsEllipseItem):
    """Visual representation of a network device on canvas"""
    
    def __init__(self, device: Device, canvas):
        super().__init__(device.x - 30, device.y - 30, 60, 60)
        self.device = device
        self.canvas = canvas
        self.setAcceptHoverEvents(True)
        
        color = QColor(device.get_color())
        self.setBrush(QBrush(color))
        self.setPen(QPen(QColor("#333333"), 2))
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
        self.setCursor(QCursor(Qt.OpenHandCursor))
        self.setZValue(100)
        
        self.text = QGraphicsTextItem(device.label or device.get_type_label(), self)
        self.text.setFont(QFont("Arial", 9, QFont.Bold))
        self.text.setDefaultTextColor(QColor("#000000"))
        self.text.setPos(-20, -8)
    
    def mousePressEvent(self, event):
        """Handle mouse press"""
        if event.button() == Qt.RightButton:
            self.show_context_menu(event.scenePos())
        else:
            super().mousePressEvent(event)
            self.canvas.selected_item = self
            self.setCursor(QCursor(Qt.ClosedHandCursor))
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        super().mouseReleaseEvent(event)
        self.setCursor(QCursor(Qt.OpenHandCursor))
    
    def mouseMoveEvent(self, event):
        """Handle mouse move"""
        super().mouseMoveEvent(event)
        self.device.x = self.rect().center().x()
        self.device.y = self.rect().center().y()
        self.canvas.update_links_for_device(self.device.device_id)
    
    def mouseDoubleClickEvent(self, event):
        """Handle double click to edit properties"""
        self.canvas.edit_device(self.device)
    
    def show_context_menu(self, pos):
        """Show right-click context menu"""
        menu = QMenu()
        menu.addAction("✏️  Edit", lambda: self.canvas.edit_device(self.device))
        menu.addAction("🔗 Connect to...", lambda: self.canvas.start_connection(self.device))
        menu.addSeparator()
        menu.addAction("🗑️  Delete", lambda: self.canvas.delete_device(self.device.device_id))
        menu.exec_(QCursor.pos())

class LinkItem(QGraphicsLineItem):
    """Visual representation of a connection between devices"""
    
    def __init__(self, link: Link, canvas):
        super().__init__()
        self.link = link
        self.canvas = canvas
        self.setAcceptHoverEvents(True)
        
        pen = QPen(QColor("#666666"), 2)
        self.setPen(pen)
        self.selected_pen = QPen(QColor("#FF6B6B"), 3)
        self.setZValue(10)
    
    def update_line(self, from_pos, to_pos):
        """Update line position"""
        self.setLine(QLineF(from_pos, to_pos))
    
    def mousePressEvent(self, event):
        """Handle mouse press on link"""
        if event.button() == Qt.RightButton:
            menu = QMenu()
            menu.addAction("✏️  Edit", lambda: self.canvas.edit_link(self.link))
            menu.addAction("🗑️  Delete", lambda: self.canvas.delete_link(self.link.link_id))
            menu.exec_(QCursor.pos())
        super().mousePressEvent(event)
    
    def hoverEnterEvent(self, event):
        """Highlight on hover"""
        self.setPen(self.selected_pen)
    
    def hoverLeaveEvent(self, event):
        """Remove highlight on leave"""
        self.setPen(QPen(QColor("#666666"), 2))

class NetworkCanvas(QGraphicsView):
    """Canvas for drawing network diagrams"""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.project = None
        self.drawing_mode = None
        self.selected_item = None
        
        self.scene_obj = QGraphicsScene(0, 0, 1600, 1000)
        self.setScene(self.scene_obj)
        self.setRenderHint(QPainter.Antialiasing)
        
        self.device_items = {}
        self.link_items = {}
        
        self.connecting = False
        self.connection_from_device = None
        self.temp_line = None
        
        self.setStyleSheet("""
            QGraphicsView {
                border: 2px solid #DDD;
                background-color: #FAFAFA;
            }
        """)
        
        self.setDragMode(self.ScrollHandDrag)
    
    def set_project(self, project: Project):
        """Set the project to display"""
        self.project = project
        self.scene_obj.clear()
        self.device_items.clear()
        self.link_items.clear()
        
        for device in project.devices:
            self.add_device_visual(device)
        
        for link in project.links:
            self.add_link_visual(link)
    
    def set_drawing_mode(self, device_type: DeviceType):
        """Set mode to draw devices"""
        self.drawing_mode = device_type
        self.setCursor(QCursor(Qt.CrossCursor))
    
    def mousePressEvent(self, event):
        """Handle mouse press on canvas"""
        scene_pos = self.mapToScene(event.pos())
        
        if self.drawing_mode and event.button() == Qt.LeftButton:
            device_id = str(uuid.uuid4())[:8]
            device = Device(
                device_id=device_id,
                device_type=self.drawing_mode,
                x=scene_pos.x(),
                y=scene_pos.y(),
                label=DEVICE_LABELS.get(self.drawing_mode, "Device")
            )
            
            self.project.add_device(device)
            self.add_device_visual(device)
            self.drawing_mode = None
            self.setCursor(QCursor(Qt.ArrowCursor))
            self.main_window.status_bar.showMessage(f"Added {device.get_type_label()}")
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move"""
        if self.connecting and self.temp_line:
            scene_pos = self.mapToScene(event.pos())
            self.temp_line.setLine(QLineF(
                self.temp_line.line().p1(),
                scene_pos
            ))
        super().mouseMoveEvent(event)
    
    def add_device_visual(self, device: Device):
        """Add device to canvas"""
        item = DeviceItem(device, self)
        self.scene_obj.addItem(item)
        self.device_items[device.device_id] = item
    
    def add_link_visual(self, link: Link):
        """Add link to canvas"""
        from_device = self.project.get_device(link.from_device_id)
        to_device = self.project.get_device(link.to_device_id)
        
        if from_device and to_device:
            item = LinkItem(link, self)
            item.update_line(
                QPointF(from_device.x, from_device.y),
                QPointF(to_device.x, to_device.y)
            )
            self.scene_obj.addItem(item)
            self.link_items[link.link_id] = item
    
    def start_connection(self, device: Device):
        """Start drawing a connection from device"""
        self.connecting = True
        self.connection_from_device = device
        self.main_window.status_bar.showMessage(f"Connecting from {device.label}... Click target device")
        
        self.temp_line = QGraphicsLineItem()
        self.temp_line.setPen(QPen(QColor("#0066CC"), 2, Qt.DashLine))
        self.temp_line.setLine(QLineF(
            QPointF(device.x, device.y),
            QPointF(device.x, device.y)
        ))
        self.scene_obj.addItem(self.temp_line)
    
    def finish_connection(self, to_device: Device):
        """Finish connection between two devices"""
        if self.connection_from_device and self.connection_from_device.device_id != to_device.device_id:
            link_id = str(uuid.uuid4())[:8]
            link = Link(
                link_id=link_id,
                from_device_id=self.connection_from_device.device_id,
                to_device_id=to_device.device_id
            )
            
            self.project.add_link(link)
            self.add_link_visual(link)
            self.main_window.status_bar.showMessage(
                f"Connected {self.connection_from_device.label} to {to_device.label}"
            )
        
        if self.temp_line:
            self.scene_obj.removeItem(self.temp_line)
            self.temp_line = None
        
        self.connecting = False
        self.connection_from_device = None
    
    def update_links_for_device(self, device_id: str):
        """Update all links connected to a device"""
        device = self.project.get_device(device_id)
        if not device:
            return
        
        for link in self.project.links:
            if link.from_device_id == device_id or link.to_device_id == device_id:
                if link.link_id in self.link_items:
                    from_dev = self.project.get_device(link.from_device_id)
                    to_dev = self.project.get_device(link.to_device_id)
                    if from_dev and to_dev:
                        self.link_items[link.link_id].update_line(
                            QPointF(from_dev.x, from_dev.y),
                            QPointF(to_dev.x, to_dev.y)
                        )
    
    def edit_device(self, device: Device):
        """Edit device properties"""
        dialog = DevicePropertiesDialog(self.main_window, device)
        if dialog.exec_():
            if device.device_id in self.device_items:
                item = self.device_items[device.device_id]
                item.text.setPlainText(device.label or device.get_type_label())
    
    def edit_link(self, link: Link):
        """Edit link properties"""
        dialog = LinkPropertiesDialog(self.main_window, link)
        dialog.exec_()
    
    def delete_device(self, device_id: str):
        """Delete device from canvas"""
        if device_id in self.device_items:
            item = self.device_items[device_id]
            self.scene_obj.removeItem(item)
            del self.device_items[device_id]
        
        self.project.remove_device(device_id)
        
        links_to_remove = []
        for link in self.project.links:
            if link.link_id in self.link_items:
                links_to_remove.append(link.link_id)
        
        for link_id in links_to_remove:
            if link_id in self.link_items:
                item = self.link_items[link_id]
                self.scene_obj.removeItem(item)
                del self.link_items[link_id]
        
        self.main_window.status_bar.showMessage("Device deleted")
    
    def delete_link(self, link_id: str):
        """Delete link from canvas"""
        if link_id in self.link_items:
            item = self.link_items[link_id]
            self.scene_obj.removeItem(item)
            del self.link_items[link_id]
        
        self.project.remove_link(link_id)
        self.main_window.status_bar.showMessage("Connection deleted")
    
    def delete_selected(self) -> int:
        """Delete selected item and return count"""
        count = 0
        selected_items = self.scene_obj.selectedItems()
        for item in selected_items:
            if isinstance(item, DeviceItem):
                self.delete_device(item.device.device_id)
                count += 1
            elif isinstance(item, LinkItem):
                self.delete_link(item.link.link_id)
                count += 1
        return count
