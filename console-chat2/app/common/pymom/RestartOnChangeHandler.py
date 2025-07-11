from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

SCRIPT_TO_RUN = "app/main.py"

class RestartOnChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = self.start_process()

    def start_process(self):
        print(f"🚀 Lanzando {SCRIPT_TO_RUN}...")
        return subprocess.Popen(["python", SCRIPT_TO_RUN])


    def restart_process(self):
        print("🔄 Cambio detectado. Reiniciando xx...")
        self.process.terminate()
        self.process.wait()
        self.process = self.start_process()

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            self.restart_process()

