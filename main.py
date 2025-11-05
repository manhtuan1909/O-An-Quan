"""Entry point cho game Ô Ăn Quan."""
import tkinter as tk
from gui import OAnQuanGUI


def main():
    """Khởi chạy game."""
    root = tk.Tk()
    app = OAnQuanGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

