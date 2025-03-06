import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Initialize OpenCV tracker
tracker = cv2.legacy.TrackerCSRT_create()  # or cv2.legacy.TrackerKCF_create()
tracking = False
bounding_box = None

# Function to start video capture
def start_video():
    global cap, tracking
    if not cap.isOpened():
        messagebox.showerror("Error", "Unable to open video source.")
        return
    tracking = False
    update_frame()

# Function to select object for tracking
def select_object():
    global bounding_box, tracking
    ret, frame = cap.read()
    if not ret:
        messagebox.showerror("Error", "Unable to read video frame.")
        return
    bounding_box = cv2.selectROI("Select Object", frame, fromCenter=False)
    cv2.destroyWindow("Select Object")
    tracker.init(frame, bounding_box)
    tracking = True

# Function to update video frames
def update_frame():
    global tracking
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            if tracking:
                success, bounding_box = tracker.update(frame)
                if success:
                    x, y, w, h = map(int, bounding_box)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "Tracking Failure", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            # Convert frame to RGB and display in Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
            video_label.after(10, update_frame)  # Update every 10ms
        else:
            messagebox.showinfo("Info", "Video ended.")
            cap.release()

# Function to exit the application
def exit_app():
    cap.release()
    root.destroy()

# Initialize Tkinter
root = tk.Tk()
root.title("Real-Time Object Tracking System")

# Video capture
cap = cv2.VideoCapture(0)  # Use 0 for webcam or provide video file path

# Create UI elements
video_label = tk.Label(root)
video_label.pack()

start_button = tk.Button(root, text="Start Video", command=start_video)
start_button.pack(side=tk.LEFT, padx=10, pady=10)

select_button = tk.Button(root, text="Select Object", command=select_object)
select_button.pack(side=tk.LEFT, padx=10, pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Run the Tkinter main loop
root.mainloop()