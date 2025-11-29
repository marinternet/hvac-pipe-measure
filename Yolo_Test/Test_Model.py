from email.mime import base
import tkinter as tk                            # use for dialog box
from tkinter.filedialog import askopenfilename  # use for open file dialog box
import cv2                                      # use for computer vision
from ultralytics import YOLO                    # use for classication and segmentation
import os                                       # use for modification folder
import shutil                                   # use for moving file operations
import numpy as np                              # use for array


# function to load or download the YOLO model
def load_or_download_yolo_model(model_name):
    """
    Load YOLO model from local directory if available.
    If not, download it, move it to the specified directory, and then load it.
    """
    # 1. Specify the directory where the model will be saved
    model_dir = r'Yolo Model'
    local_path = os.path.join(model_dir, model_name)

    # 2. Check if the model file already exists in the target folder
    if os.path.exists(local_path):
        print(f"Loading {model_name} model from {local_path}...")
        model = YOLO(local_path)
        print(f"{model_name} model successfully loaded from {local_path}")
    else:
        print(f"File {model_name} not found in directory {model_dir}. Downloading...")
        
        try:
            # Initialize YOLO to trigger the auto-download.
            # By default, this downloads the file to the current working directory (root).
            temp_model = YOLO(model_name)
            
            # Create the target directory if it does not exist
            os.makedirs(model_dir, exist_ok=True)
            
            # 3. Move the downloaded file from root to the target directory
            # The file is currently in the root folder with the name 'model_name'
            if os.path.exists(model_name):
                shutil.move(model_name, local_path)
                print(f"Model successfully moved to {local_path}.")
            
            # 4. Reload the model from the correct local path to ensure consistency
            model = YOLO(local_path)
            print(f"Model {model_name} successfully loaded.")
            
        except Exception as e:
            print(f"ERROR: Failed to download or organize model {model_name}. Please ensure a stable internet connection.")
            raise e
    
    return model

# support function to decide download model
def decide_download_model(user_choice):
    """
    Decide whether to download a YOLO model based on user input.
    """
    while True:
        if user_choice == 'y':
            model_name = input("Enter the YOLO model name to download (e.g., yolo12n.pt): ").strip()
            model = load_or_download_yolo_model(model_name)
            return model
        elif user_choice == 'n':
            print("No model will be downloaded.")
            return None
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

# function to find path image with dialog box
def find_path_image():

    # Hide the root window
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)  # Bring the dialog to the front
    
    # Open file dialog to select an image file
    path_image = askopenfilename(title="Select an Image File", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])

    #check if user cancel the dialog box
    if not path_image:
        print("No file selected. use default image instead.\n")
        root.destroy()  # Close the root window

        # use absolute path for default image (resolve path issue when running another command line)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path_image = os.path.join(base_dir, r'Sample_Image\Sample_Car.jpg')

        return path_image  # return default image path
    
    root.destroy()  # Close the root window
    
    return path_image

def run_realtime_detection():
    # --- Load YOLO Detection Model ---
    print("\nLoading Detection Model...")

    #list the model in Yolo Model folder
    model_dir = r'Yolo Model'
    if os.path.exists(model_dir):
        print("Available models in 'Yolo Model' directory:")
        for file in os.listdir(model_dir):
            if file.endswith('.pt'):
                print(f"- {file}")
        print()

        while True:
            
            # ask user to select the model from the list
            model_name = input("Enter the YOLO model name to use (e.g., yolo12n.pt): ").strip() 
            model_path = os.path.join(model_dir, model_name)

            if os.path.exists(model_path):
                model = YOLO(model_path)
                print(f"{model_name} model successfully loaded from {model_path}")
                break
            
            else:
                print(f"Model {model_name} not found in 'Yolo Model' directory. Please try again.\n")
                continue

    else:
        print("No models found in 'Yolo Model' directory. Please download a model first.")
        return

    print()

    # initial image from file for test purpose
    # logic code to get image from user or use default image
    choice_image = input("do you want to select an image file? (y/n): ").strip().lower()

    if choice_image == 'n': # use default image
        print("Using default image 'Sample_Car.jpg' for detection.")

        # use absolute path for default image (resolve path issue when running another command line)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path__image = os.path.join(base_dir, r'Sample_Image\Sample_Car.jpg')

        var_image = cv2.imread(path__image)

    else: # open dialog box to select image
        print("Please select an image file for detection.")
        var_image = cv2.imread(find_path_image())

    # Check if image is loaded successfully
    if var_image is None:
        print("ERROR: Failed to load image. Please check the file path.")
        return

    # Set image resolution (optional)
    var_image = cv2.resize(var_image, (800, 600))

    # --- Run Inference on the Image ---
    print("Running YOLO Inference on the Image...")
    results = model(var_image, stream=True, verbose=False)

    # --- Process and Display Results ---
    for r in results:
        annotated_image = r.plot() # plot() returns the image as a numpy array with bounding boxes drawn
        cv2.imshow("YOLO Detection", annotated_image)

        # Exit condition: Press any key to close the window
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

    # --- Cleanup ---
    cv2.destroyAllWindows()
    print("Program ended.")

def menu_test_model():

    """
    Display a menu for testing the YOLO model.
    list the menu for user to select the option
    1. checking the model or download the model
    2. run the real-time detection
    3. exit the program
    """

    while True:

        print("\n--- YOLO Model Test Menu ---")
        print("1. check the model or download the model")
        print("2. run the real-time detection")
        print("3. exit the program")

        choice_user = input("Please select an option (1-3): ")
        if choice_user == '1':
            # check the model on Yolo Model folder and show the list of model
            print("\n Checking the model...\n")
            model_dir = r'Yolo Model'
            if os.path.exists(model_dir) and os.listdir(model_dir) != []:
                print("Available models in 'Yolo Model' directory:")
                for file in os.listdir(model_dir):
                    if file.endswith('.pt'):
                        print(f"- {file}")
                print()

                # ask user to download another model or go back to menu
                check_model = decide_download_model(input("Do you want to download another model? (y/n): ").strip().lower())
                if check_model is None:
                    # ask user back to menu
                    choice_user = input("press 'b' to go back to menu or any other key to exit: ").strip().lower()
                    if choice_user == 'b':
                        continue  # go back to the menu
                    else:
                        print("\nExiting the program")
                        exit()

            else:
                
                # no model found in the folder, ask user to download the model
                check_model = decide_download_model(input("No models found. Do you want to download a model? (y/n): ").strip().lower())
                if check_model is not None:
                    # ask user back to menu
                    choice_user = input("press 'b' to go back to menu or any other key to exit: ").strip().lower()
                    if choice_user == 'b':
                        continue  # go back to the menu
                    else:
                        print("\nExiting the program")
                        exit()


        elif choice_user == '2':
            # Run real-time detection
            run_realtime_detection()

        elif choice_user == '3':
            # Exit the program
            print("\nExiting the program. Goodbye!")
            exit()

        else:
            print("Invalid choice. Please select a valid option (1-3).")

#--- Main Execution ---
if __name__ == "__main__":
    menu_test_model() # start the menu for testing the model