import cv2
import numpy as np
import time
import tkinter as tk
from tkinter import Button, messagebox
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime

class CameraApp:
    def __init__(self, root, database_name):
        self.root = root
        self.root.title("Privacy Enhancement")
        self.root.geometry("1200x800")
        self.database_name = database_name
        self.capture = cv2.VideoCapture(0)
        self.current_frame = None
        self.background = None
        self.privacy_mode = False

        self.config_file = r'Task 3 - Video Inpainting Object Detection\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        self.frozen_model = r'Task 3 - Video Inpainting Object Detection\frozen_inference_graph.pb'
        self.labels_file = r'Task 3 - Video Inpainting Object Detection\labels.txt'
        self.class_labels = self.load_labels()
        self.model = self.load_model()

        self.create_widgets()
        self.update_camera()

    def load_labels(self):
        with open(self.labels_file, 'rt') as fpt:
            class_labels = fpt.read().rstrip('\n').split('\n')
        return class_labels

    def load_model(self):
        model = cv2.dnn_DetectionModel(self.frozen_model, self.config_file)
        model.setInputSize(320, 320)
        model.setInputScale(1.0/127.5)
        model.setInputMean((127.5, 127.5, 127.5))
        model.setInputSwapRB(True)
        return model

    def create_widgets(self):
        # Set background image
        try:
            bg_image = Image.open(r'Task 6 - GUI and database integration\AI.jpg')
            bg_image = bg_image.resize((1200, 800), Image.LANCZOS)
            bg_photo = ImageTk.PhotoImage(bg_image)

            bg_label = tk.Label(self.root, image=bg_photo)
            bg_label.place(relwidth=1, relheight=1)
            bg_label.image = bg_photo
        except Exception as e:
            print(f"Error loading background image: {e}")

        # Create main frame to hold image frames
        main_frame = tk.Frame(self.root, bg="#f7f5f2")
        main_frame.place(relx=0.5, rely=0.4, anchor="center")

        # Create and place "before" frame
        self.before_frame = tk.Frame(main_frame, width=500, height=500, borderwidth=2, relief="solid", bg="#ffffff")
        self.before_frame.grid(row=0, column=0, padx=20, pady=10)
        self.before_canvas = tk.Canvas(self.before_frame, width=500, height=500)
        self.before_canvas.pack()
        before_label = tk.Label(main_frame, text="Before privacy enhancement", font=("Helvetica", 14), bg="#f7f5f2", fg="#a83232")
        before_label.grid(row=1, column=0, pady=10)

        # Create and place "after" frame
        self.after_frame = tk.Frame(main_frame, width=500, height=500, borderwidth=2, relief="solid", bg="#ffffff")
        self.after_frame.grid(row=0, column=1, padx=20, pady=10)
        self.after_canvas = tk.Canvas(self.after_frame, width=500, height=500)
        self.after_canvas.pack()
        after_label = tk.Label(main_frame, text="After privacy enhancement", font=("Helvetica", 14), bg="#f7f5f2", fg="#a83232")
        after_label.grid(row=1, column=1, pady=10)

        # Create and place buttons
        button_frame = tk.Frame(self.root, bg="#f7f5f2")
        button_frame.place(relx=0.5, rely=0.9, anchor="center")

        self.btn_apply = Button(button_frame, text="APPLY PRIVACY ENHANCEMENT", font=("Helvetica", 14), borderwidth=2, relief="solid", command=self.start_background_capture, bg="#a83232", fg="#ffffff")
        self.btn_apply.grid(row=0, column=0, padx=10, pady=10)

        self.btn_store = Button(button_frame, text="STORE TO DATABASE", font=("Helvetica", 14), borderwidth=2, relief="solid", command=self.store_image, bg="#a83232", fg="#ffffff")
        self.btn_store.grid(row=0, column=1, padx=10, pady=10)

        self.btn_exit = Button(button_frame, text="EXIT", font=("Helvetica", 14), borderwidth=2, relief="solid", command=self.exit_app, bg="#a83232", fg="#ffffff")
        self.btn_exit.grid(row=0, column=2, padx=10, pady=10)

    def update_camera(self):
        ret, frame = self.capture.read()
        if ret:
            self.current_frame = frame
            frame_flipped = np.flip(frame, axis=1)
            frame_rgb = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB)
            
            # Update "Before Privacy Enhancement" window
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.before_canvas.create_image(0, 0, anchor='nw', image=imgtk)
            self.before_canvas.image = imgtk

            if self.privacy_mode and self.background is not None:
                # Apply privacy enhancement
                enhanced_frame = self.apply_privacy_enhancement(frame_flipped)

                # Update "After Privacy Enhancement" window
                frame_rgb_enhanced = cv2.cvtColor(enhanced_frame, cv2.COLOR_BGR2RGB)
                img_enhanced = Image.fromarray(frame_rgb_enhanced)
                imgtk_enhanced = ImageTk.PhotoImage(image=img_enhanced)
                self.after_canvas.create_image(0, 0, anchor='nw', image=imgtk_enhanced)
                self.after_canvas.image = imgtk_enhanced
            else:
                # Update "After Privacy Enhancement" window with the original frame
                img_enhanced = Image.fromarray(frame_rgb)
                imgtk_enhanced = ImageTk.PhotoImage(image=img_enhanced)
                self.after_canvas.create_image(0, 0, anchor='nw', image=imgtk_enhanced)
                self.after_canvas.image = imgtk_enhanced

        self.root.after(10, self.update_camera)

    def start_background_capture(self):
        self.btn_apply.config(state=tk.DISABLED)
        self.root.update_idletasks()
        start_time = time.time()
        self.background = None
        while time.time() - start_time < 45:
            ret, background = self.capture.read()
            if ret:
                self.background = np.flip(background, axis=1)
        self.privacy_mode = True
        self.btn_apply.config(state=tk.NORMAL)
        messagebox.showinfo("Background Captured", "Background captured successfully. Privacy enhancement is now active.")

    def apply_privacy_enhancement(self, frame):
        if frame is not None:
            # Detect objects
            ClassIndex, confidence, bbox = self.model.detect(frame, confThreshold=0.55)
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)

            if len(ClassIndex) != 0:
                for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
                    if (ClassInd <= 80) and self.class_labels[ClassInd - 1] == 'person':
                        # Create a binary mask for the detected person
                        cv2.rectangle(mask, (boxes[0], boxes[1]), (boxes[0] + boxes[2], boxes[1] + boxes[3]), (255), thickness=cv2.FILLED)

            # Inpaint the detected person using the background
            inpainted_frame = frame.copy()
            inpainted_frame[mask == 255] = self.background[mask == 255]
            return inpainted_frame
        return frame

    def store_image(self):
        if self.current_frame is not None:
            image_name = f"image_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            cv2.imwrite(image_name, self.current_frame)
            self.save_to_database(image_name)
            messagebox.showinfo("Success", f"Image '{image_name}' stored in the database!")

    def save_to_database(self, image_name):
        try:
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, name TEXT)")
            cursor.execute("INSERT INTO images (name) VALUES (?)", (image_name,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            if conn:
                conn.close()

    def exit_app(self):
        self.capture.release()
        self.root.destroy()

if __name__ == "__main__":
    db_name = "image_database.db"
    root = tk.Tk()
    app = CameraApp(root, db_name)
    root.mainloop()