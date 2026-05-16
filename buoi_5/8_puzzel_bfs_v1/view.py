import tkinter as tk

class PuzzleView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("8-Puzzle BFS Solver (MVC)")
        self.root.geometry("1100x700")

        self.setup_ui()

    def center_window(self):
        self.root.update_idletasks()

        SCREEN_WIDTH = self.root.winfo_screenwidth()
        SCREEN_HEIGHT = self.root.winfo_screenheight()
        WIN_WIDTH = self.root.winfo_width()
        WIN_HEIGHT = self.root.winfo_height()

        x = (SCREEN_WIDTH - WIN_WIDTH) // 2
        y = (SCREEN_HEIGHT - WIN_HEIGHT) // 2

        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{x}+{y}")

    def setup_ui(self):
        # -- MAIN CONTAINER --
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # -- LEFT FRAME: Thông tin trạng thái --
        self.left_frame = tk.Frame(self.main_frame, width=200, bd=2, relief="groove")
        self.left_frame.pack(side="left", fill="y", padx=5)
        tk.Label(self.left_frame, text="THÔNG TIN (INFO)", font=("Arial", 12, "bold")).pack(pady=10)
        self.lbl_status = tk.Label(self.left_frame, text="Trạng thái: Đang chờ...", fg="blue", wraplength=180)
        self.lbl_status.pack(pady=5)
        self.lbl_reached = tk.Label(self.left_frame, text="Số state đã duyệt:\n0", font=("Arial", 11))
        self.lbl_reached.pack(pady=5)

        # -- RIGHT FRAME: Nhập liệu & Nút chức năng --
        self.right_frame = tk.Frame(self.main_frame, width=200, bd=2, relief="groove")
        self.right_frame.pack(side="right", fill="y", padx=5)
        tk.Label(self.right_frame, text="ĐẦU VÀO (INPUT)", font=("Arial", 12, "bold")).pack(pady=10)
        
        self.entries = [[None for _ in range(3)] for _ in range(3)]
        grid_frame = tk.Frame(self.right_frame)
        grid_frame.pack(pady=10)
        for i in range(3):
            for j in range(3):
                ent = tk.Entry(grid_frame, width=3, font=("Arial", 18, "bold"), justify="center")
                ent.grid(row=i, column=j, padx=2, pady=2)
                self.entries[i][j] = ent

        self.btn_random = tk.Button(self.right_frame, text="Tạo ngẫu nhiên", command=self.controller.generate_random)
        self.btn_random.pack(fill="x", padx=20, pady=5)
        self.btn_solve = tk.Button(self.right_frame, text="Giải bằng BFS", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), command=self.controller.start_solving)
        self.btn_solve.pack(fill="x", padx=20, pady=5)

        # -- CENTER FRAME: Bàn cờ & Lịch sử bước đi --
        self.center_frame = tk.Frame(self.main_frame)
        self.center_frame.pack(side="left", fill="both", expand=True, padx=10)

        # Center Top: Bàn cờ 3x3
        self.center_top = tk.Frame(self.center_frame)
        self.center_top.pack(side="top", fill="both", expand=True)
        self.board_labels = [[None for _ in range(3)] for _ in range(3)]
        board_container = tk.Frame(self.center_top, bg="black", bd=2)
        board_container.place(relx=0.5, rely=0.5, anchor="center") # Căn giữa
        for i in range(3):
            for j in range(3):
                lbl = tk.Label(board_container, text="", width=4, height=2, font=("Arial", 24, "bold"), bg="white", borderwidth=1, relief="solid")
                lbl.grid(row=i, column=j, padx=2, pady=2)
                self.board_labels[i][j] = lbl

        # Center Bottom: Chuỗi bước đi
        self.center_bottom = tk.Frame(self.center_frame, height=100, bd=2, relief="sunken")
        self.center_bottom.pack(side="bottom", fill="x", pady=10)
        tk.Label(self.center_bottom, text="Chuỗi nước đi (Solution Path):", font=("Arial", 10, "bold")).pack(anchor="w")
        self.lbl_moves = tk.Label(self.center_bottom, text="", font=("Arial", 12), fg="red", wraplength=400, justify="left")
        self.lbl_moves.pack(anchor="w", padx=10, pady=5)

        self.center_window()
        

    def draw_pipe(self):
        self.root.update_idletasks()
        win_width = self.root.winfo_width()
        pipe_length = int(win_width * 0.7)
        x1 = (win_width - pipe_length) // 2
        x2 = x1 + pipe_length

        self.canvas.delete("all") # Xóa cũ vẽ lại
        self.canvas.create_line(x1, 20, x2, 20, width=4, fill="#3498db")
        self.canvas.create_line(x1, 80, x2, 80, width=4, fill="#3498db")
        self.canvas.create_text(x1 - 60, 50, text="Vào ->", font=("Arial", 12, "bold"), fill="green")
        self.canvas.create_text(x2 + 60, 50, text="-> Ra", font=("Arial", 12, "bold"), fill="red")

    def update_board(self, matrix):
        for i in range(3):
            for j in range(3):
                val = matrix[i][j]
                if val == 0:
                    self.board_labels[i][j].config(text="", bg="#ecf0f1")
                else:
                    self.board_labels[i][j].config(text=str(val), bg="white")

    def get_input_matrix(self):
        matrix = []
        for i in range(3):
            row = []
            for j in range(3):
                val = self.entries[i][j].get()
                if not val.isdigit():
                    return None
                row.append(int(val))
            matrix.append(row)
        return matrix

    def set_input_matrix(self, matrix):
        for i in range(3):
            for j in range(3):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(matrix[i][j]))
