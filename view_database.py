#!/usr/bin/env python3
"""
View SoilDoctor database contents
"""

import sqlite3
import json

def view_database():
    """View all database contents"""
    print("🔍 SoilDoctor Database Viewer")
    print("=" * 40)
    
    # Connect to the API database
    try:
        conn = sqlite3.connect('soildoctor_api.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"📊 Found {len(tables)} tables:")
        for table in tables:
            table_name = table['name']
            print(f"\n🗂️  Table: {table_name}")
            print("-" * 30)
            
            # Get table structure
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print("Columns:", [col['name'] for col in columns])
            
            # Get table data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            if rows:
                print(f"Records ({len(rows)}):")
                for i, row in enumerate(rows, 1):
                    print(f"  {i}: {dict(row)}")
            else:
                print("No records found")
        
        conn.close()
        
    except sqlite3.OperationalError as e:
        print(f"❌ Database file not found: {e}")
        print("💡 Start the API server first: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

def view_api_database():
    """View in-memory API database"""
    print("🔍 API Database Viewer (In-Memory)")
    print("=" * 40)
    
    try:
        # Import the app module to access its database
        import sys
        import os
        sys.path.append(os.path.dirname(__file__))
        
        from app import get_db
        
        conn = get_db()
        cursor = conn.cursor()
        
        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"📊 Found {len(tables)} tables:")
        for table in tables:
            table_name = table['name']
            print(f"\n🗂️  Table: {table_name}")
            print("-" * 30)
            
            # Get table structure
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print("Columns:", [col['name'] for col in columns])
            
            # Get table data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            if rows:
                print(f"Records ({len(rows)}):")
                for i, row in enumerate(rows, 1):
                    print(f"  {i}: {dict(row)}")
            else:
                print("No records found")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure the API server is running")

if __name__ == "__main__":
    print("Choose viewing option:")
    print("1. View file database (soildoctor_api.db)")
    print("2. View API in-memory database")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        view_database()
    elif choice == "2":
        view_api_database()
    else:
        print("❌ Invalid choice")
