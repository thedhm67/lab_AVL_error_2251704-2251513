import sys

# -------------------------------------------------------
# Clase que representa un nodo del árbol AVL
# -------------------------------------------------------
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # Todo nodo nuevo empieza con altura 1


# -------------------------------------------------------
# Funciones auxiliares
# -------------------------------------------------------

# Retorna la altura de un nodo (0 si es None)
def getHeight(node):
    if not node:
        return 0
    return node.height

# Calcula el factor de balance: altura izquierda - altura derecha
def getBalance(node):
    if not node:
        return 0
    return getHeight(node.left) - getHeight(node.right)

# Actualiza la altura de un nodo según sus hijos
def updateHeight(node):
    if node:
        node.height = 1 + max(getHeight(node.left), getHeight(node.right))


# -------------------------------------------------------
# Rotaciones para rebalancear el árbol
# -------------------------------------------------------

# Rotación simple a la derecha
def rotate_right(y):
    x = y.left
    T2 = x.right

    x.right = y
    y.left = T2

    updateHeight(y)
    updateHeight(x)

    return x  # x es la nueva raíz de este subárbol

# Rotación simple a la izquierda
def rotate_left(x):
    y = x.right
    T2 = y.left

    y.left = x
    x.right = T2

    updateHeight(x)
    updateHeight(y)

    return y  # y es la nueva raíz de este subárbol


# -------------------------------------------------------
# Función para encontrar el nodo con el valor mínimo
# (se usa en la eliminación)
# -------------------------------------------------------
def getMinNode(node):
    current = node
    while current.left is not None:
        current = current.left
    return current


# -------------------------------------------------------
# Clase principal del Árbol AVL
# -------------------------------------------------------
class AVLTree:
    def __init__(self):
        self.root = None

    # --------------------------------------------------
    # INSERCIÓN
    # --------------------------------------------------
    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        # Caso base: lugar vacío, se crea el nodo
        if not node:
            return Node(value)

        # Insertar en el subárbol correspondiente
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node  # Valores duplicados no se insertan

        # Actualizar altura del nodo actual
        updateHeight(node)

        # Calcular el factor de balance
        balance = getBalance(node)

        # --- Caso 1: Desbalance izquierda-izquierda → rotación derecha simple ---
        if balance > 1 and getBalance(node.left) >= 0:
            node = rotate_right(node)  # ERROR ORIGINAL: faltaba "node ="

        # --- Caso 2: Desbalance izquierda-derecha → rotación doble ---
        elif balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            node = rotate_right(node)  # ERROR ORIGINAL: faltaba "node ="

        # --- Caso 3: Desbalance derecha-derecha → rotación izquierda simple ---
        elif balance < -1 and getBalance(node.right) <= 0:
            node = rotate_left(node)  # ERROR ORIGINAL: faltaba "node ="

        # --- Caso 4: Desbalance derecha-izquierda → rotación doble ---
        elif balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            node = rotate_left(node)  # ERROR ORIGINAL: faltaba "node ="

        return node

    # --------------------------------------------------
    # ELIMINACIÓN
    # --------------------------------------------------
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        # Caso base: el valor no está en el árbol
        if not node:
            print(f"El valor {value} no se encontró en el árbol.")
            return node

        # Buscar el nodo a eliminar
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Nodo encontrado, hay 3 casos:

            # Caso A: nodo con solo hijo derecho o sin hijos
            if node.left is None:
                return node.right

            # Caso B: nodo con solo hijo izquierdo
            elif node.right is None:
                return node.left

            # Caso C: nodo con dos hijos
            # Se reemplaza con el sucesor en inorden (mínimo del subárbol derecho)
            sucesor = getMinNode(node.right)
            node.value = sucesor.value
            node.right = self._delete_recursive(node.right, sucesor.value)

        # Actualizar altura
        updateHeight(node)

        # Calcular balance y rebalancear si es necesario
        balance = getBalance(node)

        # Caso 1: Desbalance izquierda-izquierda
        if balance > 1 and getBalance(node.left) >= 0:
            node = rotate_right(node)

        # Caso 2: Desbalance izquierda-derecha
        elif balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            node = rotate_right(node)

        # Caso 3: Desbalance derecha-derecha
        elif balance < -1 and getBalance(node.right) <= 0:
            node = rotate_left(node)

        # Caso 4: Desbalance derecha-izquierda
        elif balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            node = rotate_left(node)

        return node

    # --------------------------------------------------
    # RECORRIDO IN-ORDER (devuelve elementos en orden ascendente)
    # --------------------------------------------------
    def inorder(self):
        resultado = []
        self._inorder_recursive(self.root, resultado)
        return resultado

    def _inorder_recursive(self, node, resultado):
        if node:
            self._inorder_recursive(node.left, resultado)
            resultado.append(node.value)
            self._inorder_recursive(node.right, resultado)

    # --------------------------------------------------
    # VISUALIZACIÓN del árbol (muestra valor, altura y balance)
    # --------------------------------------------------
    def visualizar(self):
        if not self.root:
            print("El árbol está vacío.")
            return
        print("\n--- Visualización del árbol AVL ---")
        self._visualizar_recursive(self.root, "", True)
        print()

    def _visualizar_recursive(self, node, prefijo, es_derecha):
        if node:
            # Mostrar el hijo derecho primero (aparece arriba en consola)
            self._visualizar_recursive(node.right, prefijo + ("│   " if not es_derecha else "    "), False)

            # Mostrar el nodo actual con su valor, altura y factor de balance
            conector = "└── " if es_derecha else "┌── "
            print(prefijo + conector + f"[{node.value}] h={node.height} b={getBalance(node)}")

            # Mostrar el hijo izquierdo
            self._visualizar_recursive(node.left, prefijo + ("    " if not es_derecha else "│   "), True)


# -------------------------------------------------------
# PRUEBAS
# -------------------------------------------------------

avl = AVLTree()
values_to_insert = [10, 20, 30, 40, 50, 25]

print("Insertando valores:", values_to_insert)
for val in values_to_insert:
    avl.insert(val)

print("\n--- Después de inserciones ---")
avl.visualizar()
print("Recorrido in-order:", avl.inorder())

print("\nEliminando el valor 40...")
avl.delete(40)
print("\n--- Después de eliminar 40 ---")
avl.visualizar()
print("Recorrido in-order:", avl.inorder())

print("\nEliminando el valor 10...")
avl.delete(10)
print("\n--- Después de eliminar 10 ---")
avl.visualizar()
print("Recorrido in-order:", avl.inorder())

print("\nIntentando eliminar un valor que no existe (99)...")
avl.delete(99)
