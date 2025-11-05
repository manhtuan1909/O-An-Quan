import tkinter as tk
from PIL import Image, ImageTk
from GUI_broad_stone import GameUI
import time, os


class HandAnimation:
    def __init__(self, canvas, image_folder="ImagesHand/"):
        self.canvas = canvas
        self.image_folder = image_folder

        self.raiso_img = ImageTk.PhotoImage(Image.open(os.path.join(image_folder, "raison.png")).resize((155, 57)))
        self.raiso_label = None
        # Load 4 ảnh tay
        self.hand_imgs = {
            "h0": ImageTk.PhotoImage(Image.open(os.path.join(image_folder, "h0.png")).resize((60, 60))),
            "h1": ImageTk.PhotoImage(Image.open(os.path.join(image_folder, "h1.png")).resize((60, 60))),
            "h2": ImageTk.PhotoImage(Image.open(os.path.join(image_folder, "h2.png")).resize((60, 60))),
            "h3": ImageTk.PhotoImage(Image.open(os.path.join(image_folder, "h3.png")).resize((60, 60))),
        }

        # Load leftright (để nguyên chiều thực)
        img_lr = Image.open(os.path.join(image_folder, "leftright.png")).resize((100, 45))
        self.arrow_photo = ImageTk.PhotoImage(img_lr)

        # Ảnh đảo ngược (để khi chọn hướng trái)
        self.arrow_photo_flip = ImageTk.PhotoImage(img_lr.transpose(Image.FLIP_LEFT_RIGHT))

        self.hand = None
        self.arrow = None

    def show_hand(self, img_key, x, y):
        """Hiển thị ảnh tay"""
        if self.hand:
            self.canvas.delete(self.hand)
        self.hand = self.canvas.create_image(x, y, image=self.hand_imgs[img_key], anchor="center")

    def show_arrow_choice(self, x, y):
        """Hiển thị leftright tại ô"""
        if self.arrow:
            self.canvas.delete(self.arrow)
        self.arrow = self.canvas.create_image(x, y-30, image=self.arrow_photo, anchor="center")

    def show_arrow_choice_flipped(self, x, y):
        """Hiển thị leftright đảo chiều"""
        if self.arrow:
            self.canvas.delete(self.arrow)
        self.arrow = self.canvas.create_image(x, y-30, image=self.arrow_photo_flip, anchor="center")

    def hide_arrow(self):
        if self.arrow:
            self.canvas.delete(self.arrow)
            self.arrow = None

    def move_and_drop(self, ui, board_state, start_idx, direction="right"):
        """Animation rải quân"""
        stones = board_state[start_idx]
        board_state[start_idx] = 0
        ui.draw_board(board_state)
        self.canvas.update()

        idx = start_idx
        self.show_hand("h1", *ui.cell_positions[idx])
        self.canvas.update()
        time.sleep(0.25)

         # Hiển thị ảnh "Rải Sỏi"
        if self.raiso_label:
            self.canvas.delete(self.raiso_label)
        self.raiso_label = self.canvas.create_image(600, 80, image=self.raiso_img, anchor="center")
        self.canvas.update()


        for i in range(stones):
            if direction == "right":
                idx = (idx + 1) % 12
            else:
                idx = (idx - 1) % 12

            x, y = ui.cell_positions[idx]
            self.show_hand("h2", x, y - 25)
            self.canvas.update()
            time.sleep(0.25)

            board_state[idx] += 1
            ui.draw_board(board_state)
            self.canvas.update()
            time.sleep(0.18)
        
        # Kiểm tra ô kế tiếp có rỗng không => chỉ đập 1 lần ở ô đó
        next_idx = (idx + 1) % 12 if direction == "right" else (idx - 1) % 12
        if board_state[next_idx] == 0:
            x_next, y_next = ui.cell_positions[next_idx]
            self.show_hand("h3", x_next, y_next - 25)
            self.canvas.update()
            time.sleep(0.4)

        self.canvas.delete(self.hand)