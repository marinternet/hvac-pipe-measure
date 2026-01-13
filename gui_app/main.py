import tkinter as tk
from tkinter import ttk
import os

# Import Panels
from left_panel import LeftPanel
from middle_panel import MiddlePanel
from right_panel import RightPanel

class HVAC_App:
    """
    Main Application Controller for the HVAC Pipe Measurement System.
    Orchestrates the separate panels and manages shared state.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("HVAC Pipe Measurement System")
        self.root.geometry("1400x900")
        self.root.minsize(1280, 800)

        # Set Icon
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_path, 'assets', 'logo.ico')
            self.root.iconbitmap(icon_path)
        except Exception:
            pass

        # Shared State
        self.image_path = None

        # Configuration
        self._configure_styles()
        
        # Initialization
        self._init_ui()

    def _configure_styles(self):
        """
        Define application-wide styles and color palette.
        """
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Color Palette
        self.colors = {
            'bg_main': '#f4f7f6',       # Very light gray/blueish background
            'bg_sidebar': '#2c3e50',    # Deep Blue/Teal for sidebar
            'bg_panel': '#ffffff',      # White panel background
            'primary': '#3498db',       # Bright Blue primary button
            'primary_hover': '#2980b9',
            'danger': '#e74c3c',        # Red danger button
            'danger_hover': '#c0392b',
            'success': '#2ecc71',       # Green success button
            'success_hover': '#27ae60',
            'text_sidebar': '#ecf0f1',  # Light text for sidebar
            'text': '#2c3e50',          # Dark text for main area
            'text_light': '#7f8c8d'     # Gray text
        }

        self.root.configure(bg=self.colors['bg_main'])

        # Frame Styles
        self.style.configure('Main.TFrame', background=self.colors['bg_main'])
        self.style.configure('Sidebar.TFrame', background=self.colors['bg_sidebar'])
        self.style.configure('Panel.TFrame', background=self.colors['bg_panel'], relief='flat')
        
        # Label Styles
        self.style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), background=self.colors['bg_sidebar'], foreground=self.colors['text_sidebar'])
        self.style.configure('SubHeader.TLabel', font=('Segoe UI', 12, 'bold'), background=self.colors['bg_panel'], foreground=self.colors['text'])
        self.style.configure('Normal.TLabel', font=('Segoe UI', 10), background=self.colors['bg_panel'], foreground=self.colors['text'])
        self.style.configure('SidebarText.TLabel', font=('Segoe UI', 10), background=self.colors['bg_sidebar'], foreground=self.colors['text_sidebar'])
        self.style.configure('Placeholder.TLabel', font=('Segoe UI', 10, 'italic'), background='#ecf0f1', foreground=self.colors['text_light'], anchor='center')

        # Button Styles
        self.style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'), background=self.colors['primary'], foreground='white', borderwidth=0, focuscolor='none')
        self.style.map('Primary.TButton', background=[('active', self.colors['primary_hover'])])

        self.style.configure('Danger.TButton', font=('Segoe UI', 10, 'bold'), background=self.colors['danger'], foreground='white', borderwidth=0, focuscolor='none')
        self.style.map('Danger.TButton', background=[('active', self.colors['danger_hover'])])

    def _init_ui(self):
        """
        Initialize and pack the UI components.
        """
        # Main Container
        self.main_container = ttk.Frame(self.root, style='Main.TFrame')
        self.main_container.pack(fill='both', expand=True)

        # 1. Left Panel (Sidebar) - Passed self as controller
        self.left_panel = LeftPanel(self.main_container, controller=self, colors=self.colors)
        self.left_panel.pack(side='left', fill='y')

        # 2. Right Panel (Log)
        self.right_panel = RightPanel(self.main_container, colors=self.colors)
        self.right_panel.pack(side='right', fill='y', padx=(10, 0))

        # 3. Middle Panel (Content)
        self.middle_panel = MiddlePanel(self.main_container, colors=self.colors)
        self.middle_panel.pack(side='left', fill='both', expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = HVAC_App(root)
    root.mainloop()
