from datetime import datetime
from datetime import timedelta
print(type(datetime.now().strftime("%H:%M")))

time = datetime.now() + timedelta(seconds=1000)
print(time.strftime("%H:%M"))



