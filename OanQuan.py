import tkinter as tk
from PIL import Image, ImageTk
from GUI_broad_stone import GameUI
import time, os


class HandAnimation:
    def __init__(self, canvas, image_folder="ImagesHand/"):
        self.canvas = canvas
        self.image_folder = image_folder

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
        self.arrow = self.canvas.create_image(x, y, image=self.arrow_photo, anchor="center")

    def show_arrow_choice_flipped(self, x, y):
        """Hiển thị leftright đảo chiều"""
        if self.arrow:
            self.canvas.delete(self.arrow)
        self.arrow = self.canvas.create_image(x, y, image=self.arrow_photo_flip, anchor="center")

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


class OAnQuanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Ô Ăn Quan - Hand Fixed Version")
        self.ui = GameUI(root, "ImagesHand/broad_main.png", "ImagesHand/main_stone.png")
        self.board = [5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 1]
        self.ui.draw_board(self.board)

        self.hand = HandAnimation(self.ui.canvas, "ImagesHand/")
        self.ui.canvas.bind("<Button-1>", self.on_click_cell)

    def get_clicked_cell(self, x, y):
        for i, pos in enumerate(self.ui.cell_positions):
            cx, cy = pos
            if abs(x - cx) < 40 and abs(y - cy) < 40:
                return i
        return None

    def on_click_cell(self, event):
        clicked_idx = self.get_clicked_cell(event.x, event.y)
        if clicked_idx is not None and 6 <= clicked_idx <= 10 and self.board[clicked_idx] > 0:
            x, y = self.ui.cell_positions[clicked_idx]

            # Hiển thị tay h0
            self.hand.show_hand("h0", x, y - 25)
            # Hiển thị leftright trong ô
            self.hand.show_arrow_choice(x, y + 25)

            # Gắn sự kiện click vào leftright
            self.ui.canvas.tag_bind(self.hand.arrow, "<Button-1>",
                                    lambda e: self.handle_direction_choice(clicked_idx, e.x, e.y))

    def handle_direction_choice(self, idx, click_x, click_y):
        x, _ = self.ui.cell_positions[idx]
        self.hand.hide_arrow() 
        if click_x > x:
            # Hướng trái
            self.hand.show_arrow_choice_flipped(x, _ + 25)
            self.ui.canvas.update()
            time.sleep(0.2)
            self.hand.hide_arrow()
            self.hand.move_and_drop(self.ui, self.board, idx, direction="left")
        else:
            # Hướng phải
            self.hand.show_arrow_choice(x, _ + 25)
            self.ui.canvas.update()
            time.sleep(0.2)
            self.hand.hide_arrow()
            self.hand.move_and_drop(self.ui, self.board, idx, direction="right")


if __name__ == "__main__":
    root = tk.Tk()
    game = OAnQuanGame(root)
    root.mainloop()
