import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd


class SubtractCSV:
    def __init__(self, frame):
        self.frame = frame
        tk.Label(self.frame, text="File Processing - Subtract CSV Files").pack(pady=10)

        self.selected_file1_label = tk.Label(self.frame, text="No file selected (File 1)")
        self.selected_file1_label.pack(pady=5)

        self.selected_file2_label = tk.Label(self.frame, text="No file selected (File 2)")
        self.selected_file2_label.pack(pady=5)

        tk.Button(self.frame, text="Select File 1 (Base File)", command=self.select_file1).pack(pady=5)
        tk.Button(self.frame, text="Select File 2 (Subtract File)", command=self.select_file2).pack(pady=5)
        tk.Button(self.frame, text="Subtract Files", command=self.subtract_files).pack(pady=5)

        self.stats_label = tk.Label(self.frame, text="")
        self.stats_label.pack(pady=10)

    def select_file1(self):
        self.file1_path = filedialog.askopenfilename(
            title="Select File 1 (Base CSV File)",
            filetypes=[("CSV files", "*.csv")]
        )
        if self.file1_path:
            self.selected_file1_label.config(text=f"File 1 selected: {self.file1_path}")
        else:
            self.selected_file1_label.config(text="No file selected (File 1)")

    def select_file2(self):
        self.file2_path = filedialog.askopenfilename(
            title="Select File 2 (Subtract CSV File)",
            filetypes=[("CSV files", "*.csv")]
        )
        if self.file2_path:
            self.selected_file2_label.config(text=f"File 2 selected: {self.file2_path}")
        else:
            self.selected_file2_label.config(text="No file selected (File 2)")

    def subtract_files(self):
        if not hasattr(self, 'file1_path') or not self.file1_path:
            messagebox.showerror("Error", "File 1 not selected.")
            return

        if not hasattr(self, 'file2_path') or not self.file2_path:
            messagebox.showerror("Error", "File 2 not selected.")
            return

        try:
            # Load both files
            file1_data = pd.read_csv(self.file1_path, header=None, usecols=[0, 1, 2])
            file2_data = pd.read_csv(self.file2_path, header=None, usecols=[0, 1, 2])

            # Subtract file2_data from file1_data based on the third column (email)
            initial_count = len(file1_data)
            result_data = file1_data[~file1_data[2].isin(file2_data[2])]
            remaining_rows = len(result_data)

            # Save the result
            output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if output_file:
                result_data.to_csv(output_file, index=False, header=False)
                messagebox.showinfo("Success", f"File processed.\nInitial rows: {initial_count}\nRemaining rows: {remaining_rows}")

            self.stats_label.config(text=f"Initial rows: {initial_count}, Remaining rows: {remaining_rows}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while processing the files: {str(e)}")
