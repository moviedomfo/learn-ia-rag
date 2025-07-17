

# Usamos el modelo chico para demos
# llm = Ollama(model="llama3.2:1B-Q4_0")


# pregunta = "¿Qué es un endpoint REST en programación?"
# respuesta = llm.invoke(pregunta)

# print(f"🧠 Pregunta: {pregunta}")
# print(f"🤖 Respuesta: {respuesta}")
from pathlib import Path
import traceback

from app.boot_llama import ChatBootLlama

print("Iniciando start...")
def main():
    try:
        chat:ChatBootLlama = ChatBootLlama()
        chat.run_chat()
    except Exception as e:
        
        print(f"⚠️ Error atrapado: {e}")
        traceback.print_exc()
 


if __name__ == "__main__": 
    main()
