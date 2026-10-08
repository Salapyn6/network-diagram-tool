#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Network Diagram Tool - Main Application Entry Point
A simple drag-and-drop network topology designer for Ubuntu
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Network Diagram Tool")
    app.setApplicationVersion("1.0.0")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
