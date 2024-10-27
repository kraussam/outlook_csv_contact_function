import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import re

class TextToCSV:
    def __init__(self, frame):
        self.frame = frame
        tk.Label(self.frame, text="Paste Text and Convert to CSV").pack(pady=10)

        self.text_input = tk.Text(self.frame, height=10, width=50)
        self.text_input.pack(pady=5)

        tk.Button(self.frame, text="Process and Save CSV", command=self.process_pasted_text).pack(pady=5)
        self.stats_label = tk.Label(self.frame, text="")
        self.stats_label.pack(pady=10)

    def process_pasted_text(self):
        """Process the pasted text and convert it to CSV format."""
        # Get text from input
        pasted_text = self.text_input.get("1.0", tk.END)

        # Regular expression to extract names and emails from the string
        pattern = r'"([^"]+)"\s*<([^>]+)>'
        matches = re.findall(pattern, pasted_text)

        if not matches:
            messagebox.showerror("Error", "No valid names and emails found.")
            return

        # Process each match to split names into First and Last Name
        data = []
        for full_name, email in matches:
            # Split the full name into first and last name (assuming first space separates them)
            name_parts = full_name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''  # Handle cases with no last name
            data.append([first_name, last_name, email])

        # Create a DataFrame with First Name, Last Name, and Email
        df = pd.DataFrame(data, columns=['First Name', 'Last Name', 'Email'])

        # Prompt the user to save the CSV
        output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if output_file:
            df.to_csv(output_file, index=False)
            messagebox.showinfo("Success", f"CSV file saved successfully with {len(df)} entries.")
            self.stats_label.config(text=f"Processed {len(df)} entries.")
        else:
            self.stats_label.config(text="No file saved.")
