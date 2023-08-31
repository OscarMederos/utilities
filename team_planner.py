import sqlite3

def get_valid_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Please enter a valid integer.")

conn = sqlite3.connect('pokemon.db')
cursor = conn.cursor()

print("Pokemon Team Builder 1.0")
search_term_type = input("What type are you looking for? ")
search_term_stats = get_valid_integer_input("What base stat total minimum are you looking for? ")

search_term_type = '%' + search_term_type + '%'  # Wildcards for partial matches

cursor.execute("SELECT * FROM pokedex WHERE LOWER(type) LIKE LOWER(?) AND total > ? ORDER BY total DESC", (search_term_type, search_term_stats))
result = cursor.fetchall()
conn.close()

for row in result:
    print(row)
