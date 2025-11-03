import tkinter as tk
from GUI_broad_stone import GameUI

def main():
    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Ô Ăn Quan")
    root.geometry("1200x800")
    
    # Tạo UI với đường dẫn ảnh
    board_image_path = "Images/broad_main.png"
    stone_image_path = "Images/main_stone.png"
    ui = GameUI(root, board_image_path, stone_image_path)
    
    # Tạo trạng thái bàn cờ mẫu để hiển thị
    sample_board = [5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 1]
    

    
    # Vẽ bàn cờ với trạng thái mẫu
    ui.draw_board(sample_board)
    
    # Chạy ứng dụng
    root.mainloop()

if __name__ == "__main__":
    main()