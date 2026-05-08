# MOT Thể thao Nâng cao: Theo dõi & Phân tích

Ứng dụng Streamlit này cung cấp một giao diện nâng cao cho việc Theo dõi Đa đối tượng (MOT) trong các video thể thao. Nó tận dụng mô hình YOLO (You Only Look Once) để phát hiện và theo dõi cầu thủ trong thời gian thực, đồng thời cung cấp một bộ công cụ phân tích để đánh giá hiệu suất của cầu thủ và mô hình.

## Tính năng

-   **Theo dõi Cầu thủ Thời gian thực**: Tải lên một video thể thao và xem mô hình phát hiện và theo dõi các cầu thủ theo từng khung hình.
-   **Cấu hình Mô hình Linh hoạt**: Dễ dàng chuyển đổi giữa các mô hình phát hiện và thuật toán theo dõi khác nhau (`ByteTrack`, `BotSort`).
-   **Bảng điều khiển Hiệu suất**: Theo dõi hiệu suất hệ thống (FPS, CPU, RAM) và chất lượng theo dõi (độ tin cậy, số lượng cầu thủ) trong thời gian thực.
-   **Phân tích Nâng cao**:
    -   **Bản đồ Nhiệt di chuyển**: Trực quan hóa vị trí và phạm vi hoạt động của cầu thủ trên sân.
    -   **Quãng đường Di chuyển**: Định lượng chuyển động của cầu thủ bằng cách tính tổng quãng đường đã đi (tính bằng pixel).
    -   **Điểm Tin cậy**: Theo dõi điểm tin cậy trung bình của mô hình theo thời gian.

## Yêu cầu

Trước khi chạy ứng dụng, hãy đảm bảo bạn có:

-   Python 3.8+
-   Một tệp mô hình phát hiện YOLOv8 đã được huấn luyện (ví dụ: `best.pt`).
-   Các gói Python cần thiết, có thể được cài đặt qua `pip`.

## Hướng dẫn Sử dụng

### 1. Cài đặt

Sao chép repository và cài đặt các gói cần thiết bằng tệp `requirements.txt`:

### 2. Chạy Ứng dụng

Khởi chạy ứng dụng Streamlit bằng lệnh sau trong terminal của bạn:

```bash
streamlit run streamlit_app.py
```

Ứng dụng sẽ mở trong trình duyệt web mặc định của bạn.

### 3. Sử dụng Giao diện

1.  **Cấu hình Mô hình**:
    -   Trong thanh bên, chỉ định đường dẫn đến **Mô hình Phát hiện** YOLO của bạn (ví dụ: `best.pt`).
    -   Chọn một **Mô hình Theo dõi** từ danh sách thả xuống (`bytetrack.yaml` hoặc `botsort.yaml`).
    -   Điều chỉnh thanh trượt **Ngưỡng Tin cậy** để lọc bỏ các phát hiện có độ tin cậy thấp.

2.  **Tải lên và Phân tích Video**:
    -   Kéo và thả một tệp video thể thao (MP4, AVI, MOV) vào bảng điều khiển chính.
    -   Nhấp vào nút **"Bắt đầu Theo dõi & Phân tích"** để bắt đầu xử lý.

3.  **Diễn giải Kết quả**:
    -   **Bảng điều khiển Trực tiếp**: Theo dõi các chỉ số hiệu suất thời gian thực cho hệ thống và trình theo dõi.
    -   **Phân tích Trực quan**:
        -   **Theo dõi Trực tiếp**: Xem video với các cầu thủ được xác định bằng các hộp giới hạn và ID duy nhất.
        -   **Bản đồ Nhiệt di chuyển**: Quan sát một bản đồ nhiệt trực quan hóa các khu vực có lưu lượng truy cập cao trên sân.
    -   **Phân tích Dữ liệu**:
        -   **Biểu đồ Tin cậy**: Xem độ tin cậy trung bình của mô hình thay đổi như thế nào trong suốt video.
        -   **Bảng Quãng đường**: Xem lại danh sách xếp hạng 10 cầu thủ hàng đầu theo quãng đường di chuyển.
