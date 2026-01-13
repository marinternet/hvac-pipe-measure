import tkinter as tk
from tkinter import ttk
import datetime

class RightPanel(ttk.Frame):
    """
    Right Panel of the HVAC Pipe Measurement Application.
    Handles logging of system activities and messages.
    """

    def __init__(self, parent, colors):
        """
        Initialize the Right Panel.

        Args:
            parent (tk.Widget): The parent widget (container).
            colors (dict): Dictionary of color codes used for styling.
        """
        super().__init__(parent, style='Panel.TFrame', padding="20", width=250)
        self.pack_propagate(False) # Prevent frame from shrinking to fit content
        self.colors = colors
        self._create_widgets()

    def _create_widgets(self):
        """
        Create and arrange widgets within the panel.
        """
        # Header Label
        ttk.Label(self, text="Log Activity", style='SubHeader.TLabel').pack(anchor='w', pady=(0, 20))
        
        # Log Text Area (ReadOnly)
        self.log_text = tk.Text(self, font=('Consolas', 9), state='disabled', relief='flat', bg='#f8f9fa', height=20)
        self.log_text.pack(fill='both', expand=True, pady=(0, 10))
        
        # Clear Log Button
        ttk.Button(self, text="🗑 Clear Log", style='Danger.TButton', command=self.clear_log, cursor='hand2').pack(fill='x')
        
        # Initial Log Message
        self.log_message("Application started.")

    def log_message(self, message):
        """
        Append a message to the log text area with a current timestamp.

        Args:
            message (str): The message text to log.
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{timestamp}] {message}\n"
        
        try:
            self.log_text.config(state='normal') # Enable editing
            self.log_text.insert(tk.END, full_msg) # Append message
            self.log_text.see(tk.END) # Scroll to bottom
            self.log_text.config(state='disabled') # Disable editing
        except Exception as e:
            print(f"Error logging message: {e}")

    def clear_log(self):
        """
        Clear all content from the log text area.
        """
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        self.log_message("Log cleared.")
