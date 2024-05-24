import sys, requests, json, time

if len(sys.argv) < 2:
    user_input = str(input("> Envíe su mensaje: "))
else:
    user_input = str(sys.argv[1])

def send_request():
    url = 'http://localhost:11434/api/generate'
    data = {
        "model": "llama3",
        "prompt": user_input
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
