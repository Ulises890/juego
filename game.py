import time

import speech_recognition as sr
from googletrans import Translator
from random import choice

# posibles idiomas con sus códigos
descriptions = {
    "inglés": "en",
    "francés": "fr",
    "alemán": "de",
    "italiano": "it",
    "portugués": "pt",
    "español": "es"
}

# Diccionario de palabras por nivel
words_by_level = {
    "facil": [
        "gato", "perro", "manzana", "leche", "sol",
        "casa", "libro", "silla", "mesa", "flor"
    ],
    "medio": [
        "banano", "escuela", "amigo", "ventana", "amarillo",
        "cocina", "jardín", "familia", "ciudad", "puerta"
    ],
    "dificil": [
        "tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion",
        "desarrollo", "conocimiento", "experiencia", "conversacion", "aplicacion"
    ]
}

translator = Translator()



def get_translation(spanish_word: str, dest_language: str = "en") -> str:
    """Traduce la palabra del español al idioma destino."""
    result = translator.translate(spanish_word, src="es", dest=dest_language)
    return result.text.lower()


def play_round(level: str, dest_language: str) -> bool:
    """Juega una ronda; devuelve True si la respuesta fue correcta.

    `dest_language` se utiliza tanto para traducir la palabra como
    para configurar el idioma del reconocimiento.
    """
    palabras = words_by_level.get(level, [])
    if not palabras:
        print("Nivel desconocido. Selecciona fácil, medio o dificil.")
        return False

    palabra = choice(palabras)
    print(f"Palabra en español: {palabra}")

    traduccion = get_translation(palabra, dest_language=dest_language)
    # imprimimos traducción para pruebas
    # print(f"(debug) traducción esperada: {traduccion}")

    # escuchar la pronunciación del usuario mediante el micrófono
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Escuchando... pronuncia la traducción en el idioma seleccionado ({dest_language}).")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            print("No se detectó ninguna voz.")
            return
    try:
        # usar el mismo código de idioma para el reconocimiento de voz
        respuesta = r.recognize_google(audio, language=dest_language).lower()
    except sr.UnknownValueError:
        respuesta = ""
    except sr.RequestError as e:
        print(f"Error en el servicio de reconocimiento: {e}")
        respuesta = ""

    if not respuesta:
        print("No se entendió tu pronunciación. Intenta de nuevo.")
        return

    print(f"Has dicho: {respuesta}")

    if respuesta.strip() == traduccion.strip():
        print("¡Correcto! La pronunciación coincide con la traducción.")
        return True
    else:
        print(f"Incorrecto. La traducción correcta era '{traduccion}'.")
        return False


def main():
    print("=== Juego de traducción por voz ===")
    print("Idiomas disponibles:")
    for name, code in descriptions.items():
        print(f"  {name} ({code})")
    dest_language = input("Selecciona un idioma por nombre o código: ")
    if dest_language.lower() == "salir":
        print("¡Gracias por jugar!")
        return
    dest_language = dest_language.lower().strip()
    # convertir nombre a código si es necesario
    if dest_language in descriptions:
        dest_language = descriptions[dest_language]
    # si no coincide con un código válido, avisar y salir
    elif dest_language not in descriptions.values():
        print("Idioma no reconocido, usando inglés por defecto.")
        dest_language = "en"

    nivel = input("Elige un nivel (facil/medio/dificil): ")
    if nivel.lower() == "salir":
        print("¡Gracias por jugar!")
        return
    nivel = nivel.lower()

    print("Puedes escribir 'salir' en cualquier momento para detener el juego.")
    score = 0
    rounds = 0
    while True:
        correcto = play_round(nivel, dest_language)
        rounds += 1
        if correcto:
            score += 1
        print(f"Puntuación: {score}/{rounds}")
        print()
        # pequeña pausa
        time.sleep(1)
        seguir = input("Presiona Enter para la siguiente palabra o escribe 'salir' para terminar: ")
        if seguir.lower() == "salir":
            print("¡Gracias por jugar! Tu puntuación final fue {}/{}.".format(score, rounds))
            break


if __name__ == "__main__":
    main()
