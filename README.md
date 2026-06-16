# Dự án Trí Tuệ Nhân Tạo (Artificial Intelligence) - 8-Puzzle Solver

> **Môn học**: Trí Tuệ Nhân Tạo (Artificial Intelligence) – Trường Đại Học Sư Phạm Kỹ Thuật TP.HCM (HCMUTE)  
> **Sinh viên thực hiện**: Lê Đặng Hoàng Anh  
> **MSSV**: 24162006  

Dự án này là tập hợp các bài tập và sản phẩm thực hành xuyên suốt khóa học Trí Tuệ Nhân Tạo. Trọng tâm lớn nhất của dự án là một ứng dụng GUI hoàn chỉnh áp dụng kiến trúc phần mềm chuyên nghiệp để minh họa, giải quyết và phân tích hiệu suất của hàng loạt thuật toán tìm kiếm kinh điển và nâng cao áp dụng trên bài toán 8-Puzzle.

---

## Tính năng Kỹ thuật nổi bật

1. **Kiến trúc MVC (Model-View-Controller)**: Ứng dụng GUI chính (`main.py`) được thiết kế tách biệt giao diện (`PuzzleView`), logic dữ liệu (`PuzzleModel`), và bộ điều khiển (`PuzzleController`), đảm bảo code dễ bảo trì và mở rộng.
2. **Registry Pattern cho Thuật Toán**: Các thuật toán được nạp thông qua một bộ cấu hình động `ALGORITHMS`. Giao diện sẽ tự động thích ứng (bật/tắt nút, hiển thị đa bàn cờ) dựa trên metadata (`type`) của từng thuật toán được chọn.
3. **Môi trường Khuyết thông tin (Complex Environments)**: Hệ thống hỗ trợ xử lý môi trường không chắc chắn (chứa ký tự `?`). Thuật toán cốt lõi sẽ tự động tính toán không gian trạng thái giả định (**Belief States**) và phân rã các tập khả năng để tìm đường đi chung.
4. **Data Binding & Reactive UI**: Bảng lưới Tkinter (`Entry`) được liên kết với cơ chế `trace_add` (Observer), giúp các thay đổi của người dùng được phản hồi và đồng bộ hóa lên màn hình hiển thị trực quan (Bàn cờ) theo thời gian thực (zero-latency).
5. **Threaded Execution & Animation**: Thuật toán tìm kiếm được chạy trên Background Thread (Daemon Thread) để giao diện không bị treo (non-blocking). Toàn bộ quá trình giải sẽ được lưu log, và các bước di chuyển (Action Path) được hoạt họa mượt mà.

---

## Cấu trúc Thư mục và File chi tiết

Dự án được cấu trúc theo mô hình phân tán, các thuật toán được chia về các thư mục ứng với tiến trình học tập (các buổi học) nhưng được tích hợp và gọi thông qua một Giao Diện Chính và các bộ Core dùng chung tại thư mục gốc.

### 1. File Nền Tảng Lõi (Thư mục Gốc)
Đây là các file trái tim của hệ thống:
* **`main.py`**: Ứng dụng giao diện chính (UI Application). Tích hợp Tkinter, kết nối tất cả các thuật toán vào một giao diện đồng nhất.
* **`puzzle_core.py`**: Lõi cấu trúc dữ liệu nền tảng. Định nghĩa class `Node`, class `Problem`, và các hàm tiện ích cốt lõi (như hàm `expand`, tính `g_cost`, `h_cost`, kiểm tra trạng thái giải được `is_solvable`). Mọi thuật toán tìm kiếm tiêu chuẩn đều kế thừa các base class này.
* **`complex_core.py`**: Lõi xử lý logic cho môi trường khuyết (`?`). Xây dựng logic tổ hợp chập (permutations) tạo `Belief State`, và tính Heuristic phức hợp (`complex_h_cost`) dùng khoảng cách Manhattan cho nhiều state song song.

### 2. Các Phân Hệ Thuật Toán (Thư mục `buoi_*`)
Chứa các Notebook học thuyết (nếu có) và file thực thi thuật toán. Các thuật toán này đều tuân thủ chung chuẩn Interface `def algorithm(problem, log_cb=None)` để `main.py` có thể tự động liên kết dữ liệu và render đồ họa.

* **`buoi_02/` & `buoi_03/` & `buoi_04/`**: Giới thiệu lý thuyết, các mô hình hóa bài toán cơ bản dạng Jupyter Notebook và sơ đồ.
* **`buoi_05/`**: Breadth-First Search (BFS). Có các phiên bản cơ bản và tối ưu. Chứa các file `test_bfs_v1.py` và `test_bfs_v2.py`.
* **`buoi_06/`**: Depth-First Search (DFS) và Iterative Deepening Search (IDS). Chứa `test_dfs_v2.py` và `test_ids.py`.
* **`buoi_07/`**: Tìm kiếm chi phí đồng nhất (Uniform Cost Search - UCS) trong `ucs.py` và Greedy Search trong `gs.py`.
* **`buoi_08/`**: Tìm kiếm có thông tin / Khám phá Heuristic. Chứa các thuật toán ưu tú A* (`a_star.py`) và IDA* (`ida_star.py`).
* **`buoi_09/`**: Tìm kiếm cục bộ (Local Search) cơ bản. Chứa các thuật toán Leo đồi (`simple_hill_climbing.py` và `steepest_ascent_hill_climbing.py`).
* **`buoi_10/`**: Local Search nâng cao. Chứa các biến thể Leo đồi tối ưu (`stochastic_hill_climbing.py`, `random_restart_hill_climbing.py`) và thuật toán Chùm tia (`local_beam_search.py`).
* **`buoi_11/`**: Môi trường khuyết thông tin (Complex Environments). Chứa logic sinh Belief State, Luyện kim nhân tạo (`simulated_annealing.py`), và các biến thể A* phức tạp giải bài toán khuyết:
  * `complex_a_star_missing_input.py`
  * `complex_a_star_missing_goal.py`
  * `complex_a_star_missing_both.py`
* **`buoi_12/`**: Các kiến trúc nâng cao: Backtracking Search (`backtracking_search.py`) và AND-OR Search (`and_or_search.py`).

---

## Hướng dẫn Cài đặt và Chạy ứng dụng

### Yêu cầu hệ thống
* **Ngôn ngữ**: Python 3.8 trở lên.
* **Thư viện**: 
  * Giao diện dùng `tkinter` (thường được cài sẵn cùng với bộ cài Python tiêu chuẩn trên Windows/macOS/Linux).
  * Đối với môi trường Jupyter Notebook trong các buổi học cũ, bạn có thể cần `jupyter`.

### Cách chạy

**1. Clone thư mục dự án và di chuyển đến thư mục chứa project:**
```bash
cd ttnt
```

**2. Khởi chạy Ứng dụng GUI Chính:**
```bash
python main.py
```
*(Lưu ý: Màn hình cần độ phân giải tối thiểu 1100x700 để hiển thị tốt nhất. Ứng dụng có tích hợp DPI Awareness giúp hiển thị sắc nét trên màn hình High DPI của Windows).*

---

## Hướng dẫn Sử dụng Giao diện (Dành cho Giảng viên/Người đánh giá)

1. **Chọn Thuật toán**: Phía panel bên trái, có Dropdown liệt kê tất cả hơn 15+ thuật toán. Khi chọn một thuật toán thuộc nhóm `Complex A*`, giao diện sẽ tự động bật 2 bàn cờ song song để thể hiện trực quan môi trường bất định.
2. **Nhập liệu Trực tiếp**:
   * Chuyển qua lại giữa các tab **Start States** và **Goal States** ở panel bên phải.
   * Bạn có thể bấm nút `+` hoặc `-` để tạo thêm các trạng thái đầu vào/đầu ra khác nhau.
   * Sử dụng phím `Mũi tên (Lên/Xuống/Trái/Phải)` trên bàn phím để di chuyển ô nhập liệu nhanh chóng. Giao diện thay đổi tức thời theo mỗi nút bạn bấm.
3. **Thử nghiệm Ô Khuyết**:
   * Xóa một số và gõ dấu `?` vào ô đó.
   * Chọn một trong 3 thuật toán `Complex A* (Khuyết ... )`.
   * Bấm nút **▶▶ Giải Tất Cả**. Hệ thống sẽ tự động sinh các hoán vị, lọc ra ma trận hợp lệ và tìm một chuỗi hành động duy nhất giải quyết được mọi khả năng có thể xảy ra của dấu `?`.
4. **Đọc Log và Path**:
   * Cột giữa màn hình sẽ phát lại chuỗi hành động `(L ➔ U ➔ R ...)` sau khi tìm được kết quả thành công.
   * Cửa sổ **Log - States Đã Duyệt** ở dưới cùng hiển thị chi tiết lịch sử mọi state mà thuật toán đã duyệt qua (kèm Parent State và điểm số Heuristic `G_Cost`, `H_Cost`). Đóng vai trò làm công cụ debug trực quan tuyệt vời.
