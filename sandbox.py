from datetime import datetime
import pandas as pd

def get_today_str():
    return datetime.today().strftime('%Y_%m_%d')

