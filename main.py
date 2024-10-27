import tkinter as tk
from combine_csv import CombineCSV
from text_to_csv import TextToCSV
from repair_csv import RepairCSV
from subtract_csv import SubtractCSV

class CSVProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('CSV Processor App')
        self.root.geometry('500x400')

        # Create the menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # Combine CSV Pane
        self.combine_csv_frame = tk.Frame(self.root)
        self.combine_csv = CombineCSV(self.combine_csv_frame)

        # Subtract CSV Pane
        self.subtract_csv_frame = tk.Frame(self.root)  # New subtract frame
        self.subtract_csv = SubtractCSV(self.subtract_csv_frame)

        # Text to CSV Pane
        self.text_to_csv_frame = tk.Frame(self.root)
        self.text_to_csv = TextToCSV(self.text_to_csv_frame)

        # Repair CSV Pane
        self.repair_csv_frame = tk.Frame(self.root)
        self.repair_csv = RepairCSV(self.repair_csv_frame)

        # Add menu options to switch between panes
        self.menu.add_command(label="Combine CSV", command=self.show_combine_csv)
        self.menu.add_command(label="Subtract CSV", command=self.show_subtract_csv)  # Add subtract option
        self.menu.add_command(label="Text to CSV", command=self.show_text_to_csv)
        self.menu.add_command(label="Repair CSV", command=self.show_repair_csv)

        # Show default pane (Combine CSV)
        self.show_combine_csv()

    def show_combine_csv(self):
        """Show the Combine CSV Pane."""
        self.hide_all_frames()
        self.combine_csv_frame.pack(fill=tk.BOTH, expand=True)

    def show_subtract_csv(self):
        """Show the Subtract CSV Pane."""
        self.hide_all_frames()
        self.subtract_csv_frame.pack(fill=tk.BOTH, expand=True)  # Add for subtract

    def show_text_to_csv(self):
        """Show the Text to CSV Pane."""
        self.hide_all_frames()
        self.text_to_csv_frame.pack(fill=tk.BOTH, expand=True)

    def show_repair_csv(self):
        """Show the Repair CSV Pane."""
        self.hide_all_frames()
        self.repair_csv_frame.pack(fill=tk.BOTH, expand=True)

    def hide_all_frames(self):
        """Hide all frames."""
        self.combine_csv_frame.pack_forget()
        self.subtract_csv_frame.pack_forget()  # Add for subtract
        self.text_to_csv_frame.pack_forget()
        self.repair_csv_frame.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVProcessorApp(root)
    root.mainloop()