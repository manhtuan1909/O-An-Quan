import tkinter as tk
from GUI_broad_stone import GameUI
from hand_animation import HandAnimation
import time


class OAnQuanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Ô Ăn Quan")

        self.ui = GameUI(root, "O-An-Quan/ImagesHand/broad_main.png", "O-An-Quan/ImagesHand/main_stone.png")

        # Trạng thái bàn cờ ban đầu
        self.board = [5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 1]

        # Vẽ bàn cờ
        self.ui.draw_board(self.board)

        # Khởi tạo animation của tay
        self.hand = HandAnimation(self.ui.canvas, "O-An-Quan/ImagesHand/")

        # Gán sự kiện click chuột
        self.ui.canvas.bind("<Button-1>", self.on_click_cell)

    def get_clicked_cell(self, x, y):
        """Xác định ô được click"""
        for i, pos in enumerate(self.ui.cell_positions):
            cx, cy = pos
            if abs(x - cx) < 40 and abs(y - cy) < 40:
                return i
        return None

    def on_click_cell(self, event):
        """Khi người chơi click vào ô"""
        clicked_idx = self.get_clicked_cell(event.x, event.y)
        if clicked_idx is not None and 6 <= clicked_idx <= 10 and self.board[clicked_idx] > 0:
            x, y = self.ui.cell_positions[clicked_idx]

            # Hiển thị tay và mũi tên chọn hướng
            self.hand.show_hand("h0", x, y - 25)
            self.hand.show_arrow_choice(x, y + 25)

            # Gắn sự kiện khi click vào mũi tên
            self.ui.canvas.tag_bind(self.hand.arrow, "<Button-1>",
                                    lambda e: self.handle_direction_choice(clicked_idx, e.x, e.y))

    def handle_direction_choice(self, idx, click_x, click_y):
        """Xử lý khi chọn hướng trái hoặc phải"""
        x, y = self.ui.cell_positions[idx]
        self.hand.hide_arrow()

        if click_x < x:
            # Hướng phải
            self.hand.show_arrow_choice(x, y + 25)
            self.ui.canvas.update()
            time.sleep(0.2)
            self.hand.hide_arrow()
            self.hand.move_and_drop(self.ui, self.board, idx, direction="right")
        else:
            # Hướng trái
            self.hand.show_arrow_choice_flipped(x, y + 25)
            self.ui.canvas.update()
            time.sleep(0.2)
            self.hand.hide_arrow()
            self.hand.move_and_drop(self.ui, self.board, idx, direction="left")


if __name__ == "__main__":
    root = tk.Tk()
    game = OAnQuanGame(root)
    root.mainloop()
