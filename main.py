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
from buoi_05.test_bfs_v1 import bfs_v1 as _bfs
from buoi_05.test_bfs_v2 import bfs_v2 as _bfs_v2
from buoi_06.test_dfs_v2 import dfs_v2 as _dfs
from buoi_06.test_ids import ids as _ids
from buoi_07.ucs import ucs as _ucs
from buoi_07.gs import gs as _gs
from buoi_08.a_star import a_star as _a_star
from buoi_08.ida_star import ida_star as _ida_star
from buoi_09.simple_hill_climbing import simple_hill_climbing as _simple_hill_climbing
from buoi_09.steepest_ascent_hill_climbing import steepest_ascent_hill_climbing as _steepest_ascent_hill_climbing
from buoi_10.stochastic_hill_climbing import stochastic_hill_climbing as _stochastic_hill_climbing
from buoi_10.random_restart_hill_climbing import random_restart_hill_climbing as _random_restart_hill_climbing
from buoi_10.local_beam_search import local_beam_search as _local_beam_search
from buoi_11.simulated_annealing import simulated_annealing as _simulated_annealing

from buoi_11.complex_a_star_missing_input import complex_a_star_missing_input as _complex_a_star_missing_input
from buoi_11.complex_a_star_missing_goal import complex_a_star_missing_goal as _complex_a_star_missing_goal
from buoi_11.complex_a_star_missing_both import complex_a_star_missing_both as _complex_a_star_missing_both

from buoi_12.backtracking_search import backtracking_search as _backtracking_search
from buoi_12.and_or_search import and_or_search as _and_or_search
from buoi_13.ac_3 import ac_3 as _ac_3
from buoi_13.min_conflict import min_conflict as _min_conflict

ALGORITHMS = {
    "BFS": {"func": _bfs, "type": "normal"},
    "BFS_V2": {"func": _bfs_v2, "type": "normal"},
    "DFS": {"func": _dfs, "type": "normal"},
    "IDS": {"func": _ids, "type": "normal"},
    "UCS": {"func": _ucs, "type": "normal"},
    "GS": {"func": _gs, "type": "normal"},
    "A-Star": {"func": _a_star, "type": "normal"},
    "IDA-Star": {"func": _ida_star, "type": "normal"},
    "Simple Hill-Climbing": {"func": _simple_hill_climbing, "type": "normal"},
    "Steepest Ascent Hill-Climbing": {"func": _steepest_ascent_hill_climbing, "type": "normal"},
    "Stochastic Hill-Climbing": {"func": _stochastic_hill_climbing, "type": "normal"},
    "Random Restart Hill-Climbing": {"func": _random_restart_hill_climbing, "type": "normal"},
    "Local Beam Search": {"func": _local_beam_search, "type": "normal"},
    "Simulated Annealing": {"func": _simulated_annealing, "type": "normal"},

    "Complex A* (Khuyết Input)": {"func": _complex_a_star_missing_input, "type": "missing_input"},
    "Complex A* (Khuyết Goal)": {"func": _complex_a_star_missing_goal, "type": "missing_goal"},
    "Complex A* (Khuyết Input & Goal)": {"func": _complex_a_star_missing_both, "type": "missing_both"},
    
    "Backtracking Search": {"func": _backtracking_search, "type": "normal"},
    "AND-OR Search": {"func": _and_or_search, "type": "normal"},
    "AC-3": {"func": _ac_3, "type": "normal"},
    "Min-Conflicts": {"func": _min_conflict, "type": "normal"},
}

class StopSearchException(Exception):
    pass

class PuzzleModel:
    def __init__(self):
        self.reached_count = 0
        self.solution_nodes = []
        self.log_entries = []

    def _log_cb(self, stop_check_fn=None):
        def cb(node):
            if stop_check_fn and stop_check_fn():
                raise StopSearchException()
            st = getattr(node, 'belief_state', node.state)
            pt = None
            if node.parent:
                pt = getattr(node.parent, 'belief_state', node.parent.state)
            self.log_entries.append({
                "state": copy.deepcopy(st),
                "parent": copy.deepcopy(pt),
                "action": node.action,
                "path_cost": node.path_cost,
                "g_cost": getattr(node, 'g_cost', 0),
                "h_cost": getattr(node, 'h_cost', 0)
            })
        return cb

    def _get_path(self, n):
        path = []
        while n:
            path.append(n)
            n = n.parent
        path.reverse()
        return path

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
            self.frame, font=font, fg=fg, bg=bg, relief="flat", bd=0, height=height, wrap="word", state="disabled", highlightthickness=0
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
        b = tk.Button(parent, text=text, command=cmd, font=FONT["btn"], bg=bg, fg=fg, relief="flat", bd=0, padx=12, pady=8, activebackground=bg, activeforeground=fg, cursor="hand2", **kw)
        return b

    def _div(self, parent, orient="h", pad=8):
        if orient == "h":
            tk.Frame(parent, bg=C["border"], height=1).pack(fill="x", padx=pad, pady=6)
        else:
            tk.Frame(parent, bg=C["border"], width=1).pack(fill="y", padx=6, pady=pad, side="left")

    def _navigate(self, row, col, entries):
        if 0 <= row < 3 and 0 <= col < 3:
            e = entries[row][col]
            e.focus_set()
            e.select_range(0, tk.END)
            e.icursor(tk.END)

    def _build(self):
        body = self._fr(self.root, bg=C["win"])
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._left(body)
        self._right(body)
        self._center_col(body)
        self._on_algo_change()

    def _left(self, body):
        left = self._fr(body, width=220)
        left.pack(side="left", fill="y", padx=(0, 8), pady=2)
        left.pack_propagate(False)

        tk.Frame(left, bg=C["border"], width=1).pack(side="right", fill="y")
        self._section(left, "THUẬT TOÁN")
        self.combo = ttk.Combobox(left, values=list(ALGORITHMS.keys()), state="readonly", font=FONT["label"])
        self.combo.set(self.ctrl._algo)
        self.combo.pack(fill="x", padx=12, pady=(0, 8))
        self.combo.bind("<<ComboboxSelected>>", self._on_algo_change)

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
        right = self._fr(body, width=280)
        right.pack(side="right", fill="y", padx=(8, 0), pady=2)
        right.pack_propagate(False)

        tk.Frame(right, bg=C["border"], width=1).pack(side="left", fill="y")
        
        self._section(right, "ĐẦU VÀO & MỤC TIÊU")
        self.nb = ttk.Notebook(right)
        self.nb.pack(fill="both", expand=True, padx=10, pady=5)
        
        # --- Start States Tab ---
        tab_start = self._fr(self.nb)
        self.nb.add(tab_start, text="Start States")
        
        ctrl_frame = self._fr(tab_start)
        ctrl_frame.pack(fill="x", pady=5)
        
        self.state_combo = ttk.Combobox(ctrl_frame, state="readonly", width=12, font=FONT["label"])
        self.state_combo.pack(side="left", padx=5)
        self.state_combo.bind("<<ComboboxSelected>>", self._on_state_selected)
        
        btn_add = tk.Button(ctrl_frame, text="+", command=self._add_state, bg=C["success"], fg="white", relief="flat", width=2)
        btn_add.pack(side="left", padx=2)
        btn_del = tk.Button(ctrl_frame, text="-", command=self._del_state, bg=C["danger"], fg="white", relief="flat", width=2)
        btn_del.pack(side="left", padx=2)

        self.start_entries = [[None]*3 for _ in range(3)]
        grid_frame_start = self._fr(tab_start)
        grid_frame_start.pack(pady=10)
        
        for i in range(3):
            for j in range(3):
                e = tk.Entry(grid_frame_start, width=3, font=("Segoe UI", 20, "bold"),
                             justify="center", bg=C["tile_bg"], fg=C["tile_num"],
                             insertbackground=C["accent"], relief="solid", bd=1,
                             highlightthickness=2, highlightbackground=C["border"],
                             highlightcolor=C["accent"])
                e.grid(row=i, column=j, padx=3, pady=3, ipady=4)
                self.start_entries[i][j] = e
                e.bind("<Up>",    lambda event, r=i, c=j: self._navigate(r - 1, c, self.start_entries))
                e.bind("<Down>",  lambda event, r=i, c=j: self._navigate(r + 1, c, self.start_entries))
                e.bind("<Left>",  lambda event, r=i, c=j: self._navigate(r, c - 1, self.start_entries))
                e.bind("<Right>", lambda event, r=i, c=j: self._navigate(r, c + 1, self.start_entries))
                
        self._lbl(tab_start, "Dùng '?' cho ô khuyết state", font=FONT["small"], fg=C["text_dim"]).pack()

        # --- Goal State Tab ---
        tab_goal = self._fr(self.nb)
        self.nb.add(tab_goal, text="Goal State")
        
        ctrl_frame_goal = self._fr(tab_goal)
        ctrl_frame_goal.pack(fill="x", pady=5)
        
        self.goal_combo = ttk.Combobox(ctrl_frame_goal, state="readonly", width=12, font=FONT["label"])
        self.goal_combo.pack(side="left", padx=5)
        self.goal_combo.bind("<<ComboboxSelected>>", self._on_goal_selected)
        
        btn_add_goal = tk.Button(ctrl_frame_goal, text="+", command=self._add_goal, bg=C["success"], fg="white", relief="flat", width=2)
        btn_add_goal.pack(side="left", padx=2)
        btn_del_goal = tk.Button(ctrl_frame_goal, text="-", command=self._del_goal, bg=C["danger"], fg="white", relief="flat", width=2)
        btn_del_goal.pack(side="left", padx=2)
        
        self.goal_entries = [[None]*3 for _ in range(3)]
        grid_frame_goal = self._fr(tab_goal)
        grid_frame_goal.pack(pady=10)
        
        for i in range(3):
            for j in range(3):
                e = tk.Entry(grid_frame_goal, width=3, font=("Segoe UI", 20, "bold"),
                             justify="center", bg=C["tile_bg"], fg=C["tile_num"],
                             insertbackground=C["accent"], relief="solid", bd=1,
                             highlightthickness=2, highlightbackground=C["border"],
                             highlightcolor=C["accent"])
                e.grid(row=i, column=j, padx=3, pady=3, ipady=4)
                self.goal_entries[i][j] = e
                e.bind("<Up>",    lambda event, r=i, c=j: self._navigate(r - 1, c, self.goal_entries))
                e.bind("<Down>",  lambda event, r=i, c=j: self._navigate(r + 1, c, self.goal_entries))
                e.bind("<Left>",  lambda event, r=i, c=j: self._navigate(r, c - 1, self.goal_entries))
                e.bind("<Right>", lambda event, r=i, c=j: self._navigate(r, c + 1, self.goal_entries))
                
        self._lbl(tab_goal, "Dùng '?' cho ô khuyết goal", font=FONT["small"], fg=C["text_dim"]).pack()
        
        self.goal_states_data = [] 
        self.current_goal_idx = 0
        
        self._add_goal(default=True)
        self._add_goal(default=False)
        self.goal_combo.current(0)
        self._on_goal_selected()

        self.start_states_data = [] 
        self.current_state_idx = 0
        
        self._add_state()
        self._add_state()
        self.state_combo.current(0)
        self._on_state_selected()

        self._div(right)

        self.btn_random = self._btn(right, "⟳   Random Current", self.ctrl.generate_random, bg=C["panel_inset"], fg=C["text"])
        self.btn_random.pack(fill="x", padx=14, pady=3)
        self.btn_solve_single = self._btn(right, "▶   Giải State Đang Chọn", self.ctrl.start_solving_single, bg=C["success"])
        self.btn_solve_single.pack(fill="x", padx=14, pady=3)
        self.btn_solve_all = self._btn(right, "▶▶  Giải Tất Cả", self.ctrl.start_solving_all, bg=C["accent"])
        self.btn_solve_all.pack(fill="x", padx=14, pady=3)
        self.btn_stop = self._btn(right, "⏹   Dừng", self.ctrl.stop_solving, bg=C["panel_inset"], fg=C["text_dim"])
        self.btn_stop.pack(fill="x", padx=14, pady=3)
        self.btn_clr  = self._btn(right, "✖   Xóa Log", self.clear_log, bg=C["panel_inset"], fg=C["text"])
        self.btn_clr.pack(fill="x", padx=14, pady=3)

    def _add_state(self):
        new_vars = [[tk.StringVar() for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                new_vars[i][j].trace_add("write", lambda *args: self.ctrl.sync_board_with_inputs())
        self.start_states_data.append(new_vars)
        self._update_state_combo()
        self.state_combo.current(len(self.start_states_data) - 1)
        self._on_state_selected()

    def _del_state(self):
        if len(self.start_states_data) > 1:
            idx = self.state_combo.current()
            self.start_states_data.pop(idx)
            self._update_state_combo()
            self.state_combo.current(max(0, idx - 1))
            self._on_state_selected()

    def _update_state_combo(self):
        self.state_combo["values"] = [f"State {i+1}" for i in range(len(self.start_states_data))]

    def _on_state_selected(self, event=None):
        idx = self.state_combo.current()
        if idx >= 0:
            for i in range(3):
                for j in range(3):
                    self.start_entries[i][j].config(textvariable=self.start_states_data[idx][i][j])
            self.current_state_idx = idx
            if hasattr(self, 'ctrl') and self.ctrl:
                self.ctrl.sync_board_with_inputs()

    def _add_goal(self, default=False):
        new_vars = [[tk.StringVar() for _ in range(3)] for _ in range(3)]
        if default:
            default_goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
            for i in range(3):
                for j in range(3):
                    new_vars[i][j].set(str(default_goal[i][j]))
        for i in range(3):
            for j in range(3):
                new_vars[i][j].trace_add("write", lambda *args: self.ctrl.sync_board_with_inputs())
        self.goal_states_data.append(new_vars)
        self._update_goal_combo()
        self.goal_combo.current(len(self.goal_states_data) - 1)
        self._on_goal_selected()

    def _del_goal(self):
        if len(self.goal_states_data) > 1:
            idx = self.goal_combo.current()
            self.goal_states_data.pop(idx)
            self._update_goal_combo()
            self.goal_combo.current(max(0, idx - 1))
            self._on_goal_selected()

    def _update_goal_combo(self):
        self.goal_combo["values"] = [f"Goal {i+1}" for i in range(len(self.goal_states_data))]

    def _on_goal_selected(self, event=None):
        idx = self.goal_combo.current()
        if idx >= 0:
            for i in range(3):
                for j in range(3):
                    self.goal_entries[i][j].config(textvariable=self.goal_states_data[idx][i][j])
            self.current_goal_idx = idx
            if hasattr(self, 'ctrl') and self.ctrl:
                self.ctrl.sync_board_with_inputs()

    def _on_algo_change(self, event=None):
        algo_name = self.combo.get()
        if algo_name in ALGORITHMS:
            algo_type = ALGORITHMS[algo_name]["type"]
            is_complex = algo_type.startswith("missing_")
            
            if is_complex:
                self.board_frame_2.pack(side="left", padx=10, fill="y")
                self.btn_solve_single.config(state="disabled", bg=C["panel_inset"], fg=C["text_dim"])
                self.btn_solve_all.config(state="normal", bg=C["accent"], fg="#ffffff")
            else:
                self.board_frame_2.pack_forget()
                self.btn_solve_single.config(state="normal", bg=C["success"], fg="#ffffff")
                self.btn_solve_all.config(state="disabled", bg=C["panel_inset"], fg=C["text_dim"])
                
            if hasattr(self, 'ctrl') and self.ctrl:
                self.ctrl.set_algorithm(algo_name)
                self.ctrl.sync_board_with_inputs()

    def _center_col(self, body):
        center = self._fr(body, bg=C["win"])
        center.pack(side="left", fill="both", expand=True, pady=2)

        board_panel = self._fr(center, bg=C["panel"])
        board_panel.pack(fill="x")
        board_wrap = self._fr(board_panel, bg=C["panel"])
        board_wrap.pack(pady=16)

        self._lbl(board_wrap, "TRẠNG THÁI BÀN CỜ", font=FONT["title"], fg=C["accent"]).pack(pady=(0, 12))

        boards_container = tk.Frame(board_wrap, bg=C["panel"])
        boards_container.pack()
        
        self.board_labels_1 = [[None]*3 for _ in range(3)]
        self.board_labels_2 = [[None]*3 for _ in range(3)]
        
        self.board_frame_1 = tk.Frame(boards_container, bg=C["panel"])
        self.board_frame_1.pack(side="left", padx=10)
        self.lbl_state1 = self._lbl(self.board_frame_1, "Bàn cờ 1", font=FONT["label"], fg=C["text"])
        self.lbl_state1.pack(pady=(0,4))
        self.tile_outer1 = tk.Frame(self.board_frame_1, bg=C["tile_border"], bd=0)
        self.tile_outer1.pack()
        for i in range(3):
            for j in range(3):
                lbl = tk.Label(self.tile_outer1, text="", width=3, height=1, font=FONT["tile"], bg=C["tile_bg"], fg=C["tile_num"], relief="solid", bd=1)
                lbl.grid(row=i, column=j, padx=2, pady=2)
                self.board_labels_1[i][j] = lbl
                
        self.board_frame_2 = tk.Frame(boards_container, bg=C["panel"])
        self.board_frame_2.pack(side="left", padx=10)
        self.lbl_state2 = self._lbl(self.board_frame_2, "Bàn cờ 2", font=FONT["label"], fg=C["text"])
        self.lbl_state2.pack(pady=(0,4))
        self.tile_outer2 = tk.Frame(self.board_frame_2, bg=C["tile_border"], bd=0)
        self.tile_outer2.pack()
        for i in range(3):
            for j in range(3):
                lbl = tk.Label(self.tile_outer2, text="", width=3, height=1, font=FONT["tile"], bg=C["tile_bg"], fg=C["tile_num"], relief="solid", bd=1)
                lbl.grid(row=i, column=j, padx=2, pady=2)
                self.board_labels_2[i][j] = lbl

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

        cols = ("#", "State (ma trận)", "Parent State", "Action", "Path Cost", "G_Cost", "H_Cost")

        self.tree = ttk.Treeview(log_panel, columns=cols, show="headings", style="Log.Treeview", height=8)

        widths = [40, 262, 262, 40, 40, 40, 40]

        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, minwidth=w, anchor="w")

        vsb = ttk.Scrollbar(log_panel, orient="vertical",   command=self.tree.yview)

        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

    def update_board(self, matrix_or_tuple):
        if isinstance(matrix_or_tuple, tuple) and len(matrix_or_tuple) == 2:
            mat1, mat2 = matrix_or_tuple
            self._update_single_board(self.board_labels_1, mat1)
            self._update_single_board(self.board_labels_2, mat2)
        else:
            self._update_single_board(self.board_labels_1, matrix_or_tuple)
            self._update_single_board(self.board_labels_2, [[0]*3 for _ in range(3)])

    def _update_single_board(self, board_labels, matrix):
        for i in range(3):
            for j in range(3):
                v = matrix[i][j]

                if v == 0:
                    board_labels[i][j].config(text="", bg=C["tile_empty"])
                elif v == '?':
                    board_labels[i][j].config(text="?", bg="#feebc8", fg="#c05621")
                else:
                    board_labels[i][j].config(text=str(v), bg=C["tile_bg"], fg=C["tile_num"])

    def get_input_states(self):
        states = []
        for vars_grid in self.start_states_data:
            matrix = []
            for i in range(3):
                row = []
                for j in range(3):
                    val = vars_grid[i][j].get().strip()
                    if val == '?' or val == '*' or val == '':
                        row.append('?')
                    elif val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
                        row.append(int(val))
                    else:
                        return None
                matrix.append(row)
            states.append(matrix)
        return states

    def get_goal_states(self):
        goals = []
        for vars_grid in self.goal_states_data:
            matrix = []
            for i in range(3):
                row = []
                for j in range(3):
                    val = vars_grid[i][j].get().strip()
                    if val == '?' or val == '*' or val == '':
                        row.append('?')
                    elif val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
                        row.append(int(val))
                    else:
                        return None
                matrix.append(row)
            goals.append(matrix)
        return goals

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
            st = e["state"]
            pt = e["parent"]
            a  = (e["action"] or "—").upper()
            c  = str(e["path_cost"])
            g = str(e["g_cost"])
            h = str(e["h_cost"])

            tag = "ra" if (offset+idx)%2==0 else "rb"
            
            if isinstance(st, tuple) and len(st) == 2:
                s1 = self._mat_str(st[0])
                s2 = self._mat_str(st[1])
                p1 = self._mat_str(pt[0]) if pt else "—"
                p2 = self._mat_str(pt[1]) if pt else "—"
                
                self.tree.insert("", "end", values=(offset+idx+1, s1, p1, a, c, g, h), tags=(tag,))
                self.tree.insert("", "end", values=("", s2, p2, "", "", "", ""), tags=(tag,))
            else:
                s  = self._mat_str(st)
                p  = self._mat_str(pt) if pt else "—"
                self.tree.insert("", "end", values=(offset+idx+1, s, p, a, c, g, h), tags=(tag,))

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
            self.btn_solve_single.config(state="disabled", bg=C["panel_inset"], fg=C["text_dim"])
            self.btn_solve_all.config(state="disabled", bg=C["panel_inset"], fg=C["text_dim"])
            self.btn_random.config(state="disabled")
            self.btn_clr.config(state="disabled")
            self.btn_stop.config(state="normal", bg=C["danger"], fg="#ffffff")
            self.btn_stop.bind("<Leave>", lambda e: self.btn_stop.config(bg=C["danger"]))
        else:
            algo_type = ALGORITHMS.get(self.ctrl._algo, {"type": "normal"})["type"]
            if algo_type.startswith("missing_"):
                self.btn_solve_single.config(state="disabled", bg=C["panel_inset"], fg=C["text_dim"])
                self.btn_solve_all.config(state="normal", bg=C["accent"], fg="#ffffff")
            else:
                self.btn_solve_single.config(state="normal", bg=C["success"], fg="#ffffff")
                self.btn_solve_all.config(state="disabled", bg=C["panel_inset"], fg=C["text_dim"])
            
            self.btn_random.config(state="normal")
            self.btn_clr.config(state="normal")
            self.btn_stop.config(state="disabled", bg=C["panel_inset"], fg=C["text_dim"])
            self.btn_stop.bind("<Leave>", lambda e: self.btn_stop.config(bg=C["panel_inset"]))

    def _mat_str(self, m):
        if m is None: return "—"
        return " | ".join(str(row).replace(" ", "") for row in m)

class PuzzleController:
    def __init__(self, root):
        self._algo = list(ALGORITHMS.keys())[0]
        self._is_stopped = False
        self.model = PuzzleModel()
        self.view = PuzzleView(root, self)
        self.generate_random()

    def select_algo(self, name):
        self._algo = name
        short = name.split("—")[0].strip()
        self.view.lbl_status.config(text=f"Thuật toán: {short}", fg=C["accent2"])
        self.view.lbl_algo.config(text=f"Thuật toán:  {short}")
        self.view._on_algo_change()

    def set_algorithm(self, name):
        self._algo = name

    def sync_board_with_inputs(self, *args):
        try:
            all_starts = self.view.get_input_states()
        except Exception:
            return
            
        if not all_starts:
            return
            
        algo_info = ALGORITHMS.get(self._algo, {"type": "normal"})
        algo_type = algo_info["type"]
        is_complex = algo_type.startswith("missing_")
        
        if is_complex:
            if algo_type == "missing_input":
                starts_arr = all_starts
            elif algo_type == "missing_goal":
                starts_arr = [all_starts[self.view.current_state_idx]]
            else:
                starts_arr = [all_starts[self.view.current_state_idx]]
                
            from complex_core import get_first_two_states
            init_tuple = get_first_two_states(starts_arr)
            if init_tuple:
                self.view.update_board(init_tuple)
            else:
                if len(starts_arr) > 0:
                    self.view.update_board(starts_arr[0])
        else:
            idx = self.view.current_state_idx
            if idx < len(all_starts):
                self.view.update_board(all_starts[idx])
            elif len(all_starts) > 0:
                self.view.update_board(all_starts[0])

    def generate_random(self):
        m = random_matrix()
        current_tab = self.view.nb.index(self.view.nb.select())
        
        if current_tab == 0:
            idx = self.view.state_combo.current()
            if idx >= 0:
                for i in range(3):
                    for j in range(3):
                        self.view.start_states_data[idx][i][j].set(str(m[i][j]))
        else:
            idx = self.view.goal_combo.current()
            if idx >= 0:
                for i in range(3):
                    for j in range(3):
                        self.view.goal_states_data[idx][i][j].set(str(m[i][j]))
                        
        self.view.lbl_moves.config(text="")
        self.view.lbl_status.config(text="Ma trận mới đã tạo", fg=C["accent2"])
        self.view.lbl_reached.config(text="States duyệt:  —")
        self.view.lbl_steps.config(text="Số bước giải:  —")

    def clear_log(self):
        self.view.clear_log()

    def stop_solving(self):
        self._is_stopped = True
        self.view.lbl_status.config(text="Đang dừng...", fg=C["danger"])

    def start_solving_single(self):
        self._start_solving(solve_all=False)
        
    def start_solving_all(self):
        self._start_solving(solve_all=True)

    def _start_solving(self, solve_all=True):
        self.clear_log()
        all_starts = self.view.get_input_states()
        all_goals = self.view.get_goal_states()
        
        if not all_starts or not all_goals:
            messagebox.showerror("Lỗi", "Vui lòng nhập các số hợp lệ hoặc '?' cho ô khuyết.")
            return

        if solve_all:
            starts = all_starts
            goals = all_goals
            lbl_text = f"Đang giải toàn bộ {len(starts)} states"
        else:
            idx = self.view.current_state_idx
            starts = [all_starts[idx]]
            goal_idx = self.view.current_goal_idx
            goals = [all_goals[goal_idx]]
            lbl_text = f"Đang giải State {idx + 1}"

        self._is_stopped = False
        self.view.set_solving_state(True)
        self.view.lbl_moves.config(text="")
        
        algo_info = ALGORITHMS.get(self._algo, {"func": ALGORITHMS["BFS"]["func"], "type": "normal"})
        algo_func = algo_info["func"]
        algo_type = algo_info["type"]
        is_complex = algo_type.startswith("missing_")
        
        if is_complex:
            if algo_type == "missing_input":
                starts_arr = starts
                goals_arr = [goals[0]]
            elif algo_type == "missing_goal":
                starts_arr = [starts[0]]
                goals_arr = goals
            else:
                starts_arr = [starts[0]]
                goals_arr = [goals[0]]
                
            prob = Problem(starts_arr, goals_arr)
            
            def run_complex():
                try:
                    res, count = algo_func(prob, self.model._log_cb(lambda: self._is_stopped))
                    if self._is_stopped:
                        self._complete_search("Đã dừng", "red")
                        return
                        
                    if res:
                        self.model.solution_nodes = self.model._get_path(res)
                        self._complete_search(f"Thành công! {len(self.model.solution_nodes)-1} bước.", C["success"], self.model.solution_nodes, count)
                    else:
                        self._complete_search("Không tìm thấy đường đi.", "red", count=count)
                except StopSearchException:
                    self._complete_search("Đã dừng", "red")
                except Exception as e:
                    self._complete_search(f"Lỗi: {e}", "red")

            threading.Thread(target=run_complex, daemon=True).start()
            return

        def run():
            sol_nodes = []
            total_count = 0
            last_prob = None

            for i, st in enumerate(starts):
                if self._is_stopped:
                    self._complete_search("Đã dừng", "red")
                    return
                try:
                    prob = Problem(st, goals[0])
                    last_prob = prob
                    res, count = algo_func(prob, self.model._log_cb(lambda: self._is_stopped))
                    total_count += count
                    if res and res != "cutoff":
                        sol_nodes.append(self.model._get_path(res))
                    else:
                        break
                except StopSearchException:
                    self._complete_search("Đã dừng", "red")
                    return
                except Exception as e:
                    self._complete_search(f"Lỗi: {e}", "red")
                    return

            if self._is_stopped:
                return

            if sol_nodes:
                self.model.solution_nodes = sol_nodes[0]
                res_node = self.model.solution_nodes[-1]
                
                is_goal = False
                if getattr(res_node, 'h_cost', -1) == 0:
                    is_goal = True
                elif last_prob and last_prob.goal_test(getattr(res_node, 'state', None)):
                    is_goal = True
                    
                if is_goal:
                    self._complete_search(f"Thành công! {len(self.model.solution_nodes)-1} bước.", C["success"], self.model.solution_nodes, total_count)
                else:
                    self._complete_search(f"Thất bại: Đạt cực trị cục bộ! {len(self.model.solution_nodes)-1} bước.", C["warning"], self.model.solution_nodes, total_count)
            else:
                self._complete_search("Không tìm thấy đường đi.", "red", count=total_count)

        threading.Thread(target=run, daemon=True).start()
        self.view.lbl_status.config(text=lbl_text, fg=C["warning"])

    def _complete_search(self, msg, color, path=None, count=None):
        def cb():
            self.view.lbl_status.config(text=msg, fg=color)
            if count is not None:
                self.view.lbl_reached.config(text=f"States duyệt:  {count}")
                self.model.reached_count = count

            if self.model.log_entries:
                self.view.append_log(self.model.log_entries)
                self.model.log_entries = []

            if path:
                self.view.lbl_steps.config(text=f"Số bước giải:  {len(path) - 1}")
                self._animate(0, "")
            else:
                self.view.set_solving_state(False)

        self.view.root.after(0, cb)

    def _animate(self, idx, path_str):
        if self._is_stopped:
            self.view.lbl_status.config(text="Đã dừng hiển thị nước đi!", fg=C["danger"])
            self.view.set_solving_state(False)
            return

        nodes = self.model.solution_nodes

        if idx < len(nodes):
            n = nodes[idx]
            st = getattr(n, 'belief_state', n.state)
            self.view.update_board(st)
            action_str = n.action.upper() if n.action else ""
            if action_str:
                path_str += (" ➔ " if path_str else "") + action_str
            self.view.lbl_moves.config(text=path_str)
            self.view.root.after(750, self._animate, idx+1, path_str)
        else:
            self.view.lbl_status.config(text="✓ Hoàn thành!", fg=C["success"])
            self.view.set_solving_state(False)

if __name__ == "__main__":
    root = tk.Tk()
    PuzzleController(root)
    root.mainloop()