# TTNT – Trí Tuệ Nhân Tạo (Artificial Intelligence)
> Tập hợp bài tập thực hành môn **Trí Tuệ Nhân Tạo** – HCMUTE  
> Sinh viên: Lê Đặng Hoàng Anh · MSSV: 24162006

---

## Cấu trúc dự án

```
ttnt/
├── README.md
│
├── buoi_2/                         # Buổi 2 – Khám phá bài toán (bài tập ảnh chụp)
│   └── bt1.jpg
│
├── buoi_3/                         # Buổi 3 – BFS / DFS cơ bản (Jupyter + Python)
│   ├── TTNT_1.ipynb                  # Notebook giải thích lý thuyết BFS/DFS
│   ├── TTNT_2.py                     # Triển khai BFS/DFS thuần Python
│   ├── 24162006_LeDangHoangAnh_8_Puzzle.ipynb       # Bài nộp 8-Puzzle
│   └── 24162006_LeDangHoangAnh_Robot_Hut_Bui.*      # Bài nộp Robot Hút Bụi
│
├── buoi_4/                         # Buổi 4 – Mô hình hóa bài toán (Model-based)
│   ├── 24162006_LeDangHoangAnh_8_Puzzel_Model.ipynb
│   └── 24162006_LeDangHoangAnh_Robot_Hut_Bui_Model.ipynb
│
├── buoi_5/                         # Buổi 5 – Phát triển solver có giao diện (Tkinter GUI)
│   ├── 8_puzzel_bfs_v1/              # Phiên bản v1: GUI + BFS cơ bản
│   └── 8_puzzel_bfs_v2/              # Phiên bản v2: GUI + BFS cải tiến early goal-test
│
└── buoi_6/                         # Buổi 6 – Solver đa thuật toán (module hóa đầy đủ)
    ├── 8_puzzle_dfs_v2/              # Thử nghiệm DFS riêng
    ├── 8_puzzle_ids.py/              # Thử nghiệm IDS riêng
    └── 8_puzzle_solver/              # ★ Module chính – xem chi tiết bên dưới
```

---

## Module chính: `buoi_6/8_puzzle_solver/`

Module này là phiên bản hoàn chỉnh nhất, áp dụng kiến trúc **MVC (Model–View–Controller)** và hỗ trợ nhiều thuật toán tìm kiếm thông qua một **registry tập trung**.

```
8_puzzle_solver/
│
├── puzzle_core.py          # Lớp dùng chung (Node, Problem) và các hàm tiện ích
├── bfs.py                  # Thuật toán BFS (2 biến thể: late / early goal-test)
├── dfs.py                  # Thuật toán DFS (graph-search có tập visited)
├── ids.py                  # Thuật toán IDS (depth-limited + iterative deepening)
└── 8_puzzle_solver.py      # Ứng dụng chính: GUI Tkinter + MVC Controller
```

### Vai trò từng file

| File | Vai trò |
|------|---------|
| `puzzle_core.py` | Định nghĩa `Node`, `Problem`, các hàm `get_index`, `tuple_matrix`, `expand`, `child_node`, `random_matrix` — **không import Tkinter**, dùng được độc lập |
| `bfs.py` | Hàm `bfs()` (late goal-test) và `bfs_v2()` (early goal-test) |
| `dfs.py` | Hàm `dfs()` — DFS có tập `reached` tránh lặp vô hạn |
| `ids.py` | Hàm `ids()` — IDS tối ưu bộ nhớ; hàm nội bộ `_depth_limited_search()` |
| `8_puzzle_solver.py` | `PuzzleModel` (logic), `PuzzleView` (GUI), `PuzzleController` (điều phối); registry `ALGORITHMS` ánh xạ tên → hàm |

---

## Quy trình thêm thuật toán mới vào `8_puzzle_solver.py`

### Bước 1 – Tạo file thuật toán (`my_algo.py`)

Mỗi file thuật toán **phải** tuân theo khung chuẩn sau:

```python
"""<Tên đầy đủ thuật toán> cho bài toán 8-puzzle.

Mô tả ngắn: nguyên lý hoạt động, đặc điểm (tối ưu / không tối ưu, ...).
"""

from puzzle_core import Node, Problem, tuple_matrix, expand   # import những gì cần thiết


def my_algo(problem: Problem, log_cb=None):
    """<Tên hàm bằng snake_case, trùng với tên file>.

    Chữ ký (signature) PHẢI giữ nguyên: nhận `problem` và `log_cb`.

    Parameters
    ----------
    problem : Problem
        Đối tượng chứa `problem.start`, `problem.goal`, `problem.goal_test()`,
        `problem.get_actions()`.
    log_cb  : callable | None
        Callback ``log_cb(child_node)`` do PuzzleModel cung cấp để ghi log
        từng trạng thái con được sinh ra.  Truyền vào `expand()` / `child_node()`.

    Returns
    -------
    tuple[Node | False, int]
        - ``(goal_node, visited_count)`` nếu tìm được lời giải.
        - ``(False, visited_count)``     nếu không tồn tại lời giải.
    """
    # ── Khởi tạo ─────────────────────────────────────────────────────────
    root = Node(problem.start, None, None, 0)
    # ... khởi tạo frontier, tập visited, ...

    # ── Vòng lặp tìm kiếm chính ──────────────────────────────────────────
    while frontier:
        node = ...                              # lấy node tiếp theo
        if node.state == problem.goal:
            return node, len(visited)           # ← trả về đúng format

        for child in expand(problem, node, log_cb):   # log_cb PHẢI được truyền vào expand()
            ...

    return False, len(visited)                  # ← không tìm được nghiệm
```

> **Lưu ý quan trọng:**
> - `log_cb` **phải** được truyền xuống `expand()` hoặc `child_node()` — đây là cơ chế duy nhất để GUI ghi log và cơ chế dừng giữa chừng (Stop) hoạt động.
> - Hàm **không được** import Tkinter hay tương tác trực tiếp với GUI.
> - Hàm **phải** trả về đúng kiểu `(Node | False, int)`.

---

### Bước 2 – Đăng ký vào registry trong `8_puzzle_solver.py`

```python
# 8_puzzle_solver.py  (đầu file, ngay sau các import hiện có)

from my_algo import my_algo as _my_algo          # 1. Import hàm

ALGORITHMS = {
    "BFS":      _bfs,
    "BFS_V2":   _bfs_v2,
    "DFS":      _dfs,
    "IDS":      _ids,
    "MY_ALGO":  _my_algo,                        # 2. Thêm vào dict
}
```

Chỉ cần hai thay đổi trên, thuật toán mới sẽ **tự động xuất hiện** trong Combobox của giao diện mà không cần sửa thêm bất kỳ dòng nào trong `PuzzleModel`, `PuzzleView`, hay `PuzzleController`.

---

## Yêu cầu cài đặt

```bash
python -m pip install tk   # thường đã đi kèm với Python 3.x
```

Chạy ứng dụng:

```bash
cd buoi_6/8_puzzle_solver
python 8_puzzle_solver.py
```
