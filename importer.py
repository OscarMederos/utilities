import requests
from bs4 import BeautifulSoup
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('pokemon.db')
cursor = conn.cursor()

# Create table to store Pokemon data
cursor.execute('''CREATE TABLE IF NOT EXISTS pokedex (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    type TEXT,
                    total INTEGER,
                    hp INTEGER,
                    attack INTEGER,
                    defense INTEGER,
                    sp_attack INTEGER,
                    sp_defense INTEGER,
                    speed INTEGER
                    )''')

# Send a GET request to the URL
url = 'https://pokemondb.net/pokedex/all'
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing Pokemon data
table = soup.find('table', {'id': 'pokedex'})

# Extract data from each row in the table
rows = table.find_all('tr')[1:]  # Exclude the header row

for row in rows:
    # Extract the data from each column
    columns = row.find_all('td')
    
    # Extract the relevant information
    pokemon_id = int(columns[0].text.strip())
    name = columns[1].find('a').text.strip()
    types = [t.text.strip() for t in columns[2].find_all('a')]
    total = int(columns[3].text.strip())
    hp = int(columns[4].text.strip())
    attack = int(columns[5].text.strip())
    defense = int(columns[6].text.strip())
    sp_attack = int(columns[7].text.strip())
    sp_defense = int(columns[8].text.strip())
    speed = int(columns[9].text.strip())
    
    # Insert the data into the database
    cursor.execute('''INSERT OR IGNORE INTO pokedex (
                        id, name, type, total, hp, attack, defense, sp_attack, sp_defense, speed
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (pokemon_id, name, ', '.join(types), total, hp, attack, defense, sp_attack, sp_defense, speed))

# Commit the changes and close the connection
conn.commit()

# Execute a SELECT query to retrieve the data
cursor.execute("SELECT * FROM pokedex")

# Fetch all the rows from the result set
rows = cursor.fetchall()

# Display the data
for row in rows:
    print(row)

# Close the connection
conn.close()

print("\n")
print("Pokedex data scraped and stored in the database.")
