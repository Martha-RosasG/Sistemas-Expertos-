# Actividad 1.Python_Inventario_Actividad modificada 
import array

# Tuplas para categorías de productos
CATEGORIAS = ("Alimentos", "Bebidas", "Limpieza", "Otros")

# Clase base para los productos
class Producto:
    def __init__(self, nombre, precio, categoria, stock):
        # Diccionario para almacenar la información del producto
        self.info_producto = {
            'nombre': nombre,
            'precio': precio,
            'categoria': categoria
        }
        # Array para manejar la cantidad de productos en stock
        self.stock = array.array('i', [stock])
    
    def mostrar_info(self):
        print(f"Producto: {self.info_producto['nombre']}")
        print(f"Categoría: {self.info_producto['categoria']}")
        print(f"Precio unitario: ${self.info_producto['precio']:.2f}")
        print(f"Stock disponible: {self.stock[0]}")
    
    def actualizar_stock(self, cantidad):
        self.stock[0] = cantidad
        print(f"Nuevo stock de {self.info_producto['nombre']}: {self.stock[0]}")
    
    def valor_total(self):
        return self.info_producto['precio'] * self.stock[0]

# Clase que maneja el Inventario
class Inventario:
    def __init__(self):
        # Lista para almacenar todos los productos
        self.productos = []
    
    def agregar_producto(self, producto):
        self.productos.append(producto)
        print(f"Producto {producto.info_producto['nombre']} agregado al inventario.")
    
    def mostrar_inventario(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print("\nInventario actual:")
            for producto in self.productos:
                producto.mostrar_info()
                print("-" * 25)
    
    def buscar_por_categoria(self, categoria):
        print(f"\nBuscando productos en la categoría: {categoria}")
        encontrados = [p for p in self.productos if p.info_producto['categoria'] == categoria]
        if encontrados:
            for producto in encontrados:
                producto.mostrar_info()
                print("-" * 25)
        else:
            print("No se encontraron productos en esta categoría.")
    
    def valor_total_inventario(self):
        total = sum(p.valor_total() for p in self.productos)
        print(f"\nValor total del inventario: ${total:.2f}")
        return total

# Instanciando el inventario
mi_inventario = Inventario()

# Agregando productos del minisúper
producto1 = Producto("Leche", 25.50, "Alimentos", 20)
producto2 = Producto("Pan Bimbo", 38.00, "Alimentos", 15)
producto3 = Producto("Refresco Coca-Cola 2L", 42.00, "Bebidas", 30)
producto4 = Producto("Detergente Ariel 1kg", 85.00, "Limpieza", 10)

mi_inventario.agregar_producto(producto1)
mi_inventario.agregar_producto(producto2)
mi_inventario.agregar_producto(producto3)
mi_inventario.agregar_producto(producto4)

# Mostrar inventario completo
mi_inventario.mostrar_inventario()

# Buscar productos por categoría
mi_inventario.buscar_por_categoria("Alimentos")

# Actualizar stock de un producto (ej: vendiste 5 refrescos)
producto3.actualizar_stock(25)

# Mostrar inventario actualizado
mi_inventario.mostrar_inventario()

# Calcular valor total del inventario
mi_inventario.valor_total_inventario()
