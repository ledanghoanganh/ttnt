# Dự án Trí Tuệ Nhân Tạo (Artificial Intelligence) - 8-Puzzle Solver

> **Môn học**: Trí Tuệ Nhân Tạo (Artificial Intelligence) – Trường Đại Học Sư Phạm Kỹ Thuật TP.HCM (HCMUTE)  
> **Sinh viên thực hiện**: Lê Đặng Hoàng Anh  
> **MSSV**: 24162006  

Dự án này là tập hợp các bài tập và sản phẩm thực hành xuyên suốt khóa học Trí Tuệ Nhân Tạo. Trọng tâm lớn nhất của dự án là module `eight_puzzle_solver/`, một ứng dụng GUI hoàn chỉnh áp dụng kiến trúc phần mềm chuyên nghiệp để minh họa, giải quyết và phân tích hiệu suất của hàng loạt thuật toán tìm kiếm kinh điển và nâng cao áp dụng trên bài toán 8-Puzzle.

---

## 🌟 Tính năng Kỹ thuật nổi bật

1. **Kiến trúc MVC (Model-View-Controller)**: Ứng dụng GUI chính (`eight_puzzle_solver.py`) được thiết kế tách biệt giao diện (`PuzzleView`), logic dữ liệu (`PuzzleModel`), và bộ điều khiển (`PuzzleController`), đảm bảo code dễ bảo trì và mở rộng.
2. **Registry Pattern cho Thuật Toán**: Các thuật toán được nạp thông qua một bộ cấu hình động `ALGORITHMS`. Giao diện sẽ tự động thích ứng (bật/tắt nút, hiển thị đa bàn cờ) dựa trên metadata (`type`) của từng thuật toán được chọn.
3. **Môi trường Khuyết thông tin (Complex Environments)**: Hệ thống hỗ trợ xử lý môi trường không chắc chắn (chứa ký tự `?`). Thuật toán cốt lõi sẽ tự động tính toán không gian trạng thái giả định (**Belief States**) và phân rã các tập khả năng để tìm đường đi chung.
4. **Data Binding & Reactive UI**: Bảng lưới Tkinter (`Entry`) được liên kết với cơ chế `trace_add` (Observer), giúp các thay đổi của người dùng được phản hồi và đồng bộ hóa lên màn hình hiển thị trực quan (Bàn cờ) theo thời gian thực (zero-latency).
5. **Threaded Execution & Animation**: Thuật toán tìm kiếm được chạy trên Background Thread (Daemon Thread) để giao diện không bị treo (non-blocking). Toàn bộ quá trình giải sẽ được lưu log, và các bước di chuyển (Action Path) được hoạt họa mượt mà.

---

## 📂 Cấu trúc Thư mục và File chi tiết

Dự án được chia thành các thư mục ứng với tiến trình học tập.

### 1. Thư mục Học tập cơ bản (`buoi_2` đến `buoi_7`)
Chứa các Notebook Jupyter và các script độc lập chạy trên console. Phục vụ mục đích hiểu rõ lý thuyết, cấu trúc dữ liệu cơ sở của tìm kiếm.

* `buoi_2/`: Khám phá bài toán cơ bản (bao gồm các tư liệu ảnh chụp `bt1.jpg`).
* `buoi_3/`: Giới thiệu thuật toán tìm kiếm mù. Gồm Jupyter notebook (`TTNT_1.ipynb`, bài nộp `8_Puzzle`, `Robot_Hut_Bui`) và script `TTNT_2.py` thuần Python minh họa BFS/DFS.
* `buoi_4/`: Mô hình hóa bài toán (Model-based agent). Chứa các Notebook chuyển dịch logic cơ bản thành kiến trúc hướng đối tượng (OOP).
* `buoi_5/`: Bước đệm GUI. Thử nghiệm áp dụng thư viện Tkinter lần đầu cho BFS. Có các phiên bản v1 (cơ bản) và v2 (cải thiện kiểm tra mục tiêu sớm - early goal-test).
* `buoi_6/`: Thử nghiệm thuật toán DFS (Depth-First Search) và IDS (Iterative Deepening Search).
* `buoi_7/`: Tìm kiếm chi phí đồng nhất (Uniform Cost Search - UCS).
* `buoi_8/`: Tìm kiếm có thông tin / Khám phá Heuristic. Chứa các file thuật toán A* (`a_star.py`) và IDA* (`ida_star.py`).
* `buoi_9/`: Tìm kiếm cục bộ (Local Search) cơ bản. Chứa các thuật toán Leo đồi (`simple_hill_climbing.py` và `steepest_ascent_hill_climbing.py`).
* `buoi_10/`: Local Search nâng cao. Chứa các biến thể Leo đồi tối ưu (`stochastic_hill_climbing.py`, `random_restart_hill_climbing.py`) và chùm tia (`local_beam_search.py`).
* `buoi_11/`: Môi trường khuyết thông tin (Complex Environments). Chứa logic sinh Belief State và các biến thể A* phức tạp (`complex_a_star_*.py`) cùng thuật toán Luyện kim nhân tạo (`simulate_annealing.py`).

### 2. Module Sản Phẩm Cuối Cùng (`eight_puzzle_solver/`)
Đây là trái tim của hệ thống. Nơi tổng hợp toàn bộ các thuật toán và công nghệ GUI vào một ứng dụng duy nhất. Cấu trúc được chia làm 3 nhóm chính:

#### Nhóm Core (Lõi hệ thống)
* `puzzle_core.py`: Cấu trúc dữ liệu nền tảng. Định nghĩa class `Node`, class `Problem`, và các hàm toán học hỗ trợ (như chuyển `matrix` thành `tuple` tĩnh, sinh `random_matrix`, v.v).
* `complex_core.py`: Lõi xử lý logic cho môi trường khuyết (`?`). Xây dựng `ComplexNode`, logic tổ hợp tổ hợp chập (permutations) tạo `Belief State`, và hàm Heuristic phức hợp (`complex_h_cost`) dùng khoảng cách Manhattan tính cho nhiều state song song.

#### Nhóm Thuật Toán Kinh Điển (Normal)
Các file này nhận vào một bài toán `Problem(start, goal)` và trả về đường đi.
* `bfs.py`: Breadth-First Search (có phiên bản `bfs_v2` tối ưu).
* `dfs.py`: Depth-First Search (Graph-search chặn chu trình).
* `ids.py`: Iterative Deepening Search.
* `ucs.py`: Uniform Cost Search.
* `gs.py`: Greedy Search (Sử dụng hàm heuristic thuần túy).
* `a_star.py`: Thuật toán A* kinh điển (kết hợp `g_cost` và `h_cost`).
* `ida_star.py`: Iterative Deepening A*.

#### Nhóm Tìm kiếm Địa phương (Local Search)
Các file thực thi chiến lược tìm kiếm theo phương thức leo đồi và chùm tia:
* `simple_hill_climbing.py`: Leo đồi đơn giản.
* `steepest_ascent_hill_climbing.py`: Leo đồi dốc nhất.
* `stochastic_hill_climbing.py`: Leo đồi ngẫu nhiên.
* `random_restart_hill_climbing.py`: Leo đồi khởi động lại ngẫu nhiên.
* `local_beam_search.py`: Local beam search duy trì `k` trạng thái tốt nhất.

#### Nhóm Thuật Toán Phức Tạp (Complex / Missing Info)
Nhóm thuật toán giải bài toán dựa trên `Belief States`.
* `complex_a_star_missing_input.py`: Giải 8-puzzle khi đầu vào bị khuyết/ẩn một hoặc nhiều ô (nhập `?`).
* `complex_a_star_missing_goal.py`: Giải bài toán khi người dùng nhập nhiều Goal (đa mục tiêu).
* `complex_a_star_missing_both.py`: Giải bài toán khó nhất – vừa khuyết thông tin tại đầu vào, vừa khuyết thông tin tại đầu ra.

#### Giao Diện Chính (UI Application)
* `eight_puzzle_solver.py`: Điểm khởi chạy của chương trình. Tích hợp Tkinter.

---

## 🚀 Hướng dẫn Cài đặt và Chạy ứng dụng

### Yêu cầu hệ thống
* **Ngôn ngữ**: Python 3.8 trở lên.
* **Thư viện**: 
  * Giao diện dùng `tkinter` (thường được cài sẵn (built-in) cùng với bộ cài Python tiêu chuẩn trên Windows/macOS).
  * Đối với môi trường Jupyter Notebook trong các buổi học cũ, bạn có thể cần `jupyter`.

### Cách chạy

**1. Clone thư mục dự án và di chuyển đến thư mục chứa ứng dụng:**
```bash
cd ttnt/eight_puzzle_solver
```

**2. Khởi chạy Ứng dụng GUI:**
```bash
python main.py
```
*(Lưu ý: Màn hình cần độ phân giải tối thiểu 1100x700 để hiển thị tốt nhất. Ứng dụng có tích hợp DPI Awareness giúp hiển thị sắc nét trên màn hình High DPI của Windows).*

---

## 💡 Hướng dẫn Sử dụng Giao diện (Dành cho Giảng viên/Người đánh giá)

1. **Chọn Thuật toán**: Phía panel bên trái, có Dropdown liệt kê tất cả hơn 15+ thuật toán. Khi chọn một thuật toán thuộc nhóm `Complex A*`, giao diện sẽ tự động bật 2 bàn cờ song song để thể hiện trực quan môi trường bất định.
2. **Nhập liệu Trực tiếp**:
   * Chuyển qua lại giữa các tab **Start States** và **Goal States** ở panel bên phải.
   * Bạn có thể bấm nút `+` hoặc `-` để tạo thêm các trạng thái đầu vào/đầu ra khác nhau.
   * Sử dụng phím `Mũi tên (Lên/Xuống/Trái/Phải)` trên bàn phím để di chuyển ô nhập liệu nhanh chóng. Giao diện thay đổi tức thời theo mỗi nút bạn bấm.
3. **Thử nghiệm Ô Khuyết**:
   * Xóa một số và gõ dấu `?` vào ô đó.
   * Chọn một trong 3 thuật toán `Complex A*`.
   * Bấm nút **▶▶ Giải Tất Cả**. Hệ thống sẽ tự động sinh các hoán vị, lọc ra ma trận hợp lệ và tìm một chuỗi hành động duy nhất giải quyết được mọi khả năng có thể xảy ra của dấu `?`.
4. **Đọc Log và Path**:
   * Cột giữa màn hình sẽ phát lại chuỗi hành động `(L ➔ U ➔ R ...)` sau khi tìm được kết quả thành công.
   * Cửa sổ **Log - States Đã Duyệt** ở dưới cùng hiển thị chi tiết lịch sử mọi state mà thuật toán đã duyệt qua (kèm Parent State và điểm số Heuristic `G_Cost`, `H_Cost`). Đóng vai trò làm công cụ debug trực quan tuyệt vời.
