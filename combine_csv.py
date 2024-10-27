import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd


class CombineCSV:
    def __init__(self, frame):
        self.frame = frame
        tk.Label(self.frame, text="File Processing - Combine CSV Files").pack(pady=10)

        self.selected_files_label = tk.Label(self.frame, text="No files selected")
        self.selected_files_label.pack(pady=5)

        tk.Button(self.frame, text="Select CSV Files", command=self.select_csv_files).pack(pady=5)
        tk.Button(self.frame, text="Process Files", command=self.process_files).pack(pady=5)

        self.stats_label = tk.Label(self.frame, text="")
        self.stats_label.pack(pady=10)

    def select_csv_files(self):
        self.file_paths = filedialog.askopenfilenames(
            title="Select CSV Files",
            filetypes=[("CSV files", "*.csv")]
        )

        if self.file_paths:
            self.selected_files_label.config(text=f"{len(self.file_paths)} files selected")
        else:
            self.selected_files_label.config(text="No files selected")

    def process_files(self):
        if not hasattr(self, 'file_paths') or not self.file_paths:
            messagebox.showerror("Error", "No files selected.")
            return

        combined_data = pd.DataFrame()
        total_rows = 0
        duplicates_removed = 0

        # Read CSV files and combine them
        for file_path in self.file_paths:
            try:
                data = pd.read_csv(file_path, header=None, usecols=[0, 1, 2])  # First three columns
                total_rows += len(data)
                combined_data = pd.concat([combined_data, data], ignore_index=True)
            except Exception as e:
                messagebox.showerror("Error", f"Could not read {file_path}: {str(e)}")
                return

        # Remove duplicates (assuming email is in the third column)
        initial_count = len(combined_data)
        combined_data.drop_duplicates(subset=2, inplace=True)
        duplicates_removed = initial_count - len(combined_data)

        # Save the combined data
        output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if output_file:
            combined_data.to_csv(output_file, index=False, header=False)
            messagebox.showinfo("Success",
                                f"Files processed.\nTotal rows: {total_rows}\nDuplicates removed: {duplicates_removed}")

        self.stats_label.config(text=f"Total rows: {total_rows}, Duplicates removed: {duplicates_removed}")
