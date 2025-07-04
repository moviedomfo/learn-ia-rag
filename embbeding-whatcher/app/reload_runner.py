import sys
from pathlib import Path

# Agrega la carpeta raíz del proyecto al path
root_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_path))

from app.common.pymom.RestartOnChangeHandler  import RestartOnChangeHandler
from watchdog.observers import Observer



if __name__ == "__main__":
    path_to_watch = Path(__file__).parent / "app"
    observer = Observer()
    handler = RestartOnChangeHandler()
    # observer.schedule(handler, path=str(path_to_watch), recursive=True)
    observer.schedule(handler, path=path_to_watch.as_posix(), recursive=True)

    observer.start()
    print(f"👀 Observando cambios en {path_to_watch}...")
    try:
        while True:
            pass  # Mantener el script en ejecución
    except KeyboardInterrupt:
        print("🛑 Deteniendo watcher...")
        observer.stop()
        handler.process.terminate()
        
    observer.join()