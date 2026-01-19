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
