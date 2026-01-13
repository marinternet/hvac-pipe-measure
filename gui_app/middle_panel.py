import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import numpy as np

class MiddlePanel(ttk.Frame):
    """
    Middle Panel of the HVAC Pipe Measurement Application.
    Handles the display of images (input & results) and prediction text.
    """

    def __init__(self, parent, colors):
        """
        Initialize the Middle Panel.

        Args:
            parent (tk.Widget): Parent widget.
            colors (dict): Color palette.
        """
        super().__init__(parent, style='Main.TFrame', padding="20")
        self.colors = colors
        
        # Initialize placeholders references
        self.input_placeholder = None
        self.frame_cls = None
        self.frame_seg = None
        self.frame_col = None
        self.result_text = None

        self._create_widgets()

    def _create_widgets(self):
        """
        Create the layout and widgets.
        """
        # --- Input Overview Section ---
        self.overview_container = ttk.Frame(self, style='Panel.TFrame', padding="20")
        self.overview_container.pack(fill='x', pady=(0, 20))

        ttk.Label(self.overview_container, text="Input Overview Image", style='SubHeader.TLabel').pack(anchor='center', pady=(0, 10))
        
        # Display Area for Input Image
        self.input_frame = ttk.Frame(self.overview_container, width=300, height=200) # Fixed dimensions
        self.input_frame.pack(anchor='center')
        self.input_frame.pack_propagate(False)

        self.input_placeholder = ttk.Label(self.input_frame, text="No Input Image Selected", style='Placeholder.TLabel', relief='solid', borderwidth=0)
        self.input_placeholder.pack(fill='both', expand=True) 

        # --- Pipeline Results Section ---
        self.image_container = ttk.Frame(self, style='Panel.TFrame', padding="20")
        self.image_container.pack(fill='both', expand=True, pady=(0, 20))

        ttk.Label(self.image_container, text="Prediction Pipeline", style='SubHeader.TLabel').pack(anchor='w', pady=(0, 20))

        # Grid for pipeline images
        self.images_grid = ttk.Frame(self.image_container, style='Panel.TFrame')
        self.images_grid.pack(fill='both', expand=True)

        self.images_grid.columnconfigure(0, weight=1)
        self.images_grid.columnconfigure(1, weight=1)
        self.images_grid.columnconfigure(2, weight=1)
        self.images_grid.rowconfigure(0, weight=1)

        # Create 3 placeholders for different stages
        self.frame_cls = self._create_image_placeholder(self.images_grid, "YOLO Classification", 0)
        self.frame_seg = self._create_image_placeholder(self.images_grid, "YOLO Segmentation", 1)
        self.frame_col = self._create_image_placeholder(self.images_grid, "Color Segmentation", 2)

        # --- Result Text Section ---
        self.result_frame = ttk.Frame(self, style='Panel.TFrame', padding="20")
        self.result_frame.pack(fill='x', ipady=10)

        ttk.Label(self.result_frame, text="Prediction Results", style='SubHeader.TLabel').pack(anchor='w', pady=(0, 10))

        self.result_text = tk.Text(self.result_frame, height=5, font=('Consolas', 10), state='disabled', relief='flat', bg='#f4f7f6', padx=10, pady=10)
        self.result_text.pack(fill='x')


    def _create_image_placeholder(self, parent, title, col_idx):
        """
        Helper method to create a unified image placeholder frame within a grid.

        Args:
            parent (tk.Widget): Parent widget.
            title (str): Title for the image section.
            col_idx (int): Column index in the grid.
        
        Returns:
            ttk.Label: The label widget where image will be displayed.
        """
        frame = ttk.Frame(parent, style='Panel.TFrame')
        frame.grid(row=0, column=col_idx, sticky='nsew', padx=10)

        # Title
        ttk.Label(frame, text=title, style='Normal.TLabel', font=('Segoe UI', 10, 'bold')).pack(pady=(0, 10))

        # Placeholder Box
        placeholder_frame = ttk.Frame(frame, width=270, height=250)
        placeholder_frame.pack(anchor='center')
        placeholder_frame.pack_propagate(False)

        placeholder = ttk.Label(placeholder_frame, text="No Image", style='Placeholder.TLabel', relief='solid', borderwidth=0)
        placeholder.pack(fill='both', expand=True)
        
        return placeholder

    def display_image(self, image_source, target_widget='input'):
        """
        Load, resize, and display an image on a specific target widget.

        Args:
            image_source (str or np.ndarray): File path or numpy array of the image.
            target_widget (str): Identifier for which widget to update ('input', 'cls', 'seg', 'col').
        """
        # Mapping target strings to actual widgets and dimensions
        widgets_map = {
            'input': (self.input_placeholder, 300, 200),
            'cls': (self.frame_cls, 270, 250),
            'seg': (self.frame_seg, 270, 250),
            'col': (self.frame_col, 270, 250)
        }

        if target_widget not in widgets_map:
            print(f"Error: Unknown target widget '{target_widget}'")
            return

        label_widget, width, height = widgets_map[target_widget]

        try:
            img = None
            # Handle File Path
            if isinstance(image_source, str):
                if not os.path.exists(image_source):
                     print(f"Error: Image path not found: {image_source}")
                     label_widget.config(text="Image Not Found", image="")
                     return
                img = Image.open(image_source)
            
            # Handle Numpy Array (OpenCV)
            elif isinstance(image_source, np.ndarray):
                # OpenCV is BGR, PIL is RGB. Convert BGR -> RGB
                img = Image.fromarray(image_source[..., ::-1])
            
            else:
                print(f"Error: Unsupported image type: {type(image_source)}")
                label_widget.config(text="Unsupported Format", image="")
                return

            # Resize
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Update Label
            label_widget.config(image=photo, text="") 
            label_widget.image = photo # Keep reference
            
        except Exception as e:
            print(f"Error displaying image: {e}")
            label_widget.config(text="Error Loading Image", image="")

    def update_result(self, text):
        """
        Update the text in the results area.

        Args:
            text (str): The result text to display.
        """
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state='disabled')
