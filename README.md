# TTNT – Trí Tuệ Nhân Tạo (Artificial Intelligence)
> Tập hợp bài tập thực hành môn **Trí Tuệ Nhân Tạo** – HCMUTE  
> Sinh viên: Lê Đặng Hoàng Anh · MSSV: 24162006

---

## Cấu trúc dự án

```
ttnt/
├── README.md
│
├── eight_puzzle_solver/              # ★ Module chính (MVC, GUI Tkinter, đa thuật toán) – xem chi tiết bên dưới
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
│   ├── 24162006_LeDangHoangAnh_Robot_Hut_Bui_Model.ipynb
│   └── 24162006_LeDangHoangAnh_Robot_Hut_Bui_Simple.ipynb
│
├── buoi_5/                         # Buổi 5 – Phát triển solver có giao diện (Tkinter GUI)
│   ├── 8_puzzel_bfs_v1/              # Phiên bản v1: GUI + BFS cơ bản
│   └── 8_puzzel_bfs_v2/              # Phiên bản v2: GUI + BFS cải tiến early goal-test
│
├── buoi_6/                         # Buổi 6 – DFS & IDS
│   ├── 8_puzzle_dfs_v2/              # Thử nghiệm DFS riêng
│   └── 8_puzzle_ids.py/              # Thử nghiệm IDS riêng
│
└── buoi_7/                         # Buổi 7 – Tìm kiếm chi phí đồng nhất (UCS)
    └── ucs.py                      # Bài tập UCS
```

---

## Module chính: `eight_puzzle_solver/`

Module này là phiên bản hoàn chỉnh nhất, áp dụng kiến trúc **MVC (Model–View–Controller)** và hỗ trợ nhiều thuật toán tìm kiếm thông qua một **registry tập trung**.

```
eight_puzzle_solver/
│
├── puzzle_core.py          # Lớp dùng chung (Node, Problem) và các hàm tiện ích
├── bfs.py                  # Thuật toán BFS (2 biến thể: late / early goal-test)
├── dfs.py                  # Thuật toán DFS (graph-search có tập visited)
├── ids.py                  # Thuật toán IDS (depth-limited + iterative deepening)
├── ucs.py                  # Thuật toán UCS (Uniform Cost Search)
├── ida_star.py             # Thuật toán IDA* (Iterative Deepening A*)
└── eight_puzzle_solver.py  # Ứng dụng chính: GUI Tkinter + MVC Controller
```

### Vai trò từng file

| File | Vai trò |
|------|---------|
| `puzzle_core.py` | Định nghĩa `Node`, `Problem`, các hàm `get_index`, `tuple_matrix`, `expand`, `child_node`, `random_matrix` — **không import Tkinter**, dùng được độc lập |
| `bfs.py` | Hàm `bfs()` (late goal-test) và `bfs_v2()` (early goal-test) |
| `dfs.py` | Hàm `dfs()` — DFS có tập `reached` tránh lặp vô hạn |
| `ids.py` | Hàm `ids()` — IDS tối ưu bộ nhớ; hàm nội bộ `_depth_limited_search()` |
| `ucs.py` | Hàm `ucs()` — Thuật toán tìm kiếm chi phí đồng nhất (Uniform Cost Search) |
| `ida_star.py` | Hàm `ida_star()` — Thuật toán tìm kiếm IDA* kết hợp heuristic để tối ưu |
| `eight_puzzle_solver.py` | `PuzzleModel` (logic), `PuzzleView` (GUI), `PuzzleController` (điều phối); registry `ALGORITHMS` ánh xạ tên → hàm |

---


## Yêu cầu cài đặt

```bash
python -m pip install tk   # thường đã đi kèm với Python 3.x
```

Chạy ứng dụng:

```bash
cd eight_puzzle_solver
python eight_puzzle_solver.py
```
