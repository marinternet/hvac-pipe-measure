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
    # basically 0 is ID default camera from laptop 
    # change 1 or 2 if it has external camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        return

    print("\nStarting Real-time Object Detection. Press 'q' to exit.")

    # Set camera resolution (optional, to get more efficient)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        # 1. Read frame from camera
        success, frame = cap.read()
        if not success:
            print("Failed to read frame from webcam. Exiting...")
            break

        # 2. Run YOLO inference on the frame
        # stream=True is recommended for video sources to manage memory efficiently
        results = model(frame, stream=True, verbose=False)

        # 3. Process results and display
        # YOLO results is a generator when stream=True, so we iterate once per frame
        for r in results:
            # plot() returns the image as a numpy array with bounding boxes drawn
            annotated_frame = r.plot()

            # 4. Display the frame using OpenCV
            cv2.imshow("YOLO Real-time Detection", annotated_frame)

        # 5. Exit Loop Condition
        # Press 'q' on the keyboard to quit the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # --- Cleanup ---
    cap.release()
    cv2.destroyAllWindows()
    print("Program ended.")

if __name__ == "__main__":
    run_realtime_detection()