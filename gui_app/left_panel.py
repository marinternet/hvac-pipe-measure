import tkinter as tk
from tkinter import ttk, filedialog
import os

class LeftPanel(ttk.Frame):
    """
    Left Panel of the HVAC Pipe Measurement Application.
    Contains the control buttons for the application (Upload, Predict, etc.).
    """

    def __init__(self, parent, controller, colors):
        """
        Initialize the Left Panel.

        Args:
            parent (tk.Widget): Parent widget.
            controller (App): Reference to the main application class for access to other panels/state.
            colors (dict): Color palette.
        """
        super().__init__(parent, style='Sidebar.TFrame', padding="20", width=200)
        self.pack_propagate(False)
        self.controller = controller
        self.colors = colors
        
        self._create_widgets()

    def _create_widgets(self):
        """
        Create buttons and layout.
        """
        # App Title
        title_label = ttk.Label(self, text="HVAC Pipe\nMeasure", style='Header.TLabel', justify='center')
        title_label.pack(pady=(20, 50))

        # Buttons
        self._create_button("📤 Upload Image", self.upload_image, 'Primary.TButton')
        self._create_button("▶ Start Predict", self.start_predict, 'Primary.TButton')
        self._create_button("⏹ Stop Predict", self.stop_predict, 'Danger.TButton')
        self._create_button("🗑 Clear Image", self.clear_image, 'Danger.TButton')

        # Separator
        separator = tk.Frame(self, bg=self.colors['text_light'], height=1)
        separator.pack(fill='x', pady=30)

        # Status Label
        self.status_label = ttk.Label(self, text="System Ready", style='SidebarText.TLabel')
        self.status_label.pack(side='bottom', pady=20)

    def _create_button(self, text, command, style):
        """
        Helper to create a unified button style.
        """
        if command:
             btn = ttk.Button(self, text=text, style=style, command=command, cursor='hand2')
        else:
             btn = ttk.Button(self, text=text, style=style, cursor='hand2')
        
        btn.pack(fill='x', pady=10, ipady=5)
        return btn

    def upload_image(self):
        """
        Handle image upload. Opens dialog, updates internal state, and displays image.
        """
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            filename = os.path.basename(file_path)
            self.controller.image_path = file_path # Update App state
            self.controller.right_panel.log_message(f"Image uploaded: {filename}")
            
            # Display: Input Overview
            self.controller.middle_panel.display_image(file_path, 'input')
            
            # Showing 3 image based on process
            self.controller.middle_panel.display_image(file_path, 'cls')
            self.controller.middle_panel.display_image(file_path, 'seg')
            self.controller.middle_panel.display_image(file_path, 'col')
           
            
        else:
            self.controller.right_panel.log_message("Image upload cancelled.")

    def start_predict(self):
        """
        Run the YOLO prediction pipeline.
        """
        if self.controller.image_path is None:
            self.controller.right_panel.log_message("Please upload an image first.")
            return

        try:
            
            self.controller.right_panel.log_message("Starting prediction...")
            
            self.controller.right_panel.log_message("Prediction completed.")
            
            # Update Text Results (Mockup for now as original code mocked it)
            self.controller.middle_panel.update_result("Prediction Results\nDiameter estimated: 12\nStatus: Success")

        except Exception as e:
            self.controller.right_panel.log_message(f"Error during prediction: {str(e)}")
            print(f"Prediction Error: {e}")

    def stop_predict(self):
        """
        Placeholder for stopping prediction.
        """
        self.controller.right_panel.log_message("Stop function not implemented yet.")

    def clear_image(self):
        """
        Clear images and reset state.
        """
        self.controller.image_path = None

        # Notice log message that clear_image is worth
        self.controller.right_panel.log_message("Images cleared.")
