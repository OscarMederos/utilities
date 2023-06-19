import sqlite3

conn = sqlite3.connect('pokemon.db')
cursor = conn.cursor()

print("Pokemon Team Builder 1.0")
search_term_type = input("What type are you looking for? ")
search_term_stats = input("What base stat total-minium are you looking for? ")

cursor.execute("SELECT * FROM pokedex WHERE type LIKE ? AND total > ?", (search_term_type, search_term_stats))
result = cursor.fetchall()
conn.close()

for row in result:
    print(row)