import os
import sys
import numpy as np
import pandas as pd

amapola_data_file = 'data/amapola.txt'

amapola_data = pd.read_csv(amapola_data_file)
print(amapola_data)
