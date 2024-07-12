import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class VideoProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Processor")

        self.folder_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        lbl_select_folder = tk.Label(frame, text="Select Folder Containing Videos:")
        lbl_select_folder.grid(row=0, column=0, padx=5, pady=5)

        self.entry_folder = tk.Entry(frame, textvariable=self.folder_path, width=50)
        self.entry_folder.grid(row=0, column=1, padx=5, pady=5)

        btn_browse = tk.Button(frame, text="Browse", command=self.browse_folder)
        btn_browse.grid(row=0, column=2, padx=5, pady=5)

        btn_process = tk.Button(frame, text="Process Videos", command=self.process_videos)
        btn_process.grid(row=1, columnspan=3, pady=10)

        self.progress = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=2, columnspan=3, pady=5)

        self.lbl_status = tk.Label(frame, text="Status: Waiting to start...")
        self.lbl_status.grid(row=3, columnspan=3, pady=5)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def process_videos(self):
        folder_path = self.folder_path.get()

        if not os.path.exists(folder_path):
            messagebox.showerror("Error", f"The folder path '{folder_path}' does not exist.")
            return

        video_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

        if not video_files:
            messagebox.showinfo("Info", "No .mp4 files found in the selected folder.")
            return

        self.progress["maximum"] = len(video_files)

        output_folder = folder_path

        for index, video_file in enumerate(video_files):
            input_path = os.path.join(folder_path, video_file)
            output_path = os.path.join(output_folder, f"a{index+1}.mp4")
            command = ["ffmpeg", "-i", input_path, "-vcodec", "libx264", "-crf", "27", output_path]
            subprocess.run(command)
            self.progress["value"] = index + 1
            self.lbl_status.config(text=f"Processed {index + 1}/{len(video_files)}: {video_file}")
            self.root.update_idletasks()

        messagebox.showinfo("Info", "Processing complete!")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoProcessorApp(root)
    root.mainloop()
