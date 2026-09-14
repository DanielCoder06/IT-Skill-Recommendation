from src.pipeline.load_jobs import load_jobs
import sqlite3

connection = sqlite3.connect("data/it_jobs.db")

jobs =  load_jobs()

print("Số lượng jobs: ", len(jobs))

for job in jobs:
    """Process each job"""
    company_name = job["company"]
    
    result = connection.execute(
    """
    SELECT id
    FROM companies
    WHERE name = ?
    """,
    (company_name,)
    )
    
    company_id = result.fetchone()
    
    if company_id is None:
        connection.execute(
            """
            INSERT INTO companies (name)
            VALUES (?)
            """,
            (company_name,)
        )
        connection.commit()
        
        company_id = connection.execute(
            """
            SELECT id
            FROM companies
            WHERE name = ?
            """,
            (company_name,)
        ).fetchone()[0]

    else:
        company_id = company_id[0]
        
    print(company_name, "->", company_id)
    
    """Process each location"""
    location_city = job["location"]
    
    result = connection.execute(
        """
        SELECT id
        FROM locations
        WHERE city = ?
        """,
        (location_city,)
    )
    location = result.fetchone()
    
    if location is None:
        connection.execute(
            """ 
            INSERT INTO locations (city)
            VALUES (?)
            """,
            (location_city,)
        )
        
        connection.commit()
        
        location_id = connection.execute(
            """ 
            SELECT id
            FROM locations
            WHERE city = ?
            """,
            (location_city,)
        ).fetchall()[0]
    
    else:
        location_id = location[0]
        
    print(location_city, "->", location_id)

connection.close()