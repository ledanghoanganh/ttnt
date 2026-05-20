import tkinter as tk
from tkinter import messagebox, ttk
import threading

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

from puzzle_core import random_matrix, Problem
from bfs import bfs as _bfs, bfs_v2 as _bfs_v2
from dfs import dfs as _dfs
from ids import ids as _ids

ALGORITHMS = {
    "BFS": _bfs,
    "BFS_V2": _bfs_v2,
    "DFS": _dfs,
    "IDS": _ids,
}


class StopSearchException(Exception):
    """Ngoại lệ tùy chỉnh được ném ra để dừng ngay tức khắc luồng tìm kiếm dưới nền"""
    pass


class PuzzleModel:
    """Lớp Model xử lý trạng thái dữ liệu và thực thi thuật toán tìm kiếm"""
    GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]] 

    def __init__(self):
        self.reached_count = 0
        self.solution_nodes = []
        self.log_entries = []

    def _log_cb(self, stop_check_fn=None):
        """Hàm callback được gọi mỗi khi sinh ra trạng thái mới để ghi nhận vào Log"""
        def cb(node):
            if stop_check_fn and stop_check_fn():
                raise StopSearchException()
            self.log_entries.append({
                "state": [r[:] for r in node.state],
                "parent": [r[:] for r in node.parent.state] if node.parent else None,
                "action": node.action,
                "path_cost": node.path_cost,
            })
        return cb

    def solve(self, algo_name, start, stop_check_fn=None):
        """Hàm thực thi giải thuật toán dựa trên tên thuật toán được lựa chọn"""
        self.log_entries = []
        self.solution_nodes = []
        fn = ALGORITHMS[algo_name]
        try:
            result, count = fn(Problem(start, self.GOAL), self._log_cb(stop_check_fn))
            self.reached_count = count
            if result and result != "cutoff":
                path = []
                n = result
                while n.parent:
                    path.append(n)
                    n = n.parent
                path.reverse()
                self.solution_nodes = path
                return True
        except StopSearchException:
            self.reached_count = len(self.log_entries)
            return "stopped"
        return False


C = {
    "win":          "#f0f0f0",      # Nền cửa sổ chính
    "panel":        "#ffffff",      # Nền của các khung chứa (Frame)
    "panel_alt":    "#fafafa",      # Nền phụ cho các panel phụ
    "panel_inset":  "#e8e8e8",      # Màu nền các nút bấm/khung thụt vào
    "border":       "#dddddd",      # Màu viền chia cắt
    "text":         "#2d3748",      # Màu chữ chính
    "text_dim":     "#718096",      # Màu chữ phụ
    "text_head":    "#4a5568",      # Màu chữ tiêu đề log
    
    # Màu sắc làm điểm nhấn (Accents)
    "accent":       "#3182ce",      # Màu xanh da trời (Nút Giải, tiêu đề)
    "accent2":      "#4a5568",      # Màu xám thép
    "success":      "#38a169",      # Xanh lá cây (Thông báo thành công)
    "warning":      "#dd6b20",      # Màu cam (Đang xử lý)
    "danger":       "#e53e3e",      # Màu đỏ (Nút Dừng, Trạng thái lỗi)
    
    # Ô số bàn cờ
    "tile_bg":      "#ebf8ff",      # Nền ô số bình thường
    "tile_num":     "#2b6cb0",      # Màu số bình thường
    "tile_empty":   "#edf2f7",      # Nền ô số trống (số 0)
    "tile_border":  "#cbd5e0",      # Viền ô số
    
    # Bảng Log ghi nhận trạng thái
    "log_head":     "#edf2f7",      # Nền thanh tiêu đề Log
    "log_row_a":    "#ffffff",      # Nền dòng Log A
    "log_row_b":    "#f7fafc",      # Nền dòng Log B (đan xen)
    "log_sel":      "#bee3f8",      # Màu dòng log được nhấp chọn
}

FONT = {
    # Bộ phông chữ cấu hình
    "title":        ("Segoe UI", 10, "bold"),
    "label":        ("Segoe UI", 9),
    "small":        ("Segoe UI", 8),
    "btn":          ("Segoe UI", 9, "bold"),
    "tile":         ("Segoe UI", 24, "bold"),
    "path":         ("Consolas", 10, "bold"),
    "mono":         ("Consolas", 9),
}


class ScrollableMovesLabel:
    """Lớp tùy chỉnh bọc xung quanh tk.Text và ttk.Scrollbar để tạo nhãn hiển thị nước đi có thanh cuộn"""
    def __init__(self, parent, font, fg, bg, height=2):
        self.frame = tk.Frame(parent, bg=bg)
        
        self.text_widget = tk.Text(
            self.frame,
            font=font,
            fg=fg,
            bg=bg,
            relief="flat",
            bd=0,
            height=height,
            wrap="word",
            state="disabled",
            highlightthickness=0
        )
        
        self.sb = ttk.Scrollbar(self.frame, orient="vertical", command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=self.sb.set)
        
        self.text_widget.pack(side="left", fill="both", expand=True, padx=(4, 0))
        self.sb.pack(side="right", fill="y")
        
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
        
    def config(self, text=None, **kwargs):
        """Hàm cập nhật nội dung văn bản và tự động cuộn xuống cuối dòng mới nhất"""
        if text is not None:
            self.text_widget.config(state="normal")
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert(tk.END, text)
            self.text_widget.config(state="disabled")
            self.text_widget.see(tk.END)


class PuzzleView:
    """Lớp View chịu trách nhiệm vẽ giao diện Tkinter và liên kết các sự kiện cơ bản"""
    def __init__(self, root, ctrl):
        self.root = root
        self.ctrl = ctrl
        root.title("8-Puzzle Solver")
        root.configure(bg=C["win"])
        root.geometry("1280x760")
        root.minsize(1100, 700)
        self._build()
        self._center()

    def _center(self):
        """Hàm hỗ trợ căn giữa cửa sổ ứng dụng trên màn hình máy tính"""
        self.root.update_idletasks()
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        w,  h  = self.root.winfo_width(),       self.root.winfo_height()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _fr(self, parent, bg=None, **kw):
        return tk.Frame(parent, bg=bg or C["panel"], bd=0, **kw)

    def _lbl(self, parent, text, font=None, fg=None, **kw):
        kw.setdefault("bg", parent.cget("bg"))
        return tk.Label(parent, text=text, font=font or FONT["label"], fg=fg or C["text"], **kw)

    def _btn(self, parent, text, cmd, bg=None, fg="#ffffff", **kw):
        bg = bg or C["accent"]
        b = tk.Button(parent, text=text, command=cmd,
                      font=FONT["btn"], bg=bg, fg=fg,
                      relief="flat", bd=0, padx=12, pady=8,
                      activebackground=bg, activeforeground=fg,
                      cursor="hand2", **kw)
        return b

    def _div(self, parent, orient="h", pad=8):
        """Hàm tạo đường kẻ thanh mảnh phân chia giao diện"""
        if orient == "h":
            tk.Frame(parent, bg=C["border"], height=1).pack(fill="x", padx=pad, pady=6)
        else:
            tk.Frame(parent, bg=C["border"], width=1).pack(fill="y", padx=6, pady=pad, side="left")

    def _navigate(self, row, col):
        """Hàm di chuyển tiêu điểm (focus) giữa các ô nhập 3x3 và tự động bôi đen chữ số cũ"""
        if 0 <= row < 3 and 0 <= col < 3:
            e = self.entries[row][col]
            e.focus_set()
            e.select_range(0, tk.END) 
            e.icursor(tk.END)

    def _build(self):
        body = self._fr(self.root, bg=C["win"])
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self._left(body) # Panel điều hướng trái (Thuật toán, Status, Stats)
        self._right(body) # Panel nhập liệu bên phải (Ma trận 3x3, Các nút hành động)
        self._center_col(body) # Panel chính giữa (Bàn cờ di chuyển, chuỗi nước đi, Bảng log Treeview)


    def _left(self, body):
        """Vẽ cột bảng điều khiển bên trái"""
        left = self._fr(body, width=220)
        left.pack(side="left", fill="y", padx=(0, 8), pady=2)
        left.pack_propagate(False) # Cố định chiều rộng cột
        tk.Frame(left, bg=C["border"], width=1).pack(side="right", fill="y")

        # ── Chọn thuật toán ────────────────────────────────────
        self._section(left, "THUẬT TOÁN")
        
        # Dùng ttk.Combobox chuẩn, tối giản hóa mã nguồn mà vẫn hoạt động cực kỳ mượt mà, đầy đủ tính năng cuộn chuột
        self.combo = ttk.Combobox(left, values=list(ALGORITHMS.keys()), state="readonly", font=FONT["label"])
        self.combo.set(self.ctrl._algo)
        self.combo.pack(fill="x", padx=12, pady=(0, 8))
        self.combo.bind("<<ComboboxSelected>>", lambda e: self.ctrl.select_algo(self.combo.get()))

        # Áp dụng màu sắc đồng bộ cho combobox chuẩn
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=C["tile_bg"], background=C["border"], foreground=C["text"])

        self._div(left)

        # ── Trạng thái hoạt động ──────────────────────────────
        self._section(left, "TRẠNG THÁI")
        self.lbl_status = self._lbl(left, "Đang chờ...", fg=C["accent2"], wraplength=190, justify="left")
        self.lbl_status.pack(padx=14, pady=(2, 6), anchor="w")

        self._div(left)

        # ── Thống kê chỉ số ───────────────────────────────────
        self._section(left, "THỐNG KÊ")
        self.lbl_reached = self._lbl(left, "States duyệt:  —", fg=C["text"], font=FONT["label"])
        self.lbl_reached.pack(padx=14, pady=2, anchor="w")
        self.lbl_steps   = self._lbl(left, "Số bước giải:  —", fg=C["text"], font=FONT["label"])
        self.lbl_steps.pack(padx=14, pady=2, anchor="w")
        self.lbl_algo    = self._lbl(left, "Thuật toán:  —", fg=C["text"], font=FONT["label"], wraplength=190, justify="left")
        self.lbl_algo.pack(padx=14, pady=2, anchor="w")

        self._div(left)

        # ── Hướng dẫn ghi chú ──────────────────────────────────
        self._section(left, "GHI CHÚ")
        notes = ("• 0 = ô trống\n"
                 "• Mỗi số 0-8 xuất hiện 1 lần\n"
                 "• 50% puzzle không giải được\n"
                 "• DFS/IDDFS có thể chậm hơn")
        self._lbl(left, notes, font=FONT["small"], fg=C["text_dim"], justify="left", wraplength=192).pack(padx=14, anchor="w")

    def _section(self, parent, title):
        self._lbl(parent, title, font=FONT["title"], fg=C["accent"]).pack(padx=14, pady=(10, 4), anchor="w")

    def _right(self, body):
        """Vẽ cột bảng nhập liệu bên phải"""
        right = self._fr(body, width=240)
        right.pack(side="right", fill="y", padx=(8, 0), pady=2)
        right.pack_propagate(False)
        tk.Frame(right, bg=C["border"], width=1).pack(side="left", fill="y")

        self._section(right, "ĐẦU VÀO (INPUT)")

        # Lưới ô nhập ma trận đầu vào 3x3
        gf = self._fr(right)
        gf.pack(pady=4)
        self.entries = [[None]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                e = tk.Entry(gf, width=3, font=("Segoe UI", 20, "bold"),
                             justify="center",
                             bg=C["tile_bg"], fg=C["tile_num"],
                             insertbackground=C["accent"],
                             relief="solid", bd=1,
                             highlightthickness=2,
                             highlightbackground=C["border"],
                             highlightcolor=C["accent"])
                e.grid(row=i, column=j, padx=3, pady=3, ipady=4)
                self.entries[i][j] = e

                # Gắn phím điều hướng mũi tên lên/xuống/trái/phải
                e.bind("<Up>",    lambda event, r=i, c=j: self._navigate(r - 1, c))
                e.bind("<Down>",  lambda event, r=i, c=j: self._navigate(r + 1, c))
                e.bind("<Left>",  lambda event, r=i, c=j: self._navigate(r, c - 1))
                e.bind("<Right>", lambda event, r=i, c=j: self._navigate(r, c + 1))

        self._div(right)

        # ── Các nút hành động chính ────────────────────────────
        self.btn_random = self._btn(right, "⟳   Tạo ngẫu nhiên", self.ctrl.generate_random, bg=C["panel_inset"], fg=C["text"])
        self.btn_random.pack(fill="x", padx=14, pady=3)

        self.btn_solve = self._btn(right, "▶   Giải", self.ctrl.start_solving, bg=C["accent"])
        self.btn_solve.pack(fill="x", padx=14, pady=3)

        # Nút Dừng có màu đỏ (C["danger"]) khi thuật toán đang tìm kiếm
        self.btn_stop = self._btn(right, "⏹   Dừng", self.ctrl.stop_solving, bg=C["panel_inset"], fg=C["text_dim"])
        self.btn_stop.pack(fill="x", padx=14, pady=3)
        self.btn_stop.config(state="disabled")

        self.btn_clr = self._btn(right, "✕   Xoá log", self.ctrl.clear_log, bg=C["panel_inset"], fg=C["text_dim"])
        self.btn_clr.pack(fill="x", padx=14, pady=3)

    def _center_col(self, body):
        """Vẽ cột hiển thị chính ở giữa màn hình"""
        center = self._fr(body, bg=C["win"])
        center.pack(side="left", fill="both", expand=True, pady=2)

        # ── Khu vực bàn cờ dịch chuyển trực quan ───────────────
        board_panel = self._fr(center, bg=C["panel"])
        board_panel.pack(fill="x")

        board_wrap = self._fr(board_panel, bg=C["panel"])
        board_wrap.pack(pady=20)

        self._lbl(board_wrap, "TRẠNG THÁI BÀN CỜ", font=FONT["title"], fg=C["accent"]).pack(pady=(0, 12))

        # Khung viền chứa 9 ô số bàn cờ
        tile_outer = tk.Frame(board_wrap, bg=C["tile_border"], bd=0)
        tile_outer.pack()
        self.board_labels = [[None]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                lbl = tk.Label(tile_outer, text="", width=3, height=1, font=FONT["tile"], bg=C["tile_bg"], fg=C["tile_num"], relief="solid", bd=1)
                lbl.grid(row=i, column=j, padx=2, pady=2)
                self.board_labels[i][j] = lbl

        # ── Khung chuỗi nước đi tối ưu cuộn ngang ──────────────
        path_frame = self._fr(center, bg=C["panel_alt"])
        path_frame.pack(fill="x", pady=(6, 0))
        tk.Frame(path_frame, bg=C["border"], height=1).pack(fill="x")
        self._lbl(path_frame, "  CHUỖI NƯỚC ĐI:", font=FONT["small"], fg=C["text_dim"]).pack(anchor="w", pady=(6, 0))
        
        # Gọi đối tượng ScrollableMovesLabel giới hạn tối đa 2 dòng cuộn mượt mà
        self.lbl_moves = ScrollableMovesLabel(path_frame, FONT["path"], C["success"], C["panel_alt"], height=2)
        self.lbl_moves.pack(fill="x", expand=True, padx=10, pady=(2, 8))
        tk.Frame(path_frame, bg=C["border"], height=1).pack(fill="x")

        # ── Bảng nhật ký trạng thái (Log Table) ───────────────
        log_panel = self._fr(center, bg=C["panel"])
        log_panel.pack(fill="both", expand=True, pady=(6, 0))

        log_hdr = self._fr(log_panel, bg=C["log_head"])
        log_hdr.pack(fill="x")
        tk.Frame(log_hdr, bg=C["border"], height=1).pack(fill="x", side="bottom")
        
        self._lbl(log_hdr, "  ◉  LOG — STATES ĐÃ DUYỆT", font=FONT["title"], fg=C["text_head"], bg=C["log_head"]).pack(side="left", pady=7)
        
        # Nhãn hiển thị số lượng bản ghi log thực tế dưới chân thanh tiêu đề
        self.lbl_log_count = self._lbl(log_hdr, "0 entries", font=FONT["small"], fg=C["text_dim"], bg=C["log_head"])
        self.lbl_log_count.pack(side="right", padx=14)

        # Cấu hình thẩm mỹ phong cách hiển thị Treeview phẳng tối giản
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Log.Treeview",
                        background=C["log_row_a"],
                        foreground=C["text"],
                        fieldbackground=C["log_row_a"],
                        rowheight=22,
                        font=FONT["mono"],
                        bordercolor=C["border"],
                        relief="flat")
        style.configure("Log.Treeview.Heading",
                        background=C["log_head"],
                        foreground=C["text_head"],
                        font=("Segoe UI", 9, "bold"),
                        relief="flat", padding=(6, 5))
        style.map("Log.Treeview",
                  background=[("selected", C["log_sel"])],
                  foreground=[("selected", C["text"])])

        cols = ("#", "State (ma trận)", "Parent State", "Action", "Path Cost")
        self.tree = ttk.Treeview(log_panel, columns=cols, show="headings", style="Log.Treeview", height=8)
        widths = [42, 265, 265, 76, 76]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, minwidth=w, anchor="w")

        # Khởi tạo hai thanh cuộn ngang và dọc cho bảng Treeview
        vsb = ttk.Scrollbar(log_panel, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(log_panel, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        hsb.pack(side="bottom", fill="x")

    # CÁC PHƯƠNG THỨC GIAO TIẾP DỮ LIỆU CÔNG KHAI (PUBLIC API) ─────────────────────────────
    def update_board(self, matrix):
        """Cập nhật các số hiển thị trên bàn cờ di động chính dựa trên ma trận trạng thái"""
        for i in range(3):
            for j in range(3):
                v = matrix[i][j]
                if v == 0:
                    self.board_labels[i][j].config(text="", bg=C["tile_empty"])
                else:
                    self.board_labels[i][j].config(text=str(v), bg=C["tile_bg"])

    def get_input_matrix(self):
        """Đọc và phân tích các số nhập từ lưới đầu vào 3x3"""
        matrix = []
        for i in range(3):
            row = []
            for j in range(3):
                val = self.entries[i][j].get().strip()
                if not val.isdigit():
                    return None
                row.append(int(val))
            matrix.append(row)
        return matrix

    def set_input_matrix(self, matrix):
        """Đặt giá trị số vào 3x3 ô nhập đầu vào"""
        for i in range(3):
            for j in range(3):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(matrix[i][j]))

    def append_log(self, entries, offset=0):
        """Đổ dữ liệu states đã duyệt vào Treeview
        
        HIỆU NĂNG TỐI ƯU: Việc render hàng chục ngàn dòng trong Tkinter đồng bộ sẽ làm đóng băng giao diện.
        Chúng tôi giới hạn hiển thị tối đa chỉ 1000 dòng để luôn duy trì tốc độ phản hồi cực mượt mà dưới 0.01 giây,
        trong khi nhãn thông số tổng số bản ghi duyệt vẫn hiển thị chính xác con số thực tế đầy đủ.
        """
        max_display = 1000
        current_tree_size = len(self.tree.get_children())
        
        # Nếu cây đã đạt hoặc vượt quá giới hạn 1000 dòng, chỉ cần cộng dồn số lượng bản ghi hiển thị
        if current_tree_size >= max_display:
            try:
                prev = int(self.lbl_log_count.cget("text").split()[0])
            except Exception:
                prev = 0
            self.lbl_log_count.config(text=f"{prev+len(entries)} entries")
            return

        # Tính toán dung lượng ô còn trống cho phép chèn
        allowed = max_display - current_tree_size
        display_entries = entries[:allowed]
        
        for idx, e in enumerate(display_entries):
            s  = self._mat_str(e["state"])
            p  = self._mat_str(e["parent"]) if e["parent"] else "—"
            a  = (e["action"] or "—").upper()
            c  = str(e["path_cost"])
            tag = "ra" if (offset+idx)%2==0 else "rb"
            self.tree.insert("", "end", values=(offset+idx+1, s, p, a, c), tags=(tag,))
            
        self.tree.tag_configure("ra", background=C["log_row_a"])
        self.tree.tag_configure("rb", background=C["log_row_b"])
        
        try:
            prev = int(self.lbl_log_count.cget("text").split()[0])
        except Exception:
            prev = 0
        self.lbl_log_count.config(text=f"{prev+len(entries)} entries")
        
        # Cuộn thanh xem dọc xuống dòng cuối cùng vừa chèn
        if display_entries:
            self.tree.yview_moveto(1.0)

    def clear_log(self):
        """Xoá sạch sẽ các dòng log khỏi giao diện hiển thị bảng"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.lbl_log_count.config(text="0 entries")

    def set_solving_state(self, is_solving):
        """Chuyển đổi linh hoạt trạng thái điều khiển trên giao diện khi Đang giải (Solving) vs Nhàn rỗi (Idle)"""
        if is_solving:
            # Vô hiệu hóa nút Giải, Tạo mới và Xóa log để tránh chồng chéo luồng xử lý
            self.btn_solve.config(state="disabled", bg=C["panel_inset"], fg=C["text_dim"])
            self.btn_random.config(state="disabled")
            self.btn_clr.config(state="disabled")
            # Kích hoạt nút Dừng nổi bật màu đỏ nguy hiểm
            self.btn_stop.config(state="normal", bg=C["danger"], fg="#ffffff")
            self.btn_stop.bind("<Leave>", lambda e: self.btn_stop.config(bg=C["danger"]))
        else:
            # Khôi phục trạng thái điều khiển bình thường
            self.btn_solve.config(state="normal", bg=C["accent"], fg="#ffffff")
            self.btn_random.config(state="normal")
            self.btn_clr.config(state="normal")
            # Vô hiệu hóa nút Dừng màu xám thụt vào
            self.btn_stop.config(state="disabled", bg=C["panel_inset"], fg=C["text_dim"])
            self.btn_stop.bind("<Leave>", lambda e: self.btn_stop.config(bg=C["panel_inset"]))

    def _mat_str(self, m):
        if m is None: return "—"
        return " | ".join(str(row).replace(" ", "") for row in m)


class PuzzleController:
    """Lớp Controller quản lý luồng chạy, chạy nền thuật toán trên Thread và điều khiển hoạt ảnh (Animation)"""
    def __init__(self, root):
        self.model = PuzzleModel()
        self._algo = list(ALGORITHMS.keys())[0]
        self._log_off = 0
        self._is_stopped = False
        self.view = PuzzleView(root, self)
        self.generate_random()

    def select_algo(self, name):
        """Được gọi khi người dùng lựa chọn thuật toán mới trên thanh Combobox"""
        self._algo = name
        short = name.split("—")[0].strip()
        self.view.lbl_status.config(text=f"Thuật toán: {short}", fg=C["accent2"])
        self.view.lbl_algo.config(text=f"Thuật toán:  {short}")

    def generate_random(self):
        """Khởi tạo trạng thái ngẫu nhiên cho bảng nhập ma trận đầu vào"""
        m = random_matrix()
        self.view.set_input_matrix(m)
        self.view.update_board(m)
        self.view.lbl_moves.config(text="")
        self.view.lbl_status.config(text="Ma trận mới đã tạo", fg=C["accent2"])
        self.view.lbl_reached.config(text="States duyệt:  —")
        self.view.lbl_steps.config(text="Số bước giải:  —")

    def clear_log(self):
        """Xử lý sự kiện làm trống bảng Log nhật ký"""
        self.view.clear_log()
        self._log_off = 0

    def start_solving(self):
        """Bước khởi động tìm kiếm lời giải dựa trên đầu vào ma trận 3x3"""
        mat = self.view.get_input_matrix()
        # Kiểm tra tính hợp lệ của dữ liệu ma trận nhập vào trước khi giải
        if not mat:
            messagebox.showerror("Lỗi", "Vui lòng nhập đủ các số từ 0-8 hợp lệ.")
            return
        if sorted(x for r in mat for x in r) != list(range(9)):
            messagebox.showerror("Lỗi", "Ma trận phải chứa đúng các số 0-8, mỗi số một lần.")
            return

        self._is_stopped = False
        self.view.set_solving_state(True)
        self.view.lbl_moves.config(text="")
        self.view.update_board(mat)
        
        short = self._algo.split("—")[0].strip()
        self.view.lbl_status.config(text=f"Đang giải bằng {short}...\n(Có thể mất vài giây)", fg=C["warning"])

        # THREADING: Chúng ta bắt buộc phải chạy thuật toán tìm kiếm trên một luồng nền phụ (background thread).
        # Nếu chúng ta gọi trực tiếp hàm giải trên luồng chính, giao diện Tkinter sẽ bị đóng băng hoàn toàn, 
        # khiến người dùng không thể nhấn nút "Dừng" được nữa!
        threading.Thread(target=self._thread, args=(mat,), daemon=True).start()

    def stop_solving(self):
        """Sự kiện kích hoạt khi người dùng nhấp chọn nút Dừng để hủy tính toán hoặc dừng hoạt ảnh"""
        self._is_stopped = True

    def _thread(self, mat):
        """Tiến trình phụ thực thi tính toán thuật toán sâu dưới nền"""
        ok = self.model.solve(self._algo, mat, lambda: self._is_stopped)
        
        # TKINTER RULE: Không bao giờ thay đổi các widget giao diện trực tiếp từ một luồng phụ khác.
        # Luôn luôn phải đẩy các lệnh cập nhật giao diện trở lại luồng chính (Main Thread) thông qua root.after()
        self.view.root.after(0, self._done, ok)

    def _done(self, ok):
        """Hàm nhận kết quả trả về từ luồng phụ để kết xuất lên giao diện chính"""
        self.view.lbl_reached.config(text=f"States duyệt:  {self.model.reached_count:,}")
        self.view.append_log(self.model.log_entries, self._log_off)
        self._log_off += len(self.model.log_entries)

        if ok == "stopped":
            # Xử lý trường hợp người dùng chủ động ngắt tiến trình giải giữa chừng
            self.view.lbl_status.config(text="Đã dừng tìm kiếm\ntheo yêu cầu!", fg=C["danger"])
            self.view.set_solving_state(False)
        elif ok:
            # Thành công tìm ra đường đi ngắn nhất
            self.view.lbl_steps.config(text=f"Số bước giải:  {len(self.model.solution_nodes)}")
            short = self._algo.split("—")[0].strip()
            self.view.lbl_algo.config(text=f"Thuật toán:  {short}")
            self.view.lbl_status.config(text="Đã tìm thấy giải pháp!\nĐang hiển thị...", fg=C["success"])
            
            # Kích hoạt bắt đầu chạy hoạt ảnh di chuyển ô số từng bước một
            self._animate(0, "")
        else:
            # Trường hợp thuật toán duyệt hết cây mà không thể giải (vô nghiệm)
            self.view.lbl_status.config(text="Không thể giải!\nTrạng thái này vô nghiệm.", fg=C["danger"])
            self.view.set_solving_state(False)

    def _animate(self, idx, path_str):
        """Hàm đệ quy điều khiển dịch chuyển bàn cờ từng bước một
        
        Tkinter KHÔNG dùng vòng lặp time.sleep() vì nó sẽ khóa chặt Main Thread của GUI.
        Cách tiếp cận chuẩn là dùng phương thức phi chặn `.after(miliseconds, callback)` của Tkinter.
        """
        # Nếu người dùng nhấn nút Dừng trong quá trình chạy hoạt ảnh di chuyển, lập tức hủy hiển thị và thoát
        if self._is_stopped:
            self.view.lbl_status.config(text="Đã dừng hiển thị nước đi!", fg=C["danger"])
            self.view.set_solving_state(False)
            return

        nodes = self.model.solution_nodes
        if idx < len(nodes):
            n = nodes[idx]
            # Di chuyển ô trống trên giao diện thực tế
            self.view.update_board(n.state)
            path_str += (" ➔ " if path_str else "") + n.action.upper()
            self.view.lbl_moves.config(text=path_str)
            
            # Lên lịch hẹn thực hiện bước di chuyển kế tiếp sau 750 mili giây
            self.view.root.after(750, self._animate, idx+1, path_str)
        else:
            # Hoàn thành trọn vẹn tất cả các nước đi tới đích
            self.view.lbl_status.config(text="✓ Hoàn thành!", fg=C["success"])
            self.view.set_solving_state(False)


if __name__ == "__main__":
    root = tk.Tk()
    PuzzleController(root)
    root.mainloop()