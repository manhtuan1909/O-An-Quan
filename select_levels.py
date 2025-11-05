import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont

class LevelSelect:
    def __init__(self, master):
        self.master = master
        self.master.title("Chọn cấp độ")
        self.master.geometry("800x500")

        # --- Background ---
        bg = Image.open("O-An-Quan/ImagesHand/select_level.png").resize((800, 500))
        self.bg_img = ImageTk.PhotoImage(bg)
        self.bg_label = tk.Label(master, image=self.bg_img)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # --- Danh sách cấp độ ---
        levels = [
            {"name": "Dễ", "img": "ava1.png", "pos": (180, 230)},
            {"name": "Trung bình", "img": "ava2.png", "pos": (370, 230)},
            {"name": "Khó", "img": "ava3.png", "pos": (560, 230)}
        ]

        # Giữ tham chiếu ảnh
        self.avatars = []
        self.labels = []

        for lvl in levels:
            # Avatar
            ava_img = Image.open(f"O-An-Quan/ImagesHand/{lvl['img']}").convert("RGBA")
            ava_tk = ImageTk.PhotoImage(ava_img)
            self.avatars.append(ava_tk)

            # Button ảnh
            btn = tk.Button(
                master,
                image=ava_tk,
                bd=0,
                highlightthickness=0,
                bg="#0e4001",
                activebackground="#0e4001",
                command=lambda name=lvl["name"]: self.select_level(name)
            )
            btn.place(x=lvl["pos"][0], y=lvl["pos"][1])

            # Label kiểu viền vàng chữ đỏ cam
            label = tk.Label(
                master,
                text=lvl["name"],
                font=("Arial", 16, "bold"),
                fg="#ffcc00",  # vàng
                bg="#314504"
            )
            label.place(x=lvl["pos"][0] + 45, y=lvl["pos"][1] + 120, anchor="center")
            self.labels.append(label)

    def select_level(self, name):
        print(f"Đã chọn cấp độ: {name}")

# --- Chạy ---
root = tk.Tk()
app = LevelSelect(root)
root.mainloop()
