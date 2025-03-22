import random
import copy

#---------------------------------------------------------------

class Nodo:
    def __init__(self, identificador, valor=None, es_max=True):
        self.id = identificador
        self.valor = valor
        self.hijos = []
        self.es_max = es_max   # True para nodos MAX, False para nodos MIN
        self.podado = False    # Indica si el nodo ha sido podado
    
    def es_hoja(self):
        return len(self.hijos) == 0
    
    def anadir_hijo(self, nodo):
        self.hijos.append(nodo)
        
    def __str__(self):
        if self.es_hoja():
            return f"Hoja({self.id}: {self.valor})"
        else:
            tipo = "MAX" if self.es_max else "MIN"
            return f"Nodo {tipo}({self.id}: {len(self.hijos)} hijos)"

#---------------------------------------------------------------

def crear_arbol(factor_ramificacion, profundidad, min_valor=0, max_valor=100, raiz_es_max=True):
    """
    Crea un árbol con el factor de ramificación y profundidad especificado.
    Parámetros:
       factor_ramificacion: Número de hijos para cada nodo (no hoja)
       profundidad: Profundidad máxima del árbol (0 es sólo la raíz)
       min_valor, max_valor: Rango para los valores aleatorios en las hojas
       raíz_es_max: Si la raíz es un nodo MAX (True) o MIN (False)
    Retorna:
       La raíz del árbol generado
    """
    contador_id = 0
    
    def _generar_subarbol(prof_actual, es_max):
        nonlocal contador_id
        identificador_actual = contador_id
        contador_id += 1
        
        nodo = Nodo(identificador_actual, es_max=es_max)
        
        # Si es una hoja (hemos llegado a la profundidad máxima), asignamos un valor aleatorio
        if prof_actual >= profundidad:
            nodo.valor = random.uniform(min_valor, max_valor)
            return nodo
        
        # De lo contrario, crear a los hijos (con tipo contrario al padre)
        for _ in range(factor_ramificacion):
            hijo = _generar_subarbol(prof_actual + 1, not es_max)
            nodo.anadir_hijo(hijo)
            
        return nodo
    
    # Iniciar la generació recursiva des de l'arrel (profunditat 0)
    return _generar_subarbol(0, raiz_es_max)

#---------------------------------------------------------------

def imprimir_arbol(nodo, nivel=0):
    """Imprime el árbol en formato texto con sangrado"""
    prefijo = "  " * nivel
    
    if nodo.podado:
        estado = "[PODADO]"
    else:
        estado = ""
        
    if nodo.es_hoja():
        print(f"{prefijo}Hoja {nodo.id}: {nodo.valor:.2f} {estado}")
    else:
        tipo = "MAX" if nodo.es_max else "MIN"
        if nodo.valor:
            print(f"{prefijo}Nodo {tipo} {nodo.id}: {nodo.valor:.2f} {estado}")
        else:
            print(f"{prefijo}Nodo {tipo} {nodo.id} {estado}")
            
    for hijo in nodo.hijos:
        imprimir_arbol(hijo, nivel + 1)

#---------------------------------------------------------------
# --- Función auxiliar para marcar como podados  ---- 
# ---        los hijos de los podados            ----

def marca_podado(nodo):
    nodo.podado = True
    if not nodo.es_hoja():
        for hijo in nodo.hijos:
            marca_podado(hijo) 

#---------------------------------------------------------------

def alfa_beta(nodo, alfa=-float('inf'), beta=float('inf')):
    """
    Aplica el algoritmo de poda alfa-beta en el árbol.
    Parámetros
       nodo: Nodo actual
       alfa: Mejor valor para el jugador MAX hasta ahora
       beta: Mejor valor para el jugador MIN hasta ahora
    Retorna
       El valor minimax del nodo
    """
    # Si es una hoja, devolvemos su valor
    if nodo.es_hoja():
        return nodo.valor
    
    # Si es un nodo MAX
    if nodo.es_max:
        valor = -float('inf')
        for hijo in nodo.hijos:
            valor = max(valor, alfa_beta(hijo, alfa, beta))
            alfa = max(alfa, valor)
            
            # Poda Beta
            if alfa >= beta:
                # Marcamos como podados los hijos restantes
                for hijo_restante in nodo.hijos[nodo.hijos.index(hijo) + 1:]:
                    marca_podado(hijo_restante)
                break
                
        nodo.valor = valor
        return valor
    
    # Si es un nodo MIN
    else:
        valor = float('inf')
        for hijo in nodo.hijos:
            valor = min(valor, alfa_beta(hijo, alfa, beta))
            beta = min(beta, valor)
            
            # Poda Alfa
            if alfa >= beta:
                # Marcamos como podados los hijos restantes
                for hijo_restante in nodo.hijos[nodo.hijos.index(hijo) + 1:]:
                    marca_podado(hijo_restante)
                break
                
        nodo.valor = valor
        return valor

#--------------------------------------------------------------------------
# APARTADO 2B - CREACIÓN DE PODAS ALFABETA DERECHA -> IZQUIERDA
def alfa_beta_derecha(nodo, alfa=-float('inf'), beta=float('inf')):
    if nodo.es_hoja():
        return nodo.valor
    if nodo.es_max:
        valor =-float('inf')
        for hijo in reversed(nodo.hijos):
            valor = max(valor, alfa_beta_derecha(hijo, alfa, beta))
            alfa = max(alfa, valor)
            if alfa >= beta:
                for hijo_restante in reversed(nodo.hijos[:nodo.hijos.index(hijo)]):
                    marca_podado(hijo_restante)
                break
            nodo.valor = valor
        else:
            valor = float('inf')
        for hijo in reversed(nodo.hijos):
            valor = max(valor, alfa_beta_derecha(hijo, alfa, beta))
            alfa = max(alfa, valor)
            if alfa >= beta:
                for hijo_restante in reversed(nodo.hijos[:nodo.hijos.index(hijo)]):
                    marca_podado(hijo_restante)
                break
            nodo.valor = valor
        return valor
#--------------------------------------------------------------------------
# Parámetros del árbol
factor_ramificacion = 3
profundidad = 2
    
# Crear el árbol (la raíz es un nodo MAX por defecto)
arbol1 = crear_arbol(factor_ramificacion, profundidad, min_valor=1, max_valor=100)
arbol2 = crear_arbol(factor_ramificacion, profundidad, min_valor=1, max_valor=100)
#-----------------------------------------------

# Aplicar el algoritmo de poda alfa-beta, de izquierda a derecha
resultado = alfa_beta(arbol1)
print(f"\nResultado de alfa-beta (de izquierda a derecha): {resultado:.2f}")
print("\nÁrbol después de la poda alfa-beta (de izquierda a derecha):")
imprimir_arbol(arbol1)

# Aplicar el algoritmo de poda alfa-beta, de derecha a izquierda
resultado = alfa_beta(arbol2)
print(f"\nResultado de alfa-beta (derecha a izquierda): {resultado:.2f}")
print("\nÁrbol después de la poda alfa-beta (derecha a izquierda):")
imprimir_arbol(arbol2)
