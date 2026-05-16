import threading
import random
from tkinter import messagebox
from model import PuzzleModel
from view import PuzzleView

class PuzzleController:
    def __init__(self, root):
        self.model = PuzzleModel()
        self.view = PuzzleView(root, self)
        
        self.view.root.after(100, self.view.draw_pipe)
        
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
        start_matrix = self.view.get_input_matrix()
        if not start_matrix:
            messagebox.showerror("Lỗi", "Vui lòng nhập đủ các số từ 0-8 hợp lệ.")
            return

        self.view.btn_solve.config(state="disabled")
        self.view.btn_random.config(state="disabled")
        self.view.lbl_status.config(text="Đang giải bằng BFS...\n(Có thể mất vài giây)", fg="orange")
        self.view.lbl_moves.config(text="")
        self.view.update_board(start_matrix) # Reset lại board về trạng thái ban đầu

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
            self.view.lbl_status.config(text="Đã tìm thấy giải pháp!\nĐang hiển thị...", fg="green")
            self.model.get_solution(success)
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