
Jumpyter --> <http://localhost:8888/tree>

```bash
 # Create a new conda environment with Python 3.13.5
 conda create -n bootagents python=3.13.5

 # Activate the environment
 conda activate bootagent

 # Install poetry from conda-forge
 conda install -c conda-forge poetry
 
 # guardo el ambiente par ala proxima en otro pc 
 # si no ponemos --from-history te emete todas las deps juntas con proetry
 conda env export --from-history > environment.yml
```

Lo demas que se instale lo maneja poetry como gestor de dependencias

# Create a new environment from the YAML file Esto si ya estoy en otro pc

```bash
 conda env create -f environment.yml
```

- Create pyproject.toml

```bash
    poetry init
```

 If Error:
  check name = "app"
  readme file exxist
  app folder withi main.py exist
  
# reparar el toml

 Para que se puedan hacer instalaciones langchaing y salen errores
    For langchain-text-splitters, a possible solution would be to set the `python` property to ">=3.13,<4.0"

 ```bash
  requires-python = ">=3.10,<4.0"    # ← aquí ajustas el rango de Python
 ```

# regullary update with

```bash
 conda env update -f environment.yml
```

🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹
                            Installing dependencies
🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹

✅ poetry add langchain langchain-community
✅ poetry add dotenv pendulum
✅ poetry add faiss-cpu  

  ❌ poetry add sentence-transformers
✅ conda install -c conda-forge sentence-transformers
❌ conda install -c conda-forge huggingface-hub
✅ poetry add huggingface-hub
✅ poetry add langchain-core langchain-ollama
✅ poetry add langchain-huggingface

📌falta pero con docker llama no hace falta
 poetry add llama-cpp-python
     ¿Cuándo usar llama-cpp-python?
        Lo que querés hacer ¿Usás llama-cpp-python?
        Usar modelos GGUF sin Docker ni servidor ✅ Sí
        Integrar con LangChain sin levantar Ollama ✅ Sí
        Usar LangChain con Ollama y Docker ❌ No hace falta

 conda install -c conda-forge llama-cpp-python -y

¿Por qué usar Poetry si ya tienes conda y pip?
    Consistencia de versiones: pip por sí solo no crea un lock file (salvo que uses pip freeze > requirements.txt,
    pero eso no captura bien los sub–dependencias). Poetry automatiza este proceso de lock.
    Reproducibilidad: Si en tu equipo o CI alguien corre poetry install, obtiene el mismo entorno exacto de versiones.

¿No se arma un quilombo mezclándolos?
    Puede haber conflictos si instalas cosas al voleo con conda install dentro del virtualenv que Poetry creó,
    o si combinas pip install y poetry add sin cuidado. Para evitarlo:

  1-  Seleccioná una sola capa para tu proyecto:

        Opción A: Todo con Conda.

            - conda create -n proyecto python=3.x

       Usás conda install y, en última instancia, pip install para paquetes que no existan en conda-forge.

🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹
                            Ollama Contrainer
🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹
Chat <https://chatgpt.com/c/6874fa6b-f334-8002-bb53-d764816185e5>

🚫 Antes hay que descargarce Ollama <https://ollama.com/download>

Hay que descargar el modelo dentro del contenedor

✅ Resumen técnico
El contenedor ollama/ollama expone el servicio en <http://localhost:11434>
LangChain se conecta automáticamente a ese endpoint
  Ollama(model="llama3.2:1B-Q4_0")
  Si no está descargado, da error hasta que hagas:
  
Probá desde terminal (modo curl):

1) revisar docker-compose.yml para ver el nombre del contenedor
2) Levantar el container
    docker compose up -d
3) entro en el contenedor
 docker exec -it llama3 bash

  🐳 Descargar el modelo dentro del contenedor
  
    ollama pull llama3           modelos como llama3
    ollama pull llama3.2:1b      modelos como llama3.2:1B-Q4_0

  ✅ ¿Qué pasa si se apaga el contenedor?

  El modelo no se borra.
   Docker guarda ese volumen (ollama-data) en el host.

  ✅ desde dentro del contenedor, el modelo se descarga y se guarda en:

    /root/.ollama

    volumes:
      - ollama-data:/root/.ollama
