import sqlite3
import os

# Test creating database in current directory
try:
    print("Current working directory:", os.getcwd())
    print("Attempting to create test.db...")
    
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO test (name) VALUES ('test')")
    
    conn.commit()
    conn.close()
    
    print("✅ Test database created successfully!")
    
    # Verify file exists
    if os.path.exists("test.db"):
        print("✅ test.db file exists")
        print(f"File size: {os.path.getsize('test.db')} bytes")
    else:
        print("❌ test.db file not found")
        
except Exception as e:
    print(f"❌ Error: {e}")
