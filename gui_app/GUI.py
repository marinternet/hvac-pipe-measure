import tkinter as tk                        # Import tkinter for GUI
from tkinter import ttk                     # Import ttk for styling
from tkinter import filedialog, messagebox  # Import file dialog and message box
import os                                   # Import os for file path handling
import datetime                             # Import datetime for timestamp
from PIL import Image, ImageTk              # Import PIL for image processing

class HVAC_Measure_App:
    """
    Main application class for the HVAC Pipe Measurement GUI.
    This class handles the UI layout, styling, and placeholder interactions.
    """

    # initialize variables
    image_path = None

    def __init__(self, root):
        """
        Initialize the application.

        Args:
            root (tk.Tk): The root window of the application.
        """
        self.root = root
        self.root.title("HVAC Pipe Measurement System")
        self.root.geometry("1400x900") # Increased size
        self.root.minsize(1200, 800)

        # Add icon to the window
        base_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_path, 'assets', 'logo.ico')
        try:
            self.root.iconbitmap(icon_path)
        except Exception:
            pass # Icon might not exist yet

        # Configure styling
        self._configure_styles()

        # Create main layout frames
        self._create_layout()

        # Initialize UI components
        self._create_control_panel()
        self._create_display_area()
        self._create_result_area()
        self._create_log_panel()

    def _configure_styles(self):
        """
        Configure custom styles for a modern look using ttk.
        """
        style = ttk.Style()
        style.theme_use('clam')

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
        style.configure('Main.TFrame', background=self.colors['bg_main'])
        style.configure('Sidebar.TFrame', background=self.colors['bg_sidebar'])
        style.configure('Panel.TFrame', background=self.colors['bg_panel'], relief='flat')
        
        # Label Styles
        style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), background=self.colors['bg_sidebar'], foreground=self.colors['text_sidebar'])
        style.configure('SubHeader.TLabel', font=('Segoe UI', 12, 'bold'), background=self.colors['bg_panel'], foreground=self.colors['text'])
        style.configure('Normal.TLabel', font=('Segoe UI', 10), background=self.colors['bg_panel'], foreground=self.colors['text'])
        style.configure('SidebarText.TLabel', font=('Segoe UI', 10), background=self.colors['bg_sidebar'], foreground=self.colors['text_sidebar'])
        style.configure('Placeholder.TLabel', font=('Segoe UI', 10, 'italic'), background='#ecf0f1', foreground=self.colors['text_light'], anchor='center')

        # Button Styles
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'), background=self.colors['primary'], foreground='white', borderwidth=0, focuscolor='none')
        style.map('Primary.TButton', background=[('active', self.colors['primary_hover'])])

        style.configure('Danger.TButton', font=('Segoe UI', 10, 'bold'), background=self.colors['danger'], foreground='white', borderwidth=0, focuscolor='none')
        style.map('Danger.TButton', background=[('active', self.colors['danger_hover'])])

    def _create_layout(self):
        """
        Create the main grid layout structure.
        """
        # Main container
        self.main_container = ttk.Frame(self.root, style='Main.TFrame')
        self.main_container.pack(fill='both', expand=True)

        # 1. Left Sidebar (Control Panel)
        self.control_frame = ttk.Frame(self.main_container, style='Sidebar.TFrame', padding="20", width=200) # Reduced width
        self.control_frame.pack(side='left', fill='y')
        self.control_frame.pack_propagate(False)

        # 2. Right Log Panel
        self.log_frame = ttk.Frame(self.main_container, style='Panel.TFrame', padding="20", width=250) # Reduced width
        self.log_frame.pack(side='right', fill='y', padx=(10, 0))
        self.log_frame.pack_propagate(False)

        # 3. Center Content Area (Display + Results)
        self.content_frame = ttk.Frame(self.main_container, style='Main.TFrame', padding="20")
        self.content_frame.pack(side='left', fill='both', expand=True)

    def _create_control_panel(self):
        """
        Create buttons and controls in the left sidebar.
        """
        # App Title in Sidebar
        title_label = ttk.Label(self.control_frame, text="HVAC Pipe\nMeasure", style='Header.TLabel', justify='center')
        title_label.pack(pady=(20, 50))

        # Buttons with Emojis
        self._create_button("📤 Upload Image", self.upload_image, 'Primary.TButton')
        self._create_button("▶ Start Predict", None, 'Primary.TButton')
        self._create_button("⏹ Stop Predict", None, 'Danger.TButton')
        self._create_button("🗑 Clear Image", None, 'Danger.TButton')

        # Separator
        separator = tk.Frame(self.control_frame, bg=self.colors['text_light'], height=1)
        separator.pack(fill='x', pady=30)

        # Status Label
        self.status_label = ttk.Label(self.control_frame, text="System Ready", style='SidebarText.TLabel')
        self.status_label.pack(side='bottom', pady=20)

    def _create_button(self, text, command, style):
        """
        Helper to create a button
        """
        if command:
             btn = ttk.Button(self.control_frame, text=text, style=style, command=command, cursor='hand2')
        else:
             btn = ttk.Button(self.control_frame, text=text, style=style, cursor='hand2')
        
        btn.pack(fill='x', pady=10, ipady=5)
        return btn

    def _create_display_area(self):
        """
        Create the area for displaying images and showing real image path (Input Overview + Pipeline Results).
        """
        # --- Input Overview Section ---
        self.overview_container = ttk.Frame(self.content_frame, style='Panel.TFrame', padding="20")
        self.overview_container.pack(fill='x', pady=(0, 20))

        ttk.Label(self.overview_container, text="Input Overview Image", style='SubHeader.TLabel').pack(anchor='center', pady=(0, 10))
        
        # Placeholder for Input Image - Fixed size to prevent squashing
        # Using a Frame to enforce size, and Label inside it
        self.input_frame = ttk.Frame(self.overview_container, width=300, height=200) # Fixed dimensions
        self.input_frame.pack(anchor='center')
        self.input_frame.pack_propagate(False) # Don't shrink

        self.input_placeholder = ttk.Label(self.input_frame, text="No Input Image Selected", style='Placeholder.TLabel', relief='solid', borderwidth=0)
        self.input_placeholder.pack(fill='both', expand=True) 
        
        # Check if image_path is set and display it
        if self.image_path and os.path.exists(self.image_path):
             self.display_image(self.image_path, self.input_placeholder, 300, 200)


        # --- Pipeline Results Section ---
        self.image_container = ttk.Frame(self.content_frame, style='Panel.TFrame', padding="20")
        self.image_container.pack(fill='both', expand=True, pady=(0, 20))

        ttk.Label(self.image_container, text="Prediction Pipeline", style='SubHeader.TLabel').pack(anchor='w', pady=(0, 20))

        # Grid for 3 images
        self.images_grid = ttk.Frame(self.image_container, style='Panel.TFrame')
        self.images_grid.pack(fill='both', expand=True)

        self.images_grid.columnconfigure(0, weight=1)
        self.images_grid.columnconfigure(1, weight=1)
        self.images_grid.columnconfigure(2, weight=1)
        self.images_grid.rowconfigure(0, weight=1)

        # 1. YOLO Classification
        self.frame_cls = self._create_image_placeholder(self.images_grid, "YOLO Classification", 0)
        
        # 2. YOLO Segmentation
        self.frame_seg = self._create_image_placeholder(self.images_grid, "YOLO Segmentation", 1)
        
        # 3. Color Segmentation
        self.frame_col = self._create_image_placeholder(self.images_grid, "Color Segmentation", 2)

    def _create_image_placeholder(self, parent, title, col_idx):
        """
        Helper to create a unified image placeholder frame.
        """
        frame = ttk.Frame(parent, style='Panel.TFrame')
        frame.grid(row=0, column=col_idx, sticky='nsew', padx=10)

        # Title
        ttk.Label(frame, text=title, style='Normal.TLabel', font=('Segoe UI', 10, 'bold')).pack(pady=(0, 10))

        # Placeholder Box - Fixed Size Frame
        # Using a Frame to enforce size, and Label inside it
        placeholder_frame = ttk.Frame(frame, width=250, height=200) # Reduced fixed dimensions for pipeline images
        placeholder_frame.pack(anchor='center')
        placeholder_frame.pack_propagate(False) # Don't shrink/expand

        placeholder = ttk.Label(placeholder_frame, text="No Image", style='Placeholder.TLabel', relief='solid', borderwidth=0)
        placeholder.pack(fill='both', expand=True)
        
        return placeholder

    def _create_result_area(self):
        """
        Create the text result area at the bottom.
        """
        self.result_frame = ttk.Frame(self.content_frame, style='Panel.TFrame', padding="20")
        self.result_frame.pack(fill='x', ipady=10)

        ttk.Label(self.result_frame, text="Prediction Results", style='SubHeader.TLabel').pack(anchor='w', pady=(0, 10))

        # Text widget for results
        self.result_text = tk.Text(self.result_frame, height=5, font=('Consolas', 10), state='disabled', relief='flat', bg='#f4f7f6', padx=10, pady=10)
        self.result_text.pack(fill='x')

        # Show text result
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Prediction Results\nDiameter estimated: 12")
        self.result_text.config(state='disabled')

    def _create_log_panel(self):
        """
        Create the Log History panel on the right side.
        """
        ttk.Label(self.log_frame, text="Log Activity", style='SubHeader.TLabel').pack(anchor='w', pady=(0, 20))
        
        # Log Text Area
        self.log_text = tk.Text(self.log_frame, font=('Consolas', 9), state='disabled', relief='flat', bg='#f8f9fa', height=20)
        self.log_text.pack(fill='both', expand=True, pady=(0, 10))
        
        # Clear Log Button
        ttk.Button(self.log_frame, text="🗑 Clear Log", style='Danger.TButton', command=self.clear_log, cursor='hand2').pack(fill='x')
        
        self.log_message("Application started.")

    def log_message(self, message):
        """
        Append a message to the log panel with a timestamp.
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{timestamp}] {message}\n"
        
        try:
            self.log_text.config(state='normal')
            self.log_text.insert(tk.END, full_msg)
            self.log_text.see(tk.END)
            self.log_text.config(state='disabled')
        except AttributeError:
            pass

    def clear_log(self):
        """
        Clear the log history.
        """
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        self.log_message("Log cleared.")

    # --- Helper Functionalities ---
    
    def display_image(self, image_path, label_widget, width, height):
        """
        Load, resize, and display an image on a given Label widget.
        Resizes to fill the dimensions exactly (stretch).
        
        Args:
            image_path (str): Path to the image file.
            label_widget (ttk.Label): The label widget to display the image on.
            width (int): Target width.
            height (int): Target height.
        """
        try:
            # Open the image
            img = Image.open(image_path)
            
            # Resize to exact dimensions (stretch) to ensure it fills the frame and doesn't shift layout
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Update Label
            label_widget.config(image=photo, text="") # Remove text, show image
            label_widget.image = photo # Keep reference to prevent garbage collection
            
            print(f"Displayed image: {image_path} on {label_widget}")
        except Exception as e:
            print(f"Error displaying image: {e}")
            label_widget.config(text="Error Loading Image", image="")

    def upload_image(self):
        """
        Handle image upload action.
        """
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            filename = os.path.basename(file_path)
            self.image_path = file_path # Update current path
            self.log_message(f"Image uploaded: {filename}")
            
            # Display the image in the Input Overview
            self.display_image(self.image_path, self.input_placeholder, 300, 200)
            
            # Display the image in ALL Pipeline placeholders (Fixed 250x200)
            target_size = (250, 200) 
            
            self.display_image(self.image_path, self.frame_cls, *target_size)
            self.display_image(self.image_path, self.frame_seg, *target_size)
            self.display_image(self.image_path, self.frame_col, *target_size)
            
        else:
            self.log_message("Image upload cancelled.")


if __name__ == "__main__":
    root = tk.Tk()
    app = HVAC_Measure_App(root)
    root.mainloop()
