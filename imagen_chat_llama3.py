import sys, requests, json, base64

if len(sys.argv) < 2:
    user_input = str(input("> Envíe su mensaje: "))
else:
    user_input = str(sys.argv[1])


# Ruta de la imagen a codificar en Base64
imagen_ruta = "/home/admin1/Downloads/images.png"

# Leer la imagen en modo binario
with open(imagen_ruta, "rb") as imagen_file:
    # Leer los bytes de la imagen
    imagen_bytes = imagen_file.read()
    # Codificar los bytes en Base64
    imagen_base64 = base64.b64encode(imagen_bytes).decode("utf-8")


def send_request():
    url = 'http://localhost:11434/api/generate'
    data = {
        "model": "llava",
        "prompt": user_input,
        "images": [imagen_base64]
    }
    response = requests.post(url, data=json.dumps(data))
    return response.text  # Devuelve el texto de la respuesta en lugar de intentar convertirlo a JSON

def interpret_response(response_text):
    responses = []
    lines = response_text.strip().split('\n')  # Divide la respuesta en líneas
    for line in lines:
        try:
            json_data = json.loads(line)  # Intenta cargar cada línea como JSON
            if not json_data["done"]:
                responses.append(json_data["response"])
        except json.JSONDecodeError:
            pass  # Ignora las líneas que no son JSON válidos
    return responses

response_text = send_request()
responses = interpret_response(response_text)
print("> ", ''.join(responses))