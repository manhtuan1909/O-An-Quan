"""Game logic và điều khiển animation."""
import time
from constants import *
from ai import OAnQuanAI


class GameController:
    """Điều khiển logic game và animation."""
    
    def __init__(self, gui, game_board, game_mode=None, difficulty=None):
        self.gui = gui
        self.board = game_board
        self.game_mode = game_mode
        self.difficulty = difficulty
        self.current_player = 1
        self.selected_cell = None
        self.hand_visible = False
        self.direction_arrows_visible = False
        self.animation_running = False
        self.borrowed_p1 = 0
        self.borrowed_p2 = 0
        
        if self.game_mode == 'pve' and self.difficulty:
            self.ai = OAnQuanAI(self.difficulty)
            print(f"AI đã sẵn sàng - Độ khó: {self.difficulty}")
        else:
            self.ai = None
    
    def get_direction_offset(self, direction):
        """Chuyển đổi direction thành offset theo góc nhìn của player."""
        if self.current_player == 1:
            return 1 if direction == 'left' else -1
        else:
            return -1 if direction == 'left' else 1
        
    def can_select_cell(self, cell_id):
        """Kiểm tra ô có thể chọn không."""
        if cell_id in QUAN_CELLS:
            return False
        if self.board.cells[cell_id].is_empty():
            return False
        if self.current_player == 1:
            return cell_id in PLAYER1_CELLS
        else:
            return cell_id in PLAYER2_CELLS
    
    def on_cell_click(self, cell_id):
        """Xử lý khi click vào ô."""
        if self.animation_running:
            return
        
        if self.selected_cell is not None and cell_id != self.selected_cell:
            self.hide_selection()
            if self.can_select_cell(cell_id):
                self.selected_cell = cell_id
                self.show_hand_h0(cell_id)
                self.hand_visible = True
                self.direction_arrows_visible = False
        elif self.selected_cell is None and self.can_select_cell(cell_id):
            self.selected_cell = cell_id
            self.show_hand_h0(cell_id)
            self.hand_visible = True
            self.direction_arrows_visible = False
        elif self.selected_cell == cell_id and not self.direction_arrows_visible:
            self.show_direction_arrows(cell_id)
            self.direction_arrows_visible = True
        elif self.selected_cell == cell_id and self.direction_arrows_visible:
            self.hide_direction_arrows()
            self.direction_arrows_visible = False
    
    def hide_selection(self):
        """Ẩn tất cả selection."""
        self.gui.hide_hand()
        self.hide_direction_arrows()
        self.selected_cell = None
        self.hand_visible = False
        self.direction_arrows_visible = False
    
    def show_hand_h0(self, cell_id):
        """Hiển thị bàn tay h0."""
        x, y = self.board.cells[cell_id].center
        self.gui.show_hand('h0', x, y)
    
    def show_direction_arrows(self, cell_id):
        """Hiển thị nút chọn hướng trái/phải."""
        x, y = self.board.cells[cell_id].center
        arrow_y = y + 50
        spacing = 60
        
        self.left_arrow_id = self.gui.canvas.create_image(
            x - spacing, arrow_y,
            image=self.gui.images.get('left'),
            anchor='center',
            tags='direction_arrow'
        )
        
        self.right_arrow_id = self.gui.canvas.create_image(
            x + spacing, arrow_y,
            image=self.gui.images.get('right'),
            anchor='center',
            tags='direction_arrow'
        )
        self.gui.canvas.tag_bind(self.left_arrow_id, '<Button-1>', 
                                lambda e: self.start_move('left'))
        self.gui.canvas.tag_bind(self.right_arrow_id, '<Button-1>', 
                                lambda e: self.start_move('right'))
        self.gui.canvas.tag_bind(self.left_arrow_id, '<Enter>', 
                                lambda e: self.gui.canvas.config(cursor='hand2'))
        self.gui.canvas.tag_bind(self.left_arrow_id, '<Leave>', 
                                lambda e: self.gui.canvas.config(cursor=''))
        self.gui.canvas.tag_bind(self.right_arrow_id, '<Enter>', 
                                lambda e: self.gui.canvas.config(cursor='hand2'))
        self.gui.canvas.tag_bind(self.right_arrow_id, '<Leave>', 
                                lambda e: self.gui.canvas.config(cursor=''))
    
    def hide_direction_arrows(self):
        """Ẩn nút chọn hướng."""
        self.gui.canvas.delete('direction_arrow')
    
    def start_move(self, direction):
        """Bắt đầu di chuyển đá."""
        if self.selected_cell is None or self.animation_running:
            return
        
        self.animation_running = True
        self.hide_direction_arrows()
        self.gui.root.after(100, lambda: self.distribute_stones(
            self.selected_cell, direction
        ))
    
    def distribute_stones(self, start_cell, direction):
        """Rải quân theo luật game."""
        stones = self.board.pick_stones(start_cell)
        num_stones = len(stones)
        
        if num_stones == 0:
            self.animation_running = False
            return
        
        x, y = self.board.cells[start_cell].center
        self.gui.show_hand('h1', x, y)
        self.gui.draw_all_stones()
        self.gui.root.update()
        time.sleep(0.3)
        
        current_cell = start_cell
        
        for i in range(num_stones):
            offset = self.get_direction_offset(direction)
            current_cell = (current_cell + offset) % 12
            
            from_cell = start_cell if i == 0 else prev_cell
            self.animate_hand_move(
                self.board.cells[from_cell].center,
                self.board.cells[current_cell].center,
                'h1'
            )
            
            stone = stones[i]
            self.board.drop_stone(current_cell, stone)
            
            x, y = self.board.cells[current_cell].center
            self.gui.show_hand('h2', x, y)
            self.gui.draw_all_stones()
            self.gui.root.update()
            time.sleep(0.3)
            
            if i < num_stones - 1:
                self.gui.show_hand('h1', x, y)
                self.gui.root.update()
                time.sleep(0.2)
            
            prev_cell = current_cell
        
        offset = self.get_direction_offset(direction)
        next_cell = (current_cell + offset) % 12
        
        if self.board.cells[next_cell].is_empty():
            self.check_and_capture(current_cell, next_cell, direction)
        elif next_cell in QUAN_CELLS:
            self.end_turn()
        else:
            time.sleep(0.3)
            self.gui.root.after(100, lambda: self.distribute_stones(next_cell, direction))
    
    def check_and_capture(self, current_cell, empty_cell, direction):
        """Kiểm tra và ăn quân."""
        self.animate_hand_move(
            self.board.cells[current_cell].center,
            self.board.cells[empty_cell].center,
            'h1'
        )
        
        x, y = self.board.cells[empty_cell].center
        self.gui.show_hand('h3', x, y)
        self.gui.root.update()
        time.sleep(0.4)
        
        offset = self.get_direction_offset(direction)
        capture_cell = (empty_cell + offset) % 12
        
        if self.board.cells[capture_cell].is_empty():
            self.end_turn()
            return
        
        if capture_cell in QUAN_CELLS:
            has_quan = any(s.type == "Quan" for s in self.board.cells[capture_cell].stones)
            if has_quan:
                num_dan = sum(1 for s in self.board.cells[capture_cell].stones if s.type != "Quan")
                if num_dan < 5:
                    self.end_turn()
                    return
        
        self.animate_hand_move(
            self.board.cells[empty_cell].center,
            self.board.cells[capture_cell].center,
            'h1'
        )
        
        captured_stones = self.board.pick_stones(capture_cell)
        x, y = self.board.cells[capture_cell].center
        self.gui.show_hand('h1', x, y)
        self.gui.draw_all_stones()
        self.gui.root.update()
        time.sleep(0.3)
        
        self.board.capture_stones(self.current_player, captured_stones)
        
        quan_count = sum(1 for s in captured_stones if s.type == "Quan")
        dan_count = sum(1 for s in captured_stones if s.type != "Quan")
        if quan_count > 0:
            print(f"Player {self.current_player} ăn được {quan_count} quan và {dan_count} dân!")
            print(f"   Điểm từ nước này: {quan_count * 10 + dan_count * 1}")
        
        self.gui.draw_all_stones()
        self.gui.root.update()
        time.sleep(0.3)
        
        offset = self.get_direction_offset(direction)
        next_empty = (capture_cell + offset) % 12
        
        if self.board.cells[next_empty].is_empty():
            self.check_and_capture(capture_cell, next_empty, direction)
        else:
            self.end_turn()
    
    def animate_hand_move(self, from_pos, to_pos, hand_type):
        """Animation di chuyển bàn tay."""
        steps = 10
        for step in range(steps + 1):
            t = step / steps
            x = from_pos[0] + (to_pos[0] - from_pos[0]) * t
            y = from_pos[1] + (to_pos[1] - from_pos[1]) * t
            self.gui.show_hand(hand_type, x, y)
            self.gui.root.update()
            time.sleep(0.02)
    
    def end_turn(self):
        """Kết thúc lượt chơi."""
        self.gui.hide_hand()
        self.hide_selection()
        self.animation_running = False
        
        if self.check_game_over():
            winner = self.get_winner()
            if self.ai is not None:
                self.print_ai_log()
            self.gui.root.after(1000, lambda: self.gui.show_winner(winner))
        else:
            self.switch_turn()
    
    def print_ai_log(self):
        """In bảng nhật ký AI."""
        log = self.ai.get_log_stats()
        print("\n" + "="*60)
        print("  BẢNG NHẬT KÝ AI - TỐI ƯU TỐC ĐỘ")
        print("="*60)
        print(f"  Độ khó: {self.difficulty.upper()}")
        print(f"  Depth: {self.ai.depth}")
        print(f"  Alpha-Beta: {'Có' if self.ai.use_alpha_beta else 'Không'}")
        print(f"  Tổng số nước: {log['total_moves']}")
        print(f"  Tổng thời gian: {log['total_time']:.3f}s")
        print(f"  Thời gian trung bình: {log['avg_time']:.3f}s/nước")
        print(f"  Nodes đã evaluate: {log['nodes_evaluated']}")
        print(f"  Số lần pruning: {log['pruning_count']}")
        if log['nodes_evaluated'] > 0:
            pruning_rate = (log['pruning_count'] / log['nodes_evaluated']) * 100
            print(f"  Tỷ lệ pruning: {pruning_rate:.2f}%")
        print("="*60 + "\n")
    
    def switch_turn(self):
        """Chuyển lượt chơi."""
        self.current_player = 2 if self.current_player == 1 else 1
        
        if self.current_player == 1:
            my_cells = PLAYER1_CELLS
        else:
            my_cells = PLAYER2_CELLS
        
        has_stones = any(not self.board.cells[i].is_empty() for i in my_cells)
        
        if not has_stones:
            self.borrow_and_distribute()
        else:
            print(f"Lượt chơi: Player {self.current_player}")
        
        if self.current_player == 2 and self.ai is not None:
            self.gui.root.after(500, self.ai_make_move)
    
    def ai_make_move(self):
        """AI tự động chọn nước đi."""
        if self.animation_running or self.current_player != 2:
            return
        
        print("AI đang suy nghĩ...")
        
        best_move = self.ai.get_best_move(self.board)
        
        if best_move:
            cell_id, direction = best_move
            print(f"AI chọn: Ô {cell_id}, Hướng {direction}")
            self.selected_cell = cell_id
            self.start_move(direction)
        else:
            print("AI không tìm thấy nước đi hợp lệ")
    
    def borrow_and_distribute(self):
        """Rải lại 5 dân khi hết dân, vay nếu cần."""
        if self.current_player == 1:
            captured = self.board.player1_captured
            my_cells = PLAYER1_CELLS
        else:
            captured = self.board.player2_captured
            my_cells = PLAYER2_CELLS
        
        dan_to_distribute = []
        for stone in captured[:]:
            if stone.type != "Quan":
                dan_to_distribute.append(stone)
                captured.remove(stone)
                if len(dan_to_distribute) == 5:
                    break
        
        if len(dan_to_distribute) < 5:
            needed = 5 - len(dan_to_distribute)
            if self.current_player == 1:
                self.borrowed_p1 += needed
                opponent_captured = self.board.player2_captured
            else:
                self.borrowed_p2 += needed
                opponent_captured = self.board.player1_captured
            
            for stone in opponent_captured[:]:
                if stone.type != "Quan":
                    dan_to_distribute.append(stone)
                    opponent_captured.remove(stone)
                    if len(dan_to_distribute) == 5:
                        break
        
        for i, cell_id in enumerate(my_cells):
            if i < len(dan_to_distribute):
                stone = dan_to_distribute[i]
                if hasattr(stone, 'captured_position_set'):
                    delattr(stone, 'captured_position_set')
                self.board.drop_stone(cell_id, stone)
        
        self.gui.draw_all_stones()
        self.animation_running = False
        self.selected_cell = None
        self.hand_visible = False
        self.direction_arrows_visible = False
        self.gui.hide_hand()
        self.hide_direction_arrows()
        print(f"Player {self.current_player} rải lại 5 dân - Sẵn sàng chơi tiếp")
    
    def check_game_over(self):
        """Kiểm tra game kết thúc."""
        quan_5_empty = self.board.cells[5].is_empty()
        quan_11_empty = self.board.cells[11].is_empty()
        return quan_5_empty and quan_11_empty
    
    def get_winner(self):
        """Xác định người thắng."""
        print("Hết quan - Bắt đầu hốt tàn cuộc!")
        
        for cell_id in PLAYER1_CELLS:
            stones = self.board.pick_stones(cell_id)
            if stones:
                self.board.capture_stones(1, stones)
                print(f"  P1 hốt {len(stones)} dân từ ô {cell_id}")
        
        for cell_id in PLAYER2_CELLS:
            stones = self.board.pick_stones(cell_id)
            if stones:
                self.board.capture_stones(2, stones)
                print(f"  P2 hốt {len(stones)} dân từ ô {cell_id}")
        
        self.gui.draw_all_stones()
        self.gui.root.update()
        time.sleep(0.5)
        
        score1 = self.board.calculate_score(1) - self.borrowed_p1
        score2 = self.board.calculate_score(2) - self.borrowed_p2
        
        print(f"Điểm P1: {score1} (vay: {self.borrowed_p1})")
        print(f"Điểm P2: {score2} (vay: {self.borrowed_p2})")
        
        return 1 if score1 > score2 else 2
