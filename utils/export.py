# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtSvg import QSvgGenerator

class Exporter:
    """Export diagrams to various formats"""
    
    @staticmethod
    def export_to_png(scene, filepath: str) -> bool:
        """Export diagram to PNG"""
        try:
            rect = scene.itemsBoundingRect()
            if rect.isEmpty():
                return False
            
            pixmap = QPixmap(int(rect.width()) + 40, int(rect.height()) + 40)
            pixmap.fill()
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            scene.render(painter, target=pixmap.rect(), source=rect)
            painter.end()
            
            return pixmap.save(filepath)
        except Exception as e:
            print(f"Error exporting to PNG: {e}")
            return False
    
    @staticmethod
    def export_to_svg(scene, filepath: str) -> bool:
        """Export diagram to SVG"""
        try:
            rect = scene.itemsBoundingRect()
            if rect.isEmpty():
                return False
            
            generator = QSvgGenerator()
            generator.setFileName(filepath)
            generator.setSize(rect.size().toSize())
            generator.setViewBox(rect)
            
            painter = QPainter()
            painter.begin(generator)
            painter.setRenderHint(QPainter.Antialiasing)
            scene.render(painter, target=rect, source=rect)
            painter.end()
            
            return True
        except Exception as e:
            print(f"Error exporting to SVG: {e}")
            return False
