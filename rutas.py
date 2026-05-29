nodos_campus = {
    "puerta_m1": {"lat": -33.4662648, "lon": -70.5979135},
    "puerta_m2": {"lat": -33.4662648, "lon": -70.5979135},
    "puerta_m3": {"lat": -33.4662648, "lon": -70.5979135},
    "puerta_m5": {"lat": -33.4665308, "lon": -70.5968849},
    "puerta_m6": {"lat": -33.4660757, "lon": -70.5967263},
    "entrada1_m7": {"lat": -33.4460206, "lon": -70.5969161},
    "entrada2_m7": {"lat": -33.4660041, "lon": -70.5972755},
    "entrada1_m8": {"lat": -33.4664914, "lon": -70.5968769},
    "entrada2_m8": {"lat": -33.4661392, "lon": -70.5968450},
    "entrada_container": {"lat": -33.4659135, "lon": -70.5965909},

    "interseccion1": {"lat": -33.4662908, "lon": -70.5969858},
    "interseccion2": {"lat": -33.4665095, "lon": -70.5969965},
    "interseccion3": {"lat": -33.4661311, "lon": -70.5969647},
    "interseccion4": {"lat": -33.4660690, "lon": -70.5968390},
    "interseccion5": {"lat": -33.4660293, "lon": -70.5968390},
    "interseccion6": {"lat": -33.4659155, "lon": -70.5968302},
}

caminos_campus = [
    # Desde M1 a M5
    {
        "origen": "edificio_m1",
        "destino": "puerta_m1",
        "peso": 1,
        "accesible": True
    },

    {
        "origen": "puerta_m1",
        "destino": "interseccion1",
        "peso": 3,
        "accesible": True
    },

    {
        "origen": "interseccion1",
        "destino": "interseccion2",
        "peso": 15,
        "accesible": True
    },

    {
        "origen": "interseccion2",
        "destino": "puerta_m5",
        "peso": 5,
        "accesible": True

    },

    {
        "origen": "puerta_m5",
        "destino": "edificio_m5",
        "peso": 1,
        "accesible": True

    },

    # Desde Interseccion 1 a M6
    {
        "origen": "interseccion1",
        "destino": "interseccion3",
        "peso": 15,
        "accesible": True
    },

    {
        "origen": "interseccion3",
        "destino": "entrada2_m8",
        "peso": 15,
        "accesible": True
    },


    {
        "origen": "entrada2_m8",
        "destino": "interseccion4",
        "peso": 15,
        "accesible": True
    },

    {
        "origen": "interseccion4",
        "destino": "puerta_m6",
        "peso": 15,
        "accesible": True
    },

    {
        "origen": "puerta_m6",
        "destino": "edificio_m6",
        "peso": 1,
        "accesible": True
    },
    # Desde Interseccion 4 a Puerta 1 M7
    {
        "origen": "interseccion4",
        "destino": "interseccion5",
        "peso": 15,
        "accesible": True
    },

    {
        "origen": "interseccion5",
        "destino": "entrada1_m7",
        "peso": 15,
        "accesible": True
    },

    {
        "origen": "entrada1_m7",
        "destino": "edificio_m7",
        "peso": 1,
        "accesible": True
    },
    # Desde Interseccion 5 a Container
    {
        "origen": "interseccion5",
        "destino": "interseccion6",
        "peso": 15,
        "accesible": True
    },

    {
        "origen": "interseccion6",
        "destino": "entrada_container",
        "peso": 15,
        "accesible": True
    },
    {
        "origen": "entrada_container",
        "destino": "container",
        "peso": 1,
        "accesible": True
    },

]

#Prueba
