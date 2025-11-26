import csv
import os
from typing import List, Dict, Any
from abc import ABC, abstractmethod


class CSVPersistence(ABC):
    """Base class for CSV persistence operations"""
    
    def __init__(self, filepath: str, fieldnames: List[str]):
        self.filepath = filepath
        self.fieldnames = fieldnames
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create file with headers if it doesn't exist"""
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
    
    def save_all(self, data: List[Dict[str, Any]]) -> None:
        """Save all data to CSV file (overwrite)"""
        try:
            with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            raise ValueError(f"Failed to save data to {self.filepath}: {e}")
    
    def load_all(self) -> List[Dict[str, Any]]:
        """Load all data from CSV file"""
        try:
            data = []
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    data = [row for row in reader]
            return data
        except Exception as e:
            raise ValueError(f"Failed to load data from {self.filepath}: {e}")
    
    def append_row(self, row: Dict[str, Any]) -> None:
        """Append a single row to CSV file"""
        try:
            with open(self.filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writerow(row)
        except Exception as e:
            raise ValueError(f"Failed to append data to {self.filepath}: {e}")
    
    def backup_file(self) -> str:
        """Create a backup of the current file"""
        if os.path.exists(self.filepath):
            backup_path = f"{self.filepath}.backup"
            try:
                import shutil
                shutil.copy2(self.filepath, backup_path)
                return backup_path
            except Exception as e:
                raise ValueError(f"Failed to create backup: {e}")
        return ""


def test_module():
    import tempfile
    import os
    
    # Test with temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        test_file = f.name
    
    try:
        # Test CSV persistence
        fieldnames = ['id', 'name', 'value']
        
        class TestCSVPersistence(CSVPersistence):
            pass
        
        persistence = TestCSVPersistence(test_file, fieldnames)
        
        # Test file creation
        assert os.path.exists(test_file)
        
        # Test saving and loading
        test_data = [
            {'id': '1', 'name': 'test1', 'value': '100'},
            {'id': '2', 'name': 'test2', 'value': '200'}
        ]
        
        persistence.save_all(test_data)
        loaded_data = persistence.load_all()
        
        assert len(loaded_data) == 2
        assert loaded_data[0]['id'] == '1'
        assert loaded_data[1]['name'] == 'test2'
        
        # Test append
        new_row = {'id': '3', 'name': 'test3', 'value': '300'}
        persistence.append_row(new_row)
        
        loaded_data = persistence.load_all()
        assert len(loaded_data) == 3
        assert loaded_data[2]['value'] == '300'
        
        # Test backup
        backup_path = persistence.backup_file()
        assert os.path.exists(backup_path)
        
    finally:
        # Cleanup
        try:
            os.unlink(test_file)
            os.unlink(f"{test_file}.backup")
        except:
            pass