import tkinter as tk
from tkinter import ttk
import cv2
from threading import Thread
from PIL import Image, ImageTk


class WebcamApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1300x750")
        self.root.title("Astro Collimator")

        row_index = 0

        # Dropdown for webcam selection
        self.camera_label = tk.Label( self.root, text="Select Camera:")
        self.camera_label.grid(row=row_index, column=0, padx=5)
        row_index += 1

        self.camera_list = self.get_connected_cameras()
        self.selected_camera = tk.StringVar(value=self.camera_list[0])
        self.camera_dropdown = ttk.Combobox( self.root, textvariable=self.selected_camera, values=self.camera_list,
                                            state="readonly")
        self.camera_dropdown.grid(row=row_index, column=0, padx=5)
        self.camera_dropdown.bind("<<ComboboxSelected>>", self.on_camera_selected)
        row_index += 1

        # Camera loading lable
        self.loading_label = tk.Label(self.root, text="")
        self.loading_label.grid(row=row_index, column=0, padx=5)
        row_index += 1

        # Gain slider
        self.gain_slider = tk.Scale(
            self.root,
            from_=0,
            to=100,
            length=200,
            orient=tk.HORIZONTAL,
            command=lambda value: self.set_camera_value(cv2.CAP_PROP_GAIN, int(value)),
            label="Gain"
        )
        self.gain_slider.grid(row=row_index, column=0, padx=5)
        row_index += 1

        # Exposure slider
        self.exposure_slider = tk.Scale(
            self.root,
            from_=-13,
            to=0,
            length=200,
            orient=tk.HORIZONTAL,
            command=lambda value: self.set_camera_value(cv2.CAP_PROP_EXPOSURE, int(value)),
            label="Exposure"
        )
        self.exposure_slider.grid(row=row_index, column=0, padx=5)
        row_index += 1

        # Zoom slider
        self.zoom_slider = tk.Scale(
            self.root,
            from_=1,
            to=100,
            resolution=1,
            length=200,
            orient=tk.HORIZONTAL,
            command=lambda value: self.set_camera_value(cv2.CAP_PROP_ZOOM, int(value)),
            label="Zoom"
        )
        self.zoom_slider.grid(row=row_index, column=0, padx=5)
        row_index += 1

        # mouse wheel zoom
        self.zoom_factor = 1.0  # Initialize zoom factor
        self.root.bind("<MouseWheel>", self.zoom_with_scroll)

        # Focus slider
        self.focus_slider = tk.Scale(
            self.root,
            from_=0,
            to=100,
            length=200,
            orient=tk.HORIZONTAL,
            command=lambda value: self.set_camera_value(cv2.CAP_PROP_FOCUS, int(value)),
            label="Focus"
        )
        self.focus_slider.grid(row=row_index, column=0, padx=5)
        row_index += 1

        # Add a spacer
        self.spacer_label = tk.Label(self.root, text="", height=1)
        self.spacer_label.grid(row=row_index, column=0)
        row_index += 1

        # Add crosshair toggle button
        self.crosshair_button = tk.Button(
            self.root, text="Toggle Crosshair", command=self.toggle_crosshair
        )
        self.crosshair_button.grid(row=row_index, column=0, padx=5)
        row_index += 1

        # Circle 1 slider
        self.circle1_frame = tk.Frame(self.root)
        self.circle1_frame.grid(row=row_index, column=0, padx=5, pady=5)

        self.circle1_minus = tk.Button(self.circle1_frame, text="-",
                                       command=lambda: self.circle1_slider.set(self.circle1_slider.get() - 1))
        self.circle1_minus.grid(row=0, column=0, padx=5, sticky="s")

        self.circle1_slider = tk.Scale(self.circle1_frame, from_=10, to=400, orient=tk.HORIZONTAL,
                                       label="Circle 1 Radius")
        self.circle1_slider.grid(row=0, column=1, padx=5)

        self.circle1_plus = tk.Button(self.circle1_frame, text="+",
                                      command=lambda: self.circle1_slider.set(self.circle1_slider.get() + 1))
        self.circle1_plus.grid(row=0, column=2, padx=5, sticky="s")

        self.circle1_slider.set(100)
        row_index += 1

        # Circle 2 slider
        self.circle2_frame = tk.Frame(self.root)
        self.circle2_frame.grid(row=row_index, column=0, padx=5, pady=5)

        self.circle2_minus = tk.Button(self.circle2_frame, text="-",
                                       command=lambda: self.circle2_slider.set(self.circle2_slider.get() - 1))
        self.circle2_minus.grid(row=0, column=0, padx=5, sticky="s")

        self.circle2_slider = tk.Scale(self.circle2_frame, from_=10, to=400, orient=tk.HORIZONTAL,
                                       label="Circle 2 Radius")
        self.circle2_slider.grid(row=0, column=1, padx=5)

        self.circle2_plus = tk.Button(self.circle2_frame, text="+",
                                      command=lambda: self.circle2_slider.set(self.circle2_slider.get() + 1))
        self.circle2_plus.grid(row=0, column=2, padx=5, sticky="s")

        self.circle2_slider.set(150)
        row_index += 1

        # Circle 3 slider
        self.circle3_frame = tk.Frame(self.root)
        self.circle3_frame.grid(row=row_index, column=0, padx=5, pady=5)

        self.circle3_minus = tk.Button(self.circle3_frame, text="-",
                                       command=lambda: self.circle3_slider.set(self.circle3_slider.get() - 1))
        self.circle3_minus.grid(row=0, column=0, padx=5, sticky="s")

        self.circle3_slider = tk.Scale(self.circle3_frame, from_=10, to=400, orient=tk.HORIZONTAL,
                                       label="Circle 3 Radius")
        self.circle3_slider.grid(row=0, column=1, padx=5)

        self.circle3_plus = tk.Button(self.circle3_frame, text="+",
                                      command=lambda: self.circle3_slider.set(self.circle3_slider.get() + 1))
        self.circle3_plus.grid(row=0, column=2, padx=5, sticky="s")

        self.circle3_slider.set(200)
        row_index += 1

        # Add a spacer
        self.spacer_label = tk.Label(self.root, text="", height=1)
        self.spacer_label.grid(row=row_index, column=0)
        row_index += 1

        # D-pad frame
        self.dpad_frame = tk.Frame(self.root)
        self.dpad_frame.grid(row=row_index, column=0, padx=5)
        row_index += 1

        # D-pad buttons
        self.up_button = tk.Button(self.dpad_frame, text="↑", command=lambda: self.move_crosshair(0, -1), width=5, height=2)
        self.up_button.grid(row=0, column=1)

        self.left_button = tk.Button(self.dpad_frame, text="←", command=lambda: self.move_crosshair(-1, 0), width=5, height=2)
        self.left_button.grid(row=1, column=0)

        self.right_button = tk.Button(self.dpad_frame, text="→", command=lambda: self.move_crosshair(1, 0), width=5, height=2)
        self.right_button.grid(row=1, column=2)

        self.down_button = tk.Button(self.dpad_frame, text="↓", command=lambda: self.move_crosshair(0, 1), width=5, height=2)
        self.down_button.grid(row=2, column=1)

        self.reset_button = tk.Button(self.dpad_frame, text="Reset", command=self.reset_crosshair, width=5, height=2)
        self.reset_button.grid(row=1, column=1, padx=10, pady=10)

        # Keyboard bindings for D-pad
        self.root.bind("<Up>", lambda event: self.move_crosshair(0, -1))
        self.root.bind("<Down>", lambda event: self.move_crosshair(0, 1))
        self.root.bind("<Left>", lambda event: self.move_crosshair(-1, 0))
        self.root.bind("<Right>", lambda event: self.move_crosshair(1, 0))

        # Add a blank area below all controls
        self.black_area = tk.Frame(self.root)
        self.black_area.grid(row=row_index, column=0, sticky="nsew")

        # Video display area
        self.video_label = tk.Label(root)
        self.video_label.grid(row=0, column=1, rowspan=row_index+1, padx=5)

        # Ensure the video frame expands with the window
        self.root.grid_columnconfigure(1, weight=1)  # Video frame column

        # Ensure the black area takes up remaining space
        self.root.grid_rowconfigure(row_index, weight=1)

        # Initialize crosshair state
        self.show_crosshair = False

        self.camera_on = False
        self.cap = None
        self.thread = None
        self.running = False

        # Set initial video dimensions to match the window size
        scaling = 1.5
        self.video_width = int(640 * scaling)
        self.video_height = int(480 * scaling)
        self.aspect_ratio = self.video_width / self.video_height

        self.crosshair_x = self.video_width // 2  # Initialize crosshair center X
        self.crosshair_y = self.video_height // 2  # Initialize crosshair center Y

        # Start camera 0 on startup
        self.on_camera_selected(None)

    def set_camera_value(self, prop, value):
        if hasattr(self, 'cap') and self.cap and self.cap.isOpened():
            self.cap.set(prop, value)

    def zoom_with_scroll(self, event):
        # Adjust zoom factor based on scroll direction
        if event.delta > 0:  # Scroll up
            self.zoom_factor = min(self.zoom_factor + 0.1, 3.0)  # Max zoom factor is 3.0
        else:  # Scroll down
            self.zoom_factor = max(self.zoom_factor - 0.1, 1.0)  # Min zoom factor is 1.0

    def toggle_crosshair(self):
        self.show_crosshair = not self.show_crosshair

    def move_crosshair(self, dx, dy):
        self.crosshair_x = max(0, min(self.video_width, self.crosshair_x + dx))
        self.crosshair_y = max(0, min(self.video_height, self.crosshair_y + dy))

    def reset_crosshair(self):
        self.crosshair_x = self.video_width // 2
        self.crosshair_y = self.video_height // 2

    def get_connected_cameras(self):
        cameras = []
        index = 0
        while True:
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                cameras.append(f"Camera {index}")
                cap.release()
                index += 1
            else:
                cap.release()
                break
        return cameras if cameras else ["No Cameras Found"]

    def on_camera_selected(self, event):
        print(f"Selected camera: {self.selected_camera.get()}")
        # Set loading label
        self.loading_label.config(text="Loading camera...")
        self.root.update_idletasks()  # Force UI update

        # Stop the current camera if it's running
        print("Stopping current camera if any...")
        if self.camera_on:
            self.running = False
            if self.cap:
                self.cap.release()

        # Start the newly selected camera
        print("Starting new camera...")
        self.camera_on = True
        self.running = True
        self.start_camera()

        # Clear loading label
        self.loading_label.config(text="")

    def start_camera(self):
        print("Initializing camera...")
        camera_index = int(self.selected_camera.get().split()[-1])
        self.cap = cv2.VideoCapture(camera_index)

        if self.cap.isOpened():
            print("Camera opened successfully.")

            # Read and set initial gain and zoom levels
            gain = self.cap.get(cv2.CAP_PROP_GAIN)
            self.gain_slider.set(gain)

            exposure = self.cap.get(cv2.CAP_PROP_EXPOSURE)
            self.exposure_slider.set(exposure)

            zoom = self.cap.get(cv2.CAP_PROP_ZOOM)
            self.zoom_slider.set(zoom)

            focus = self.cap.get(cv2.CAP_PROP_FOCUS)
            self.focus_slider.set(focus)

            print(f"Initial Gain: {gain}, Initial Zoom: {zoom}")

            self.thread = Thread(target=self.update_frame, daemon=True)
            self.thread.start()
        else:
            print("Failed to open the camera.")
            self.cap.release()

    def update_frame(self):
        print("Starting frame update loop...")
        while self.running:

            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Apply digital zoom
                height, width, _ = frame.shape
                new_width, new_height = int(width / self.zoom_factor), int(height / self.zoom_factor)
                x1, y1 = (width - new_width) // 2, (height - new_height) // 2
                cropped_frame = frame[y1:y1 + new_height, x1:x1 + new_width]

                frame = cv2.resize(cropped_frame, (self.video_width, self.video_height))

                if self.show_crosshair:
                    cv2.line(frame, (self.crosshair_x, 0), (self.crosshair_x, self.video_height), (255, 0, 0), 1)
                    cv2.line(frame, (0, self.crosshair_y), (self.video_width, self.crosshair_y), (255, 0, 0), 1)

                    # Draw concentric circles
                    radius1 = self.circle1_slider.get()
                    radius2 = self.circle2_slider.get()
                    radius3 = self.circle3_slider.get()
                    cv2.circle(frame, (self.crosshair_x, self.crosshair_y), radius1, (255, 0, 0), 1)
                    cv2.circle(frame, (self.crosshair_x, self.crosshair_y), radius2, (255, 0, 0), 1)
                    cv2.circle(frame, (self.crosshair_x, self.crosshair_y), radius3, (255, 0, 0), 1)

                img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.video_label.config(image=img)
                self.video_label.image = img
            else:
                break

    def on_closing(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()