import os
import time
from app.common.app_constants import AppConstants  
from pathlib import Path

from app.common.helpers.DateFunctions import DateFunctions
from app.common.helpers.FileFunctions import FileFunctions
from app.common.rag.embedding_generator_openapi import EmbeddingGeneratorOpenApi


ARCHIVO_LOG = Path(AppConstants.API_LOGS_PATH.value) / "processed_files.txt"

def start():
    print("Iniciando watcher...")

    while True:
        archivos_en_carpeta = [f for f in os.listdir( AppConstants.APP_PATH.value) if f.endswith(".txt")]
        archivos_procesados = get_processed_files()

        archivos_nuevos = [f for f in archivos_en_carpeta if f not in archivos_procesados]

        if archivos_nuevos:
            print(f"🔍 Encontrados {len(archivos_nuevos)} archivo(s) nuevo(s)")
            for archivo in archivos_nuevos:
                # process_files(archivo)
                generate_embeddings(archivo)
        else:
            print("✅ Sin archivos nuevos..")

        time.sleep(10)  # Espera 10 segundos y vuelve a chequear


def generate_embeddings(file_name:str):
    fulFileName= Path(AppConstants.APP_PATH.value) / file_name
    print(f"🔍 Generando embeddings para {fulFileName}...")
    gen = EmbeddingGeneratorOpenApi()
    vector = gen.generate_embeddings(fulFileName)
    
    gen.save_embeddings("vector_index", vector)

    set_as_processed(file_name)


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
    # message = f"{date} {file_name}"
    message = DateFunctions.get_dd_mm_yy(file_name)
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write(message + "\n")


    
def get_processed_files() -> set[str]:
    """Lee el archivo de log y devuelve un set con los nombres procesados."""
    if not os.path.exists(AppConstants.API_LOGS_PATH.value):
        os.makedirs(AppConstants.API_LOGS_PATH.value, exist_ok=True)
    
    if not os.path.exists(ARCHIVO_LOG):
        with open(ARCHIVO_LOG, "w", encoding="utf-8") as f:
            pass  # Crea un archivo vacío

    with open(ARCHIVO_LOG, "r", encoding="utf-8") as f:
        return set(
             linea.strip().split()[-1] 
             for linea in f.readlines()
             )