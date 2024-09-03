
import csv
import pandas as pd

def process_string(input_str):
    pairs = input_str.split(';')
    cleaned_list = []
    for pair in pairs:
        cleaned_pair = pair.replace('<', '').replace('>', '').replace('"', '').strip()
        if ' ' in cleaned_pair:
            name, email = cleaned_pair.rsplit(' ', 1)
            if '@' in name:
                cleaned_list.extend(['', ''])
                cleaned_list.append(email)
            else:
                cleaned_list.extend(name.split())
                cleaned_list.extend(['', ''])
                cleaned_list.append(email)
        else:
            cleaned_list.extend(['', ''])
            cleaned_list.append(cleaned_pair)
    return cleaned_list


def save_to_csv(data_list, filename):
    rows = []
    current_row = []
    for word in data_list:
        if '@' in word:
            current_row.append(word)
            rows.append(current_row)
            current_row = []
        elif len(current_row) == 0:
            current_row.append(word)
        else:
            if len(current_row) == 2:
                current_row[1] += " " + word
            else:
                current_row.append(word)
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['First Name', 'Last Name', 'Email'])
        writer.writerows(rows)


def process_csv_files(files):
    combined_data = []
    for file in files:
        df = pd.read_csv(file)
        combined_data.append(df)
    if not combined_data:
        raise ValueError("No data to process.")
    combined_df = pd.concat(combined_data, ignore_index=True)
    if 'Email' not in combined_df.columns:
        raise ValueError("'Email' column not found in the data.")
    combined_df['Email'] = combined_df['Email'].str.lower()
    original_count = len(combined_df)
    unique_df = combined_df.drop_duplicates(subset='Email', keep='first')
    deleted_count = original_count - len(unique_df)
    removed_emails = combined_df[combined_df.duplicated(subset='Email', keep='first')]['Email'].tolist()
    return unique_df, deleted_count, removed_emails


def subtract_csv_files(files):
    if not files:
        raise ValueError("No files to process.")

    # Load all CSV files into DataFrames
    data_frames = [pd.read_csv(file) for file in files]

    if not data_frames:
        raise ValueError("No data to process.")

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(data_frames, ignore_index=True)

    if 'Email' not in combined_df.columns:
        raise ValueError("'Email' column not found in the data.")

    # Convert 'Email' column to lowercase for consistency
    combined_df['Email'] = combined_df['Email'].str.lower()

    # Get all unique emails
    all_emails = combined_df['Email'].unique()

    # Identify duplicate emails
    duplicates = combined_df[combined_df.duplicated(subset='Email', keep=False)]

    # Remove all rows that have duplicate emails
    filtered_df = combined_df[~combined_df['Email'].isin(duplicates['Email'])]

    # Number of removed entries
    deleted_count = len(duplicates)

    # Emails removed
    removed_emails = duplicates['Email'].unique().tolist()

    return filtered_df, deleted_count, removed_emails

