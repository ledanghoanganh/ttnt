import tkinter as tk
from tkinter import messagebox, ttk
import threading
import copy

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
    pass

class PuzzleModel:
    GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def __init__(self):
        self.reached_count = 0
        self.solution_nodes = []
        self.log_entries = []

    def _log_cb(self, stop_check_fn=None):
        def cb(node):
            if stop_check_fn and stop_check_fn():
                raise StopSearchException()
            self.log_entries.append({
                "state": copy.deepcopy(node.state),
                "parent": copy.deepcopy(node.parent.state) if node.parent else None,
                "action": node.action,
                "path_cost": node.path_cost,
            })
        return cb

    def solve(self, algo_name, start, stop_check_fn=None):
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
    "win":          "#f0f0f0",
    "panel":        "#ffffff",
    "panel_alt":    "#fafafa",
    "panel_inset":  "#e8e8e8",
    "border":       "#dddddd",
    "text":         "#2d3748",
    "text_dim":     "#718096",
    "text_head":    "#4a5568",

    "accent":       "#3182ce",
    "accent2":      "#4a5568",
    "success":      "#38a169",
    "warning":      "#dd6b20",
    "danger":       "#e53e3e",

    "tile_bg":      "#ebf8ff",
    "tile_num":     "#2b6cb0",
    "tile_empty":   "#edf2f7",
    "tile_border":  "#cbd5e0",

    "log_head":     "#edf2f7",
    "log_row_a":    "#ffffff",
    "log_row_b":    "#f7fafc",
    "log_sel":      "#bee3f8",
}

FONT = {
    "title":        ("Segoe UI", 10, "bold"),
    "label":        ("Segoe UI", 9),
    "small":        ("Segoe UI", 8),
    "btn":          ("Segoe UI", 9, "bold"),
    "tile":         ("Segoe UI", 24, "bold"),
    "path":         ("Consolas", 10, "bold"),
    "mono":         ("Consolas", 9),
}

class ScrollableMovesLabel:
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
        if text is not None:
            self.text_widget.config(state="normal")
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert(tk.END, text)
            self.text_widget.config(state="disabled")
            self.text_widget.see(tk.END)

class PuzzleView:
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
        if orient == "h":
            tk.Frame(parent, bg=C["border"], height=1).pack(fill="x", padx=pad, pady=6)

        else:
            tk.Frame(parent, bg=C["border"], width=1).pack(fill="y", padx=6, pady=pad, side="left")

    def _navigate(self, row, col):
        if 0 <= row < 3 and 0 <= col < 3:
            e = self.entries[row][col]
            e.focus_set()
            e.select_range(0, tk.END)
            e.icursor(tk.END)

    def _build(self):
        body = self._fr(self.root, bg=C["win"])
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._left(body)
        self._right(body)
        self._center_col(body)

    def _left(self, body):
        left = self._fr(body, width=220)
        left.pack(side="left", fill="y", padx=(0, 8), pady=2)
        left.pack_propagate(False)

        tk.Frame(left, bg=C["border"], width=1).pack(side="right", fill="y")
        self._section(left, "THUẬT TOÁN")
        self.combo = ttk.Combobox(left, values=list(ALGORITHMS.keys()), state="readonly", font=FONT["label"])
        self.combo.set(self.ctrl._algo)
        self.combo.pack(fill="x", padx=12, pady=(0, 8))
        self.combo.bind("<<ComboboxSelected>>", lambda e: self.ctrl.select_algo(self.combo.get()))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=C["tile_bg"], background=C["border"], foreground=C["text"])
        self._div(left)
        self._section(left, "TRẠNG THÁI")

        self.lbl_status = self._lbl(left, "Đang chờ...", fg=C["accent2"], wraplength=190, justify="left")
        self.lbl_status.pack(padx=14, pady=(2, 6), anchor="w")

        self._div(left)
        self._section(left, "THỐNG KÊ")

        self.lbl_reached = self._lbl(left, "States duyệt:  —", fg=C["text"], font=FONT["label"])
        self.lbl_reached.pack(padx=14, pady=2, anchor="w")

        self.lbl_steps   = self._lbl(left, "Số bước giải:  —", fg=C["text"], font=FONT["label"])
        self.lbl_steps.pack(padx=14, pady=2, anchor="w")

        self.lbl_algo    = self._lbl(left, "Thuật toán:  —", fg=C["text"], font=FONT["label"], wraplength=190, justify="left")
        self.lbl_algo.pack(padx=14, pady=2, anchor="w")

        self._div(left)
        self._section(left, "GHI CHÚ")

        notes = ("• 0 = ô trống\n"
                 "• Mỗi số 0-8 xuất hiện 1 lần\n"
                 "• 50% puzzle không giải được\n"
                 "• DFS/IDDFS có thể chậm hơn")

        self._lbl(left, notes, font=FONT["small"], fg=C["text_dim"], justify="left", wraplength=192).pack(padx=14, anchor="w")

    def _section(self, parent, title):
        self._lbl(parent, title, font=FONT["title"], fg=C["accent"]).pack(padx=14, pady=(10, 4), anchor="w")

    def _right(self, body):
        right = self._fr(body, width=240)
        right.pack(side="right", fill="y", padx=(8, 0), pady=2)
        right.pack_propagate(False)

        tk.Frame(right, bg=C["border"], width=1).pack(side="left", fill="y")
        
        self._section(right, "ĐẦU VÀO (INPUT)")
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

                e.bind("<Up>",    lambda event, r=i, c=j: self._navigate(r - 1, c))
                e.bind("<Down>",  lambda event, r=i, c=j: self._navigate(r + 1, c))
                e.bind("<Left>",  lambda event, r=i, c=j: self._navigate(r, c - 1))
                e.bind("<Right>", lambda event, r=i, c=j: self._navigate(r, c + 1))

        self._div(right)

        self.btn_random = self._btn(right, "⟳   Tạo ngẫu nhiên", self.ctrl.generate_random, bg=C["panel_inset"], fg=C["text"])
        self.btn_random.pack(fill="x", padx=14, pady=3)
        self.btn_solve = self._btn(right, "▶   Giải", self.ctrl.start_solving, bg=C["accent"])
        self.btn_solve.pack(fill="x", padx=14, pady=3)
        self.btn_stop = self._btn(right, "⏹   Dừng", self.ctrl.stop_solving, bg=C["panel_inset"], fg=C["text_dim"])
        self.btn_stop.pack(fill="x", padx=14, pady=3)
        self.btn_stop.config(state="disabled")
        self.btn_clr = self._btn(right, "✕   Xoá log", self.ctrl.clear_log, bg=C["panel_inset"], fg=C["text_dim"])
        self.btn_clr.pack(fill="x", padx=14, pady=3)

    def _center_col(self, body):
        center = self._fr(body, bg=C["win"])
        center.pack(side="left", fill="both", expand=True, pady=2)

        board_panel = self._fr(center, bg=C["panel"])
        board_panel.pack(fill="x")
        board_wrap = self._fr(board_panel, bg=C["panel"])
        board_wrap.pack(pady=20)

        self._lbl(board_wrap, "TRẠNG THÁI BÀN CỜ", font=FONT["title"], fg=C["accent"]).pack(pady=(0, 12))

        tile_outer = tk.Frame(board_wrap, bg=C["tile_border"], bd=0)
        tile_outer.pack()

        self.board_labels = [[None]*3 for _ in range(3)]

        for i in range(3):
            for j in range(3):
                lbl = tk.Label(tile_outer, text="", width=3, height=1, font=FONT["tile"], bg=C["tile_bg"], fg=C["tile_num"], relief="solid", bd=1)
                lbl.grid(row=i, column=j, padx=2, pady=2)
                self.board_labels[i][j] = lbl

        path_frame = self._fr(center, bg=C["panel_alt"])
        path_frame.pack(fill="x", pady=(6, 0))

        tk.Frame(path_frame, bg=C["border"], height=1).pack(fill="x")

        self._lbl(path_frame, "  CHUỖI NƯỚC ĐI:", font=FONT["small"], fg=C["text_dim"]).pack(anchor="w", pady=(6, 0))
        self.lbl_moves = ScrollableMovesLabel(path_frame, FONT["path"], C["success"], C["panel_alt"], height=2)
        self.lbl_moves.pack(fill="x", expand=True, padx=10, pady=(2, 8))

        tk.Frame(path_frame, bg=C["border"], height=1).pack(fill="x")

        log_panel = self._fr(center, bg=C["panel"])
        log_panel.pack(fill="both", expand=True, pady=(6, 0))
        log_hdr = self._fr(log_panel, bg=C["log_head"])
        log_hdr.pack(fill="x")

        tk.Frame(log_hdr, bg=C["border"], height=1).pack(fill="x", side="bottom")

        self._lbl(log_hdr, "  ◉  LOG — STATES ĐÃ DUYỆT", font=FONT["title"], fg=C["text_head"], bg=C["log_head"]).pack(side="left", pady=7)
        self.lbl_log_count = self._lbl(log_hdr, "0 entries", font=FONT["small"], fg=C["text_dim"], bg=C["log_head"])
        self.lbl_log_count.pack(side="right", padx=14)

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

        vsb = ttk.Scrollbar(log_panel, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(log_panel, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        hsb.pack(side="bottom", fill="x")

    def update_board(self, matrix):
        for i in range(3):
            for j in range(3):
                v = matrix[i][j]

                if v == 0:
                    self.board_labels[i][j].config(text="", bg=C["tile_empty"])
                else:
                    self.board_labels[i][j].config(text=str(v), bg=C["tile_bg"])

    def get_input_matrix(self):
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
        for i in range(3):
            for j in range(3):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(matrix[i][j]))

    def append_log(self, entries, offset=0):
        max_display = 1000
        current_tree_size = len(self.tree.get_children())
        if current_tree_size >= max_display:
            try:
                prev = int(self.lbl_log_count.cget("text").split()[0])
            except Exception:
                prev = 0
            self.lbl_log_count.config(text=f"{prev+len(entries)} entries")
            return

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

        if display_entries:
            self.tree.yview_moveto(1.0)

    def clear_log(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.lbl_log_count.config(text="0 entries")

    def set_solving_state(self, is_solving):
        if is_solving:
            self.btn_solve.config(state="disabled", bg=C["panel_inset"], fg=C["text_dim"])
            self.btn_random.config(state="disabled")
            self.btn_clr.config(state="disabled")
            self.btn_stop.config(state="normal", bg=C["danger"], fg="#ffffff")
            self.btn_stop.bind("<Leave>", lambda e: self.btn_stop.config(bg=C["danger"]))
        else:
            self.btn_solve.config(state="normal", bg=C["accent"], fg="#ffffff")
            self.btn_random.config(state="normal")
            self.btn_clr.config(state="normal")
            self.btn_stop.config(state="disabled", bg=C["panel_inset"], fg=C["text_dim"])
            self.btn_stop.bind("<Leave>", lambda e: self.btn_stop.config(bg=C["panel_inset"]))

    def _mat_str(self, m):
        if m is None: return "—"
        return " | ".join(str(row).replace(" ", "") for row in m)

class PuzzleController:
    def __init__(self, root):
        self.model = PuzzleModel()
        self._algo = list(ALGORITHMS.keys())[0]
        self._log_off = 0
        self._is_stopped = False
        self.view = PuzzleView(root, self)
        self.generate_random()

    def select_algo(self, name):
        self._algo = name
        short = name.split("—")[0].strip()
        self.view.lbl_status.config(text=f"Thuật toán: {short}", fg=C["accent2"])
        self.view.lbl_algo.config(text=f"Thuật toán:  {short}")

    def generate_random(self):
        m = random_matrix()
        self.view.set_input_matrix(m)
        self.view.update_board(m)
        self.view.lbl_moves.config(text="")
        self.view.lbl_status.config(text="Ma trận mới đã tạo", fg=C["accent2"])
        self.view.lbl_reached.config(text="States duyệt:  —")
        self.view.lbl_steps.config(text="Số bước giải:  —")

    def clear_log(self):
        self.view.clear_log()
        self._log_off = 0

    def start_solving(self):
        mat = self.view.get_input_matrix()
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
        threading.Thread(target=self._thread, args=(mat,), daemon=True).start()

    def stop_solving(self):
        self._is_stopped = True

    def _thread(self, mat):
        ok = self.model.solve(self._algo, mat, lambda: self._is_stopped)
        self.view.root.after(0, self._done, ok)

    def _done(self, ok):
        self.view.lbl_reached.config(text=f"States duyệt:  {self.model.reached_count:,}")
        self.view.append_log(self.model.log_entries, self._log_off)
        self._log_off += len(self.model.log_entries)

        if ok == "stopped":
            self.view.lbl_status.config(text="Đã dừng tìm kiếm\ntheo yêu cầu!", fg=C["danger"])
            self.view.set_solving_state(False)
        elif ok:
            self.view.lbl_steps.config(text=f"Số bước giải:  {len(self.model.solution_nodes)}")
            short = self._algo.split("—")[0].strip()
            self.view.lbl_algo.config(text=f"Thuật toán:  {short}")
            self.view.lbl_status.config(text="Đã tìm thấy giải pháp!\nĐang hiển thị...", fg=C["success"])
            self._animate(0, "")
        else:
            self.view.lbl_status.config(text="Không thể giải!\nTrạng thái này vô nghiệm.", fg=C["danger"])
            self.view.set_solving_state(False)

    def _animate(self, idx, path_str):
        if self._is_stopped:
            self.view.lbl_status.config(text="Đã dừng hiển thị nước đi!", fg=C["danger"])
            self.view.set_solving_state(False)
            return

        nodes = self.model.solution_nodes

        if idx < len(nodes):
            n = nodes[idx]
            self.view.update_board(n.state)
            path_str += (" ➔ " if path_str else "") + n.action.upper()
            self.view.lbl_moves.config(text=path_str)
            self.view.root.after(750, self._animate, idx+1, path_str)
        else:
            self.view.lbl_status.config(text="✓ Hoàn thành!", fg=C["success"])
            self.view.set_solving_state(False)

if __name__ == "__main__":
    root = tk.Tk()
    PuzzleController(root)
    root.mainloop()
