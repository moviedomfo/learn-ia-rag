<http://localhost:8888/tree>?

```bash
# Create a new conda environment with Python 3.13.5
conda create -n bootagents python=3.13.5

# Activate the environment
conda activate bootagent

# Install poetry from conda-forge
conda install -c conda-forge poetry
conda install -c conda-forge faiss-cpu
# Export the environment to a YAML file
conda env export > environment.yml


```

```bash
# Create a new environment from the YAML file
conda env create -f environment.yml
```

```bash
# regullary update with
conda env update -f environment.yml
                    
```

pip install -r requirements.txt
pip install --upgrade --quiet  llama-cpp-python
pip install llama-cpp-python

Install with conda

```bash
    conda install -c conda-forge pendulum
    conda install -c conda-forge llama-cpp-python
    conda install -c conda-forge langchain-community
```
