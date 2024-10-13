import tkinter as tk
from tkinter import ttk, Toplevel, filedialog, messagebox, BooleanVar, DISABLED, NORMAL
from ttkthemes import ThemedTk
from convert_to_pdf import convert_to_pdf
from convert_to_image import convert_to_image


class App:
    def __init__(self):
        self.root = ThemedTk(theme="black")
        # self.root = ThemedTk(theme="arc")
        self.root.geometry("+600+200")
        self.root.title("File converters")
        self.__create_content()

    def run(self):
        self.root.mainloop()

    def __create_content(self):
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(pady=0, fill="both")

        converters = [
            ("IMG to PDF", lambda: self.__select_file("img", "pdf"), True),
            ("DOC to PDF", lambda: self.__select_file("doc", "pdf")),
            ("TXT to PDF", lambda: self.__select_file("txt", "pdf")),
            ("PDF to PNG", lambda: self.__select_file("pdf", "png"), True),
            ("JPG to PNG", lambda: self.__select_file("jpg", "png"), True),
            ("PDF to JPG", lambda: self.__select_file("pdf", "jpg"), True),
            ("PNG to JPG", lambda: self.__select_file("png", "jpg"), True),
            ("MP4 to MP3", lambda: self.__select_file("mp4")),
            ("CSV to XLSX", lambda: self.__select_file("csv")),
        ]

        for i, converter in enumerate(converters):
            text, command, *rest = converter
            enable = rest[0] if rest else False
            col = i % 3
            row = i // 3
            self.__create_conversion_option(text, row, col, command, enable)

    def __create_conversion_option(
        self, text: str, row: int, col: int, command, enable: bool = False
    ):
        button = ttk.Button(
            self.content_frame,
            text=text,
            width=15,
            padding=20,
            command=command,
            state=NORMAL if enable else DISABLED,
        )
        button.grid(row=row, column=col, padx=20, pady=25)

    def __select_file(self, original_type: str, output_type: str = "pdf"):
        filetypes = {
            "doc": [("Word Documents", "*.docx *.doc")],
            "img": [("Images", "*.png *jpg *jpeg *gif")],
            "png": [("Png Images", "*png")],
            "jpg": [("JPEG Images", "*jpg *jpeg")],
            "txt": [("Text Files", "*.txt")],
            "pdf": [("Pdf Files", "*.pdf")],
        }

        selected_file = filedialog.askopenfilename(
            title="Select File",
            filetypes=filetypes.get(original_type, [("All Files", "*.*")]),
        )
        if selected_file:
            self.__open_confirmation_window(selected_file, original_type, output_type)

    def __open_confirmation_window(self, file_path, file_type, output_type):
        file_name = (
            file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1]
        )

        output_name = file_name.split(".")[0] + "." + output_type

        confirm_win = Toplevel(self.root)
        confirm_win.title("Confirm Selection")
        confirm_win.geometry("400x200")
        confirm_win.resizable(False, False)
        confirm_win.grab_set()

        confirm_frame = ttk.Frame(confirm_win, padding=20)
        confirm_frame.pack(expand=True, fill="both")

        file_label = ttk.Label(
            confirm_frame,
            text=f"Selected File: {file_name}",
            font=("Helvetica", 12),
            wraplength=320,
        )
        file_label.pack(pady=10)

        rename_var = BooleanVar()

        def toggle_entry():
            if rename_var.get():
                new_name_entry.delete(0, tk.END)
                new_name_entry.insert(0, output_name)
                new_name_entry.pack(pady=10, before=confirm_button)
            else:
                new_name_entry.pack_forget()

        rename_checkbox = ttk.Checkbutton(
            confirm_frame,
            text="Change the file name",
            variable=rename_var,
            command=toggle_entry,
        )
        rename_checkbox.pack(pady=10)

        new_name_entry = ttk.Entry(confirm_frame, width=30, textvariable=output_name)

        def confirm_action():
            o = output_name
            if rename_var.get():
                new_name = new_name_entry.get().strip()
                if not new_name:
                    messagebox.showwarning(
                        "Input Required",
                        "Please enter a new file name.",
                        parent=confirm_frame,
                    )
                    return

                o = new_name
                messagebox.showinfo(
                    "Renamed",
                    f"File will be renamed to: {new_name}",
                    parent=confirm_frame,
                )
            res = -1

            match output_type:
                case "pdf":
                    res = convert_to_pdf(file_type, file_path, o)
                case "png" | "jpg" | "jpeg" | "gif":
                    res = convert_to_image(file_type, output_type, file_path, o)

            if res == -1:
                messagebox.showerror(
                    "Failure", "Error while converting", parent=confirm_frame
                )
                confirm_win.destroy()
                return

            messagebox.showinfo(
                "Converted", f"{o} is created successfully!", parent=confirm_frame
            )
            confirm_win.destroy()

        confirm_button = ttk.Button(
            confirm_frame, text="Confirm", command=confirm_action
        )
        confirm_button.pack(pady=0)


if __name__ == "__main__":
    App().run()
