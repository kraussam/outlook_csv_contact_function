import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox

class RepairCSV:
    def __init__(self, frame):
        self.frame = frame

        # Create UI components inside the frame
        self.load_button = tk.Button(self.frame, text="Load CSV", command=self.load_csv)
        self.load_button.pack(pady=10)

        self.repair_button = tk.Button(self.frame, text="Repair CSV", command=self.repair_csv)
        self.repair_button.pack(pady=10)

        self.save_button = tk.Button(self.frame, text="Save Repaired CSV", command=self.save_csv, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.df = None

    def load_csv(self):
        """Load a CSV file for processing."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            messagebox.showinfo("CSV Loaded", "CSV file has been loaded successfully.")

    def save_csv(self):
        """Save the repaired CSV to a new file."""
        if self.df is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if save_path:
                self.df.to_csv(save_path, index=False)
                messagebox.showinfo("CSV Saved", "Repaired CSV file has been saved successfully.")
        else:
            messagebox.showwarning("No CSV Loaded", "Please load a CSV file first.")

    def repair_csv(self):
        """Perform all repair actions on the loaded CSV."""
        if self.df is None:
            messagebox.showwarning("No CSV Loaded", "Please load a CSV file first.")
            return

        repair_processor = CSVRepairProcessor(self.df)
        repair_processor.repair()

        # Update DataFrame after repair and allow saving
        self.df = repair_processor.df
        self.save_button.config(state=tk.NORMAL)

        # Show repair report
        report = repair_processor.report()
        messagebox.showinfo("Repair Report", f"Repair Complete:\n{report}")

class CSVRepairProcessor:
    def __init__(self, dataframe):
        self.df = dataframe
        self.removed_non_alpha = 0
        self.removed_spaces = 0
        self.deleted_entries = 0
        self.names_filled = 0
        self.flagged_for_review = 0

    def strip_non_alphabetic(self, value):
        """Removes non-alphabetic characters except hyphens."""
        non_alpha_removed = len(re.findall(r"[^a-zA-Z\-]", value))
        self.removed_non_alpha += non_alpha_removed
        return re.sub(r"[^a-zA-Z\-]", "", value)

    def strip_spaces(self, value):
        """Removes leading and trailing spaces."""
        spaces_removed = len(value) - len(value.strip())
        self.removed_spaces += spaces_removed
        return value.strip()

    def normalize_case(self, value):
        """Converts to lowercase and capitalizes the first letter of each word."""
        return value.lower().title()

    def extract_names_from_email(self, email):
        """Extracts first and last name from the local part of the email."""
        local_part = email.split('@')[0]  # Only consider the part before the '@'

        if '.' in local_part:
            # Split only at the first dot
            first_name, last_name = local_part.split('.', 1)
        else:
            # If no dot is present, treat the entire local part as first name and last name as empty
            first_name, last_name = local_part, ''

        # Strip spaces and non-alphabetic characters from names
        first_name = self.strip_non_alphabetic(self.strip_spaces(first_name))
        last_name = self.strip_non_alphabetic(self.strip_spaces(last_name))

        return first_name, last_name

    def clean_names(self):
        """Cleans and fills names where necessary."""
        for idx, row in self.df.iterrows():
            email = row['Email']
            first_name = row['First Name']
            last_name = row['Last Name']

            # Normalize email and strip spaces
            if pd.notna(email):
                email = self.strip_spaces(email).lower()
            else:
                self.df.drop(idx, inplace=True)
                self.deleted_entries += 1
                continue

            # Strip spaces and non-alphabetic characters from first and last name
            if pd.notna(first_name):
                first_name = self.strip_non_alphabetic(self.strip_spaces(first_name))
                first_name = self.normalize_case(first_name)
            if pd.notna(last_name):
                last_name = self.strip_non_alphabetic(self.strip_spaces(last_name))
                last_name = self.normalize_case(last_name)

            # Handle missing or placeholder names
            if pd.isna(first_name) or first_name.lower() in ["legal name"] or '@' in first_name:
                extracted_first, extracted_last = self.extract_names_from_email(email)
                if extracted_first:
                    first_name = self.normalize_case(extracted_first)
                    last_name = self.normalize_case(extracted_last) if extracted_last else last_name
                    self.names_filled += 1

            # Check if the email is empty; only delete the row if the email is empty
            if pd.isna(email) or email.strip() == "":
                self.df.drop(idx, inplace=True)
                self.deleted_entries += 1
            elif not first_name or not last_name:  # Only check names if email is not empty
                # If either name is still empty after extraction, drop the row
                self.df.drop(idx, inplace=True)
                self.deleted_entries += 1
            else:
                # Reassign cleaned values back to the dataframe
                self.df.at[idx, 'First Name'] = first_name
                self.df.at[idx, 'Last Name'] = last_name
                self.df.at[idx, 'Email'] = email

    def strip_all_columns(self):
        """Applies stripping and normalizing to all cells."""
        for column in ['First Name', 'Last Name', 'Email']:
            self.df[column] = self.df[column].fillna("").apply(lambda x: self.strip_spaces(x))
            if column != 'Email':
                self.df[column] = self.df[column].apply(lambda x: self.strip_non_alphabetic(x))
            self.df[column] = self.df[column].apply(lambda x: x.lower() if column == 'Email' else self.normalize_case(x))

    def delete_empty_entries(self):
        """Deletes rows where all columns (First Name, Last Name, Email) are empty."""
        initial_count = len(self.df)
        self.df.dropna(subset=['Email'], inplace=True)
        self.deleted_entries += (initial_count - len(self.df))

    def repair(self):
        """Main repair function to process all the rules."""
        self.strip_all_columns()
        self.delete_empty_entries()
        self.clean_names()

    def report(self):
        """Generates a summary of the repair process."""
        return {
            'Non-Alphabetic Characters Removed': self.removed_non_alpha,
            'Spaces Removed': self.removed_spaces,
            'Entries Deleted': self.deleted_entries,
            'Names Filled': self.names_filled,
            'Flagged for Manual Review': self.flagged_for_review
        }
