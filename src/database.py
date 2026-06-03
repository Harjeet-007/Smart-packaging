"""Database Module - SQLite operations and data persistence"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import json
from pathlib import Path
from src.config import DATABASE_PATH_STR


class Database:
    """Manages SQLite database operations for scan history."""
    
    def __init__(self, db_path: str = DATABASE_PATH_STR):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """
        Initialize database schema if not exists.
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            
            # Create scans table
            c.execute('''
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    packaging_date TEXT NOT NULL,
                    packaging_time TEXT,
                    rgb_values TEXT NOT NULL,
                    predicted_ph REAL NOT NULL,
                    freshness_status TEXT NOT NULL,
                    freshness_label TEXT,
                    confidence REAL,
                    distance REAL,
                    shelf_life_days INTEGER,
                    time_elapsed TEXT,
                    advice TEXT,
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indices for faster queries
            c.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON scans(timestamp)')
            c.execute('CREATE INDEX IF NOT EXISTS idx_packaging_date ON scans(packaging_date)')
            c.execute('CREATE INDEX IF NOT EXISTS idx_freshness ON scans(freshness_status)')
            
            conn.commit()
    
    def log_scan(self, scan_data: Dict) -> Tuple[bool, str, int]:
        """
        Log a scan event to database.
        
        Args:
            scan_data: Dictionary containing scan information
            
        Returns:
            Tuple of (success, message, scan_id)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                
                # Prepare data
                timestamp = datetime.now().isoformat()
                rgb_str = str(scan_data.get('rgb_values', ()))
                
                c.execute('''
                    INSERT INTO scans (
                        timestamp, packaging_date, packaging_time, rgb_values,
                        predicted_ph, freshness_status, freshness_label,
                        confidence, distance, shelf_life_days, time_elapsed, advice, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    timestamp,
                    scan_data.get('packaging_date'),
                    scan_data.get('packaging_time'),
                    rgb_str,
                    scan_data.get('predicted_ph'),
                    scan_data.get('freshness_status'),
                    scan_data.get('freshness_label'),
                    scan_data.get('confidence'),
                    scan_data.get('distance'),
                    scan_data.get('shelf_life_days'),
                    scan_data.get('time_elapsed'),
                    scan_data.get('advice'),
                    scan_data.get('notes')
                ))
                
                conn.commit()
                scan_id = c.lastrowid
                
                return True, f"Scan logged successfully (ID: {scan_id})", scan_id
        
        except Exception as e:
            return False, f"Error logging scan: {str(e)}", 0
    
    def get_all_scans(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        Retrieve all scans with pagination.
        
        Args:
            limit: Number of records to retrieve
            offset: Number of records to skip
            
        Returns:
            List of scan dictionaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                
                c.execute('''
                    SELECT * FROM scans
                    ORDER BY timestamp DESC
                    LIMIT ? OFFSET ?
                ''', (limit, offset))
                
                return [dict(row) for row in c.fetchall()]
        
        except Exception as e:
            print(f"Error retrieving scans: {str(e)}")
            return []
    
    def get_scan_by_id(self, scan_id: int) -> Optional[Dict]:
        """
        Retrieve a specific scan by ID.
        
        Args:
            scan_id: ID of the scan to retrieve
            
        Returns:
            Scan dictionary or None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                
                c.execute('SELECT * FROM scans WHERE id = ?', (scan_id,))
                row = c.fetchone()
                
                return dict(row) if row else None
        
        except Exception as e:
            print(f"Error retrieving scan: {str(e)}")
            return None
    
    def get_scans_by_status(
        self, status: str, limit: int = 100
    ) -> List[Dict]:
        """
        Get scans by freshness status.
        
        Args:
            status: 'FRESH', 'CAUTION', or 'ALERT'
            limit: Maximum number of records
            
        Returns:
            List of scan dictionaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                
                c.execute('''
                    SELECT * FROM scans
                    WHERE freshness_status = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (status, limit))
                
                return [dict(row) for row in c.fetchall()]
        
        except Exception as e:
            print(f"Error retrieving scans by status: {str(e)}")
            return []
    
    def get_statistics(self) -> Dict:
        """
        Get database statistics.
        
        Returns:
            Dictionary with statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                
                c.execute('SELECT COUNT(*) as total FROM scans')
                total = c.fetchone()[0]
                
                c.execute('''
                    SELECT freshness_status, COUNT(*) as count
                    FROM scans
                    GROUP BY freshness_status
                ''')
                status_counts = {row[0]: row[1] for row in c.fetchall()}
                
                c.execute('SELECT AVG(predicted_ph) as avg_ph FROM scans')
                avg_ph = c.fetchone()[0] or 0
                
                c.execute('SELECT AVG(confidence) as avg_conf FROM scans')
                avg_conf = c.fetchone()[0] or 0
                
                return {
                    'total_scans': total,
                    'status_counts': status_counts,
                    'average_ph': round(avg_ph, 2),
                    'average_confidence': round(avg_conf, 4)
                }
        
        except Exception as e:
            print(f"Error calculating statistics: {str(e)}")
            return {}
    
    def export_to_csv(self, filename: str = None) -> Tuple[bool, str, Optional[str]]:
        """
        Export all scans to CSV file.
        
        Args:
            filename: Output filename (optional)
            
        Returns:
            Tuple of (success, message, file_path)
        """
        try:
            import csv
            
            if filename is None:
                filename = f"scans_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            scans = self.get_all_scans(limit=10000)
            
            if not scans:
                return False, "No scans to export", None
            
            # Create file
            filepath = Path('exports') / filename
            filepath.parent.mkdir(exist_ok=True)
            
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=scans[0].keys())
                writer.writeheader()
                writer.writerows(scans)
            
            return True, f"Exported {len(scans)} scans to {filename}", str(filepath)
        
        except Exception as e:
            return False, f"Error exporting to CSV: {str(e)}", None
    
    def export_to_json(self, filename: str = None) -> Tuple[bool, str, Optional[str]]:
        """
        Export all scans to JSON file.
        
        Args:
            filename: Output filename (optional)
            
        Returns:
            Tuple of (success, message, file_path)
        """
        try:
            if filename is None:
                filename = f"scans_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            scans = self.get_all_scans(limit=10000)
            
            if not scans:
                return False, "No scans to export", None
            
            filepath = Path('exports') / filename
            filepath.parent.mkdir(exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(scans, f, indent=2, default=str)
            
            return True, f"Exported {len(scans)} scans to {filename}", str(filepath)
        
        except Exception as e:
            return False, f"Error exporting to JSON: {str(e)}", None
    
    def delete_scan(self, scan_id: int) -> Tuple[bool, str]:
        """
        Delete a scan by ID.
        
        Args:
            scan_id: ID of scan to delete
            
        Returns:
            Tuple of (success, message)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('DELETE FROM scans WHERE id = ?', (scan_id,))
                conn.commit()
                
                return True, f"Scan {scan_id} deleted successfully"
        
        except Exception as e:
            return False, f"Error deleting scan: {str(e)}"
    
    def clear_all_scans(self) -> Tuple[bool, str]:
        """
        Clear all scans from database (use with caution!).
        
        Returns:
            Tuple of (success, message)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('DELETE FROM scans')
                conn.commit()
                
                return True, "All scans cleared"
        
        except Exception as e:
            return False, f"Error clearing scans: {str(e)}"
