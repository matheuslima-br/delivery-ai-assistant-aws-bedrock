import json
import math
import urllib.request
import urllib.parse


# URL da API Overpass utilizada para consultar
# dados do OpenStreetMap.
URL_OVERPASS = "https://overpass-api.de/api/interpreter"


def calcular_distancia(latitude1, longitude1, latitude2, longitude2):
    """
    Calcula a distância entre duas coordenadas geográficas
    utilizando a fórmula de Haversine.

    Retorna a distância em quilômetros.
    """

    raio_terra_km = 6371

    latitude1_rad = math.radians(latitude1)
    latitude2_rad = math.radians(latitude2)

    diferenca_latitude = math.radians(
        latitude2 - latitude1
    )

    diferenca_longitude = math.radians(
        longitude2 - longitude1
    )

    a = (
        math.sin(diferenca_latitude / 2) ** 2
        + math.cos(latitude1_rad)
        * math.cos(latitude2_rad)
        * math.sin(diferenca_longitude / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return raio_terra_km * c


def criar_consulta_overpass(
    latitude,
    longitude,
    raio,
    culinaria
):
    """
    Cria a consulta que será enviada para a API Overpass.
    """

    if culinaria and culinaria.lower() != "qualquer":

        filtro_culinaria = (
            f'[cuisine="{culinaria}"]'
        )

    else:

        filtro_culinaria = ""

    consulta = f"""
    [out:json];

    (
        node[
            "amenity"="restaurant"
            {filtro_culinaria}
        ](
            around:{raio},
            {latitude},
            {longitude}
        );

        way[
            "amenity"="restaurant"
            {filtro_culinaria}
        ](
            around:{raio},
            {latitude},
            {longitude}
        );
    );

    out center;
    """

    return consulta


def consultar_overpass(consulta):
    """
    Envia a consulta para a API Overpass.
    """

    dados = urllib.parse.urlencode({
        "data": consulta
    }).encode("utf-8")

    requisicao = urllib.request.Request(
        URL_OVERPASS,
        data=dados,
        headers={
            "User-Agent": "assistente-delivery-ia/1.0"
        }
    )

    with urllib.request.urlopen(
        requisicao,
        timeout=30
    ) as resposta:

        return json.loads(
            resposta.read().decode("utf-8")
        )


def extrair_restaurantes(
    dados,
    latitude_usuario,
    longitude_usuario
):
    """
    Converte os dados do OpenStreetMap
    para uma estrutura simplificada.
    """

    restaurantes = []

    for elemento in dados.get("elements", []):

        etiquetas = elemento.get(
            "tags",
            {}
        )

        latitude = elemento.get("lat")
        longitude = elemento.get("lon")

        # Objetos do tipo "way" normalmente
        # possuem suas coordenadas dentro de "center".
        if latitude is None:

            centro = elemento.get(
                "center",
                {}
            )

            latitude = centro.get("lat")
            longitude = centro.get("lon")

        if latitude is None or longitude is None:
            continue

        distancia = calcular_distancia(
            latitude_usuario,
            longitude_usuario,
            latitude,
            longitude
        )

        restaurante = {

            "nome": etiquetas.get(
                "name",
                "Restaurante sem nome"
            ),

            "culinaria": etiquetas.get(
                "cuisine",
                "Não informado"
            ),

            "endereco": etiquetas.get(
                "addr:street",
                "Endereço não informado"
            ),

            "telefone": etiquetas.get(
                "phone"
            ),

            "site": etiquetas.get(
                "website"
            ),

            "latitude": latitude,

            "longitude": longitude,

            "distancia_km": round(
                distancia,
                2
            )
        }

        restaurantes.append(
            restaurante
        )

    # Ordena os restaurantes do mais próximo
    # para o mais distante.
    restaurantes.sort(
        key=lambda restaurante:
        restaurante["distancia_km"]
    )

    return restaurantes


def lambda_handler(event, context):
    """
    Função principal da AWS Lambda.
    """

    latitude = float(
        event["latitude"]
    )

    longitude = float(
        event["longitude"]
    )

    raio = int(
        event.get(
            "raio_m",
            5000
        )
    )

    culinaria = event.get(
        "culinaria",
        "qualquer"
    )

    quantidade = int(
        event.get(
            "quantidade",
            20
        )
    )

    # Cria a consulta.
    consulta = criar_consulta_overpass(
        latitude,
        longitude,
        raio,
        culinaria
    )

    # Consulta o OpenStreetMap.
    dados = consultar_overpass(
        consulta
    )

    # Processa os restaurantes.
    restaurantes = extrair_restaurantes(
        dados,
        latitude,
        longitude
    )

    # Limita a quantidade de resultados.
    restaurantes = restaurantes[
        :quantidade
    ]

    return {

        "status": "sucesso",

        "fonte": "OpenStreetMap / Overpass API",

        "busca": {

            "latitude": latitude,

            "longitude": longitude,

            "raio_m": raio,

            "culinaria": culinaria

        },

        "quantidade": len(
            restaurantes
        ),

        "restaurantes": restaurantes
    }
