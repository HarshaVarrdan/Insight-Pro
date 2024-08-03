import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder, PolynomialFeatures
import sys

file_path = sys.argv[1]
function_name = sys.argv[2]

csvfile

def SetCsvFile(file_path):
    global csvfile
    csvfile = pd.read_csv(file_path)

def GetColumnNames():
    column_names = csvfile.columns.to_list
    return column_names

functions = {
    'SetCsvFile': SetCsvFile,
}

if function_name in functions:
    result = functions[function_name](file_path)
    print(result)
else:
    print(f"Function {function_name} not found")