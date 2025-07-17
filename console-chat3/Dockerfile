FROM ollama/ollama:latest


# Exponer puerto
EXPOSE 11434

# Servir cuando el contenedor se inicie

# Al iniciar el contenedor, descarga el modelo si no está, y luego arranca el servidor
CMD bash -c "\
  ollama serve & \
  sleep 2 && \
  ollama pull llama3.2:1B-Q4_0 && \
  fg"