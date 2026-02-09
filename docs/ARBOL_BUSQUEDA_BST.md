# Arbol Binario de Busqueda (BST) - Sistema de Riesgo Crediticio

## Tabla de Contenidos

1. [Introduccion](#introduccion)
2. [Que es un Arbol Binario de Busqueda](#que-es-un-arbol-binario-de-busqueda)
3. [Aplicacion en el Sistema de Riesgo Crediticio](#aplicacion-en-el-sistema-de-riesgo-crediticio)
4. [Estructura del Codigo](#estructura-del-codigo)
5. [Operaciones Implementadas](#operaciones-implementadas)
6. [Visualizacion Web](#visualizacion-web)
7. [Complejidad Algoritmica](#complejidad-algoritmica)
8. [Ventajas del BST](#ventajas-del-bst)

---

## Introduccion

Este documento explica la implementacion del **Arbol Binario de Busqueda (BST)** en el Sistema de Prediccion de Riesgo Crediticio. El BST se utiliza para organizar y buscar clientes de manera eficiente segun su score de riesgo crediticio.

---

## Que es un Arbol Binario de Busqueda

Un **Arbol Binario de Busqueda (BST)** es una estructura de datos jerarquica donde:

- Cada nodo tiene **como maximo dos hijos** (izquierdo y derecho)
- Para cada nodo:
  - Todos los valores en el **subarbol izquierdo** son **menores** que el nodo
  - Todos los valores en el **subarbol derecho** son **mayores** que el nodo

### Representacion Visual

```
           50 (raiz)
          /  \
        30    70
       /  \     \
     20   40    85
```

En este ejemplo:
- 50 es la raiz
- 30 y 70 son hijos de 50
- 20, 40 son hijos de 30
- 85 es hijo de 70

### Propiedad Fundamental

Si recorremos el arbol en **orden inorder** (izquierda → raiz → derecha), obtenemos los elementos **ordenados de menor a mayor**:

```
20 → 30 → 40 → 50 → 70 → 85
```

---

## Aplicacion en el Sistema de Riesgo Crediticio

### Por que usamos BST para Riesgo Crediticio?

En nuestro sistema, cada cliente tiene un **score de riesgo** (0-100):
- **0-30**: Riesgo Bajo (cliente confiable)
- **31-70**: Riesgo Medio (requiere evaluacion)
- **71-100**: Riesgo Alto (cliente riesgoso)

El BST nos permite:

1. **Organizar clientes por riesgo**: Los clientes quedan ordenados automaticamente
2. **Busqueda rapida**: Encontrar un cliente por score en O(log n)
3. **Busqueda en rango**: Encontrar todos los clientes entre score X e Y eficientemente
4. **Encontrar extremos**: Cliente con menor/mayor riesgo en O(log n)

### Ejemplo Practico

```
Clientes insertados:
- Cliente A: Score 85 (Alto riesgo)
- Cliente B: Score 25 (Bajo riesgo)
- Cliente C: Score 55 (Medio riesgo)
- Cliente D: Score 92 (Alto riesgo)
- Cliente E: Score 15 (Bajo riesgo)

Arbol resultante:
           85
          /  \
        25    92
       /  \
     15    55
```

Ahora podemos:
- Buscar clientes de alto riesgo (>70): 85, 92
- Buscar clientes de bajo riesgo (<30): 15, 25
- Encontrar el cliente mas riesgoso: 92
- Encontrar el cliente menos riesgoso: 15

---

## Estructura del Codigo

### Archivo: `src/data_structures.py`

#### 1. Clase TreeNode (Nodo del Arbol)

```python
class TreeNode:
    """
    Nodo para el Arbol Binario de Busqueda
    """
    def __init__(self, key, data=None):
        self.key = key      # Score de riesgo (valor para ordenar)
        self.data = data    # Datos del cliente
        self.left = None    # Hijo izquierdo (scores menores)
        self.right = None   # Hijo derecho (scores mayores)
```

**Que hace:**
- `key`: Es el valor que usamos para ordenar (el score de riesgo)
- `data`: Informacion adicional del cliente (nombre, monto, etc.)
- `left`: Referencia al hijo izquierdo
- `right`: Referencia al hijo derecho

**Por que es importante:**
- Es la unidad basica del arbol
- Permite almacenar tanto el score como los datos del cliente
- Las referencias left/right permiten navegar el arbol

---

#### 2. Clase BinarySearchTree (Arbol Principal)

```python
class BinarySearchTree:
    def __init__(self):
        self.root = None    # Raiz del arbol
        self._size = 0      # Cantidad de nodos
```

**Que hace:**
- `root`: Apunta al primer nodo (raiz) del arbol
- `_size`: Contador de cuantos nodos tiene el arbol

---

#### 3. Metodo Insert (Insercion)

```python
def insert(self, key, data=None):
    new_node = TreeNode(key, data)

    if self.root is None:
        self.root = new_node  # Si el arbol esta vacio, el nuevo nodo es la raiz
        self._size += 1
        return new_node

    self._insert_recursive(self.root, new_node)
    self._size += 1
    return new_node

def _insert_recursive(self, current, new_node):
    if new_node.key < current.key:
        # Si es menor, va a la izquierda
        if current.left is None:
            current.left = new_node
        else:
            self._insert_recursive(current.left, new_node)
    else:
        # Si es mayor o igual, va a la derecha
        if current.right is None:
            current.right = new_node
        else:
            self._insert_recursive(current.right, new_node)
```

**Que hace:**
1. Crea un nuevo nodo con el score y datos
2. Si el arbol esta vacio, el nuevo nodo se convierte en raiz
3. Si no, busca recursivamente la posicion correcta:
   - Si el score es menor que el nodo actual → ir a la izquierda
   - Si el score es mayor o igual → ir a la derecha
4. Cuando encuentra un espacio vacio (None), inserta el nodo

**Por que es importante:**
- Mantiene la propiedad del BST automaticamente
- Cada insercion toma O(log n) en promedio
- El arbol se construye de forma ordenada

---

#### 4. Metodo Search (Busqueda)

```python
def search(self, key):
    return self._search_recursive(self.root, key)

def _search_recursive(self, current, key):
    if current is None:
        return None  # No encontrado

    if key == current.key:
        return current  # Encontrado!
    elif key < current.key:
        return self._search_recursive(current.left, key)  # Buscar a la izquierda
    else:
        return self._search_recursive(current.right, key)  # Buscar a la derecha
```

**Que hace:**
1. Compara el valor buscado con el nodo actual
2. Si es igual, lo encontro
3. Si es menor, busca en el subarbol izquierdo
4. Si es mayor, busca en el subarbol derecho
5. Si llega a None, el valor no existe

**Por que es importante:**
- Busqueda eficiente O(log n)
- En cada paso descarta la mitad del arbol
- Mucho mas rapido que buscar en una lista O(n)

---

#### 5. Metodo Delete (Eliminacion)

```python
def delete(self, key):
    if self.search(key) is None:
        return False  # No existe

    self.root = self._delete_recursive(self.root, key)
    self._size -= 1
    return True

def _delete_recursive(self, current, key):
    if current is None:
        return None

    if key < current.key:
        current.left = self._delete_recursive(current.left, key)
    elif key > current.key:
        current.right = self._delete_recursive(current.right, key)
    else:
        # Nodo encontrado - 3 casos:

        # Caso 1: Nodo sin hijos (hoja)
        if current.left is None and current.right is None:
            return None

        # Caso 2: Nodo con un solo hijo
        if current.left is None:
            return current.right
        if current.right is None:
            return current.left

        # Caso 3: Nodo con dos hijos
        # Encontrar el sucesor inorder (minimo del subarbol derecho)
        successor = self._find_min_node(current.right)
        current.key = successor.key
        current.data = successor.data
        current.right = self._delete_recursive(current.right, successor.key)

    return current
```

**Que hace:**
- **Caso 1 (hoja)**: Simplemente elimina el nodo
- **Caso 2 (un hijo)**: Reemplaza el nodo con su unico hijo
- **Caso 3 (dos hijos)**: Encuentra el sucesor inorder y lo usa como reemplazo

**Por que es importante:**
- Permite remover clientes del sistema
- Mantiene la propiedad del BST despues de eliminar
- Maneja los 3 casos posibles de eliminacion

---

#### 6. Recorridos del Arbol

##### Inorder (Izquierda → Raiz → Derecha)

```python
def inorder(self):
    result = []
    self._inorder_recursive(self.root, result)
    return result

def _inorder_recursive(self, node, result):
    if node is not None:
        self._inorder_recursive(node.left, result)   # 1. Visitar izquierda
        result.append((node.key, node.data))          # 2. Visitar raiz
        self._inorder_recursive(node.right, result)  # 3. Visitar derecha
```

**Resultado:** Elementos en orden ascendente (ordenados de menor a mayor)

**Uso:** Obtener todos los clientes ordenados por score de riesgo

---

##### Preorder (Raiz → Izquierda → Derecha)

```python
def preorder(self):
    result = []
    self._preorder_recursive(self.root, result)
    return result

def _preorder_recursive(self, node, result):
    if node is not None:
        result.append((node.key, node.data))          # 1. Visitar raiz
        self._preorder_recursive(node.left, result)   # 2. Visitar izquierda
        self._preorder_recursive(node.right, result)  # 3. Visitar derecha
```

**Resultado:** La raiz primero, luego sus descendientes

**Uso:** Copiar la estructura del arbol, serializar para guardar

---

##### Postorder (Izquierda → Derecha → Raiz)

```python
def postorder(self):
    result = []
    self._postorder_recursive(self.root, result)
    return result

def _postorder_recursive(self, node, result):
    if node is not None:
        self._postorder_recursive(node.left, result)   # 1. Visitar izquierda
        self._postorder_recursive(node.right, result)  # 2. Visitar derecha
        result.append((node.key, node.data))            # 3. Visitar raiz
```

**Resultado:** Las hojas primero, la raiz al final

**Uso:** Eliminar el arbol de forma segura (hijos antes que padres)

---

##### Level Order (Por Niveles - BFS)

```python
def level_order(self):
    if self.root is None:
        return []

    result = []
    queue = [self.root]  # Cola para BFS

    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            node = queue.pop(0)  # Sacar el primero de la cola
            current_level.append((node.key, node.data))

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)

    return result
```

**Resultado:** Nivel por nivel, de arriba hacia abajo

**Uso:** Visualizar la estructura del arbol, BFS (Breadth-First Search)

---

#### 7. Busqueda en Rango

```python
def range_search(self, min_key, max_key):
    result = []
    self._range_search_recursive(self.root, min_key, max_key, result)
    return result

def _range_search_recursive(self, node, min_key, max_key, result):
    if node is None:
        return

    # Si el nodo es mayor que min, buscar en izquierda
    if node.key > min_key:
        self._range_search_recursive(node.left, min_key, max_key, result)

    # Si el nodo esta en el rango, agregarlo
    if min_key <= node.key <= max_key:
        result.append((node.key, node.data))

    # Si el nodo es menor que max, buscar en derecha
    if node.key < max_key:
        self._range_search_recursive(node.right, min_key, max_key, result)
```

**Que hace:**
1. Solo visita los subarboles que pueden contener valores en el rango
2. Agrega al resultado los nodos que estan dentro del rango
3. Evita visitar nodos que estan fuera del rango

**Por que es importante:**
- Complejidad O(log n + k) donde k es el numero de resultados
- Muy eficiente para encontrar clientes en un rango de riesgo
- Ejemplo: "Todos los clientes con riesgo entre 50 y 80"

---

#### 8. Clase CreditRiskBST (Especializada)

```python
class CreditRiskBST(BinarySearchTree):
    """
    Arbol especializado para Riesgo Crediticio
    """

    def insert_client(self, risk_score, client_info):
        """Inserta un cliente por su score de riesgo"""
        return self.insert(risk_score, client_info)

    def find_high_risk_clients(self, threshold=70):
        """Encuentra clientes de alto riesgo (score >= threshold)"""
        return self.range_search(threshold, 100)

    def find_low_risk_clients(self, threshold=30):
        """Encuentra clientes de bajo riesgo (score <= threshold)"""
        return self.range_search(0, threshold)

    def find_medium_risk_clients(self, low=30, high=70):
        """Encuentra clientes de riesgo medio"""
        return self.range_search(low, high)

    def get_risk_distribution(self):
        """Obtiene la distribucion de riesgo"""
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
```

**Por que es importante:**
- Extiende el BST generico con metodos especificos para riesgo
- Hace el codigo mas legible y facil de usar
- Encapsula la logica de negocio (umbrales de riesgo)

---

## Visualizacion Web

### Archivo: `templates/arbol.html`

La pagina web muestra:

#### 1. Estadisticas del Arbol
- Total de nodos (clientes en el arbol)
- Altura del arbol
- Score minimo y maximo

#### 2. Visualizacion Grafica con D3.js

```javascript
// Crear layout del arbol
var treeLayout = d3.tree().size([width, height]);

// Crear jerarquia desde JSON
var root = d3.hierarchy(treeData);

// Aplicar layout
treeLayout(root);

// Dibujar enlaces (lineas)
svg.selectAll(".link")
    .data(root.links())
    .enter()
    .append("path")
    .attr("d", d3.linkVertical());

// Dibujar nodos (circulos)
nodes.append("circle")
    .attr("r", 20)
    .attr("fill", d => getRiskColor(d.data.key));
```

**Colores por riesgo:**
- Verde (#2ecc71): Riesgo Bajo (0-30)
- Amarillo (#f39c12): Riesgo Medio (31-70)
- Rojo (#e74c3c): Riesgo Alto (71-100)

#### 3. Tabs de Recorridos
- Inorder: Muestra clientes ordenados
- Preorder: Muestra estructura del arbol
- Postorder: Muestra orden de eliminacion
- Por Niveles: Muestra nivel por nivel

#### 4. Busqueda en Rango
- Formulario para ingresar score minimo y maximo
- Muestra los clientes encontrados en ese rango

---

### Archivo: `app.py` - Ruta /arbol

```python
@app.route('/arbol')
def arbol():
    # 1. Cargar datos
    df = pd.read_csv(config.RAW_DATA_FILE)

    # 2. Calcular scores de riesgo
    for idx, row in df.iterrows():
        base_score = row['loan_status'] * 50
        interest_factor = min(row['loan_int_rate'] / 25 * 30, 30)
        income_factor = min(row['loan_percent_income'] * 50, 20)
        score = base_score + interest_factor + income_factor
        risk_scores.append(int(score))

    # 3. Construir el BST
    bst = CreditRiskBST()
    for idx in sample_indices:
        bst.insert_client(risk_scores[idx], client_data)

    # 4. Obtener datos para la vista
    traversals = {
        'inorder': bst.inorder(),
        'preorder': bst.preorder(),
        'postorder': bst.postorder(),
        'levelorder': bst.level_order()
    }

    # 5. Convertir a JSON para D3.js
    tree_json = json.dumps(tree_to_dict(bst.root))

    return render_template('arbol.html', ...)
```

---

## Complejidad Algoritmica

| Operacion | Caso Promedio | Peor Caso | Descripcion |
|-----------|---------------|-----------|-------------|
| Busqueda | O(log n) | O(n) | Encontrar un cliente por score |
| Insercion | O(log n) | O(n) | Agregar nuevo cliente |
| Eliminacion | O(log n) | O(n) | Remover cliente |
| Minimo/Maximo | O(log n) | O(n) | Encontrar extremos |
| Recorridos | O(n) | O(n) | Visitar todos los nodos |
| Busqueda en Rango | O(log n + k) | O(n) | k = resultados encontrados |

### Por que O(log n)?

En cada paso de busqueda, descartamos la mitad del arbol:
- Arbol con 1000 nodos: ~10 comparaciones
- Arbol con 1,000,000 nodos: ~20 comparaciones

### Cuando es O(n) (Peor caso)?

Cuando el arbol esta **desbalanceado** (todos los nodos en una linea):

```
1
 \
  2
   \
    3
     \
      4  ← Esto es una lista, no un arbol!
```

---

## Ventajas del BST

### 1. Eficiencia en Busqueda
- **Lista**: Buscar entre 10,000 clientes = 10,000 comparaciones
- **BST**: Buscar entre 10,000 clientes = ~13 comparaciones

### 2. Datos Siempre Ordenados
- Al insertar, los datos quedan ordenados automaticamente
- Recorrido inorder da los clientes de menor a mayor riesgo

### 3. Busqueda en Rango Eficiente
- "Todos los clientes con riesgo 50-80" es muy rapido
- Solo visita los nodos necesarios

### 4. Operaciones Dinamicas
- Insertar y eliminar sin reorganizar toda la estructura
- Ideal para sistemas con datos que cambian frecuentemente

### 5. Jerarquia Natural
- La visualizacion ayuda a entender la distribucion de riesgo
- Facil de ver donde se concentran los clientes

---

## Conclusion

El **Arbol Binario de Busqueda** es una estructura de datos fundamental que permite:

1. **Organizar** clientes por score de riesgo de forma eficiente
2. **Buscar** clientes rapidamente en O(log n)
3. **Visualizar** la distribucion de riesgo de forma jerarquica
4. **Filtrar** clientes por rangos de riesgo
5. **Mantener** datos ordenados sin esfuerzo adicional

En el contexto del **Sistema de Riesgo Crediticio**, el BST proporciona una forma elegante y eficiente de gestionar y analizar la cartera de clientes segun su nivel de riesgo.

---

## Referencias

- Cormen, T. H., et al. "Introduction to Algorithms" - Capitulo 12: Binary Search Trees
- Documentacion D3.js: https://d3js.org/
- Flask Documentation: https://flask.palletsprojects.com/

---

**Autor:** Grupo 5
**Universidad:** UNACH - Ciencia de Datos e Inteligencia Artificial
**Fecha:** 2025
