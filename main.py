# import pandas as pd
# import matplotlib.pyplot as plt
# import logging

# # Setup basic logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# def plot_and_save_counts(df, column_name, plot_file_name, text_file_name):
#     if column_name not in df.columns:
#         logging.warning(f"Column '{column_name}' does not exist.")
#         return

#     value_counts = df[column_name].dropna().value_counts()

#     if value_counts.empty:
#         logging.warning(f"No data to plot for '{column_name}'.")
#         return

#     plt.figure(figsize=(20, 10))
#     ax = value_counts.plot(kind='bar')
#     plt.title(f'Counts of Unique Values in {column_name}')
#     plt.ylabel('Counts')
#     plt.xlabel(column_name)
#     ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
#     plt.tight_layout()
#     plt.savefig(plot_file_name)
#     plt.close()

#     with open(text_file_name, 'w') as f:
#         for value, count in value_counts.items():
#             f.write(f"{value}: {count}\n")

# def has_duplicates(row, columns):
#     values = [row[col] for col in columns if not pd.isna(row[col])]
#     return len(values) != len(set(values))

# def remove_duplicates_based_on_reference(new_data_file, existing_data_file, reference_column):
#     try:
#         new_data_df = pd.read_csv(new_data_file)
#         existing_data_df = pd.read_csv(existing_data_file)
#     except Exception as e:
#         logging.error(f"Error reading files: {e}")
#         return

#     if reference_column not in new_data_df.columns or reference_column not in existing_data_df.columns:
#         logging.warning(f"Reference column '{reference_column}' not found in one or both files.")
#         return

#     unique_new_data_df = new_data_df[~new_data_df[reference_column].isin(existing_data_df[reference_column])]
#     unique_new_data_df.to_csv('unique_new_filtered.csv', index=False)
#     logging.info("Unique values retained and saved in 'unique_new_filtered.csv'.")

# # Read the Excel file
# try:
#     df_initial = pd.read_excel('/home/vlad/code/pyth/red/modified_det2_full.xlsx', dtype=str)
# except Exception as e:
#     logging.error(f"Error reading Excel file: {e}")
#     exit()

# threshold = len(df_initial.columns) - 10
# df_processed = df_initial.dropna(thresh=threshold)
# df_processed.to_csv('new_filtered.csv', index=False)

# plot_and_save_counts(df_processed, 'City', 'city_counts.png', 'city_value_counts.txt')
# plot_and_save_counts(df_processed, 'Category', 'category_counts.png', 'category_value_counts.txt')

# # Check for duplicates
# columns_to_check = ['Principal/Heigher Mgm. Emails', 'Emails', 'Other Higher Mgm. Email', 'Other Email', 'Other Email.1']
# rows_with_duplicates = df_processed.apply(has_duplicates, axis=1, columns=columns_to_check)
# df_no_duplicates = df_processed[~rows_with_duplicates]
# df_no_duplicates.to_csv('filtered_no_duplicates.csv', index=False)

# # Remove duplicates based on reference
# remove_duplicates_based_on_reference('filtered_no_duplicates.csv', 'ssaw.csv', 'School Name')

# logging.info("Processing complete.")
import pandas as pd

import pandas as pd

def load_and_prepare(file_path):
    df = pd.read_csv(file_path)
    df['School Name'] = df['School Name'].astype(str).str.lower().str.strip()
    df['Address'] = df['Address'].astype(str).str.lower().str.strip()
    return df

# Load the DataFrames
final_agent_data = load_and_prepare('FinalAgentData.csv')
unique_new_filtered = load_and_prepare('unique_new_filtered.csv')
ssaw = load_and_prepare('ssaw.csv')

# Function to find matching rows based on 'School Name' and 'Address'
def find_matches(df, ref_df):
    return pd.merge(df, ref_df, on=['School Name', 'Address'], how='inner')

# Find matches in both target dataframes
matches_with_unique = find_matches(final_agent_data, unique_new_filtered)
matches_with_ssaw = find_matches(final_agent_data, ssaw)

# Combine the matches into one DataFrame
combined_matches = pd.concat([matches_with_unique, matches_with_ssaw], ignore_index=True)

# Remove duplicate rows based on all columns
combined_matches.drop_duplicates(inplace=True)

# Save the combined data to a new CSV file for analysis
combined_matches.to_csv('Combined_Matches.csv', index=False)
