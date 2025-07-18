from app.common.app_constants import LogIcon
import pendulum
tz = pendulum.timezone('America/Argentina/Buenos_Aires')
import pendulum

class LogFunctions:
  

    @staticmethod
    def print_OK(text: str) -> None:
        LogFunctions._log(LogIcon.OK, text)

    @staticmethod
    def print_warn(text: str) -> None:
        LogFunctions._log(LogIcon.WARN, text)

    @staticmethod
    def print_error(text: str) -> None:
        LogFunctions._log(LogIcon.ERROR, text)

    @staticmethod
    def _log(icon: LogIcon, text: str) -> None:
        """Imprime un mensaje con símbolo y timestamp en formato ISO con TZ de Argentina."""
        current_date = pendulum.now(tz=tz).isoformat(timespec='auto')
        print(f"{icon.value} {current_date} {text}")
