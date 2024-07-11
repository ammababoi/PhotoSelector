import os
import shutil
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw

class PhotoSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Selector")

        self.window_width = root.winfo_screenwidth()
        self.window_height = root.winfo_screenheight()
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        self.frame = Frame(root, bg='black')
        self.frame.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(self.frame, bg='black', highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self.on_canvas_configure)

        self.second_frame = Frame(self.canvas, bg='white')
        self.canvas.create_window((self.window_width // 2, 0), window=self.second_frame, anchor="n")

        self.image_label = Label(self.second_frame, bg='white')
        self.image_label.pack()

        self.overlay_label = Label(self.second_frame, text="", bg="white", fg="black", font=("Helvetica", 16))
        self.overlay_label.pack()

        self.button_frame = Frame(self.second_frame, bg='white')
        self.button_frame.pack(pady=10)

        self.select_button = Button(self.button_frame, text="Select", command=self.toggle_selection, width=10, bg='lightgrey')
        self.select_button.pack(side=LEFT, padx=5)

        self.next_button = Button(self.button_frame, text="Next", command=self.next_image, width=10, bg='lightgrey')
        self.next_button.pack(side=LEFT, padx=5)

        self.prev_button = Button(self.button_frame, text="Previous", command=self.prev_image, width=10, bg='lightgrey')
        self.prev_button.pack(side=LEFT, padx=5)

        self.finish_button = Button(self.button_frame, text="Finish", command=self.finish_selection, width=10, bg='lightgrey')
        self.finish_button.pack(side=LEFT, padx=5)

        self.selected_photos = []
        self.current_image_index = 0
        self.image_files = []

        self.hints_label = Label(self.second_frame, text="Shortcuts: Left Arrow - Previous, Right Arrow - Next, Space - Select, Enter - Finish", bg="white", fg="blue", font=("Helvetica", 18))
        self.hints_label.pack(pady=10)

        self.load_images()
        self.root.bind('<Left>', lambda e: self.prev_image())
        self.root.bind('<Right>', lambda e: self.next_image())
        self.root.bind('<Return>', lambda e: self.finish_selection())
        self.root.bind('<space>', lambda e: self.toggle_selection())

        self.update_buttons()

    def load_images(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.image_files = [os.path.join(folder_selected, f) for f in os.listdir(folder_selected) if
                                f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

            if not self.image_files:
                messagebox.showerror("Error", "No images found in the selected directory.")
                self.root.quit()
                return

            self.image_files.sort(key=lambda x: os.path.basename(x))
            self.show_image()

    def show_image(self):
        if self.image_files:
            img_path = self.image_files[self.current_image_index]
            img_name = os.path.basename(img_path)
            try:
                img = Image.open(img_path)

                img_width = self.window_width - 100
                img_height = self.window_height - 200
                img.thumbnail((img_width, img_height), Image.LANCZOS)
                img = img.convert('RGB')
                radium_green = "#32CD32"
                if img_path in self.selected_photos:
                    draw = ImageDraw.Draw(img)
                    border_thickness = 10
                    for i in range(border_thickness):
                        draw.rectangle(
                            [(i, i), (img.size[0] - i - 1, img.size[1] - i - 1)],
                            outline=radium_green
                        )

                img_tk = ImageTk.PhotoImage(img)
                self.image_label.configure(image=img_tk)
                self.image_label.image = img_tk
                self.overlay_label.configure(text=img_name)
                self.root.title(img_name)
                self.update_buttons()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image {img_name}.\nError: {e}")

    def update_buttons(self):
        img_path = self.image_files[self.current_image_index]
        if img_path in self.selected_photos:
            self.select_button.configure(text="Selected", bg='green', fg='green')
        else:
            self.select_button.configure(text="Select", bg='lightgrey', fg='red')

    def toggle_selection(self, event=None):
        img_path = self.image_files[self.current_image_index]
        if img_path in self.selected_photos:
            self.selected_photos.remove(img_path)
        else:
            self.selected_photos.append(img_path)
        self.show_image()

    def next_image(self, event=None):
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.show_image()

    def prev_image(self, event=None):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image()

    def finish_selection(self):
        options = Toplevel(self.root)
        options.title("Finish Options")

        self.selected_options = []

        def update_selected_options(var, value):
            if var.get() == 1:
                self.selected_options.append(value)
            else:
                self.selected_options.remove(value)

        def apply_actions():
            try:
                if 'print' in self.selected_options:
                    for photo in self.selected_photos:
                        print(os.path.basename(photo))
                if 'copy' in self.selected_options:
                    dest_folder = filedialog.askdirectory()
                    if dest_folder:
                        for photo in self.selected_photos:
                            shutil.copy(photo, dest_folder)
                if 'move' in self.selected_options:
                    dest_folder = filedialog.askdirectory()
                    if dest_folder:
                        for photo in self.selected_photos:
                            shutil.move(photo, dest_folder)
                messagebox.showinfo("Success", "Actions applied successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply actions.\nError: {e}")
            finally:
                self.root.quit()

        print_var = IntVar()
        copy_var = IntVar()
        move_var = IntVar()

        Checkbutton(options, text="Print Selected Photos", variable=print_var,
                    command=lambda: update_selected_options(print_var, 'print')).pack(anchor=W)
        Checkbutton(options, text="Copy Selected Photos", variable=copy_var,
                    command=lambda: update_selected_options(copy_var, 'copy')).pack(anchor=W)
        Checkbutton(options, text="Move Selected Photos", variable=move_var,
                    command=lambda: update_selected_options(move_var, 'move')).pack(anchor=W)

        Button(options, text="Apply", command=apply_actions).pack(fill=X)

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.show_image()

if __name__ == "__main__":
    root = Tk()
    app = PhotoSelector(root)
    root.mainloop()
