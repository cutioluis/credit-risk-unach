# GUION DE PRESENTACION: Arbol Binario de Busqueda (BST)

## Sistema de Prediccion de Riesgo Crediticio

### Universidad Nacional de Chimborazo - UNACH
### Ciencia de Datos e Inteligencia Artificial
### Grupo 5 - 2025

---

# INTRODUCCION PARA EL PRESENTADOR

Este documento es un **guion tecnico** para presentar el modulo de Arboles Binarios de Busqueda (BST) del Sistema de Riesgo Crediticio. Cada seccion incluye:

- **QUE DECIR**: El texto para explicar
- **QUE MOSTRAR**: Lo que debe estar en pantalla
- **POR QUE SE HIZO ASI**: Justificacion tecnica
- **PARA QUE SIRVE**: Aplicacion practica

---

# SECCION 1: INTRODUCCION AL PROBLEMA

## QUE DECIR:

"Antes de hablar del arbol de busqueda, necesitamos entender el problema que resolvemos.

En un sistema de riesgo crediticio, tenemos **miles de clientes**, cada uno con un **score de riesgo** que va de 0 a 100. Este score indica la probabilidad de que el cliente NO pague su deuda.

El problema es: **¿Como organizamos estos datos para buscarlos eficientemente?**

Si usamos una **lista simple**, para buscar un cliente tendriamos que revisar uno por uno. Con 10,000 clientes, podriamos necesitar hasta 10,000 comparaciones. Esto es **O(n)** - tiempo lineal.

Aqui es donde entra el **Arbol Binario de Busqueda**. Con un BST, podemos reducir esas 10,000 comparaciones a solo **13 o 14**. Esto es **O(log n)** - tiempo logaritmico."

## QUE MOSTRAR:

```
COMPARACION DE EFICIENCIA:

Clientes    |  Lista O(n)    |  Arbol O(log n)
------------|----------------|------------------
100         |  100 pasos     |  7 pasos
1,000       |  1,000 pasos   |  10 pasos
10,000      |  10,000 pasos  |  13 pasos
100,000     |  100,000 pasos |  17 pasos
1,000,000   |  1,000,000     |  20 pasos
```

## POR QUE SE HIZO ASI:

Elegimos el BST porque:
1. **Eficiencia**: Busqueda en O(log n) vs O(n) de una lista
2. **Ordenamiento automatico**: Los datos quedan ordenados al insertarlos
3. **Busqueda en rango**: Podemos encontrar todos los clientes entre score X e Y eficientemente
4. **Estructura didactica**: Es una estructura fundamental en ciencias de la computacion

## PARA QUE SIRVE:

- Buscar clientes rapidamente por su score de riesgo
- Obtener clientes ordenados de menor a mayor riesgo
- Filtrar clientes por rangos de riesgo (ej: todos los de alto riesgo)
- Encontrar el cliente con menor/mayor riesgo instantaneamente

---

# SECCION 2: ¿QUE ES UN ARBOL BINARIO DE BUSQUEDA?

## QUE DECIR:

"Un Arbol Binario de Busqueda es una estructura de datos jerarquica con las siguientes propiedades:

**Propiedad 1 - Estructura Binaria:**
Cada nodo tiene como maximo DOS hijos: uno izquierdo y uno derecho.

**Propiedad 2 - Ordenamiento:**
Para CUALQUIER nodo en el arbol:
- Todos los valores en su subarbol IZQUIERDO son MENORES que el nodo
- Todos los valores en su subarbol DERECHO son MAYORES que el nodo

**Propiedad 3 - Recursividad:**
Cada subarbol es tambien un BST valido. Esta propiedad recursiva es la clave de su eficiencia.

Veamos como se construye un arbol con los valores: 50, 30, 70, 20, 40, 85"

## QUE MOSTRAR:

```
CONSTRUCCION PASO A PASO:

Insertar 50: (raiz)          Insertar 30: (30 < 50)       Insertar 70: (70 > 50)

      50                           50                           50
                                  /                            /  \
                                 30                           30   70


Insertar 20: (20<50, 20<30)  Insertar 40: (40<50, 40>30)  Insertar 85: (85>50, 85>70)

      50                           50                           50
     /  \                         /  \                         /  \
    30   70                      30   70                      30   70
   /                            /  \                         /  \    \
  20                           20  40                       20  40   85
```

## POR QUE SE HIZO ASI:

La propiedad de ordenamiento (izquierda menor, derecha mayor) permite:

1. **Busqueda por descarte**: En cada comparacion, descartamos la mitad del arbol
2. **Insercion ordenada**: No necesitamos ordenar despues, el arbol se auto-ordena
3. **Recorrido Inorder**: Al visitar izq-raiz-der, obtenemos elementos ordenados

## PARA QUE SIRVE:

```python
# En nuestro codigo (data_structures.py):

class TreeNode:
    def __init__(self, key, data=None):
        self.key = key      # Score de riesgo (0-100)
        self.data = data    # Informacion del cliente
        self.left = None    # Clientes con MENOR riesgo
        self.right = None   # Clientes con MAYOR riesgo
```

El `key` es el score de riesgo que usamos para ordenar. El `data` contiene la informacion adicional del cliente (nombre, monto del prestamo, etc).

---

# SECCION 3: OPERACION INSERT (INSERCION)

## QUE DECIR:

"La operacion de insercion es fundamental. Veamos como funciona paso a paso.

**Algoritmo:**
1. Si el arbol esta vacio, el nuevo nodo se convierte en la raiz
2. Si no, comparamos el valor a insertar con el nodo actual:
   - Si es MENOR, vamos al subarbol izquierdo
   - Si es MAYOR o IGUAL, vamos al subarbol derecho
3. Repetimos hasta encontrar una posicion vacia (None)
4. Insertamos el nuevo nodo en esa posicion

**Complejidad:** O(log n) en promedio, O(n) en el peor caso (arbol degenerado)"

## QUE MOSTRAR:

```python
# Codigo real de nuestro sistema (data_structures.py lineas 284-310):

def insert(self, key, data=None):
    """Inserta un nuevo nodo en el arbol"""
    new_node = TreeNode(key, data)

    if self.root is None:
        # Caso base: arbol vacio
        self.root = new_node
        self._size += 1
        return new_node

    # Caso recursivo: buscar posicion correcta
    self._insert_recursive(self.root, new_node)
    self._size += 1
    return new_node

def _insert_recursive(self, current, new_node):
    """Busca recursivamente la posicion correcta"""
    if new_node.key < current.key:
        # Menor: ir a la izquierda
        if current.left is None:
            current.left = new_node  # Posicion encontrada
        else:
            self._insert_recursive(current.left, new_node)
    else:
        # Mayor o igual: ir a la derecha
        if current.right is None:
            current.right = new_node  # Posicion encontrada
        else:
            self._insert_recursive(current.right, new_node)
```

## POR QUE SE HIZO ASI:

1. **Recursividad**: Usamos recursion porque el arbol es una estructura recursiva por naturaleza. Cada subarbol es un arbol valido.

2. **Comparacion simple**: Solo necesitamos comparar con el nodo actual para decidir izquierda o derecha.

3. **Sin reordenamiento**: A diferencia de una lista ordenada, no necesitamos mover elementos. Solo agregamos el nuevo nodo en la posicion correcta.

## PARA QUE SIRVE:

En el contexto de riesgo crediticio:
```python
# Insertar un nuevo cliente al sistema
bst.insert(75, {'nombre': 'Juan Perez', 'monto': 5000})

# El cliente con score 75 (alto riesgo) se ubicara
# automaticamente en la parte derecha del arbol
# junto con otros clientes de alto riesgo
```

---

# SECCION 4: OPERACION SEARCH (BUSQUEDA)

## QUE DECIR:

"La busqueda es donde el BST muestra su verdadero poder. Veamos como funciona:

**Algoritmo:**
1. Empezamos en la raiz
2. Comparamos el valor buscado con el nodo actual:
   - Si es IGUAL, lo encontramos
   - Si es MENOR, buscamos en el subarbol izquierdo
   - Si es MAYOR, buscamos en el subarbol derecho
3. Si llegamos a None, el valor no existe

**La clave:** En cada paso descartamos aproximadamente la MITAD del arbol. Por eso es O(log n)."

## QUE MOSTRAR:

```python
# Codigo real de nuestro sistema (data_structures.py lineas 312-330):

def search(self, key):
    """Busca un nodo por su clave"""
    return self._search_recursive(self.root, key)

def _search_recursive(self, current, key):
    """Busqueda recursiva"""
    # Caso base 1: no encontrado
    if current is None:
        return None

    # Caso base 2: encontrado
    if key == current.key:
        return current

    # Caso recursivo: seguir buscando
    elif key < current.key:
        return self._search_recursive(current.left, key)
    else:
        return self._search_recursive(current.right, key)
```

## EJEMPLO VISUAL:

```
Buscar el score 40 en este arbol:

        50          Paso 1: 40 < 50, voy a IZQUIERDA
       /  \
      30   70       Paso 2: 40 > 30, voy a DERECHA
     /  \    \
    20  40   85     Paso 3: 40 == 40, ENCONTRADO!

Solo 3 comparaciones para encontrar el valor.
```

## POR QUE SE HIZO ASI:

1. **Divide y venceras**: Cada comparacion reduce el espacio de busqueda a la mitad
2. **Sin necesidad de recorrer todo**: A diferencia de una lista, no revisamos todos los elementos
3. **Estructura natural**: La busqueda sigue la misma logica que la insercion

## PARA QUE SIRVE:

```python
# Buscar un cliente especifico por su score
cliente = bst.search(75)
if cliente:
    print(f"Cliente encontrado: {cliente.data}")
else:
    print("Cliente no encontrado")
```

---

# SECCION 5: RECORRIDO INORDER (EN ORDEN)

## QUE DECIR:

"El recorrido Inorder es uno de los mas importantes del BST. Visita los nodos en este orden:
1. Primero el subarbol IZQUIERDO
2. Luego la RAIZ
3. Finalmente el subarbol DERECHO

**Propiedad clave:** En un BST, el recorrido Inorder produce los elementos en orden ASCENDENTE. Esto es una consecuencia directa de la propiedad del BST (izquierda < raiz < derecha)."

## QUE MOSTRAR:

```python
# Codigo real (data_structures.py lineas 398-412):

def inorder(self):
    """Recorrido Inorder - retorna elementos ordenados"""
    result = []
    self._inorder_recursive(self.root, result)
    return result

def _inorder_recursive(self, node, result):
    if node is not None:
        # 1. Visitar subarbol izquierdo
        self._inorder_recursive(node.left, result)

        # 2. Visitar raiz (nodo actual)
        result.append((node.key, node.data))

        # 3. Visitar subarbol derecho
        self._inorder_recursive(node.right, result)
```

## EJEMPLO VISUAL:

```
Arbol:
        50
       /  \
      30   70
     /  \    \
    20  40   85

Recorrido Inorder paso a paso:

1. inorder(50) -> primero izquierda
2.   inorder(30) -> primero izquierda
3.     inorder(20) -> primero izquierda
4.       inorder(None) -> retorna
5.     VISITA 20 ✓
6.       inorder(None) -> retorna
7.   VISITA 30 ✓
8.     inorder(40) -> primero izquierda
9.       inorder(None) -> retorna
10.    VISITA 40 ✓
11.      inorder(None) -> retorna
12. VISITA 50 ✓
13.   inorder(70) -> primero izquierda
14.     inorder(None) -> retorna
15.   VISITA 70 ✓
16.     inorder(85)
17.       inorder(None) -> retorna
18.     VISITA 85 ✓
19.       inorder(None) -> retorna

Resultado: [20, 30, 40, 50, 70, 85] <- ¡ORDENADO!
```

## POR QUE SE HIZO ASI:

1. **Orden garantizado**: La propiedad del BST garantiza que izquierda < raiz < derecha
2. **Recursion natural**: El algoritmo refleja la estructura recursiva del arbol
3. **Complejidad O(n)**: Visitamos cada nodo exactamente una vez

## PARA QUE SIRVE:

```python
# Obtener todos los clientes ordenados por riesgo
clientes_ordenados = bst.inorder()

# Resultado: [(15, cliente1), (25, cliente2), (50, cliente3), ...]
# Ordenados de MENOR a MAYOR riesgo

# Util para:
# - Generar reportes ordenados
# - Ver clientes del mas seguro al mas riesgoso
# - Exportar datos ordenados
```

---

# SECCION 6: RECORRIDO PREORDER

## QUE DECIR:

"El recorrido Preorder visita los nodos en este orden:
1. Primero la RAIZ
2. Luego el subarbol IZQUIERDO
3. Finalmente el subarbol DERECHO

**Caracteristica principal:** La raiz se visita ANTES que sus hijos. Esto es util cuando necesitamos procesar un nodo antes de procesar sus descendientes."

## QUE MOSTRAR:

```python
# Codigo real (data_structures.py lineas 414-428):

def preorder(self):
    """Recorrido Preorder - raiz primero"""
    result = []
    self._preorder_recursive(self.root, result)
    return result

def _preorder_recursive(self, node, result):
    if node is not None:
        # 1. Visitar raiz PRIMERO
        result.append((node.key, node.data))

        # 2. Visitar subarbol izquierdo
        self._preorder_recursive(node.left, result)

        # 3. Visitar subarbol derecho
        self._preorder_recursive(node.right, result)
```

## EJEMPLO VISUAL:

```
Arbol:
        50
       /  \
      30   70
     /  \    \
    20  40   85

Recorrido Preorder:

1. VISITA 50 ✓ (raiz primero)
2. preorder(30)
3.   VISITA 30 ✓
4.   preorder(20)
5.     VISITA 20 ✓
6.   preorder(40)
7.     VISITA 40 ✓
8. preorder(70)
9.   VISITA 70 ✓
10.  preorder(85)
11.    VISITA 85 ✓

Resultado: [50, 30, 20, 40, 70, 85]
```

## POR QUE SE HIZO ASI:

1. **Preserva la estructura**: Si insertamos los elementos en este orden en un arbol vacio, obtenemos el MISMO arbol
2. **Serializacion**: Util para guardar el arbol en un archivo y reconstruirlo despues

## PARA QUE SIRVE:

```python
# Copiar/clonar el arbol
orden_preorder = bst.preorder()

# Para reconstruir el arbol identico:
nuevo_bst = BinarySearchTree()
for key, data in orden_preorder:
    nuevo_bst.insert(key, data)
# nuevo_bst tiene la MISMA estructura que el original
```

---

# SECCION 7: RECORRIDO POSTORDER

## QUE DECIR:

"El recorrido Postorder visita los nodos en este orden:
1. Primero el subarbol IZQUIERDO
2. Luego el subarbol DERECHO
3. Finalmente la RAIZ

**Caracteristica principal:** La raiz se visita DESPUES de sus hijos. Esto es util cuando necesitamos procesar los hijos antes que el padre."

## QUE MOSTRAR:

```python
# Codigo real (data_structures.py lineas 430-444):

def postorder(self):
    """Recorrido Postorder - raiz al final"""
    result = []
    self._postorder_recursive(self.root, result)
    return result

def _postorder_recursive(self, node, result):
    if node is not None:
        # 1. Visitar subarbol izquierdo
        self._postorder_recursive(node.left, result)

        # 2. Visitar subarbol derecho
        self._postorder_recursive(node.right, result)

        # 3. Visitar raiz AL FINAL
        result.append((node.key, node.data))
```

## EJEMPLO VISUAL:

```
Arbol:
        50
       /  \
      30   70
     /  \    \
    20  40   85

Recorrido Postorder:

1. postorder(30)
2.   postorder(20)
3.     VISITA 20 ✓ (hoja, no tiene hijos)
4.   postorder(40)
5.     VISITA 40 ✓
6.   VISITA 30 ✓ (despues de sus hijos)
7. postorder(70)
8.   postorder(85)
9.     VISITA 85 ✓
10.  VISITA 70 ✓
11. VISITA 50 ✓ (raiz al final de todo)

Resultado: [20, 40, 30, 85, 70, 50]
```

## POR QUE SE HIZO ASI:

1. **Eliminacion segura**: Para eliminar un arbol, debemos eliminar los hijos antes que los padres
2. **Calculo de tamaños**: Para calcular el tamaño de un nodo, primero necesitamos el tamaño de sus hijos

## PARA QUE SIRVE:

```python
# Eliminar el arbol de forma segura
def eliminar_arbol(nodo):
    if nodo is not None:
        eliminar_arbol(nodo.left)   # Eliminar hijos primero
        eliminar_arbol(nodo.right)
        del nodo                     # Eliminar nodo actual

# Postorder garantiza que no queden referencias huerfanas
```

---

# SECCION 8: RECORRIDO POR NIVELES (BFS)

## QUE DECIR:

"El recorrido por niveles, tambien conocido como BFS (Breadth-First Search), visita todos los nodos de un nivel antes de pasar al siguiente.

A diferencia de los otros recorridos que usan recursion (y por lo tanto una pila implicita), este usa una **cola** (queue) para mantener el orden de visita."

## QUE MOSTRAR:

```python
# Codigo real (data_structures.py lineas 470-494):

def level_order(self):
    """Recorrido por niveles usando BFS"""
    if self.root is None:
        return []

    result = []
    queue = [self.root]  # Cola inicializada con la raiz

    while queue:
        level_size = len(queue)  # Nodos en el nivel actual
        current_level = []

        for _ in range(level_size):
            node = queue.pop(0)  # Sacar el primero (FIFO)
            current_level.append((node.key, node.data))

            # Agregar hijos a la cola para el siguiente nivel
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)  # Agregar nivel completo

    return result
```

## EJEMPLO VISUAL:

```
Arbol:
        50           <- Nivel 0
       /  \
      30   70        <- Nivel 1
     /  \    \
    20  40   85      <- Nivel 2

Proceso con la cola:

Inicio: queue = [50]

Nivel 0:
  - Sacar 50, agregar sus hijos
  - queue = [30, 70]
  - Resultado nivel 0: [50]

Nivel 1:
  - Sacar 30, agregar sus hijos (20, 40)
  - Sacar 70, agregar su hijo (85)
  - queue = [20, 40, 85]
  - Resultado nivel 1: [30, 70]

Nivel 2:
  - Sacar 20 (sin hijos)
  - Sacar 40 (sin hijos)
  - Sacar 85 (sin hijos)
  - queue = []
  - Resultado nivel 2: [20, 40, 85]

Resultado final:
[
  [(50)],           # Nivel 0
  [(30), (70)],     # Nivel 1
  [(20), (40), (85)] # Nivel 2
]
```

## POR QUE SE HIZO ASI:

1. **Cola FIFO**: First-In-First-Out garantiza que procesamos los nodos en orden de nivel
2. **Iterativo**: No usa recursion, evita posibles stack overflow en arboles muy grandes
3. **Agrupa por niveles**: Util para visualizar la estructura del arbol

## PARA QUE SIRVE:

```python
# Ver la estructura del arbol nivel por nivel
niveles = bst.level_order()

for i, nivel in enumerate(niveles):
    print(f"Nivel {i}: {[n[0] for n in nivel]}")

# Salida:
# Nivel 0: [50]
# Nivel 1: [30, 70]
# Nivel 2: [20, 40, 85]

# Util para:
# - Visualizar el arbol
# - Encontrar la altura
# - Busqueda en anchura
```

---

# SECCION 9: BUSQUEDA EN RANGO

## QUE DECIR:

"La busqueda en rango es una operacion muy poderosa del BST. Permite encontrar todos los nodos cuyos valores estan dentro de un rango [min, max].

**Complejidad:** O(log n + k), donde k es la cantidad de elementos en el rango.

La belleza de esta operacion es que NO visitamos nodos que sabemos que estan fuera del rango. Usamos la propiedad del BST para podar ramas innecesarias."

## QUE MOSTRAR:

```python
# Codigo real (data_structures.py lineas 446-468):

def range_search(self, min_key, max_key):
    """Busca todos los nodos en el rango [min_key, max_key]"""
    result = []
    self._range_search_recursive(self.root, min_key, max_key, result)
    return result

def _range_search_recursive(self, node, min_key, max_key, result):
    if node is None:
        return

    # Si el nodo actual es MAYOR que min_key,
    # entonces PUEDE haber valores validos en la izquierda
    if node.key > min_key:
        self._range_search_recursive(node.left, min_key, max_key, result)

    # Si el nodo actual esta DENTRO del rango, agregarlo
    if min_key <= node.key <= max_key:
        result.append((node.key, node.data))

    # Si el nodo actual es MENOR que max_key,
    # entonces PUEDE haber valores validos en la derecha
    if node.key < max_key:
        self._range_search_recursive(node.right, min_key, max_key, result)
```

## EJEMPLO VISUAL:

```
Buscar rango [35, 75] en:

        50
       /  \
      30   70
     /  \    \
    20  40   85

Proceso:

1. En 50: 50 > 35? Si -> buscar izquierda
2.   En 30: 30 > 35? No -> NO buscar izquierda (PODA!)
3.   30 en [35,75]? No
4.   30 < 75? Si -> buscar derecha
5.     En 40: 40 > 35? Si -> buscar izq (None)
6.     40 en [35,75]? SI -> agregar 40 ✓
7.     40 < 75? Si -> buscar der (None)
8. 50 en [35,75]? SI -> agregar 50 ✓
9. 50 < 75? Si -> buscar derecha
10.   En 70: 70 > 35? Si -> buscar izq (None)
11.   70 en [35,75]? SI -> agregar 70 ✓
12.   70 < 75? Si -> buscar derecha
13.     En 85: 85 > 35? Si -> buscar izq (None)
14.     85 en [35,75]? No
15.     85 < 75? No -> NO buscar derecha (PODA!)

Resultado: [40, 50, 70]

NOTA: Nunca visitamos 20 ni la derecha de 85 (PODADAS)
```

## POR QUE SE HIZO ASI:

1. **Poda inteligente**: Solo visitamos subarboles que PUEDEN contener valores en el rango
2. **Eficiencia**: O(log n + k) es mucho mejor que O(n) de una lista
3. **Aprovecha el BST**: Usamos la propiedad de ordenamiento para descartar ramas

## PARA QUE SIRVE:

```python
# En el sistema de riesgo crediticio:

# Encontrar clientes de ALTO riesgo (70-100)
alto_riesgo = bst.range_search(70, 100)
print(f"Clientes de alto riesgo: {len(alto_riesgo)}")

# Encontrar clientes de BAJO riesgo (0-30)
bajo_riesgo = bst.range_search(0, 30)

# Encontrar clientes en rango especifico
rango_especifico = bst.range_search(45, 65)
```

---

# SECCION 10: CLASE CreditRiskBST

## QUE DECIR:

"Creamos una clase especializada llamada CreditRiskBST que extiende BinarySearchTree. Esta clase agrega metodos especificos para el dominio de riesgo crediticio, haciendo el codigo mas legible y facil de usar."

## QUE MOSTRAR:

```python
# Codigo real (data_structures.py lineas 497-560):

class CreditRiskBST(BinarySearchTree):
    """
    Arbol especializado para Riesgo Crediticio
    Extiende BinarySearchTree con metodos de dominio
    """

    def insert_client(self, risk_score, client_info):
        """Inserta un cliente por su score de riesgo"""
        return self.insert(risk_score, client_info)

    def find_high_risk_clients(self, threshold=70):
        """
        Encuentra clientes de alto riesgo

        Args:
            threshold: Score minimo para considerar alto riesgo (default 70)

        Returns:
            Lista de clientes con score >= threshold
        """
        return self.range_search(threshold, 100)

    def find_low_risk_clients(self, threshold=30):
        """Encuentra clientes de bajo riesgo (score <= threshold)"""
        return self.range_search(0, threshold)

    def find_medium_risk_clients(self, low=30, high=70):
        """Encuentra clientes de riesgo medio"""
        return self.range_search(low, high)

    def get_risk_distribution(self):
        """
        Calcula la distribucion de riesgo en la cartera

        Returns:
            Diccionario con conteo por categoria
        """
        all_clients = self.inorder()

        distribution = {
            'bajo': 0,    # Score 0-30
            'medio': 0,   # Score 31-70
            'alto': 0     # Score 71-100
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

## POR QUE SE HIZO ASI:

1. **Herencia**: Reutilizamos todo el codigo del BinarySearchTree
2. **Encapsulacion**: Los umbrales de riesgo (30, 70) estan encapsulados
3. **Legibilidad**: `find_high_risk_clients()` es mas claro que `range_search(70, 100)`
4. **Dominio especifico**: Los metodos reflejan el lenguaje del negocio

## PARA QUE SIRVE:

```python
# Uso en la aplicacion (app.py):

bst = CreditRiskBST()

# Insertar clientes
bst.insert_client(85, {'nombre': 'Juan', 'monto': 5000})
bst.insert_client(25, {'nombre': 'Maria', 'monto': 3000})

# Analisis de cartera
alto_riesgo = bst.find_high_risk_clients()
bajo_riesgo = bst.find_low_risk_clients()
distribucion = bst.get_risk_distribution()

print(f"Alto riesgo: {len(alto_riesgo)} clientes")
print(f"Bajo riesgo: {len(bajo_riesgo)} clientes")
print(f"Distribucion: {distribucion}")
```

---

# SECCION 11: INTEGRACION CON FLASK (app.py)

## QUE DECIR:

"Veamos como se integra el BST con la aplicacion web Flask. La ruta /arbol crea el arbol, calcula los scores de riesgo, y envia los datos a la plantilla HTML para visualizacion."

## QUE MOSTRAR:

```python
# Codigo real (app.py lineas 133-210):

@app.route('/arbol')
def arbol():
    """Pagina de demostracion del Arbol Binario de Busqueda"""
    try:
        # 1. CARGAR DATOS
        if os.path.exists(config.PROCESSED_DATA_FILE):
            df = pd.read_csv(config.PROCESSED_DATA_FILE)
        else:
            df = pd.read_csv(config.RAW_DATA_FILE)
            df = df.dropna()

        # 2. CALCULAR SCORES DE RIESGO
        # Formula: base + factor_interes + factor_ingreso + ruido
        np.random.seed(42)
        risk_scores = []
        for idx, row in df.iterrows():
            base_score = row['loan_status'] * 50
            interest_factor = min(row['loan_int_rate'] / 25 * 30, 30)
            income_factor = min(row['loan_percent_income'] * 50, 20)
            noise = np.random.uniform(-5, 5)
            score = max(0, min(100, base_score + interest_factor + income_factor + noise))
            risk_scores.append(int(score))

        # 3. CONSTRUIR EL BST
        sample_size = min(50, len(df))
        sample_indices = np.random.choice(len(df), sample_size, replace=False)

        bst = CreditRiskBST()
        for idx in sample_indices:
            bst.insert_client(risk_scores[idx], {
                'index': int(idx),
                'loan_amnt': float(df.iloc[idx]['loan_amnt']),
                'income': float(df.iloc[idx]['person_income'])
            })

        # 4. OBTENER DATOS PARA LA VISTA
        traversals = {
            'inorder': bst.inorder(),
            'preorder': bst.preorder(),
            'postorder': bst.postorder(),
            'levelorder': bst.level_order()
        }

        # 5. CONVERTIR ARBOL A JSON PARA D3.js
        def tree_to_dict(node):
            if node is None:
                return None
            result = {'key': node.key, 'data': node.data}
            children = []
            if node.left:
                children.append(tree_to_dict(node.left))
            if node.right:
                children.append(tree_to_dict(node.right))
            if children:
                result['children'] = children
            return result

        tree_json = json.dumps(tree_to_dict(bst.root))

        # 6. RENDERIZAR PLANTILLA
        return render_template('arbol.html',
            tree_data=True,
            tree_json=tree_json,
            stats=tree_stats,
            traversals=traversals,
            distribution=bst.get_risk_distribution(),
            range_results=range_results
        )
    except Exception as e:
        return render_template('arbol.html', tree_data=False, error=str(e))
```

## POR QUE SE HIZO ASI:

1. **Separacion de responsabilidades**:
   - `data_structures.py` → Logica del BST
   - `app.py` → Integracion web
   - `arbol.html` → Visualizacion

2. **JSON para D3.js**: Convertimos el arbol a JSON para que JavaScript pueda visualizarlo

3. **Manejo de errores**: Si algo falla, mostramos un mensaje amigable

## PARA QUE SIRVE:

La ruta `/arbol` hace todo el trabajo de:
- Cargar los datos del CSV
- Calcular scores de riesgo
- Construir el BST
- Preparar los recorridos
- Enviar todo a la plantilla para visualizacion

---

# SECCION 12: VISUALIZACION CON D3.js

## QUE DECIR:

"Para la visualizacion grafica del arbol usamos D3.js, una libreria de JavaScript para visualizacion de datos. D3 toma el JSON del arbol y genera un grafico SVG interactivo."

## QUE MOSTRAR:

```javascript
// Codigo real (arbol.html lineas 180-230):

// 1. DATOS DEL ARBOL (viene de Flask)
var treeData = {{ tree_json | safe }};

// 2. CREAR LAYOUT DEL ARBOL
var treeLayout = d3.tree().size([width, height]);
var root = d3.hierarchy(treeData);  // Convertir JSON a jerarquia D3
treeLayout(root);  // Calcular posiciones x, y

// 3. FUNCION DE COLOR SEGUN RIESGO
function getRiskColor(score) {
    if (score <= 30) return "#2ecc71";  // Verde - bajo riesgo
    if (score <= 70) return "#f39c12";  // Amarillo - medio riesgo
    return "#e74c3c";                    // Rojo - alto riesgo
}

// 4. DIBUJAR ENLACES (lineas entre nodos)
svg.selectAll(".link")
    .data(root.links())  // Obtener conexiones padre-hijo
    .enter()
    .append("path")
    .attr("class", "link")
    .attr("fill", "none")
    .attr("stroke", "rgba(255, 255, 255, 0.3)")
    .attr("d", d3.linkVertical()  // Linea vertical curva
        .x(d => d.x)
        .y(d => d.y));

// 5. DIBUJAR NODOS (circulos)
var nodes = svg.selectAll(".node")
    .data(root.descendants())  // Todos los nodos del arbol
    .enter()
    .append("g")
    .attr("transform", d => `translate(${d.x},${d.y})`);

// 6. CIRCULOS CON COLOR SEGUN RIESGO
nodes.append("circle")
    .attr("r", 20)
    .attr("fill", d => getRiskColor(d.data.key))
    .attr("stroke", "#fff")
    .on("mouseover", function() {
        d3.select(this).attr("r", 25);  // Agrandar al pasar mouse
    })
    .on("mouseout", function() {
        d3.select(this).attr("r", 20);  // Volver a tamaño normal
    });

// 7. TEXTO EN LOS NODOS
nodes.append("text")
    .attr("text-anchor", "middle")
    .attr("fill", "#fff")
    .text(d => d.data.key);  // Mostrar el score
```

## POR QUE SE HIZO ASI:

1. **D3.js**: Es el estandar para visualizacion de datos en web
2. **d3.tree()**: Layout especializado para arboles jerarquicos
3. **SVG**: Graficos vectoriales escalables, nitidos en cualquier tamaño
4. **Colores semanticos**: Verde/amarillo/rojo transmiten el significado del riesgo

## PARA QUE SIRVE:

La visualizacion permite:
- Ver la ESTRUCTURA del arbol graficamente
- Identificar rapidamente clientes de alto riesgo (nodos rojos)
- Entender como estan organizados los datos
- Interactuar con los nodos (hover)

---

# SECCION 13: COMPLEJIDAD ALGORITMICA

## QUE DECIR:

"Finalmente, hablemos de la complejidad algoritmica. Esta es la razon por la que elegimos un BST en lugar de otras estructuras.

**Notacion Big-O**: Describe como crece el tiempo de ejecucion cuando crece la cantidad de datos.

Para un BST balanceado:"

## QUE MOSTRAR:

```
TABLA DE COMPLEJIDADES:

Operacion          | Promedio  | Peor Caso | Explicacion
-------------------|-----------|-----------|---------------------------
Busqueda           | O(log n)  | O(n)      | Cada paso descarta mitad
Insercion          | O(log n)  | O(n)      | Similar a busqueda
Eliminacion        | O(log n)  | O(n)      | Buscar + reorganizar
Minimo/Maximo      | O(log n)  | O(n)      | Ir siempre izq/der
Recorridos         | O(n)      | O(n)      | Visitar todos los nodos
Busqueda en Rango  | O(log n+k)| O(n)      | k = elementos encontrados


¿POR QUE O(log n)?

En cada comparacion, descartamos aproximadamente la mitad del arbol:

n = 1000 elementos
   ↓
Paso 1: quedan ~500
Paso 2: quedan ~250
Paso 3: quedan ~125
Paso 4: quedan ~62
Paso 5: quedan ~31
Paso 6: quedan ~15
Paso 7: quedan ~7
Paso 8: quedan ~3
Paso 9: quedan ~1 → Encontrado!

log₂(1000) ≈ 10 pasos


¿CUANDO ES O(n)? (Peor caso)

Cuando el arbol esta DESBALANCEADO (degenerado):

Insertar: 1, 2, 3, 4, 5

    1
     \
      2
       \
        3
         \
          4
           \
            5  ← ¡Esto es una lista, no un arbol!

Solucion: Usar arboles balanceados (AVL, Red-Black)
```

## POR QUE SE HIZO ASI:

1. **Eficiencia practica**: O(log n) es aceptable para la mayoria de casos
2. **Simplicidad**: Un BST simple es mas facil de entender e implementar
3. **Suficiente para el proyecto**: Con 50-100 clientes, incluso O(n) seria rapido

## PARA QUE SIRVE:

Entender la complejidad ayuda a:
- Predecir el rendimiento con mas datos
- Decidir si necesitamos optimizar
- Elegir la estructura de datos correcta para cada problema

---

# SECCION 14: RESUMEN FINAL

## QUE DECIR:

"En resumen, implementamos un sistema completo de Arboles Binarios de Busqueda aplicado al dominio de riesgo crediticio:

**Estructuras implementadas:**
- TreeNode: Nodo basico del arbol
- BinarySearchTree: Arbol generico con todas las operaciones
- CreditRiskBST: Extension especializada para riesgo crediticio

**Operaciones implementadas:**
- Insert, Search, Delete
- Recorridos: Inorder, Preorder, Postorder, Level-order
- Busqueda en Rango
- Encontrar Minimo/Maximo

**Integracion:**
- Flask para el backend web
- D3.js para visualizacion
- Interfaz interactiva para el usuario

**Complejidad:**
- Busqueda: O(log n)
- Insercion: O(log n)
- Recorridos: O(n)

El sistema demuestra como una estructura de datos teorica puede aplicarse a un problema real del mundo financiero."

---

# ARCHIVOS DEL PROYECTO

```
credit_risk_system/
│
├── src/
│   └── data_structures.py    ← Implementacion del BST
│       - TreeNode (linea 252)
│       - BinarySearchTree (linea 268)
│       - CreditRiskBST (linea 497)
│
├── templates/
│   └── arbol.html            ← Visualizacion web
│       - Estadisticas
│       - Grafico D3.js
│       - Recorridos
│       - Busqueda en rango
│
├── static/css/
│   └── style.css             ← Estilos de la pagina
│       - Seccion .bst-* (linea 1375+)
│
├── app.py                    ← Ruta /arbol (linea 133)
│
└── docs/
    ├── ARBOL_BUSQUEDA_BST.md       ← Documentacion tecnica
    └── GUIA_USUARIO_ARBOL_BST.md   ← Este documento
```

---

# FIN DE LA PRESENTACION

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║                      ¡GRACIAS!                                 ║
║                                                                ║
║                   ¿PREGUNTAS?                                  ║
║                                                                ║
║                                                                ║
║   Grupo 5 - UNACH                                             ║
║   Ciencia de Datos e Inteligencia Artificial                  ║
║   2025                                                         ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```
