import os
import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import subprocess

class VideoSelector:
    def __init__(self, master, folder1, folder2):
        self.master = master
        self.master.title("Video Choice Interface")

        # Check for matching filenames
        self.matching_files = self.get_matching_filenames(folder1, folder2)
        self.folder1 = folder1
        self.folder2 = folder2

        self.current_index = 0
        self.selections = ["Unchosen"] * len(self.matching_files)
        self.current_status = tk.StringVar()
        self.filename_label = None

        # Create control pane
        self.control_pane = ttk.Frame(self.master, padding="10")
        self.control_pane.pack(fill=tk.X)

        self.prev_btn = ttk.Button(self.control_pane, text="Prev Task", command=self.prev_task)
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = ttk.Button(self.control_pane, text="Next Task", command=self.next_task)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        self.view_pane_btn = ttk.Button(self.control_pane, text="View Pane", command=self.view_pane)
        self.view_pane_btn.pack(side=tk.LEFT, padx=5)

        self.finish_btn = ttk.Button(self.control_pane, text="Finish", command=self.finish)
        self.finish_btn.pack(side=tk.LEFT, padx=5)

        # Load the first video pair
        self.load_video_pair()

    def get_matching_filenames(self, folder1, folder2):
        files1 = set(os.listdir(folder1))
        files2 = set(os.listdir(folder2))

        if files1 != files2:
            raise ValueError("The two folders do not have matching filenames.")

        return sorted(list(files1))

    def get_cover_frame(self, video_path, frame_size):
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            
            # Resize the frame while maintaining aspect ratio and fill the rest with black color
            image.thumbnail(frame_size)
            new_image = Image.new("RGB", frame_size, (0, 0, 0))
            new_image.paste(image, ((frame_size[0] - image.width) // 2, (frame_size[1] - image.height) // 2))
            
            return ImageTk.PhotoImage(image=new_image)
        else:
            return None

    def play_video(self, filename, folder):
        vlc_path = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"  # 调整为您的VLC安装路径
        video_path = os.path.join(folder, filename)
        subprocess.Popen([vlc_path, video_path])


    def load_video_pair(self):
        # Clear the current video pane
        for widget in self.master.winfo_children():
            if widget != self.control_pane:
                widget.destroy()

        filename = self.matching_files[self.current_index]

        # Display filename and status at the top
        self.update_status(filename)
        
        left_video_frame = ttk.Frame(self.master, padding="10")
        left_video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_cover_frame = self.get_cover_frame(os.path.join(self.folder1, filename), (540, 360))
        left_cover_label = ttk.Label(left_video_frame, image=left_cover_frame)
        left_cover_label.image = left_cover_frame
        left_cover_label.pack(pady=10)

        play_btn1 = ttk.Button(left_video_frame, text="Play Left Video", command=lambda: self.play_video(filename, self.folder1))
        play_btn1.pack(pady=10)

        select_btn1 = ttk.Button(left_video_frame, text="Select Left Video", command=lambda: self.select_video(1, filename))
        select_btn1.pack(pady=10)

        right_video_frame = ttk.Frame(self.master, padding="10")
        right_video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_cover_frame = self.get_cover_frame(os.path.join(self.folder2, filename), (540, 360))
        right_cover_label = ttk.Label(right_video_frame, image=right_cover_frame)
        right_cover_label.image = right_cover_frame
        right_cover_label.pack(pady=10)

        play_btn2 = ttk.Button(right_video_frame, text="Play Right Video", command=lambda: self.play_video(filename, self.folder2))
        play_btn2.pack(pady=10)

        select_btn2 = ttk.Button(right_video_frame, text="Select Right Video", command=lambda: self.select_video(2, filename))
        select_btn2.pack(pady=10)

        # After right_video_frame is packed, we can get its width and height
        status_frame = ttk.Frame(self.master, padding="10")
        status_frame.pack(fill=tk.X, pady=20)
        
        # status_label = ttk.Label(status_frame, textvariable=self.current_status, font=("Arial", 12))
        # status_label.pack(pady=5)


    def update_status(self, filename):
        status_text = "Current Task Result: " + self.selections[self.current_index]
        self.current_status.set(status_text)
        
        if self.filename_label is not None:
            self.filename_label.destroy()
        
        self.filename_label = ttk.Label(self.master, text=f"Filename: {filename}, {self.current_status.get()}", font=("Arial", 14))
        self.filename_label.pack_propagate(False)  # Prevent the label from resizing
        window_width = self.master.winfo_width()
        label_width = self.filename_label.winfo_reqwidth()
        x_position = (window_width - label_width) / 2
        self.filename_label.place(x=x_position, rely=1.0, anchor='sw')

    def select_video(self, video_num, filename):
        if video_num == 1:
            self.selections[self.current_index] = "Left"
        else:
            self.selections[self.current_index] = "Right"
        self.update_status(filename)

    def next_task(self):
        if self.current_index < len(self.matching_files) - 1:
            self.current_index += 1
            self.load_video_pair()

    def prev_task(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_video_pair()

    def view_pane(self):
        # Here's a simple implementation for view pane. It just displays all the selections in a new window.
        new_win = tk.Toplevel(self.master)
        new_win.title("View Pane")

        for idx, selection in enumerate(self.selections):
            filename = self.matching_files[idx]
            label_text = f"Filename: {filename} - Selection: {selection}"
            label = ttk.Label(new_win, text=label_text)
            label.pack(pady=5)

    def finish(self):
        # Specify the path for the output file.
        output_file = "selection_results.txt"
        
        # Write the selections to the output file.
        with open(output_file, 'w') as f:
            for idx, selection in enumerate(self.selections):
                f.write(f"Video Pair {idx + 1}: {selection}\n")
        
        print(f"Selection results saved to {output_file}")
        
        # Exit the program.
        self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    folder1 = "videos1"
    folder2 = "videos2"
    app = VideoSelector(root, folder1, folder2)
    root.mainloop()
