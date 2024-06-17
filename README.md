# Privacy Management and its Implementation in Real-time videos

The Privacy Management project aims to keep confidential information private in real-time videos. We have implemented privacy mechanisms using color-based inpainting, object-detection-based inpainting, and segmentation-based inpainting. The project is divided into seven tasks, which build upon each other to achieve the final goal.
Let's see how you can implement it in your machine.

## Installation

Before running the script, ensure you have all the required libraries installed. You can do this by installing the dependencies listed in the `requirements.txt` file.

### Steps:

1. Clone the repository:

    ```sh
    git clone https://github.com/Sejalparate/privacy-management-dp.git
    ```

2. Navigate to the project directory:

    ```sh
    cd privacy-management-dp/
    ```

3. Install the required libraries:

    ```sh
    pip install -r requirements.txt
    ```

This will install all the dependencies specified in the `requirements.txt` file.



## Task 1 - Masked Video

This task demonstrates color detection using OpenCV. The script captures video from the webcam, converts it to HSV color space, and detects objects of a specific color (green) within the video feed. Detected objects are highlighted with a bounding box. The masked video highlights portions of the video feed that match a specified color range.

Run the script with the following command:
```sh
    python Task 1 - Masked Video/Masked_video.py
```
![Example Output](https://github.com/Sejalparate/privacy-management-dp/blob/main/Task%201%20-%20Masked%20Video/Masked_Video.jpg)



## Task 2 - Color-based Inpainting

This task demonstrates color-based inpainting using OpenCV. The script captures video from the webcam, detects a specific color in the video feed, and replaces the detected color area with the background from earlier frames, creating an inpainting effect. The output video is saved to a file.

Run the script with the following command:
```sh
    python Task 2 - Color based inpainting/Color_based_inpainting.py
```
![Example Output](https://github.com/Sejalparate/privacy-management-dp/blob/main/Task%202%20-%20Color%20based%20inpainting/Color-based-inpainting.jpg)



## Video Inpainting using Object Detection

This task builds on the previous one by incorporating object detection to enhance privacy management. The script captures the background for the first 45 seconds, after which it detects specific objects (in this case, persons) in the video feed. Detected objects are highlighted with bounding boxes and replaced with the corresponding background, effectively hiding them.

Run the script with the following command:
```sh
    python Task 7 - User Authentication/main.py
```




