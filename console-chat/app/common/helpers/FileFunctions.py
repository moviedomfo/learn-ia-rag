from pathlib import Path

class FileFunctions:
    @staticmethod
    def open_txt(file_path: Path | str) -> list[str]:
        """Abre un archivo TXT y devuelve sus líneas, manejando codificaciones comunes automáticamente."""
        encodings_to_try = ["utf-8", "latin-1", "cp1252"]

        for encoding in encodings_to_try:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    return f.readlines()
            except UnicodeDecodeError:
                continue

        raise UnicodeDecodeError("No se pudo leer el archivo con codificaciones comunes (utf-8, latin-1, cp1252).")

