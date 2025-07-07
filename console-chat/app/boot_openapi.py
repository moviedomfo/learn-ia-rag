import os
import time
from app.common.app_constants import AppConstants  
from pathlib import Path

from app.common.helpers.DateFunctions import DateFunctions
from app.common.helpers.FileFunctions import FileFunctions
from langchain_core.messages import HumanMessage
# Detectar qué versión de LangChain está instalada y usar el import correcto
# try:
from langchain_openai import ChatOpenAI
print("✅ Usando langchain_openai (v0.2.0+)")

ARCHIVO_LOG = Path(AppConstants.API_LOGS_PATH.value) / "processed_files.txt"
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

def start():
    print("💬 Chat IA iniciado. Escribí 'salir' para terminar.\n")

    while True:
        prompt = input("👤 Vos: ")
        if prompt.lower() == "salir":
            break

        response = chat.invoke([HumanMessage(content=prompt)])
        print(f"🤖 Walter bot: {response}")
    

def process_files(file_name):
    """Acá va lo que quieras hacer con cada archivo nuevo."""
    # path = os.path.join(AppConstants.APP_PATH.value, file_name)
    fullName= Path(AppConstants.APP_PATH.value) / file_name
    print(f"Procesando archivo: {fullName}")
    
    # Por ahora simplemente leemos y mostramos las primeras líneas
    lineas = FileFunctions.open_txt(fullName)

    print(f"🔍 {len(lineas)} líneas en el archivo {file_name}")

        # for linea in lineas[:3]:
        #     print(" →", linea.strip())

    set_as_processed(file_name)


def set_as_processed(file_name):
    """Agrega un nombre de archivo al log de procesados."""
    # date = time.strftime("%Y-%m-%d %H:%M:%S")
    message = DateFunctions.get_dd_mm_yy(file_name)
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write(message + "\n")


    
