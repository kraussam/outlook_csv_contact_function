import tkinter as tk
from tkinter import filedialog, messagebox
import os
import tkinter.font as tkfont
import tkinterdnd2 as tkdnd2
from processing import process_string, save_to_csv, process_csv_files, subtract_csv_files


class CSVProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title('CSV Processor')

        # Set a fixed size for the window
        self.root.geometry('300x200')

        # Create the top menu
        self.menu = tk.Menu(root)
        self.root.config(menu=self.menu)
        self.menu.add_command(label="File Processing", command=self.show_file_processing)
        self.menu.add_command(label="Text to CSV", command=self.show_text_to_csv)

        # Create frames for each section
        self.file_processing_frame = tk.Frame(root)
        self.text_to_csv_frame = tk.Frame(root)

        self.create_file_processing_frame()
        self.create_text_to_csv_frame()

        # Show the file processing frame by default
        self.show_file_processing()

    def create_file_processing_frame(self):
        self.label = tk.Label(self.file_processing_frame, text="Drag and Drop CSV Files Here", font=('Arial', 12))
        self.label.pack(pady=10)

        # Buttons for file operations
        self.select_button = tk.Button(self.file_processing_frame, text="Select Files", command=self.select_files,
                                       width=20)
        self.select_button.pack(pady=5)

        self.go_button = tk.Button(self.file_processing_frame, text="Combine Files", command=self.combine_files,
                                   width=20)
        self.go_button.pack(pady=5)

        self.subtract_button = tk.Button(self.file_processing_frame, text="Subtract Files", command=self.subtract_files,
                                         width=20)
        self.subtract_button.pack(pady=5)

        self.clear_button = tk.Button(self.file_processing_frame, text="Clear File Section", command=self.clear_files,
                                      width=20)
        self.clear_button.pack(pady=5)

        self.root.drop_target_register(tkdnd2.DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)
        self.files = []

    def create_text_to_csv_frame(self):
        tk.Label(self.text_to_csv_frame, text="Paste your string below:", font=('Arial', 12)).pack(pady=10)
        self.text_area = tk.Text(self.text_to_csv_frame, height=8, width=70)
        self.text_area.pack(pady=10)
        bold_font = tkfont.Font(size=10, weight="bold")
        convert_button = tk.Button(self.text_to_csv_frame, text="Convert to CSV", command=self.convert_to_csv, width=20)
        convert_button.pack(pady=5)
        self.status_label = tk.Label(self.text_to_csv_frame, text="", font=bold_font)
        self.status_label.pack(pady=5)

    def show_file_processing(self):
        self.file_processing_frame.pack(fill=tk.BOTH, expand=True)
        self.text_to_csv_frame.pack_forget()

    def show_text_to_csv(self):
        self.text_to_csv_frame.pack(fill=tk.BOTH, expand=True)
        self.file_processing_frame.pack_forget()

    def on_drop(self, event):
        self.files = self.root.tk.splitlist(event.data)
        self.label.config(text=f"{len(self.files)} files selected")

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        if files:
            self.files = list(files)
            self.label.config(text=f"{len(self.files)} files selected")

    def combine_files(self):
        if not self.files:
            messagebox.showerror("Error", "No files selected. Please select files first.")
            return
        try:
            unique_df, deleted_count, removed_emails = process_csv_files(self.files)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if save_path:
            try:
                unique_df.to_csv(save_path, index=False)
                messagebox.showinfo("File Saved", f"File saved as {os.path.basename(save_path)}")
                if deleted_count > 0:
                    removed_emails_info = "\n".join(removed_emails[:5])
                    messagebox.showinfo("Duplicates Removed",
                                        f"Total entries: {len(unique_df)}\nNumber of duplicates removed: {deleted_count}\n\nSample removed emails:\n{removed_emails_info}")
                else:
                    messagebox.showinfo("No Duplicates", "No duplicate emails were found.")
                combine_more = messagebox.askyesno("Combine More", "Would you like to combine more CSV emailing lists?")
                if combine_more:
                    self.files = []
                    self.label.config(text="Drag and Drop CSV Files Here")
                else:
                    self.root.quit()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def subtract_files(self):
        if not self.files:
            messagebox.showerror("Error", "No files selected. Please select files first.")
            return
        try:
            filtered_df, deleted_count, removed_emails = subtract_csv_files(self.files)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if save_path:
            try:
                filtered_df.to_csv(save_path, index=False)
                messagebox.showinfo("File Saved", f"File saved as {os.path.basename(save_path)}")
                if deleted_count > 0:
                    removed_emails_info = "\n".join(removed_emails[:5])
                    messagebox.showinfo("Entries Removed",
                                        f"Total entries remaining: {len(filtered_df)}\nNumber of entries removed: {deleted_count}\n\nSample removed emails:\n{removed_emails_info}")
                else:
                    messagebox.showinfo("No Removals", "No entries were removed.")
                subtract_more = messagebox.askyesno("Subtract More",
                                                    "Would you like to subtract more CSV emailing lists?")
                if subtract_more:
                    self.files = []
                    self.label.config(text="Drag and Drop CSV Files Here")
                else:
                    self.root.quit()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def clear_files(self):
        self.files = []
        self.label.config(text="Drag and Drop CSV Files Here")

    def convert_to_csv(self):
        input_str = self.text_area.get("1.0", tk.END).strip()
        if input_str:
            cleaned_list = process_string(input_str)
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                save_to_csv(cleaned_list, file_path)
                self.status_label.config(text=f"CSV file saved successfully! Number of entries: {len(cleaned_list)}",
                                         font=bold_font)
                os.startfile(file_path)
            else:
                self.status_label.config(text="File save cancelled.")
        else:
            self.status_label.config(text="No input provided.")


if __name__ == "__main__":
    root = tkdnd2.Tk()
    app = CSVProcessor(root)
    root.mainloop()

