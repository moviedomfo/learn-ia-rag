import datetime
import pendulum
import random
tz = pendulum.timezone('America/Argentina/Buenos_Aires')

class DateFunctions:
    @staticmethod
    def get_dd_mm_yy(text:str) -> str:
        """Returns a random date between start_year and end_year."""
        current_date = pendulum.today()
        """Agrega un nombre de archivo al log de procesados."""
        # date = time.strftime("%Y-%m-%d %H:%M:%S")
        date = current_date.strftime("%d/%m/%Y %H:%M:%S")
        message = f"{date} {text}"
        return message

    @staticmethod
    def days_until_date(target_date):
        """Returns the number of days from today until the target_date."""
        today = datetime.date.today()
        if isinstance(target_date, datetime.datetime):
            target_date = target_date.date()
        return (target_date - today).days