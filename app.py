import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import firebase_admin
from firebase_admin import credentials, firestore
import networkx as nx
from rutas import nodos_campus, caminos_campus


if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)


@st.cache_data
def obtener_ubicaciones():
    db = firestore.client()
    ubicaciones_ref = db.collection("ubicaciones")
    docs = ubicaciones_ref.stream()

    lista_ubicaciones = []
    for doc in docs:
        datos = doc.to_dict()
        datos['id'] = doc.id
        if 'coordenadas' not in datos:
            datos['coordenadas'] = {'lat': 0.0, 'lon': 0.0}
        lista_ubicaciones.append(datos)

    return lista_ubicaciones


def calcular_ruta(origen, destino, solo_accesible):
    db = firestore.client()
    ubicaciones_ref = db.collection("ubicaciones")
    docs = ubicaciones_ref.stream()

    coords_firebase = {}
    for doc in docs:
        datos = doc.to_dict()
        if 'coordenadas' in datos and datos['coordenadas']:
            coords_firebase[doc.id] = datos['coordenadas']

    coords_maestro = nodos_campus.copy()
    coords_maestro.update(coords_firebase)

    G = nx.Graph()
    for camino in caminos_campus:
        if solo_accesible and not camino["accesible"]:
            continue
        G.add_edge(camino["origen"], camino["destino"], weight=camino["peso"])

    try:
        ruta_nodos = nx.shortest_path(G, source=origen, target=destino, method='dijkstra')

        coordenadas_finales = []
        for nodo in ruta_nodos:
            coords = coords_maestro.get(nodo)
            if not coords:
                continue
            coordenadas_finales.append([coords["lon"], coords["lat"]])

        return {
            'status': 'ok',
            'ruta_nodos': ruta_nodos,
            'coordenadas': coordenadas_finales
        }

    except nx.NetworkXNoPath:
        return {'status': 'error', 'mensaje': 'No existe un camino accesible entre estos puntos'}
    except Exception as e:
        return {'status': 'error', 'mensaje': str(e)}



st.set_page_config(page_title="Campus Accesible MVP", layout="wide")
st.title("Campus Accesible - Mapa Interactivo")

st.sidebar.header("Sistema de Navegación")


try:
    datos_ubicaciones = obtener_ubicaciones()
except Exception as e:
    st.error(f"Error al conectar con Firebase: {e}")
    datos_ubicaciones = None

nombre_a_nodo = {}
nombres_edificios = []

if datos_ubicaciones:
    for ubicacion in datos_ubicaciones:
        nombre = ubicacion.get("nombre", "").strip()
        nodo_id = ubicacion.get("id", "").strip()
        if nombre and nodo_id:
            nombre_a_nodo[nombre] = nodo_id
            nombres_edificios.append(nombre)


if nombres_edificios:
    origen_seleccionado = st.sidebar.selectbox("Punto de Origen:", nombres_edificios, index=0)
    destino_seleccionado = st.sidebar.selectbox(
        "Punto de Destino:", nombres_edificios, index=min(1, len(nombres_edificios) - 1)
    )
    es_accesible = st.sidebar.checkbox("Ruta para movilidad reducida")

    nodo_origen = nombre_a_nodo[origen_seleccionado]
    nodo_destino = nombre_a_nodo[destino_seleccionado]

    resultado = calcular_ruta(nodo_origen, nodo_destino, es_accesible)

    if resultado['status'] == 'ok':
        coordenadas_linea = resultado.get("coordenadas", [])
        if (
            isinstance(coordenadas_linea, list)
            and len(coordenadas_linea) >= 2
            and all(
                isinstance(p, (list, tuple))
                and len(p) == 2
                and isinstance(p[0], (int, float))
                and isinstance(p[1], (int, float))
                for p in coordenadas_linea
            )
        ):
            st.sidebar.success(f"Ruta calculada: {' ➔ '.join(resultado['ruta_nodos'])}")
            ruta_coords = coordenadas_linea
        else:
            st.sidebar.error("La ruta obtenida no contiene coordenadas válidas.")
            ruta_coords = None
    else:
        st.sidebar.error(resultado.get('mensaje', 'No se pudo calcular la ruta.'))
        ruta_coords = None
else:
    if datos_ubicaciones is not None:
        st.sidebar.warning("No hay edificios disponibles para navegación.")


if datos_ubicaciones:
    lista_puntos = []
    for punto in datos_ubicaciones:
        lista_puntos.append({
            "Nombre": punto.get("nombre", "Sin nombre"),
            "Tipo": punto.get("tipo", "Desconocido"),
            "lat": punto["coordenadas"]["lat"],
            "lon": punto["coordenadas"]["lon"],
            "Detalles": punto.get("detalles", "")
        })

    df = pd.DataFrame(lista_puntos)
    df = df.dropna(subset=["lat", "lon"])
    df = df[df["lat"].apply(lambda x: isinstance(x, (int, float)))]
    df = df[df["lon"].apply(lambda x: isinstance(x, (int, float)))]
    df = df[(df["lat"] != 0) & (df["lon"] != 0)]


    with open("edificios.geojson", "r", encoding="utf-8") as f:
        data_edificios = json.load(f)

    with open("caminos.geojson", "r", encoding="utf-8") as f:
        data_caminos = json.load(f)

    for feature in data_edificios.get('features', []):
        if 'properties' not in feature or feature['properties'] is None:
            feature['properties'] = {}

        props = feature['properties']
        nombre_edificio = ''
        if props:
            nombre_edificio = list(props.keys())[0]

        if nombre_edificio and 'origen_seleccionado' in locals() and nombre_edificio == origen_seleccionado:
            props['color_dinamico'] = [40, 200, 80, 255]
        elif nombre_edificio and 'destino_seleccionado' in locals() and nombre_edificio == destino_seleccionado:
            props['color_dinamico'] = [220, 60, 60, 255]
        else:
            props['color_dinamico'] = [210, 215, 220, 180]

    
    capa_edificios_3d = pdk.Layer(
        "GeoJsonLayer",
        data=data_edificios,
        opacity=0.7,
        stroked=True,
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation=20,
        get_fill_color="properties.color_dinamico",
        get_line_color="[255, 255, 255]",
    )

    
    capa_caminos = pdk.Layer(
        "GeoJsonLayer",
        data=data_caminos,
        opacity=0.9,
        stroked=True,
        filled=False,
        extruded=False,
        get_line_color="[120, 130, 140, 255]",
        get_line_width=3,
        line_width_min_pixels=2
    )

    capas = [capa_caminos, capa_edificios_3d]

   
    if 'ruta_coords' in locals() and ruta_coords is not None:
        capa_ruta = pdk.Layer(
            "PathLayer",
            data=[{"path": ruta_coords, "color": [46, 204, 113, 255]}],
            get_path="path",
            get_color="color",
            width_scale=3,
            width_min_pixels=6,
            joint_rounded=True,
            cap_rounded=True
        )
        capas.append(capa_ruta)

   
    if not df.empty:
        capa_nombres = pdk.Layer(
            "TextLayer",
            data=df,
            get_position='[lon, lat, 25]',
            get_text="Nombre",
            get_color="[40, 40, 40, 255]",
            get_size=15,
            get_alignment_baseline="'center'",
            get_text_anchor="'middle'"
        )
        capas.append(capa_nombres)

    
    vista_utem = pdk.ViewState(
        latitude=-33.4655,
        longitude=-70.5975,
        zoom=17.5,
        pitch=0,
        bearing=0
    )

    st.write("### Mapa de Accesibilidad Campus UTEM")

    st.pydeck_chart(pdk.Deck(
        map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
        initial_view_state=vista_utem,
        layers=capas
    ))

elif datos_ubicaciones is not None:
    st.info("No hay puntos guardados en la base de datos.")
