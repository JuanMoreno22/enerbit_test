
from datetime import datetime
import pytz

def get_colombia_time():
    timezone = pytz.timezone("America/Bogota")
    colombia_time = datetime.now(timezone)
    print("Hora en Colombia:", colombia_time)
    return colombia_time
