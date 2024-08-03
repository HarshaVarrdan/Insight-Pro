import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder, PolynomialFeatures

csvfile = None
csvfileviz = None

def setCsvFile(filepath):
    global csvfile
    csvfile = pd.read_csv(filepath)


def getColumnNames():
    if csvfile is not None:
        column_names = csvfile.columns.to_list()  # Call the method to get the list
        return column_names
    return []

class GetNumericalValues():
    def preprocess_numerical_columns():
        def convert_value(value):
            if isinstance(value, str):
                # Handle currency symbols and commas
                value = value.replace('$', '').replace(',', '').replace('₹', '')
                # Handle percentages
                if '%' in value:
                    value = value.replace('%', '')
                    try:
                        value = float(value) / 100
                    except ValueError:
                        return value  # Return original string if conversion fails
                else:
                    # Handle regular numbers
                    try:
                        value = float(value)
                    except ValueError:
                        return value  # Return original string if conversion fails
            return value

        # Apply the conversion function to each cell in the DataFrame
        csvfile1 = csvfile.applymap(convert_value)
        return csvfile1

    def convert_to_numerical():
        """Convert columns to numerical data types where possible."""
        for col in csvfile.columns:
            csvfile[col] = pd.to_numeric(csvfile[col], errors='ignore')  # Ignore errors for non-numeric values
        return csvfile

    def is_numerical_series(series):
        """Check if a pandas Series is numerical."""
        if pd.api.types.is_numeric_dtype(series):
            return True
        # Check if a majority of the values are numerical
        numeric_count = series.dropna().apply(lambda x: isinstance(x, (int, float))).sum()
        return numeric_count / len(series.dropna()) > 0.8  # Threshold can be adjusted

    def get_numerical_columns():
        # Preprocess to handle currency and percentages
        csvfile = GetNumericalValues.preprocess_numerical_columns()
        
        # Convert to numerical data types
        csvfile = GetNumericalValues.convert_to_numerical()
        
        # Identify numerical columns
        numerical_columns = [col for col in csvfile.columns if GetNumericalValues.is_numerical_series(csvfile[col])]
        return numerical_columns

    def getNumericalColumns():
        global csvfile
        numerical_columns = GetNumericalValues.get_numerical_columns()
        print("Numerical columns:", numerical_columns)

        # Retain only the numerical columns in the DataFrame
        csvfile = GetNumericalValues.preprocess_numerical_columns()
        print(csvfile.head(10))

        return DateExtraction.extractDateTime()


class DateExtraction():
    def extract_dates_and_times():
        global csvfile
        date_columns = []
        time_columns = []
        extracted_columns = []

        # Identify columns with date-like or time-like content
        for column in csvfile.columns:
            if csvfile[column].dtype == 'object':
                # Attempt to infer if the column contains date or time values
                try:
                    # Try to convert to datetime
                    temp = pd.to_datetime(csvfile[column], errors='coerce')
                    
                    # Check if conversion yields any non-null values
                    if temp.notna().any():
                        # Determine if the column should be treated as date or time
                        if any(x in column.lower() for x in ['date', 'time', 'timestamp']):
                            if temp.dt.date.notna().any():
                                date_columns.append(column)
                            if temp.dt.time.notna().any():
                                time_columns.append(column)
                except Exception:
                    continue

        # Process date columns
        for column in date_columns:
            csvfile[column] = pd.to_datetime(csvfile[column], errors='coerce')
            csvfile[f'{column}_year'] = csvfile[column].dt.year
            csvfile[f'{column}_month'] = csvfile[column].dt.month
            csvfile[f'{column}_day'] = csvfile[column].dt.day
            extracted_columns.extend([f'{column}_year', f'{column}_month', f'{column}_day'])

        # Process time columns
        for column in time_columns:
            csvfile[column] = pd.to_datetime(csvfile[column], errors='coerce').dt.time

            # Extract time components based on availability
            has_hour = csvfile[column].apply(lambda x: x.hour if pd.notna(x) else None).notna().any()
            has_minute = csvfile[column].apply(lambda x: x.minute if pd.notna(x) else None).notna().any()
            has_second = csvfile[column].apply(lambda x: x.second if pd.notna(x) else None).notna().any()

            if has_hour:
                csvfile[f'{column}_hour'] = csvfile[column].apply(lambda x: x.hour if pd.notna(x) else None)
                extracted_columns.append(f'{column}_hour')
            elif has_minute:
                csvfile[f'{column}_minute'] = csvfile[column].apply(lambda x: x.minute if pd.notna(x) else None)
                extracted_columns.append(f'{column}_minute')
            elif has_second:
                csvfile[f'{column}_second'] = csvfile[column].apply(lambda x: x.second if pd.notna(x) else None)
                extracted_columns.append(f'{column}_second')

        # Drop the original date and time columns
        columns_to_drop = date_columns + time_columns
        if columns_to_drop:
            print("Dropping columns:", columns_to_drop)
        else:
            print("No column is dropped")

        csvfile = csvfile.drop(columns=columns_to_drop, errors='ignore')

        return csvfile, extracted_columns

    # Example usage
    # Assume 'csvfile' is your DataFrame
    def extractDateTime():
        global csvfile
        csvfile, extracted_columns = DateExtraction.extract_dates_and_times()
        return ExtraFunctions.Extras()
    
class ExtraFunctions():
    def drop_empty_and_constant_columns(df):
        # Identify columns that are completely empty
        empty_columns = df.columns[df.isna().all()].tolist()
        
        # Identify columns where all values are the same
        constant_columns = [col for col in df.columns if df[col].nunique() == 1]

        # Drop columns that are completely empty or have constant values
        columns_to_drop = empty_columns + constant_columns
        df_dropped = df.drop(columns=columns_to_drop, errors='ignore')
        
        # Display the number of columns dropped and their names
        print(f"Number of columns dropped: {len(columns_to_drop)}")
        if columns_to_drop:
            print(f"Names of columns dropped: {columns_to_drop}")
        
        return df_dropped

    def fill_missing_with_median(df):
        """Replace missing values in numerical columns of a DataFrame with the median of each column
        and print missing values before and after for numerical columns only."""
        
        # Select numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        
        # Count missing values before replacement in numerical columns
        missing_before = df[numerical_cols].isna().sum()
        print("Missing values before replacement (numerical columns only):")
        print(missing_before)
        
        # Replace missing values in numerical columns with the median of each column
        for col in numerical_cols:
            # Compute the median of the column, ignoring NaNs
            median = df[col].median()
            # Replace NaNs with the median value
            df[col].fillna(median, inplace=True)
        
        # Count missing values after replacement in numerical columns
        missing_after = df[numerical_cols].isna().sum()
        print("\nMissing values after replacement (numerical columns only):")
        print(missing_after)
        
        return df

    def remove_duplicates(dataframe):
        # Display the number of duplicate rows before removal
        duplicatecount = dataframe.duplicated().sum()
        print(f"Number of duplicate rows before removal: {duplicatecount}")
        
        # Remove duplicates
        dataframe_deduplicated = dataframe.drop_duplicates()
        
        # Display the number of duplicate rows after removal
        duplicatecount1 = dataframe_deduplicated.duplicated().sum()
        print(f"Number of duplicate rows after removal: {duplicatecount1}")
        return dataframe_deduplicated

    def Extras():
        global csvfile
    # Assuming 'csvfile' is your DataFrame
        csvfile = ExtraFunctions.drop_empty_and_constant_columns(csvfile)
        csvfile = ExtraFunctions.fill_missing_with_median(csvfile)
        csvfile = ExtraFunctions.remove_duplicates(csvfile)
        csvfile = Outliers.GetOutliers()


class Outliers():
    def replace_outliers_iqr(dataframe):
        """Replace outliers in numerical columns using the IQR method and display outlier counts before and after replacement."""
        # Convert all columns to numeric, forcing non-numeric values to NaN
        numeric_data = dataframe.apply(pd.to_numeric, errors='coerce')
        
        # Identify numeric columns
        numeric_columns = numeric_data.select_dtypes(include=[np.number]).columns
        
        # Identify potential ID columns based on uniqueness and common naming conventions
        potential_id_columns = [
            col for col in dataframe.columns 
            if dataframe[col].nunique() == len(dataframe) or 'id' in col.lower()
        ]
        
        # Initialize dictionaries to store outlier counts
        outliers_count_before = {}
        outliers_count_after = {}

        # Calculate outliers before replacement
        for column in numeric_columns:
            if column not in potential_id_columns:
                Q1 = numeric_data[column].quantile(0.25)
                Q3 = numeric_data[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Identify outliers before replacement
                outliers_before = numeric_data[(numeric_data[column] < lower_bound) | (numeric_data[column] > upper_bound)]
                outliers_count_before[column] = outliers_before.shape[0]
        
        # Print number of outliers before replacement
        print("Number of outliers before replacement:")
        for col, count in outliers_count_before.items():
            print(f"{col}: {count}")

        # Replace outliers with median
        for column in numeric_columns:
            if column not in potential_id_columns:
                Q1 = numeric_data[column].quantile(0.25)
                Q3 = numeric_data[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Calculate median
                median_value = numeric_data[column].median()
                
                # Replace outliers with median in the original dataframe
                dataframe[column] = dataframe[column].apply(
                    lambda x: median_value if pd.notnull(x) and isinstance(x, (int, float)) and (x < lower_bound or x > upper_bound) else x
                )
        
        # Calculate outliers after replacement
        for column in numeric_columns:
            if column not in potential_id_columns:
                Q1 = numeric_data[column].quantile(0.25)
                Q3 = numeric_data[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers_after = dataframe[(dataframe[column] < lower_bound) | (dataframe[column] > upper_bound)]
                outliers_count_after[column] = outliers_after.shape[0]
        
        # Print number of outliers after replacement
        print("\nNumber of outliers after replacement:")
        for col, count in outliers_count_after.items():
            print(f"{col}: {count}")

        return dataframe
    
    def GetOutliers():
        global csvfile, csvfileviz
        csvfile = Outliers.replace_outliers_iqr(csvfile)
        csvfileviz = csvfile
        return csvfile
