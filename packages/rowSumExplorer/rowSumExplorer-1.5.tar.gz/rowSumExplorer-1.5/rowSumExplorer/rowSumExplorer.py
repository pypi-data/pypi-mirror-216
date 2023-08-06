import pandas as pd
from openpyxl.utils import column_index_from_string
from itertools import combinations
import time


class SetExcelTableColumn:
    def __init__(self, excel_path, sheet_name, cell_range, target_sum, n, column_name,time_limit,max_combinations,first_result):
        self.excel_path = excel_path
        self.sheet_name = sheet_name
        self.cell_range = cell_range
        self.target_sum = target_sum
        self.n= n
        self.column_name = column_name
        self.time_limit = time_limit
        self.max_combinations=max_combinations
        self.first_result=first_result
        self.bypass_time_limit = first_result

    
    def find_table(self):
        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(self.excel_path, sheet_name=self.sheet_name, header=None, engine='openpyxl')
        
        # Convert the cell_range string into a tuple of integers
        start_col, start_row, end_col, end_row = self.cell_range.split(':')
        start_col_num = column_index_from_string(start_col)
        end_col_num = column_index_from_string(end_col)
        start_row_num = int(start_row)
        end_row_num = int(end_row)
        cell_range = (start_row_num, start_col_num, end_row_num, end_col_num)
        
        # Select the specified range of cells
        df = df.iloc[cell_range[0]-1:cell_range[2], cell_range[1]-1:cell_range[3]]
        
        # Extract the table headers
        headers = df.iloc[0]
        
        # Rename the columns in the DataFrame
        df.columns = headers
        
        # Remove the header row from the DataFrame
        df = df[1:]
        
        # Reset the index of the DataFrame
        df = df.reset_index(drop=True)
        
        # Return the resulting DataFrame    
        return df
    
    def get_combinations(self, df, time_limit, max_combinations):
        """
        Generate combinations of n rows from the specified column of the given DataFrame
        where the sum of the values in each combination is equal to the target_sum.
        """
        if self.bypass_time_limit:
            time_limit = None
        column_values = df[self.column_name].tolist()
        
        # Check if target_sum can be reached based on minimum values
        sorted_column_values = sorted(column_values)

        if self.target_sum < sum(sorted_column_values[:self.n]):
            return None
        
        # Check if target_sum is greater than the maximum sum of the n biggest numbers
        if self.target_sum > sum(sorted_column_values[-self.n:]):
            return None

        result_dfs = []
        start_time = time.time()
        for combination in combinations(column_values, self.n):
            if time_limit is not None and time.time() - start_time >= time_limit:               
                break
            if max_combinations is not None and len(result_dfs) >= max_combinations:
                break
            
            if sum(combination) == self.target_sum:
                indices = [i for i, val in enumerate(column_values) if val in combination][:self.n]
                result_df = df.iloc[indices].copy()

                # Calculate the sum of the specified column and add a new row to the DataFrame
                column_sum = result_df[self.column_name].sum()
                if column_sum == self.target_sum:
                    sum_row = pd.DataFrame({self.column_name: column_sum}, index=[len(result_df)])
                    result_df = pd.concat([result_df, sum_row], axis=0, ignore_index=True)

                    # Set "ΣΥΝΟΛΟ" in the first column of the new row
                    result_df.at[len(result_df) - 1, df.columns[0]] = "TOTAL"

                    # Set the total sum in the last column of the new row
                    result_df.at[len(result_df) - 1, self.column_name] = column_sum

                    result_dfs.append(result_df)

                    if self.first_result:
                        break

        return result_dfs


    
    def run(self, output_file):
        df = self.find_table()
        result_dfs = self.get_combinations(df, self.time_limit, self.max_combinations)

        if result_dfs is None:
            with open(output_file, "w") as file:
                file.write("Target Sum can't be reached due to minimum limits")
        else:
            with open(output_file, "w") as file:
                for i, df in enumerate(result_dfs):
                    file.write(f"DataFrame {i+1}:\n")
                    file.write(df.to_string(index=False))
                    file.write("\n\n")
