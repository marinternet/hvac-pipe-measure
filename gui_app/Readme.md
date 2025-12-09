# HVAC Pipe Measurement System - GUI Application

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/Tkinter-8.6%2B-darkblue)
![Pillow](https://img.shields.io/badge/Pillow-9.5.0%2B-red)

## 📚 Overview

The GUI serves as the front-end for the pipe measurement logic. It integrates various computer vision techniques (YOLO Classification, YOLO Segmentation, and Color Segmentation) to estimate the diameter of pipes from images. The interface is built using Python's `tkinter` library and features a modern, clean layout.

## 💡 Features

Based on the interface design, here is a breakdown of the available functions and sections:

### Control Panel (Left Sidebar)
*   **Upload Image**: Click this button to open a file dialog. It allows you to select an image file (supported formats: `.jpg`, `.jpeg`, `.png`, `.bmp`) from your computer. Once selected, the image is loaded into the application for processing.
*   **Start Predict**: Initiates the analysis pipeline on the currently loaded image. This triggers the classification and segmentation algorithms to calculate the pipe's dimensions.
*   **Stop Predict**: Stops the ongoing prediction process immediately. Useful if the process is taking too long or if you want to cancel the current operation.
*   **Clear Image**: Removes the currently displayed image from all viewports (Input Overview and Pipeline) and resets the application state for a new input.

### Display Areas
*   **Input Overview Image**: This central panel displays the original, unprocessed image that you uploaded. It serves as a reference for the analysis.
*   **Prediction Pipeline**: This section visualizes the intermediate steps of the computer vision processing:
    *   **YOLO Classification**: Shows the result of the object detection model, identifying the pipe within the image.
    *   **YOLO Segmentation**: Displays the segmentation mask, highlighting the exact shape and boundaries of the pipe.
    *   **Color Segmentation**: Shows the output of the color-based segmentation algorithm, which helps in refining the pipe's area based on color properties.

### Results & Logging
*   **Prediction Results**: A dedicated text area at the bottom that displays the final calculated output, such as the **Estimated Diameter** of the pipe.
*   **Log Activity**: The panel on the right side provides a real-time history of all actions and system events (e.g., "Application started", "Image uploaded", "Error loading image").
*   **Clear Log**: A button located at the bottom of the log panel to clear the history of messages.

## 🛠️ Prerequisites

Before running the program, ensure you have the following installed:

* **Python 3.8+**: Ensure you have Python installed.

## 📦 Installation 

1.  **Clone the repository** (if you are using Git):
    ```bash
    git clone (https://github.com/marinternet/hvac-pipe-measure.git)
    cd hvac-pipe-measure/gui_app
    ```

    Note: if you already cloned, then ignore the git clone command

2.  **Install Dependencies**:
    Use the provided `requirements.txt` file to install the necessary libraries.
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

To start the GUI program, run the Python script:

```bash
python GUI.py
```
