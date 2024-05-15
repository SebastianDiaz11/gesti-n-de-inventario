import sqlite3

# Conexión a la base de datos 
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Creación de la tabla 
cursor.execute('''CREATE TABLE products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL
                )''')

def add_product(name, description, price, quantity):
    cursor.execute('INSERT INTO products (name, description, price, quantity) VALUES (?, ?, ?, ?)',
                   (name, description, price, quantity))
    conn.commit()
    print("Producto agregado correctamente.")

def delete_product(product_id):
    cursor.execute('DELETE FROM products WHERE id=?', (product_id,))
    conn.commit()
    print("Producto eliminado correctamente.")

def update_product(product_id, name=None, description=None, price=None, quantity=None):
    updates = []
    if name:
        updates.append(('name', name))
    if description:
        updates.append(('description', description))
    if price:
        updates.append(('price', price))
    if quantity:
        updates.append(('quantity', quantity))
    placeholders = ', '.join([f'{field}=?' for field, _ in updates])
    values = [value for _, value in updates]
    values.append(product_id)
    cursor.execute(f'UPDATE products SET {placeholders} WHERE id=?', tuple(values))
    conn.commit()
    print("Producto actualizado correctamente.")

def display_products():
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    if products:
        print("\nInventario:")
        for product in products:
            print(f"ID: {product[0]}, Nombre: {product[1]}, Descripción: {product[2]}, Precio: {product[3]}, Cantidad disponible: {product[4]}")
    else:
        print("El inventario está vacío.")

# Menu
while True:
    print("\n1. Agregar producto")
    print("2. Eliminar producto")
    print("3. Actualizar producto")
    print("4. Mostrar inventario")
    print("5. Salir")

    choice = input("Ingrese el número de la opción que desea realizar: ")

    if choice == '1':
        name = input("Ingrese el nombre del producto: ")
        description = input("Ingrese la descripción del producto (opcional): ")
        price = float(input("Ingrese el precio del producto: "))
        quantity = int(input("Ingrese la cantidad disponible del producto: "))
        add_product(name, description, price, quantity)
    elif choice == '2':
        product_id = int(input("Ingrese el ID del producto que desea eliminar: "))
        delete_product(product_id)
    elif choice == '3':
        product_id = int(input("Ingrese el ID del producto que desea actualizar: "))
        name = input("Ingrese el nuevo nombre del producto (deje en blanco si no desea actualizar): ")
        description = input("Ingrese la nueva descripción del producto (deje en blanco si no desea actualizar): ")
        price = float(input("Ingrese el nuevo precio del producto (deje en blanco si no desea actualizar): "))
        quantity = int(input("Ingrese la nueva cantidad disponible del producto (deje en blanco si no desea actualizar): "))
        update_product(product_id, name, description, price, quantity)
    elif choice == '4':
        display_products()
    elif choice == '5':
        break
    else:
        print("Opción no válida. Por favor, ingrese un número válido.")