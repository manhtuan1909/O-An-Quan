import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

class GameUI:
    def __init__(self, root, board_image_path, stone_image_path):
        self.root = root
        self.board_image_path = board_image_path
        self.stone_image_path = stone_image_path
        
        # Tạo canvas
        self.canvas = tk.Canvas(root, width=1200, height=700)
        self.canvas.pack()
        
        # Tọa độ các ô
        self.cell_positions = [
            (350, 330), (470, 330), (580, 330), (690, 330), (810, 330),  # 0-4: ô dân trên
            (930, 410),  # 5: quan phải
            (810, 470), (690, 470), (580, 470), (470, 470), (360, 470),  # 6-10: ô dân dưới
            (240, 410)   # 11: quan trái
        ]
        
        # Load ảnh
        self.load_images()
        
        # Biến để lưu trữ callback khi click
        self.click_callback = None
    
    def load_images(self):
        """Load ảnh bàn cờ và tạo ảnh quân cờ"""
        # Load ảnh nền bàn cờ
        self.board_bg = Image.open(self.board_image_path).convert("RGBA")
        self.board_bg = self.board_bg.resize((1200, 800))
        self.board_photo = ImageTk.PhotoImage(self.board_bg)
        
        # Tạo ảnh mũi tên
        self.create_arrow_images()
        
        # Tạo ảnh quân cờ
        self.create_stone_images()
    
    def create_arrow_images(self):
        """Tạo ảnh mũi tên trái/phải"""
        left_arrow = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
        draw = ImageDraw.Draw(left_arrow)
        draw.polygon([(30, 10), (10, 20), (30, 30)], fill=(0, 100, 200, 255))
        self.left_arrow_img = ImageTk.PhotoImage(left_arrow)
        
        right_arrow = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
        draw = ImageDraw.Draw(right_arrow)
        draw.polygon([(10, 10), (30, 20), (10, 30)], fill=(0, 100, 200, 255))
        self.right_arrow_img = ImageTk.PhotoImage(right_arrow)
    
    def create_stone_images(self):
        """Tạo ảnh quân cờ với số lượng chính xác"""
        self.stone_images = {}
        self.quan_images = {}
        
        for count in range(1, 11):
            img = self.create_stone_group(count, stone_size=20, is_quan=False)
            self.stone_images[count] = ImageTk.PhotoImage(img)
        
        for count in range(1, 2):
            img = self.create_stone_group(count, stone_size=50, is_quan=True)
            self.quan_images[count] = ImageTk.PhotoImage(img)
    
    def create_stone_group(self, count, stone_size=20, is_quan=False):
        """Tạo nhóm quân cờ để kiểm soát cho đếm số lượng quân"""
        try:
            if is_quan:
                img_size = (80, 80)
                img = Image.new("RGBA", img_size, (0, 0, 0, 0))
                stone_img = Image.open(self.stone_image_path).convert("RGBA")
                stone_img = stone_img.resize((60, 60))
                center_x = (img_size[0] - stone_img.width) // 2
                center_y = (img_size[1] - stone_img.height) // 2
                img.paste(stone_img, (center_x, center_y), stone_img)
            else:
                img_size = (60, 60)
                img = Image.new("RGBA", img_size, (0, 0, 0, 0))
                stone_img = Image.open(self.stone_image_path).convert("RGBA")
                stone_img = stone_img.resize((stone_size, stone_size))
                
                if count == 1:
                    positions = [(30, 30)]
                elif count == 2:
                    positions = [(20, 30), (40, 30)]
                elif count == 3:
                    positions = [(30, 20), (20, 40), (40, 40)]
                elif count == 4:
                    positions = [(20, 20), (40, 20), (20, 40), (40, 40)]
                else:
                    positions = [(30, 30), (15, 30), (45, 30), (30, 15), (30, 45)]
                    extra_positions = [(15, 15), (45, 15), (15, 45), (45, 45)]
                    for i in range(min(count - 5, 4)):
                        positions.append(extra_positions[i])
                
                for pos in positions[:count]:
                    x, y = pos
                    paste_x = x - stone_img.width // 2
                    paste_y = y - stone_img.height // 2
                    img.paste(stone_img, (paste_x, paste_y), stone_img)
                    
        except Exception as e:
            print(f"Lỗi load ảnh: {e}")
            return self.create_fallback_stone_group(count, stone_size, is_quan)
        
        return img

    def draw_board(self, board_state, selected_cell=None, direction=None):
        """Vẽ bàn cờ với trạng thái hiện tại số quân cờ hiện tại"""
        self.canvas.delete("all")
        
        # Vẽ nền bàn cờ
        self.canvas.create_image(0, 0, image=self.board_photo, anchor='nw')
        
        # Vẽ các quân cờ và số đếm
        for i, pos in enumerate(self.cell_positions):
            x, y = pos
            count = board_state[i]
            
            if count > 0:
                if i in [5, 11]:  # Ô quan
                    if count in self.quan_images:
                        self.canvas.create_image(x, y, image=self.quan_images[count], anchor='center')
                else:  # Ô dân
                    if count <= 10 and count in self.stone_images:
                        self.canvas.create_image(x, y, image=self.stone_images[count], anchor='center')
                    elif count > 10:
                        self.canvas.create_image(x, y, image=self.stone_images[10], anchor='center')
            
            # Vẽ số đếm
            self.canvas.create_text(x + 25, y - 25, text=str(count), 
                                  font=("Arial", 12, "bold"), fill="red")
