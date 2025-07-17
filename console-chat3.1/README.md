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