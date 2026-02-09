"""
Estructuras de datos personalizadas para el sistema de Credit Risk
Implementación de MinHeap y MaxHeap para manejo eficiente de datos
"""


class MinHeap:
    """
    MinHeap - Estructura de datos donde el padre es menor que sus hijos
    Útil para encontrar rápidamente las N mejores tasas de interés (más bajas)

    Complejidad:
    - Inserción: O(log n)
    - Extracción del mínimo: O(log n)
    - Obtener mínimo: O(1)
    """

    def __init__(self):
        self.heap = []

    def parent(self, i):
        """Retorna el índice del padre"""
        return (i - 1) // 2

    def left_child(self, i):
        """Retorna el índice del hijo izquierdo"""
        return 2 * i + 1

    def right_child(self, i):
        """Retorna el índice del hijo derecho"""
        return 2 * i + 2

    def swap(self, i, j):
        """Intercambia dos elementos en el heap"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, key):
        """
        Inserta un nuevo elemento en el heap
        Args:
            key: Elemento a insertar (puede ser número o tupla)
        """
        self.heap.append(key)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i):
        """Reorganiza el heap hacia arriba después de inserción"""
        parent = self.parent(i)
        if i > 0 and self.heap[i] < self.heap[parent]:
            self.swap(i, parent)
            self._heapify_up(parent)

    def extract_min(self):
        """
        Extrae y retorna el elemento mínimo del heap
        Returns:
            El elemento mínimo
        Raises:
            IndexError: Si el heap está vacío
        """
        if len(self.heap) == 0:
            raise IndexError("Heap vacío")

        if len(self.heap) == 1:
            return self.heap.pop()

        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return min_val

    def _heapify_down(self, i):
        """Reorganiza el heap hacia abajo después de extracción"""
        min_index = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < len(self.heap) and self.heap[left] < self.heap[min_index]:
            min_index = left

        if right < len(self.heap) and self.heap[right] < self.heap[min_index]:
            min_index = right

        if min_index != i:
            self.swap(i, min_index)
            self._heapify_down(min_index)

    def peek(self):
        """
        Retorna el elemento mínimo sin extraerlo
        Returns:
            El elemento mínimo
        """
        if len(self.heap) == 0:
            raise IndexError("Heap vacío")
        return self.heap[0]

    def size(self):
        """Retorna el tamaño del heap"""
        return len(self.heap)

    def is_empty(self):
        """Verifica si el heap está vacío"""
        return len(self.heap) == 0


class MaxHeap:
    """
    MaxHeap - Estructura de datos donde el padre es mayor que sus hijos
    Útil para encontrar rápidamente los N peores riesgos (más altos)

    Complejidad:
    - Inserción: O(log n)
    - Extracción del máximo: O(log n)
    - Obtener máximo: O(1)
    """

    def __init__(self):
        self.heap = []

    def parent(self, i):
        """Retorna el índice del padre"""
        return (i - 1) // 2

    def left_child(self, i):
        """Retorna el índice del hijo izquierdo"""
        return 2 * i + 1

    def right_child(self, i):
        """Retorna el índice del hijo derecho"""
        return 2 * i + 2

    def swap(self, i, j):
        """Intercambia dos elementos en el heap"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, key):
        """
        Inserta un nuevo elemento en el heap
        Args:
            key: Elemento a insertar (puede ser número o tupla)
        """
        self.heap.append(key)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i):
        """Reorganiza el heap hacia arriba después de inserción"""
        parent = self.parent(i)
        if i > 0 and self.heap[i] > self.heap[parent]:
            self.swap(i, parent)
            self._heapify_up(parent)

    def extract_max(self):
        """
        Extrae y retorna el elemento máximo del heap
        Returns:
            El elemento máximo
        Raises:
            IndexError: Si el heap está vacío
        """
        if len(self.heap) == 0:
            raise IndexError("Heap vacío")

        if len(self.heap) == 1:
            return self.heap.pop()

        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return max_val

    def _heapify_down(self, i):
        """Reorganiza el heap hacia abajo después de extracción"""
        max_index = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < len(self.heap) and self.heap[left] > self.heap[max_index]:
            max_index = left

        if right < len(self.heap) and self.heap[right] > self.heap[max_index]:
            max_index = right

        if max_index != i:
            self.swap(i, max_index)
            self._heapify_down(max_index)

    def peek(self):
        """
        Retorna el elemento máximo sin extraerlo
        Returns:
            El elemento máximo
        """
        if len(self.heap) == 0:
            raise IndexError("Heap vacío")
        return self.heap[0]

    def size(self):
        """Retorna el tamaño del heap"""
        return len(self.heap)

    def is_empty(self):
        """Verifica si el heap está vacío"""
        return len(self.heap) == 0


def get_top_n_min(data, n):
    """
    Obtiene los N elementos más pequeños usando MinHeap

    Args:
        data: Lista de elementos
        n: Número de elementos a obtener

    Returns:
        Lista con los N elementos más pequeños
    """
    heap = MinHeap()
    for item in data:
        heap.insert(item)

    result = []
    for _ in range(min(n, heap.size())):
        result.append(heap.extract_min())

    return result


def get_top_n_max(data, n):
    """
    Obtiene los N elementos más grandes usando MaxHeap

    Args:
        data: Lista de elementos
        n: Número de elementos a obtener

    Returns:
        Lista con los N elementos más grandes
    """
    heap = MaxHeap()
    for item in data:
        heap.insert(item)

    result = []
    for _ in range(min(n, heap.size())):
        result.append(heap.extract_max())

    return result


# =============================================================================
# ÁRBOLES BINARIOS DE BÚSQUEDA (BST)
# =============================================================================

class TreeNode:
    """
    Nodo para el Árbol Binario de Búsqueda

    Attributes:
        key: Valor clave para ordenamiento (ej: score de riesgo, monto)
        data: Datos adicionales asociados al nodo (ej: info del cliente)
        left: Referencia al hijo izquierdo
        right: Referencia al hijo derecho
    """

    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    """
    Árbol Binario de Búsqueda (BST)
    Útil para búsqueda, inserción y eliminación eficiente de datos ordenados

    Aplicación en Credit Risk:
    - Organizar clientes por score de riesgo
    - Búsqueda rápida de clientes por monto de préstamo
    - Encontrar rangos de clientes (ej: todos con score entre X e Y)

    Complejidad (caso promedio):
    - Búsqueda: O(log n)
    - Inserción: O(log n)
    - Eliminación: O(log n)

    Complejidad (peor caso - árbol degenerado):
    - Todas las operaciones: O(n)
    """

    def __init__(self):
        self.root = None
        self._size = 0

    def insert(self, key, data=None):
        """
        Inserta un nuevo nodo en el árbol

        Args:
            key: Valor clave para ordenamiento
            data: Datos adicionales asociados

        Returns:
            El nodo insertado
        """
        new_node = TreeNode(key, data)

        if self.root is None:
            self.root = new_node
            self._size += 1
            return new_node

        self._insert_recursive(self.root, new_node)
        self._size += 1
        return new_node

    def _insert_recursive(self, current, new_node):
        """Inserción recursiva en el subárbol"""
        if new_node.key < current.key:
            if current.left is None:
                current.left = new_node
            else:
                self._insert_recursive(current.left, new_node)
        else:
            if current.right is None:
                current.right = new_node
            else:
                self._insert_recursive(current.right, new_node)

    def search(self, key):
        """
        Busca un nodo por su clave

        Args:
            key: Valor a buscar

        Returns:
            El nodo encontrado o None si no existe
        """
        return self._search_recursive(self.root, key)

    def _search_recursive(self, current, key):
        """Búsqueda recursiva en el subárbol"""
        if current is None:
            return None

        if key == current.key:
            return current
        elif key < current.key:
            return self._search_recursive(current.left, key)
        else:
            return self._search_recursive(current.right, key)

    def delete(self, key):
        """
        Elimina un nodo del árbol

        Args:
            key: Valor del nodo a eliminar

        Returns:
            True si se eliminó, False si no se encontró
        """
        if self.search(key) is None:
            return False

        self.root = self._delete_recursive(self.root, key)
        self._size -= 1
        return True

    def _delete_recursive(self, current, key):
        """Eliminación recursiva en el subárbol"""
        if current is None:
            return None

        if key < current.key:
            current.left = self._delete_recursive(current.left, key)
        elif key > current.key:
            current.right = self._delete_recursive(current.right, key)
        else:
            # Nodo encontrado - 3 casos

            # Caso 1: Nodo sin hijos (hoja)
            if current.left is None and current.right is None:
                return None

            # Caso 2: Nodo con un solo hijo
            if current.left is None:
                return current.right
            if current.right is None:
                return current.left

            # Caso 3: Nodo con dos hijos
            # Encontrar el sucesor inorder (mínimo del subárbol derecho)
            successor = self._find_min_node(current.right)
            current.key = successor.key
            current.data = successor.data
            current.right = self._delete_recursive(current.right, successor.key)

        return current

    def find_min(self):
        """
        Encuentra el valor mínimo en el árbol

        Returns:
            El nodo con el valor mínimo o None si el árbol está vacío
        """
        if self.root is None:
            return None
        return self._find_min_node(self.root)

    def _find_min_node(self, node):
        """Encuentra el nodo mínimo en un subárbol"""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def find_max(self):
        """
        Encuentra el valor máximo en el árbol

        Returns:
            El nodo con el valor máximo o None si el árbol está vacío
        """
        if self.root is None:
            return None
        return self._find_max_node(self.root)

    def _find_max_node(self, node):
        """Encuentra el nodo máximo en un subárbol"""
        current = node
        while current.right is not None:
            current = current.right
        return current

    def inorder(self):
        """
        Recorrido Inorder (izquierda - raíz - derecha)
        Retorna los elementos en orden ascendente

        Returns:
            Lista de tuplas (key, data) en orden ascendente
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        """Recorrido inorder recursivo"""
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append((node.key, node.data))
            self._inorder_recursive(node.right, result)

    def preorder(self):
        """
        Recorrido Preorder (raíz - izquierda - derecha)
        Útil para copiar el árbol

        Returns:
            Lista de tuplas (key, data) en preorder
        """
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        """Recorrido preorder recursivo"""
        if node is not None:
            result.append((node.key, node.data))
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder(self):
        """
        Recorrido Postorder (izquierda - derecha - raíz)
        Útil para eliminar el árbol

        Returns:
            Lista de tuplas (key, data) en postorder
        """
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        """Recorrido postorder recursivo"""
        if node is not None:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append((node.key, node.data))

    def height(self):
        """
        Calcula la altura del árbol

        Returns:
            Altura del árbol (0 si está vacío)
        """
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        """Cálculo recursivo de altura"""
        if node is None:
            return 0
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        return 1 + max(left_height, right_height)

    def size(self):
        """Retorna el número de nodos en el árbol"""
        return self._size

    def is_empty(self):
        """Verifica si el árbol está vacío"""
        return self.root is None

    def range_search(self, min_key, max_key):
        """
        Busca todos los nodos dentro de un rango [min_key, max_key]

        Útil para encontrar clientes con score de riesgo en un rango específico

        Args:
            min_key: Límite inferior del rango (inclusivo)
            max_key: Límite superior del rango (inclusivo)

        Returns:
            Lista de tuplas (key, data) dentro del rango
        """
        result = []
        self._range_search_recursive(self.root, min_key, max_key, result)
        return result

    def _range_search_recursive(self, node, min_key, max_key, result):
        """Búsqueda en rango recursiva"""
        if node is None:
            return

        # Si el nodo actual es mayor que min_key, buscar en subárbol izquierdo
        if node.key > min_key:
            self._range_search_recursive(node.left, min_key, max_key, result)

        # Si el nodo está dentro del rango, agregarlo
        if min_key <= node.key <= max_key:
            result.append((node.key, node.data))

        # Si el nodo actual es menor que max_key, buscar en subárbol derecho
        if node.key < max_key:
            self._range_search_recursive(node.right, min_key, max_key, result)

    def level_order(self):
        """
        Recorrido por niveles (BFS - Breadth First Search)

        Returns:
            Lista de listas, donde cada sublista es un nivel del árbol
        """
        if self.root is None:
            return []

        result = []
        queue = [self.root]

        while queue:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                node = queue.pop(0)
                current_level.append((node.key, node.data))

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(current_level)

        return result


class CreditRiskBST(BinarySearchTree):
    """
    Árbol Binario de Búsqueda especializado para Riesgo Crediticio

    Extiende BinarySearchTree con métodos específicos para el dominio
    de análisis de riesgo crediticio.
    """

    def insert_client(self, risk_score, client_info):
        """
        Inserta un cliente ordenado por su score de riesgo

        Args:
            risk_score: Score de riesgo del cliente (0-100)
            client_info: Diccionario con información del cliente
        """
        return self.insert(risk_score, client_info)

    def find_high_risk_clients(self, threshold=70):
        """
        Encuentra todos los clientes con alto riesgo

        Args:
            threshold: Umbral de riesgo (default: 70)

        Returns:
            Lista de clientes con score >= threshold
        """
        return self.range_search(threshold, 100)

    def find_low_risk_clients(self, threshold=30):
        """
        Encuentra todos los clientes con bajo riesgo

        Args:
            threshold: Umbral de riesgo (default: 30)

        Returns:
            Lista de clientes con score <= threshold
        """
        return self.range_search(0, threshold)

    def find_medium_risk_clients(self, low=30, high=70):
        """
        Encuentra todos los clientes con riesgo medio

        Args:
            low: Límite inferior (default: 30)
            high: Límite superior (default: 70)

        Returns:
            Lista de clientes con score entre low y high
        """
        return self.range_search(low, high)

    def get_risk_distribution(self):
        """
        Obtiene la distribución de riesgo de todos los clientes

        Returns:
            Diccionario con conteo por categoría de riesgo
        """
        all_clients = self.inorder()

        distribution = {
            'bajo': 0,      # 0-30
            'medio': 0,     # 31-70
            'alto': 0       # 71-100
        }

        for score, _ in all_clients:
            if score <= 30:
                distribution['bajo'] += 1
            elif score <= 70:
                distribution['medio'] += 1
            else:
                distribution['alto'] += 1

        return distribution

    def get_clients_sorted_by_risk(self, ascending=True):
        """
        Obtiene todos los clientes ordenados por riesgo

        Args:
            ascending: Si True, orden ascendente (menor a mayor riesgo)

        Returns:
            Lista de clientes ordenados
        """
        clients = self.inorder()
        if not ascending:
            clients.reverse()
        return clients


def build_bst_from_list(data, key_func=None):
    """
    Construye un BST a partir de una lista de datos

    Args:
        data: Lista de elementos
        key_func: Función para extraer la clave de cada elemento
                  Si es None, se usa el elemento como clave

    Returns:
        BinarySearchTree con los datos insertados
    """
    bst = BinarySearchTree()

    for item in data:
        if key_func:
            key = key_func(item)
            bst.insert(key, item)
        else:
            bst.insert(item)

    return bst


def build_credit_bst_from_dataframe(df, score_column='risk_score'):
    """
    Construye un CreditRiskBST a partir de un DataFrame de pandas

    Args:
        df: DataFrame con datos de clientes
        score_column: Nombre de la columna con el score de riesgo

    Returns:
        CreditRiskBST con los clientes insertados
    """
    bst = CreditRiskBST()

    for idx, row in df.iterrows():
        risk_score = row[score_column]
        client_info = row.to_dict()
        bst.insert_client(risk_score, client_info)

    return bst
