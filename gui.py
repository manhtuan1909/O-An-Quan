"""GUI module cho game Ô Ăn Quan."""
import tkinter as tk
from PIL import Image, ImageTk
import random
from constants import *
from stone import GameBoard, Stone
from game_logic import GameController


class OAnQuanGUI:
    """Quản lý giao diện người dùng."""
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        
        # Canvas chính
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
        self.canvas.pack()
        
        # Game state
        self.current_screen = None
        self.game_mode = None
        self.difficulty = None
        self.game_board = None
        self.images = {}
        self.animation_running = False
        self.hand_image_id = None
        
        self.load_all_images()
        self.show_menu()
    
    def load_all_images(self):
        """Load và cache tất cả hình ảnh."""
        try:
            self.images['menu'] = self._load_image(IMAGE_MENU, WINDOW_WIDTH, WINDOW_HEIGHT)
            self.images['choose'] = self._load_image(IMAGE_CHOOSE, WINDOW_WIDTH, WINDOW_HEIGHT)
            self.images['ingame_bg'] = self._load_image(IMAGE_INGAME_BG, WINDOW_WIDTH, WINDOW_HEIGHT)
            
            self.images['player1_win'] = self._load_image(IMAGE_PLAYER1_WIN, 600, 250)
            self.images['player2_win'] = self._load_image(IMAGE_PLAYER2_WIN, 600, 250)
            self.images['h0'] = self._load_image(IMAGE_H0, 60, 60)
            self.images['h1'] = self._load_image(IMAGE_H1, 60, 60)
            self.images['h2'] = self._load_image(IMAGE_H2, 60, 60)
            self.images['h3'] = self._load_image(IMAGE_H3, 60, 60)
            
            try:
                self.images['left'] = self._load_image(IMAGE_LEFT, 50, 50)
                self.images['right'] = self._load_image(IMAGE_RIGHT, 50, 50)
            except:
                print("Không tìm thấy ảnh left/right, sử dụng mũi tên mặc định")
            
            print(" Đã load tất cả hình ảnh")
        except Exception as e:
            print(f" Lỗi load hình ảnh: {e}")
    
    def _load_image(self, path, width, height):
        """Load và resize ảnh."""
        img = Image.open(path).convert("RGBA")
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    
    def show_menu(self):
        """Hiển thị màn hình menu."""
        self.current_screen = "menu"
        self.canvas.delete("all")
        
        self.canvas.create_image(0, 0, image=self.images['menu'], anchor='nw', tags='menu_bg')
        btn_pvp = self.canvas.create_rectangle(
            MENU_BUTTON_PVP['x'] - MENU_BUTTON_PVP['width']//2,
            MENU_BUTTON_PVP['y'] - MENU_BUTTON_PVP['height']//2,
            MENU_BUTTON_PVP['x'] + MENU_BUTTON_PVP['width']//2,
            MENU_BUTTON_PVP['y'] + MENU_BUTTON_PVP['height']//2,
            fill='', outline='', tags='btn_pvp'
        )
        self.canvas.tag_bind('btn_pvp', '<Button-1>', lambda e: self.on_menu_pvp())
        self.canvas.tag_bind('btn_pvp', '<Enter>', lambda e: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('btn_pvp', '<Leave>', lambda e: self.canvas.config(cursor=''))
        btn_pve = self.canvas.create_rectangle(
            MENU_BUTTON_PVE['x'] - MENU_BUTTON_PVE['width']//2,
            MENU_BUTTON_PVE['y'] - MENU_BUTTON_PVE['height']//2,
            MENU_BUTTON_PVE['x'] + MENU_BUTTON_PVE['width']//2,
            MENU_BUTTON_PVE['y'] + MENU_BUTTON_PVE['height']//2,
            fill='', outline='', tags='btn_pve'
        )
        self.canvas.tag_bind('btn_pve', '<Button-1>', lambda e: self.on_menu_pve())
        self.canvas.tag_bind('btn_pve', '<Enter>', lambda e: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('btn_pve', '<Leave>', lambda e: self.canvas.config(cursor=''))
        btn_exit = self.canvas.create_rectangle(
            MENU_BUTTON_EXIT['x'] - MENU_BUTTON_EXIT['width']//2,
            MENU_BUTTON_EXIT['y'] - MENU_BUTTON_EXIT['height']//2,
            MENU_BUTTON_EXIT['x'] + MENU_BUTTON_EXIT['width']//2,
            MENU_BUTTON_EXIT['y'] + MENU_BUTTON_EXIT['height']//2,
            fill='', outline='', tags='btn_exit'
        )
        self.canvas.tag_bind('btn_exit', '<Button-1>', lambda e: self.root.quit())
        self.canvas.tag_bind('btn_exit', '<Enter>', lambda e: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('btn_exit', '<Leave>', lambda e: self.canvas.config(cursor=''))
    
    def on_menu_pvp(self):
        """Xử lý chọn chế độ PvP."""
        self.game_mode = "pvp"
        self.show_game()
    
    def on_menu_pve(self):
        """Xử lý chọn chế độ PvE."""
        self.game_mode = "pve"
        self.show_choose_difficulty()
    
    def show_choose_difficulty(self):
        """Hiển thị màn hình chọn độ khó."""
        self.current_screen = "choose"
        self.canvas.delete("all")
        
        self.canvas.create_image(0, 0, image=self.images['choose'], anchor='nw', tags='choose_bg')
        btn_easy = self.canvas.create_rectangle(
            CHOOSE_BUTTON_EASY['x'] - CHOOSE_BUTTON_EASY['width']//2,
            CHOOSE_BUTTON_EASY['y'] - CHOOSE_BUTTON_EASY['height']//2,
            CHOOSE_BUTTON_EASY['x'] + CHOOSE_BUTTON_EASY['width']//2,
            CHOOSE_BUTTON_EASY['y'] + CHOOSE_BUTTON_EASY['height']//2,
            fill='', outline='', tags='btn_easy'
        )
        self.canvas.tag_bind('btn_easy', '<Button-1>', lambda e: self.on_choose_difficulty('easy'))
        self.canvas.tag_bind('btn_easy', '<Enter>', lambda e: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('btn_easy', '<Leave>', lambda e: self.canvas.config(cursor=''))
        btn_medium = self.canvas.create_rectangle(
            CHOOSE_BUTTON_MEDIUM['x'] - CHOOSE_BUTTON_MEDIUM['width']//2,
            CHOOSE_BUTTON_MEDIUM['y'] - CHOOSE_BUTTON_MEDIUM['height']//2,
            CHOOSE_BUTTON_MEDIUM['x'] + CHOOSE_BUTTON_MEDIUM['width']//2,
            CHOOSE_BUTTON_MEDIUM['y'] + CHOOSE_BUTTON_MEDIUM['height']//2,
            fill='', outline='', tags='btn_medium'
        )
        self.canvas.tag_bind('btn_medium', '<Button-1>', lambda e: self.on_choose_difficulty('medium'))
        self.canvas.tag_bind('btn_medium', '<Enter>', lambda e: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('btn_medium', '<Leave>', lambda e: self.canvas.config(cursor=''))
        btn_hard = self.canvas.create_rectangle(
            CHOOSE_BUTTON_HARD['x'] - CHOOSE_BUTTON_HARD['width']//2,
            CHOOSE_BUTTON_HARD['y'] - CHOOSE_BUTTON_HARD['height']//2,
            CHOOSE_BUTTON_HARD['x'] + CHOOSE_BUTTON_HARD['width']//2,
            CHOOSE_BUTTON_HARD['y'] + CHOOSE_BUTTON_HARD['height']//2,
            fill='', outline='', tags='btn_hard'
        )
        self.canvas.tag_bind('btn_hard', '<Button-1>', lambda e: self.on_choose_difficulty('hard'))
        self.canvas.tag_bind('btn_hard', '<Enter>', lambda e: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('btn_hard', '<Leave>', lambda e: self.canvas.config(cursor=''))
        btn_back = self.canvas.create_rectangle(
            CHOOSE_BUTTON_BACK['x'] - CHOOSE_BUTTON_BACK['width']//2,
            CHOOSE_BUTTON_BACK['y'] - CHOOSE_BUTTON_BACK['height']//2,
            CHOOSE_BUTTON_BACK['x'] + CHOOSE_BUTTON_BACK['width']//2,
            CHOOSE_BUTTON_BACK['y'] + CHOOSE_BUTTON_BACK['height']//2,
            fill='', outline='', tags='btn_back'
        )
        self.canvas.tag_bind('btn_back', '<Button-1>', lambda e: self.show_menu())
        self.canvas.tag_bind('btn_back', '<Enter>', lambda e: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('btn_back', '<Leave>', lambda e: self.canvas.config(cursor=''))
    
    def on_choose_difficulty(self, difficulty):
        """Xử lý chọn độ khó."""
        self.difficulty = difficulty
        print(f"Đã chọn độ khó: {difficulty}")
        self.show_game()
    
    def show_game(self):
        """Hiển thị màn hình game."""
        self.current_screen = "game"
        self.canvas.delete("all")
        
        self.game_board = GameBoard()
        self.game_board.init_stones()
        self.game_controller = GameController(self, self.game_board, self.game_mode, self.difficulty)
        
        self.canvas.create_image(0, 0, image=self.images['ingame_bg'], anchor='nw', tags='game_bg')
        self.draw_all_stones()
        btn_undo = self.canvas.create_rectangle(
            INGAME_BUTTON_UNDO['x'] - INGAME_BUTTON_UNDO['width']//2,
            INGAME_BUTTON_UNDO['y'] - INGAME_BUTTON_UNDO['height']//2,
            INGAME_BUTTON_UNDO['x'] + INGAME_BUTTON_UNDO['width']//2,
            INGAME_BUTTON_UNDO['y'] + INGAME_BUTTON_UNDO['height']//2,
            fill='', outline='', tags='btn_undo'
        )
        self.canvas.tag_bind('btn_undo', '<Button-1>', lambda e: self.on_undo())
        self.canvas.tag_bind('btn_undo', '<Enter>', lambda e: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('btn_undo', '<Leave>', lambda e: self.canvas.config(cursor=''))
        
        btn_exit_game = self.canvas.create_rectangle(
            INGAME_BUTTON_EXIT['x'] - INGAME_BUTTON_EXIT['width']//2,
            INGAME_BUTTON_EXIT['y'] - INGAME_BUTTON_EXIT['height']//2,
            INGAME_BUTTON_EXIT['x'] + INGAME_BUTTON_EXIT['width']//2,
            INGAME_BUTTON_EXIT['y'] + INGAME_BUTTON_EXIT['height']//2,
            fill='', outline='', tags='btn_exit_game'
        )
        self.canvas.tag_bind('btn_exit_game', '<Button-1>', lambda e: self.show_menu())
        self.canvas.tag_bind('btn_exit_game', '<Enter>', lambda e: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('btn_exit_game', '<Leave>', lambda e: self.canvas.config(cursor=''))
        
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        print(f" Bắt đầu game - Mode: {self.game_mode}, Difficulty: {self.difficulty}")
        print(f" Board state: {self.game_board.get_board_state()}")
        print(f" Lượt chơi: Player {self.game_controller.current_player}")
    
    def draw_all_stones(self):
        """Vẽ tất cả đá trên bàn cờ."""
        self.canvas.delete("stone")
        
        if not hasattr(self, '_stone_images'):
            self._stone_images = []
        self._stone_images = []
        
        for cell_id, cell in self.game_board.cells.items():
            for stone in cell.stones:
                if stone.type == "Quan":
                    self.draw_stone(stone, size=QUAN_SIZE)
                else:
                    self.draw_stone(stone, size=STONE_SIZE)
        
        self.draw_captured_stones(1)
        self.draw_captured_stones(2)
        self.draw_stone_counts()
        self.draw_scores()
        
        self.canvas.tag_raise('stone_count')
        self.canvas.tag_raise('score_text')
        self.canvas.tag_raise('hand')
        self.canvas.tag_raise('direction_arrow')
    
    def draw_stone(self, stone, size=None):
        """Vẽ một viên đá."""
        try:
            if size is None:
                if stone.type == "Quan":
                    size = QUAN_SIZE
                else:
                    size = STONE_SIZE
            
            img = stone.load_image(size)
            photo = ImageTk.PhotoImage(img)
            self._stone_images.append(photo)
            
            stone.canvas_id = self.canvas.create_image(
                stone.x, stone.y,
                image=photo,
                anchor='center',
                tags='stone'
            )
        except Exception as e:
            print(f"Lỗi vẽ đá {stone}: {e}")
    
    def draw_captured_stones(self, player):
        """Vẽ đá ăn được trong vùng điểm."""
        if player == 1:
            area = SCORE_AREA_P1
            stones = self.game_board.player1_captured
        else:
            area = SCORE_AREA_P2
            stones = self.game_board.player2_captured
        
        area_width = area['x2'] - area['x1'] - 40
        area_height = area['y2'] - area['y1'] - 40
        
        for stone in stones:
            if not hasattr(stone, 'captured_position_set'):
                x = area['x1'] + 20 + random.randint(0, area_width)
                y = area['y1'] + 20 + random.randint(0, area_height)
                stone.x = x
                stone.y = y
                stone.captured_position_set = True
            
            if stone.type == "Quan":
                self.draw_stone(stone, size=QUAN_SIZE)
            else:
                self.draw_stone(stone, size=STONE_SIZE_CAPTURED)
    
    def draw_stone_counts(self):
        """Vẽ số đá trong mỗi ô."""
        self.canvas.delete("stone_count")
        
        for cell_id, cell in self.game_board.cells.items():
            count = cell.count()
            if count > 0:
                x, y = cell.center
                self.canvas.create_text(
                    x + 35, y - 35,
                    text=str(count),
                    font=("Arial", 16, "bold"),
                    fill="white",
                    tags="stone_count"
                )
    
    def draw_scores(self):
        """Vẽ điểm số của các player."""
        self.canvas.delete("score_text")
        
        score1 = self.game_board.calculate_score(1)
        score2 = self.game_board.calculate_score(2)
        
        quan_1 = sum(1 for s in self.game_board.player1_captured if s.type == "Quan")
        dan_1 = sum(1 for s in self.game_board.player1_captured if s.type != "Quan")
        quan_2 = sum(1 for s in self.game_board.player2_captured if s.type == "Quan")
        dan_2 = sum(1 for s in self.game_board.player2_captured if s.type != "Quan")
        
        if quan_1 > 0 or quan_2 > 0:
            print(f" Điểm hiện tại:")
            print(f"   P1: {quan_1} quan × 10 + {dan_1} dân × 1 = {score1} điểm")
            print(f"   P2: {quan_2} quan × 10 + {dan_2} dân × 1 = {score2} điểm")
        score_x1 = SCORE_AREA_P1['x1'] + 100
        score_y1 = SCORE_AREA_P1['y1'] + 155
        self.canvas.create_text(
            score_x1, score_y1,
            text=f"{score1}",
            font=("Arial", 22, "bold"),
            fill="yellow",
            anchor="w",
            tags="score_text"
        )
        
        # Vẽ điểm Player 2 (trên phải)
        score_x2 = SCORE_AREA_P2['x1'] + 100
        score_y2 = SCORE_AREA_P2['y1'] + 145
        self.canvas.create_text(
            score_x2, score_y2,
            text=f"{score2}",
            font=("Arial", 22, "bold"),
            fill="yellow",
            anchor="w",
            tags="score_text"
        )
    
    def on_canvas_click(self, event):
        """Xử lý click vào canvas."""
        x, y = event.x, event.y
        
        clicked_cell = None
        for cell_id, cell in self.game_board.cells.items():
            cx, cy = cell.center
            distance = ((x - cx)**2 + (y - cy)**2)**0.5
            if distance < cell.radius:
                clicked_cell = cell_id
                break
        
        if clicked_cell is not None:
            self.game_controller.on_cell_click(clicked_cell)
    
    def on_undo(self):
        """Xử lý nút Undo."""
        print("Undo chưa được implement")
    
    def show_hand(self, hand_type, x, y):
        """Hiển thị bàn tay."""
        if self.hand_image_id:
            self.canvas.delete(self.hand_image_id)
        
        self.hand_image_id = self.canvas.create_image(
            x, y + HAND_OFFSET_Y,
            image=self.images[hand_type],
            anchor='center',
            tags='hand'
        )
        self.canvas.tag_raise('hand')
    
    def hide_hand(self):
        """Ẩn bàn tay."""
        if self.hand_image_id:
            self.canvas.delete(self.hand_image_id)
            self.hand_image_id = None
    
    def show_winner(self, winner):
        """Hiển thị dialog thắng."""
        overlay = self.canvas.create_rectangle(
            0, 0, WINDOW_WIDTH, WINDOW_HEIGHT,
            fill='black', stipple='gray50',
            tags='win_overlay'
        )
        
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        if winner == 1:
            win_image = self.canvas.create_image(
                center_x, center_y,
                image=self.images['player1_win'],
                anchor='center',
                tags='win_dialog'
            )
            print("Player 1 thắng!")
        else:
            win_image = self.canvas.create_image(
                center_x, center_y,
                image=self.images['player2_win'],
                anchor='center',
                tags='win_dialog'
            )
            print("Player 2 thắng!")
        
        btn_replay_x = center_x - 80
        btn_replay_y = center_y + 150
        btn_replay = self.canvas.create_rectangle(
            btn_replay_x - 70, btn_replay_y - 25,
            btn_replay_x + 70, btn_replay_y + 25,
            fill='#4CAF50', outline='white', width=2,
            tags='btn_replay'
        )
        btn_replay_text = self.canvas.create_text(
            btn_replay_x, btn_replay_y,
            text="Chơi lại",
            font=("Arial", 16, "bold"),
            fill="white",
            tags='btn_replay_text'
        )
        self.canvas.tag_bind('btn_replay', '<Button-1>', lambda e: self.show_game())
        self.canvas.tag_bind('btn_replay_text', '<Button-1>', lambda e: self.show_game())
        self.canvas.tag_bind('btn_replay', '<Enter>', lambda e: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('btn_replay', '<Leave>', lambda e: self.canvas.config(cursor=''))
        
        btn_menu_x = center_x + 80
        btn_menu_y = center_y + 150
        btn_menu = self.canvas.create_rectangle(
            btn_menu_x - 70, btn_menu_y - 25,
            btn_menu_x + 70, btn_menu_y + 25,
            fill='#FF9800', outline='white', width=2,
            tags='btn_menu'
        )
        btn_menu_text = self.canvas.create_text(
            btn_menu_x, btn_menu_y,
            text="Menu",
            font=("Arial", 16, "bold"),
            fill="white",
            tags='btn_menu_text'
        )
        self.canvas.tag_bind('btn_menu', '<Button-1>', lambda e: self.show_menu())
        self.canvas.tag_bind('btn_menu_text', '<Button-1>', lambda e: self.show_menu())
        self.canvas.tag_bind('btn_menu', '<Enter>', lambda e: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('btn_menu', '<Leave>', lambda e: self.canvas.config(cursor=''))


def main():
    """Entry point."""
    root = tk.Tk()
    app = OAnQuanGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

