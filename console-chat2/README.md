<http://localhost:8888/tree>?

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
🔸 poetry init

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
📌falta 
	poetry add llama-cpp-python
	conda install -c conda-forge llama-cpp-python -y




How to install LangChain packages