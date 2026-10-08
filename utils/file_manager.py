# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path
from typing import Optional
from models.project import Project

class FileManager:
    """Handles saving and loading project files"""
    
    PROJECT_EXT = '.ndt'
    PROJECT_DIR = os.path.expanduser('~/.ndt_projects')
    
    @classmethod
    def _ensure_dir(cls):
        Path(cls.PROJECT_DIR).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def save_project(cls, project: Project, filename: Optional[str] = None) -> str:
        """Save project to file"""
        cls._ensure_dir()
        
        if filename is None:
            filename = project.name.replace(' ', '_')
        
        if not filename.endswith(cls.PROJECT_EXT):
            filename += cls.PROJECT_EXT
        
        filepath = os.path.join(cls.PROJECT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(project.to_dict(), f, indent=2, ensure_ascii=False)
        
        return filepath
    
    @classmethod
    def load_project(cls, filepath: str) -> Optional[Project]:
        """Load project from file"""
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Project.from_dict(data)
        except Exception as e:
            print(f"Error loading project: {e}")
            return None
    
    @classmethod
    def get_recent_projects(cls) -> list:
        """Get list of recent projects"""
        cls._ensure_dir()
        
        projects = []
        for file in Path(cls.PROJECT_DIR).glob(f'*{cls.PROJECT_EXT}'):
            projects.append({
                'name': file.stem,
                'path': str(file),
                'modified': os.path.getmtime(str(file))
            })
        
        return sorted(projects, key=lambda x: x['modified'], reverse=True)
    
    @classmethod
    def get_project_path(cls, filename: str) -> str:
        """Get full path to project file"""
        return os.path.join(cls.PROJECT_DIR, filename)
