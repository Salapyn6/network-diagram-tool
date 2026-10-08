# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QRect
from models.device import DeviceType, DEVICE_COLORS

class IconGenerator:
    """Generate simple device icons"""
    
    ICON_SIZE = 48
    
    @staticmethod
    def generate_icon(device_type: DeviceType) -> QPixmap:
        """Generate icon for device type"""
        pixmap = QPixmap(IconGenerator.ICON_SIZE, IconGenerator.ICON_SIZE)
        pixmap.fill(Qt.white)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        color = QColor(DEVICE_COLORS.get(device_type, "#CCCCCC"))
        painter.fillRect(0, 0, IconGenerator.ICON_SIZE, IconGenerator.ICON_SIZE, color)
        
        painter.setPen(QColor("#333333"))
        painter.drawRect(0, 0, IconGenerator.ICON_SIZE - 1, IconGenerator.ICON_SIZE - 1)
        
        painter.setFont(QFont("Arial", 7, QFont.Bold))
        abbrev = device_type.value[:3].upper()
        painter.drawText(QRect(0, 0, IconGenerator.ICON_SIZE, IconGenerator.ICON_SIZE),
                        Qt.AlignCenter, abbrev)
        
        painter.end()
        return pixmap
