import cv2                          # use for computer vision
from ultralytics import YOLO        # use for classication and segmentation
import os                           # use for modification folder
import shutil                       # use for moving file operations
import numpy as np                  # use for array

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

def run_realtime_detection():
    # --- Load YOLO Detection Model ---
    print("\nLoading Detection Model...")
    # Select the version and type yolo model
    model = load_or_download_yolo_model('yolo12n.pt') 

    # --- Initialize Webcam ---
    # initial image from file for test purpose
    var_image = cv2.imread(r'Yolo_Test\Sample_Image\Sample_Car.jpg')

    # Check if image is loaded successfully
    if var_image is None:
        print("ERROR: Failed to load image. Please check the file path.")
        return

    # Set iamge resolution (optional)
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

#--- Main Execution ---
if __name__ == "__main__":
    run_realtime_detection() # call the function to run real-time detection