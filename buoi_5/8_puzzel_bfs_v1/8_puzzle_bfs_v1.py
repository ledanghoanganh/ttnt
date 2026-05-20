import tkinter as tk
from tkinter import messagebox
import random
import copy
from collections import deque
import threading


try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


class Node:
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def get_index(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i, j)
        return None

class PuzzleModel:
    def __init__(self):
        self.goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.reached_count = 0
        self.solution_nodes = []

    def tuple_matrix(self, matrix):
        return tuple(tuple(row) for row in matrix)

    def get_actions(self, i, j):
        actions = []
        if i > 0: actions.append("up")
        if i < 2: actions.append("down")
        if j > 0: actions.append("left")
        if j < 2: actions.append("right")
        return actions

    def expand(self, node):
        i, j = node.get_index()
        actions = self.get_actions(i, j)
        moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        children = []
        for a in actions:
            matrix = copy.deepcopy(node.state)
            di, dj = moves[a]
            matrix[i][j], matrix[i + di][j + dj] = matrix[i + di][j + dj], matrix[i][j]
            child = Node(matrix, node, a, node.path_cost + 1)
            children.append(child)
        return children

    def eight_puzzel(self, start_matrix):
        node = Node(start_matrix, None, None, 0)
        frontier = deque(); frontier.append(node)
        frontier_states = set(); frontier_states.add(self.tuple_matrix(node.state))
        reached = set()

        while frontier:
            node = frontier.popleft() 
            if node.state == self.goal: return node
            
            reached.add(self.tuple_matrix(node.state))
            self.reached_count = len(reached)

            for child in self.expand(node):
                c = self.tuple_matrix(child.state)
                if c not in reached and c not in frontier_states:
                    frontier.append(child)    
                    frontier_states.add(c)    

        return False
    
    def solution(self, node):
        res = []
        while node.parent is not None:
            res.append(node)
            node = node.parent
        res.reverse()
        self.solution_nodes = res
        

class PuzzleView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("8-Puzzle BFS Solver Version 1")
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
        tk.Label(self.left_frame, text="THÔNG TIN", font=("Arial", 12, "bold")).pack(pady=10)
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
                entry = tk.Entry(grid_frame, width=3, font=("Arial", 18, "bold"), justify="center")
                entry.grid(row=i, column=j, padx=2, pady=2)
                self.entries[i][j] = entry

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
        self.lbl_moves = tk.Label(self.center_bottom, text="", font=("Arial", 12), fg="red", wraplength=700, justify="left")
        self.lbl_moves.pack(anchor="w", padx=10, pady=5)

        self.center_window()

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


class PuzzleController:
    def __init__(self, root):
        self.model = PuzzleModel()
        self.view = PuzzleView(root, self)
        
        self.generate_random()

    def generate_random(self):
        nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        matrix = [[0 for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                num = random.choice(nums)
                matrix[i][j] = num
                nums.remove(num)
        
        self.view.set_input_matrix(matrix)
        self.view.update_board(matrix)
        self.view.lbl_moves.config(text="")
        self.view.lbl_status.config(text="Đã tạo ma trận mới", fg="blue")

    def start_solving(self):
        self.model.reached_count = 0
        start_matrix = self.view.get_input_matrix()
        if not start_matrix:
            messagebox.showerror("Lỗi", "Vui lòng nhập đủ các số từ 0-8 hợp lệ.")
            return

        self.view.btn_solve.config(state="disabled")
        self.view.btn_random.config(state="disabled")
        self.view.lbl_status.config(text="Đang giải bằng BFS...\n(Có thể mất vài giây)", fg="orange")
        self.view.lbl_moves.config(text="")
        self.view.update_board(start_matrix)

        # Chạy BFS trên luồng riêng để không treo UI
        thread = threading.Thread(target=self.run_bfs_thread, args=(start_matrix,))
        thread.start()

    def run_bfs_thread(self, start_matrix):
        success = self.model.eight_puzzel(start_matrix)
        # Sử dụng after để gọi lại hàm cập nhật UI ở Main Thread
        self.view.root.after(0, self.on_solve_complete, success)

    def on_solve_complete(self, success):
        self.view.lbl_reached.config(text=f"Số state đã duyệt:\n{self.model.reached_count}")
        
        if success:
            self.model.solution(success)
            self.view.lbl_status.config(text="Đã tìm thấy giải pháp!\nĐang hiển thị...", fg="green")
            self.animate_solution(0, "")
        else:
            self.view.lbl_status.config(text="Thất bại!\nTrạng thái này không thể giải.", fg="red")
            self.view.btn_solve.config(state="normal")
            self.view.btn_random.config(state="normal")

    def animate_solution(self, step_index, current_moves_str):
        if step_index < len(self.model.solution_nodes):
            node = self.model.solution_nodes[step_index]
            
            # Cập nhật bàn cờ
            self.view.update_board(node.state)
            
            # Cập nhật chuỗi bước đi
            if current_moves_str:
                current_moves_str += " ➔ " + node.action.upper()
            else:
                current_moves_str = node.action.upper()
            
            self.view.lbl_moves.config(text=current_moves_str)
            
            # Đợi 800ms rồi chạy bước tiếp theo
            self.view.root.after(800, self.animate_solution, step_index + 1, current_moves_str)
        else:
            self.view.lbl_status.config(text="Hoàn thành!", fg="green")
            self.view.btn_solve.config(state="normal")
            self.view.btn_random.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleController(root)
    root.mainloop()