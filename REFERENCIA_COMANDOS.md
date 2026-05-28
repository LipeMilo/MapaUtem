# Referencia de Comandos y Sintaxis — Campus Accesible MVP

Guía de referencia rápida con todos los comandos, librerías y sintaxis utilizados en `app.py`, organizada por categorías. Incluye glosario y preguntas frecuentes para uso en clase.

---

## Índice

1. [Streamlit](#1-streamlit)
2. [Firebase Firestore](#2-firebase-firestore)
3. [NetworkX](#3-networkx)
4. [pydeck](#4-pydeck)
5. [Pandas](#5-pandas)
6. [Python Esencial](#6-python-esencial)
7. [Manejo de GeoJSON](#7-manejo-de-geojson)
8. [Glosario](#8-glosario)
9. [Preguntas Frecuentes](#9-preguntas-frecuentes)

---

## 1. Streamlit

### `st.set_page_config()`

| Qué hace | Configura el título, layout y otros ajustes globales de la página |
|---|---|
| Sintaxis | `st.set_page_config(page_title="...", layout="wide"/"centered")` |
| Ejemplo | `st.set_page_config(page_title="Campus Accesible MVP", layout="wide")` |
| Línea | 77 |

---

### `st.title()`

| Qué hace | Muestra un título en la página principal |
|---|---|
| Sintaxis | `st.title("texto")` |
| Ejemplo | `st.title("Campus Accesible - Mapa Interactivo")` |
| Línea | 78 |

---

### `st.sidebar.header()`

| Qué hace | Muestra un encabezado dentro de la barra lateral |
|---|---|
| Sintaxis | `st.sidebar.header("texto")` |
| Ejemplo | `st.sidebar.header("Sistema de Navegación")` |
| Línea | 80 |

---

### `st.sidebar.selectbox()`

| Qué hace | Crea un menú desplegable en la barra lateral |
|---|---|
| Sintaxis | `st.sidebar.selectbox("etiqueta", lista_opciones, index=posición_default)` |
| Parámetros | `index` — posición del elemento seleccionado por defecto (0 = primero) |
| Ejemplo | `st.sidebar.selectbox("Punto de Origen:", nombres_edificios, index=0)` |
| Línea | 102 |

---

### `st.sidebar.checkbox()`

| Qué hace | Crea una casilla de verificación en la barra lateral |
|---|---|
| Sintaxis | `st.sidebar.checkbox("etiqueta")` |
| Retorna | `True` si está marcada, `False` si no |
| Ejemplo | `es_accesible = st.sidebar.checkbox("Ruta para movilidad reducida")` |
| Línea | 106 |

---

### `st.sidebar.success()`, `st.sidebar.error()`, `st.sidebar.warning()`

| Qué hace | Muestra un mensaje coloreado en la barra lateral (verde, rojo, amarillo) |
|---|---|
| Sintaxis | `st.sidebar.success("mensaje")` / `st.sidebar.error("mensaje")` / `st.sidebar.warning("mensaje")` |
| Ejemplo | `st.sidebar.success(f"Ruta calculada: {' ➔ '.join(...)}")` |
| Líneas | 126, 129, 132, 136 |

---

### `st.error()` / `st.info()` / `st.write()`

| Qué hace | Muestra mensajes en el área principal (no en sidebar) |
|---|---|
| Sintaxis | `st.error("mensaje")` — mensaje de error rojo / `st.info("mensaje")` — info azul / `st.write("### texto")` — texto con markdown |
| Ejemplo | `st.error(f"Error al conectar con Firebase: {e}")` |
| Líneas | 86, 245, 254 |

---

### `st.pydeck_chart()`

| Qué hace | Renderiza un mapa 3D interactivo usando pydeck (deck.gl) |
|---|---|
| Sintaxis | `st.pydeck_chart(pdk.Deck(...))` |
| Parámetros | Recibe un objeto `pdk.Deck` con mapa base, capas y cámara |
| Ejemplo | `st.pydeck_chart(pdk.Deck(map_style=..., initial_view_state=..., layers=capas))` |
| Línea | 247 |

---

### `@st.cache_data`

| Qué hace | Decorador que cachea en memoria el resultado de una función. Streamlit re-ejecuta todo el script en cada interacción; este decorador evita llamadas repetidas a Firebase |
|---|---|
| Sintaxis | `@st.cache_data` encima de la definición de una función |
| Ejemplo | Línea 16: `@st.cache_data` sobre `def obtener_ubicaciones()` |
| Línea | 16 |
| Nota | Los datos cacheados persisten mientras la app está corriendo. Para forzar recarga: `st.cache_data.clear()` |

---

### `st.secrets`

| Qué hace | Accede a credenciales y configuraciones secretas definidas en `.streamlit/secrets.toml` (local) o en los Secrets de Streamlit Cloud (producción) |
|---|---|
| Sintaxis | `st.secrets["sección"]["campo"]` |
| Ejemplo | `st.secrets["firebase"]` — devuelve todo el bloque `[firebase]` del TOML |
| Línea | 12 |

---

## 2. Firebase Firestore

### `firebase_admin.initialize_app()`

| Qué hace | Inicializa la aplicación de Firebase con las credenciales de la cuenta de servicio |
|---|---|
| Sintaxis | `firebase_admin.initialize_app(credencial)` |
| Ejemplo | `firebase_admin.initialize_app(cred)` |
| Línea | 13 |
| Nota | El guard `if not firebase_admin._apps:` evita inicializar dos veces (Streamlit re-ejecuta el script constantemente) |

---

### `credentials.Certificate()`

| Qué hace | Crea un objeto de credenciales a partir de un diccionario con los campos de una cuenta de servicio de Google |
|---|---|
| Sintaxis | `credentials.Certificate(dict)` |
| Ejemplo | `credentials.Certificate(dict(st.secrets["firebase"]))` |
| Línea | 12 |

---

### `firestore.client()`

| Qué hace | Obtiene el cliente de Firestore para realizar operaciones en la base de datos |
|---|---|
| Sintaxis | `firestore.client()` |
| Retorna | Objeto `Client` de Firestore |
| Ejemplo | `db = firestore.client()` |
| Líneas | 18, 35 |

---

### `db.collection()`

| Qué hace | Obtiene una referencia a una colección específica de Firestore |
|---|---|
| Sintaxis | `db.collection("nombre_colección")` |
| Retorna | Objeto `CollectionReference` |
| Ejemplo | `ubicaciones_ref = db.collection("ubicaciones")` |
| Líneas | 19, 36 |

---

### `.stream()`

| Qué hace | Ejecuta la consulta y devuelve un iterador con todos los documentos de la colección |
|---|---|
| Sintaxis | `coleccion.stream()` |
| Retorna | Generator de objetos `DocumentSnapshot` |
| Ejemplo | `docs = ubicaciones_ref.stream()` |
| Líneas | 20, 37 |

---

### `.to_dict()`

| Qué hace | Convierte un `DocumentSnapshot` en un diccionario Python con los campos del documento |
|---|---|
| Sintaxis | `documento.to_dict()` |
| Retorna | `dict` |
| Ejemplo | `datos = doc.to_dict()` |
| Líneas | 25, 41 |

---

### `.id`

| Qué hace | Propiedad de `DocumentSnapshot` que devuelve el ID único del documento en Firestore |
|---|---|
| Sintaxis | `documento.id` |
| Retorna | `str` |
| Ejemplo | `datos['id'] = doc.id` |
| Líneas | 26, 42 |

---

## 3. NetworkX

### `nx.Graph()`

| Qué hace | Crea un grafo no dirigido vacío |
|---|---|
| Sintaxis | `nx.Graph()` |
| Retorna | Objeto `Graph` de NetworkX |
| Ejemplo | `G = nx.Graph()` |
| Línea | 48 |

---

### `.add_edge()`

| Qué hace | Agrega una arista (conexión) entre dos nodos, con atributos opcionales |
|---|---|
| Sintaxis | `grafo.add_edge(origen, destino, weight=peso, ...)` |
| Parámetros | `weight` — peso/costo de la arista (usado por Dijkstra) |
| Ejemplo | `G.add_edge(camino["origen"], camino["destino"], weight=camino["peso"])` |
| Línea | 52 |

---

### `nx.shortest_path()`

| Qué hace | Encuentra la ruta más corta entre dos nodos usando el algoritmo de Dijkstra |
|---|---|
| Sintaxis | `nx.shortest_path(grafo, source=origen, target=destino, weight="weight")` |
| Retorna | Lista de nodos desde el origen hasta el destino |
| Excepción | `nx.NetworkXNoPath` — si no existe ruta entre los nodos |
| Ejemplo | `ruta_nodos = nx.shortest_path(G, source=origen, target=destino, weight="weight")` |
| Línea | 55 |

---

### `nx.NetworkXNoPath`

| Qué hace | Excepción que se lanza cuando no existe ningún camino entre los nodos especificados |
|---|---|
| Sintaxis | `except nx.NetworkXNoPath:` |
| Ejemplo | Línea 70: captura esta excepción y retorna un mensaje de error |
| Línea | 70 |

---

## 4. pydeck

### `pdk.Layer()`

| Qué hace | Crea una capa de datos para renderizar en el mapa 3D. pydeck soporta múltiples tipos de capa (GeoJsonLayer, PathLayer, TextLayer, etc.) |
|---|---|
| Sintaxis | `pdk.Layer("TipoDeCapa", data=..., parámetros...)` |
| Nota | El primer argumento es un string con el nombre del tipo de capa de deck.gl |

---

### `pdk.Layer("GeoJsonLayer", ...)` — Edificios 3D

| Qué hace | Renderiza geometrías GeoJSON como polígonos 3D extruidos |
|---|---|
| Parámetros clave | `extruded=True` — activa la extrusión 3D / `get_elevation=20` — altura de extrusión / `get_fill_color` — color de relleno (puede ser una expresión deck.gl) / `opacity=0.7` / `stroked=True` — bordes visibles / `wireframe=True` — malla alámbrica |
| Ejemplo | Líneas 180-191 |
| Línea | 180 |

---

### `pdk.Layer("GeoJsonLayer", ...)` — Caminos

| Qué hace | Renderiza geometrías GeoJSON como líneas en 2D |
|---|---|
| Parámetros clave | `filled=False` — sin relleno / `extruded=False` — sin 3D / `get_line_color` — color de línea / `get_line_width=3`, `line_width_min_pixels=2` |
| Ejemplo | Líneas 194-204 |
| Línea | 194 |

---

### `pdk.Layer("PathLayer", ...)` — Ruta calculada

| Qué hace | Renderiza una línea 3D que sigue una ruta de coordenadas |
|---|---|
| Parámetros clave | `data=[{"path": coordenadas, "color": [R,G,B,A]}]` / `get_path="path"` / `get_color="color"` / `width_scale=3`, `width_min_pixels=6` / `joint_rounded=True`, `cap_rounded=True` — bordes redondeados |
| Ejemplo | Líneas 210-220 |
| Línea | 210 |

---

### `pdk.Layer("TextLayer", ...)` — Etiquetas

| Qué hace | Renderiza texto flotante en posiciones geográficas específicas |
|---|---|
| Parámetros clave | `get_position='[lon, lat, altura]'` / `get_text="Nombre"` — columna del DataFrame con el texto / `get_size=15` / `get_color="[R,G,B,A]"` / `get_alignment_baseline`, `get_text_anchor` — alineación |
| Ejemplo | Líneas 224-234 |
| Línea | 224 |

---

### `pdk.ViewState()`

| Qué hace | Define la posición y orientación inicial de la cámara del mapa |
|---|---|
| Sintaxis | `pdk.ViewState(latitude=..., longitude=..., zoom=..., pitch=..., bearing=...)` |
| Parámetros | `latitude`, `longitude` — centro del mapa / `zoom` — nivel de zoom (17.5 = muy cercano) / `pitch` — inclinación en grados (0 = vista cenital) / `bearing` — rotación |
| Ejemplo | Líneas 237-243 |
| Línea | 237 |

---

### `pdk.Deck()`

| Qué hace | Crea el objeto Deck principal que contiene todas las capas y la configuración del mapa |
|---|---|
| Sintaxis | `pdk.Deck(map_style=..., initial_view_state=..., layers=...)` |
| Parámetros | `map_style` — URL del estilo de mapa base (usamos CARTO Voyager) / `initial_view_state` — objeto `ViewState` / `layers` — lista de capas `pdk.Layer` |
| Ejemplo | Líneas 247-251 |
| Línea | 247 |

---

## 5. Pandas

### `pd.DataFrame()`

| Qué hace | Crea un DataFrame (tabla) a partir de una lista de diccionarios |
|---|---|
| Sintaxis | `pd.DataFrame(lista_de_diccionarios)` |
| Ejemplo | `df = pd.DataFrame(lista_puntos)` |
| Línea | 150 |

---

### `.dropna()`

| Qué hace | Elimina filas que contengan valores nulos (NaN) en las columnas especificadas |
|---|---|
| Sintaxis | `df.dropna(subset=["columna1", "columna2"])` |
| Ejemplo | `df = df.dropna(subset=["lat", "lon"])` |
| Línea | 151 |

---

### `.apply()`

| Qué hace | Aplica una función a cada elemento de una columna (o fila) |
|---|---|
| Sintaxis | `df["columna"].apply(función)` |
| Ejemplo | `df[df["lat"].apply(lambda x: isinstance(x, (int, float)))]` — filtra filas donde lat es numérico |
| Línea | 152 |

---

### `lambda`

| Qué hace | Función anónima de una sola línea |
|---|---|
| Sintaxis | `lambda argumentos: expresión` |
| Ejemplo | `lambda x: isinstance(x, (int, float))` — retorna `True` si `x` es entero o flotante |
| Línea | 152 |

---

## 6. Python Esencial

### `import`

| Qué hace | Importa un módulo o librería para usar en el código |
|---|---|
| Sintaxis | `import modulo` o `from modulo import submodulo` o `from modulo import submodulo as alias` |
| Ejemplos | `import streamlit as st` (línea 1) / `from rutas import nodos_campus, caminos_campus` (línea 8) |
| Líneas | 1-8 |

---

### `def`

| Qué hace | Define una función |
|---|---|
| Sintaxis | `def nombre_funcion(param1, param2):` |
| Ejemplo | `def obtener_ubicaciones():` (línea 17) |
| Líneas | 17, 34 |

---

### `if / elif / else`

| Qué hace | Ejecuta código condicionalmente |
|---|---|
| Sintaxis | `if condición: ... elif otra_condición: ... else: ...` |
| Ejemplo | Líneas 113-133: verifica si la ruta se calculó correctamente |
| Líneas | 11, 27, 42, 50, 92, 96, 101, 113, 114, 116, 131, 134, 139, 163, 172, 174, 209, 223 |

---

### `for`

| Qué hace | Itera sobre los elementos de una secuencia (lista, generador, etc.) |
|---|---|
| Sintaxis | `for variable in secuencia:` |
| Ejemplo | `for doc in docs:` (línea 24) — itera sobre documentos de Firestore |
| Líneas | 24, 40, 49, 58, 93, 141, 163 |

---

### `try / except`

| Qué hace | Captura y maneja excepciones (errores en tiempo de ejecución) |
|---|---|
| Sintaxis | `try: ... except TipoError: ...` |
| Ejemplo | Líneas 54-73: captura `nx.NetworkXNoPath` y `Exception` genérica |
| Líneas | 54, 83-87 |

---

### `with open()`

| Qué hace | Abre un archivo de forma segura (se cierra automáticamente al salir del bloque) |
|---|---|
| Sintaxis | `with open("ruta", "r", encoding="utf-8") as variable:` |
| Modos | `"r"` — lectura / `"w"` — escritura / `"a"` — agregar |
| Ejemplo | `with open("edificios.geojson", "r", encoding="utf-8") as f:` |
| Líneas | 157, 160 |

---

### `json.load()`

| Qué hace | Lee un archivo JSON y lo convierte en un diccionario o lista de Python |
|---|---|
| Sintaxis | `json.load(archivo_abierto)` |
| Ejemplo | `data_edificios = json.load(f)` |
| Líneas | 158, 161 |

---

### `isinstance()`

| Qué hace | Verifica si un objeto es de un tipo (o tipos) específico |
|---|---|
| Sintaxis | `isinstance(objeto, (tipo1, tipo2))` |
| Ejemplo | `isinstance(p[0], (int, float))` — ¿p[0] es int o float? |
| Líneas | 119, 121, 152 |

---

### `all()`

| Qué hace | Retorna `True` si TODOS los elementos de un iterable son verdaderos |
|---|---|
| Sintaxis | `all(condición for elemento in iterable)` |
| Ejemplo | `all(isinstance(p, (list, tuple)) ... for p in coordenadas_linea)` |
| Línea | 118 |

---

### `dict.get()`

| Qué hace | Obtiene el valor de una clave del diccionario. Si no existe, retorna un valor por defecto (no lanza error) |
|---|---|
| Sintaxis | `diccionario.get("clave", valor_default)` |
| Ejemplo | `punto.get("nombre", "Sin nombre")` — si no hay "nombre", retorna "Sin nombre" |
| Líneas | 59, 70, 94, 95, 132, 143, 144, 147 |

---

### `f-strings`

| Qué hace | Interpolación de variables en strings. Las expresiones van entre `{}` |
|---|---|
| Sintaxis | `f"texto {variable} texto {expresion}"` |
| Ejemplo | `f"Ruta calculada: {' ➔ '.join(resultado['ruta_nodos'])}"` |
| Línea | 126 |

---

### `locals()`

| Qué hace | Retorna un diccionario con todas las variables locales del ámbito actual |
|---|---|
| Sintaxis | `locals()` |
| Uso | Se usa para verificar si una variable existe antes de accederla: `'origen_seleccionado' in locals()` |
| Líneas | 172, 174, 209 |

---

## 7. Manejo de GeoJSON

### Estructura de un archivo GeoJSON

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[lon, lat], [lon, lat], ...]]
      },
      "properties": {
        "Nombre Edificio": "Edificio M"
      }
    }
  ]
}
```

| Campo | Descripción |
|---|---|
| `type` | Siempre `"FeatureCollection"` para el archivo completo |
| `features` | Lista de objetos, cada uno es una entidad geográfica |
| `features[].type` | Siempre `"Feature"` |
| `features[].geometry.type` | Tipo de geometría: `"Polygon"`, `"MultiPolygon"`, `"LineString"`, etc. |
| `features[].geometry.coordinates` | Array de coordenadas `[longitud, latitud]` |
| `features[].properties` | Diccionario con atributos del elemento |

### Acceso a datos en app.py

```python
data_edificios = json.load(f)          # Carga el archivo completo
features = data_edificios["features"]   # Lista de todas las entidades
props = feature["properties"]           # Atributos de una entidad
nombre_edificio = list(props.keys())[0] # Primer atributo = nombre
```

### Color dinámico de edificios

```python
# Asignación de colores según selección del usuario
props['color_dinamico'] = [40, 200, 80, 255]    # Verde = origen
props['color_dinamico'] = [220, 60, 60, 255]    # Rojo = destino
props['color_dinamico'] = [210, 215, 220, 180]  # Gris = otros
```

Los colores se asignan directamente en las `properties` de cada feature, y pydeck los lee mediante `get_fill_color="properties.color_dinamico"`.

---

## 8. Glosario

### A

**Arista** — Conexión entre dos nodos en un grafo. En nuestro proyecto, cada arista representa un camino peatonal con un peso (distancia) y un atributo de accesibilidad.

### C

**CARTO** — Proveedor de mapas base. Usamos el estilo Voyager (gratuito, sin token) como mapa de fondo en pydeck, en reemplazo de Mapbox.

**Colección** — En Firestore, agrupa documentos relacionados. Nuestro proyecto usa la colección `"ubicaciones"` para almacenar edificios, baños y rampas.

### D

**deck.gl** — Framework de visualización WebGL desarrollado por Uber. pydeck es su wrapper en Python. Permite renderizar mapas 3D con millones de puntos en el navegador.

**Dijkstra** — Algoritmo clásico de búsqueda de ruta más corta en un grafo ponderado. Funciona explorando nodos desde el origen, expandiendo siempre el de menor costo acumulado. Nuestro proyecto lo usa a través de `nx.shortest_path()`.

**Documento** — En Firestore, unidad básica de datos. Similar a un JSON o un registro en una base de datos. Cada documento tiene un ID único y campos con valores.

### F

**FeatureCollection** — Estructura GeoJSON que agrupa múltiples entidades geográficas (features). Cada feature tiene una geometría (punto, línea, polígono) y propiedades.

**Firebase Firestore** — Base de datos NoSQL en la nube de Google. Almacena datos en documentos organizados en colecciones. Se sincroniza en tiempo real y escala automáticamente.

### G

**gRPC** — Protocolo de comunicación de alto rendimiento creado por Google. Firebase Admin SDK lo usa para comunicarse con Firestore, más rápido que REST.

**Grafo** — Estructura matemática compuesta por nodos (vértices) conectados por aristas (edges). Nuestro mapa del campus es un grafo con 16 nodos y 16 aristas.

**GeoJSON** — Formato estándar para codificar estructuras de datos geográficos. Usa JSON con tipos como `Point`, `LineString`, `Polygon`, `FeatureCollection`.

### L

**Lambda** — Función anónima de una línea en Python. Sintaxis: `lambda args: expresión`. Se usa para operaciones rápidas como filtros con `.apply()`.

### M

**MVP** — Minimum Viable Product (Producto Mínimo Viable). Versión más simple de un producto que puede ser lanzada para obtener retroalimentación temprana de usuarios.

### N

**NetworkX** — Librería de Python para crear, manipular y analizar grafos y redes. Incluye algoritmos como Dijkstra, BFS, PageRank, etc.

**Nodo** — Punto o vértice en un grafo. En nuestro proyecto, los nodos representan puertas, accesos e intersecciones del campus.

### P

**pydeck** — Binding de Python para deck.gl. Permite crear mapas 3D interactivos con pocas líneas de código, integrado nativamente con Streamlit mediante `st.pydeck_chart()`.

### S

**Service Account** — Cuenta de servicio de Google Cloud. Se usa para autenticar aplicaciones servidoras (como nuestro Streamlit) contra servicios de Google como Firebase Firestore.

**Streamlit** — Framework de Python para crear aplicaciones web interactivas con scripts simples. Ideal para prototipos, dashboards y herramientas de datos sin necesidad de HTML/CSS/JS.

**`st.cache_data`** — Decorador de Streamlit que cachea el resultado de una función. Como Streamlit re-ejecuta todo el script en cada interacción, el caché evita operaciones costosas (como lecturas a Firebase) múltiples veces.

**`st.secrets`** — Sistema de Streamlit para manejar credenciales de forma segura. En local se lee desde `.streamlit/secrets.toml`. En producción se configura desde el panel de Streamlit Cloud.

### T

**TOML** — Formato de archivo de configuración minimalista (Tom's Obvious Minimal Language). Usamos `.streamlit/secrets.toml` para almacenar credenciales de Firebase. Sintaxis simple: `[sección]` y `clave = "valor"`.

---

## 9. Preguntas Frecuentes

### ¿Por qué Firebase Firestore y no SQLite o PostgreSQL?

Firestore es una base de datos NoSQL en la nube que ofrece:
- **Escalabilidad automática** — no requiere configurar servidores
- **Actualizaciones en tiempo real** — útil si en el futuro queremos que varios usuarios vean cambios simultáneos
- **Plan gratuito generoso** — 50 mil lecturas/día, suficiente para un MVP
- **Integración nativa con Google Cloud** — la universidad ya usa ecosistema Google
- Adicionalmente, las coordenadas de edificios, baños y rampas ya estaban almacenadas allí

### ¿Por qué usamos CARTO y no Mapbox como mapa base?

Mapbox requiere un token de acceso (incluso para desarrollo) y su plan gratuito tiene límites. CARTO Voyager es un estilo de mapa base **gratuito, sin token**, accesible vía URL pública. Como no necesitamos personalización avanzada del mapa, CARTO cumple perfectamente.

### ¿Qué hace exactamente el decorador `@st.cache_data`?

Streamlit re-ejecuta **todo** el script de arriba a abajo cada vez que el usuario interactúa (cambia un selectbox, marca un checkbox, etc.). Sin `@st.cache_data`, cada interacción haría una lectura a Firestore, consumiendo lecturas del plan gratuito y haciendo la app más lenta.

Con el decorador, los datos de las ubicaciones se leen **una sola vez** y se almacenan en memoria. En interacciones posteriores, Streamlit devuelve los datos cacheados instantáneamente. Si los datos en Firebase cambian, se puede forzar la recarga con `st.cache_data.clear()`.

### ¿Por qué hay dos llamadas separadas a Firebase Firestore en `obtener_ubicaciones()` y `calcular_ruta()`?

Son funcionalmente independientes:
- `obtener_ubicaciones()` — solo lista nombres para los selectores y datos para el mapa. Está cacheada.
- `calcular_ruta()` — necesita las coordenadas para construir el grafo maestro. No está cacheada porque depende de los parámetros del usuario.

Se podrían unificar, pero mantenerlas separadas es más claro y permite que una esté cacheada y la otra no.

### ¿Qué diferencia hay entre `edificios.geojson` y el grafo de `rutas.py`?

- **`edificios.geojson`** — es solo **visual**. Contiene las geometrías (polígonos) de los edificios para renderizar el mapa 3D. No participa en el cálculo de rutas.
- **`rutas.py`** — contiene el **grafo lógico** de navegación: nodos (puertas, intersecciones) y aristas (caminos) con pesos y atributos de accesibilidad. Es lo que usa NetworkX para calcular la ruta más corta.

El GeoJSON es el "dibujo", el grafo es el "mapa de calles" para la navegación.

### ¿Cómo sabe el mapa qué edificio pintar de verde (origen) y rojo (destino)?

El código itera sobre las `features` de `edificios.geojson` y compara el nombre del edificio (primera clave de `properties`) con el valor seleccionado en los `selectbox`. Según coincida con origen, destino o ninguno, asigna un color dinámico (`color_dinamico`) que pydeck lee con `get_fill_color="properties.color_dinamico"`.

### ¿Qué pasa si no existe una ruta accesible entre los puntos seleccionados?

La función `calcular_ruta()` captura la excepción `nx.NetworkXNoPath` (cuando todos los caminos entre origen y destino tienen `accesible=False`) y retorna un mensaje de error. La UI muestra `st.sidebar.error("No existe un camino accesible entre estos puntos")`.

### ¿Cómo se protegen las credenciales de Firebase?

1. Las credenciales están en `.streamlit/secrets.toml`
2. Este archivo está en `.gitignore` — **no se sube a GitHub**
3. El código las lee con `st.secrets["firebase"]`
4. En producción (Streamlit Cloud), se configuran manualmente en el panel de Secrets

El archivo `firebase-credential.json` se conserva localmente como referencia pero también está bloqueado por `.gitignore`.

### ¿Por qué se usa `in locals()` para verificar variables?

Streamlit re-ejecuta todo el script en cada interacción. Si un bloque condicional no se ejecuta (ej. `if nombres_edificios:` es falso porque Firebase falló), la variable `origen_seleccionado` nunca se define. Usar `'origen_seleccionado' in locals()` evita un `NameError` al intentar acceder a una variable que no existe.

### ¿Se puede agregar un nuevo edificio, baño o rampa sin tocar código?

**Sí.** Los datos están en Firebase Firestore, colección `ubicaciones`. Si agregas un nuevo documento allí (con `nombre`, `coordenadas`, `tipo`), automáticamente aparecerá en los selectores y en el mapa la próxima vez que se cargue la app o se limpie el caché con `st.cache_data.clear()`.

Para agregar caminos nuevos o modificar la accesibilidad de uno existente, sí hay que modificar `rutas.py` (porque las aristas del grafo están definidas en código).

### ¿Qué se necesitaría para escalar esta app más allá del MVP?

- **Autenticación** — Firebase Authentication para que cada usuario tenga sus propios datos
- **Panel de administración** — formulario web para agregar ubicaciones y caminos desde la UI (sin editar código)
- **Base de datos para el grafo** — guardar nodos y aristas en Firestore junto con las ubicaciones
- **Historial de rutas** — guardar rutas frecuentes de cada usuario
- **Mapa offline** — service workers y caché de mapas para zonas sin internet
- **Ruteo multimodal** — soporte para silla de ruedas, muletas, coches de bebé, etc.
- **Despliegue profesional** — Streamlit Cloud, Docker, CI/CD, monitoreo
