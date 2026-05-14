# HƯỚNG DẪN VÀ GIẢI THÍCH CHI TIẾT HỆ THỐNG CHUYÊN GIA TƯ VẤN PHÁP LÝ

Tài liệu này cung cấp cái nhìn tổng quan về cách sử dụng hệ thống, cũng như đi sâu vào kiến trúc cốt lõi giúp hệ thống có thể "suy nghĩ" và đưa ra lời khuyên pháp lý: **Hệ thống Suy diễn mờ (Fuzzy Inference System)**.

---

## PHẦN 1: CÁCH SỬ DỤNG HỆ THỐNG

### 1. Phân quyền và Đăng nhập
Hệ thống được thiết kế dành cho nhiều đối tượng với các quyền hạn khác nhau:
- **Quản trị viên (Admin)**: Có toàn quyền (Quản lý người dùng, quản lý văn bản, quản lý luật, xem toàn bộ lịch sử).
- **Chuyên gia (Expert)**: Có quyền tư vấn, thêm/sửa/xóa các Quy tắc logic (Luật) để làm hệ thống thông minh hơn, quản lý văn bản pháp lý.
- **Nhân viên (Staff)**: Chỉ có quyền thực hiện tư vấn cho khách hàng và xem lịch sử tư vấn.

### 2. Các chức năng chính
- **Dashboard (Tổng quan)**: Hiển thị thống kê số lượt tư vấn, biểu đồ tròn phân bố theo từng lĩnh vực (Thuế, Chuyển nhượng, Bồi thường,...).
- **Tư vấn pháp lý**: Là trái tim của ứng dụng. Bạn chọn một Nghiệp vụ (Module), hệ thống sẽ tự động vẽ ra các Form nhập liệu phù hợp (Ví dụ: Module Thuế sẽ hỏi về *Diện tích, Vị trí, Loại đất*). Sau khi điền, nhấn "Phân tích", hệ thống sẽ trả về số điểm đánh giá, mức độ rủi ro/thuế suất, và trích dẫn các văn bản luật liên quan.
- **Quản lý Văn bản**: Nơi lưu trữ các nghị định, luật (Ví dụ: Luật Đất đai 2024). Khi có luật mới, chuyên gia có thể thêm vào hệ thống để làm cơ sở pháp lý.
- **Quản lý Luật (Rule Management)**: Nơi chuyên gia định nghĩa cách mà hệ thống "suy nghĩ". Bạn có thể thêm các luật IF-THEN dạng JSON vào đây.

---

## PHẦN 2: HỆ THỐNG HOẠT ĐỘNG NHƯ THẾ NÀO?

Thay vì sử dụng các cấu trúc `IF-ELSE` cứng nhắc (ví dụ: *Nếu diện tích < 50m2 thì thuế là 10%*), hệ thống sử dụng **Logic Mờ (Fuzzy Logic)**. Logic mờ cho phép hệ thống tư duy giống con người hơn, xử lý các khái niệm tương đối như "Khá rộng", "Rất đắt", "Gần trung tâm".

Quy trình hoạt động của hệ thống khi bạn nhấn nút "Phân tích" diễn ra qua 4 bước:

### Bước 1: Mờ hóa (Fuzzification)
Khi người dùng nhập một giá trị thực (Crisp value), ví dụ: `Điểm vị trí = 7/10`.
Hệ thống không đánh giá cứng nhắc 7 là "Tốt", mà nó sẽ tính toán **Độ phụ thuộc (Membership degree)** vào các tập mờ.
- Ví dụ: Điểm 7 có thể thuộc tập "Trung bình" với độ tin cậy là `0.3`, và thuộc tập "Tốt" với độ tin cậy là `0.7`.
*Hệ thống sử dụng các hàm liên tục (Hình tam giác - Triangular) được cấu hình trong tệp `config.json` để tính toán điều này.*

### Bước 2: Đánh giá Tập luật (Rule Evaluation)
Hệ thống sẽ lấy toàn bộ các **Luật (Rules)** trong Cơ sở dữ liệu ra để đối chiếu. Một luật có dạng:
> **NẾU** Vị trí là "Tốt" **VÀ** Diện tích là "Lớn" **THÌ** Thuế suất là "Cao".

Nếu người dùng nhập: Vị trí "Tốt" (độ tin cậy 0.7), Diện tích "Lớn" (độ tin cậy 0.5).
Do dùng phép **VÀ (AND)**, hệ thống áp dụng **toán tử MIN**. Nó sẽ lấy giá trị nhỏ nhất: `MIN(0.7, 0.5) = 0.5`.
=> Vậy kết luận: Thuế suất là "Cao" đạt độ tin cậy là `0.5`.

*Đặc biệt*: Hệ thống hỗ trợ **Trọng số (Weight)** cho luật. Nếu một luật rất quan trọng, trọng số = 1.0. Nếu luật mang tính phụ trợ, trọng số = 0.5. Độ tin cậy cuối cùng sẽ được nhân thêm với Trọng số này.

### Bước 3: Tổng hợp (Aggregation)
Sẽ có hàng chục luật cùng đưa ra kết luận.
- Luật 1 bảo: Thuế "Cao" với độ tin cậy `0.5`.
- Luật 2 bảo: Thuế "Cao" với độ tin cậy `0.8`.
Hệ thống sẽ tổng hợp lại bằng **toán tử MAX**. Nó sẽ gộp tất cả các hình vẽ đồ thị của kết luận lại với nhau, tạo thành một vùng diện tích chung đại diện cho kết quả. (Trong trường hợp này, mức độ "Cao" tối đa là `0.8`).

### Bước 4: Giải mờ (Defuzzification)
Khách hàng không thể hiểu kết quả là "Thuế Cao với độ tin cậy 0.8". Họ cần một con số cụ thể.
Hệ thống sử dụng phương pháp **Tính trọng tâm (Centroid)**. Nó sẽ quét qua 1000 điểm trên vùng diện tích tổng hợp ở Bước 3, tìm ra "trung tâm khối lượng" của đồ thị đó, và gióng xuống trục hoành để lấy ra một con số duy nhất.
=> Kết quả trả về: **76.5 điểm** (Quy ra là Rủi ro/Thuế suất Cao).

---

## PHẦN 3: CÁCH QUẢN LÝ VÀ VIẾT TẬP LUẬT (RULE SETS)

Để hệ thống thông minh, Chuyên gia cần truyền đạt kiến thức của mình dưới dạng các tập luật thông qua màn hình **Quản lý Luật**.

### 1. Biến ngôn ngữ (Linguistic Variables)
Mỗi Module (nghiệp vụ) đã được định nghĩa sẵn các biến trong tệp `config.json`.
- **Ví dụ Module Thuế**: Có biến đầu vào `location_type` (Vị trí) và `land_value` (Giá trị đất).
- Mỗi biến có các **Tập mờ (Terms)**: `low` (thấp), `medium` (trung bình), `high` (cao).
- Biến đầu ra: `tax_rate` (Thuế suất) với các terms: `low_tax`, `medium_tax`, `high_tax`.

### 2. Viết luật (Mệnh đề IF)
Hệ thống yêu cầu Mệnh đề IF phải được viết dưới dạng mảng JSON. 
Ví dụ, bạn muốn viết luật: *"NẾU Vị trí là Kém (low) VÀ Giá trị đất là Thấp (low)"*
Bạn sẽ nhập vào ô "Điều kiện (JSON)":
```json
[
  {"variable": "location_type", "term": "low"},
  {"variable": "land_value", "term": "low"}
]
```
*(Hệ thống tự động hiểu đây là phép toán AND giữa các điều kiện).*

### 3. Kết luận (Mệnh đề THEN)
Ở ô **Kết luận**, bạn chỉ cần điền tên của tập mờ đầu ra. Với ví dụ trên, bạn điền: `low_tax`.

### 4. Xử lý các trường hợp phức tạp (Edge Cases)
- **Thiếu quy tắc**: Nếu người dùng nhập một tổ hợp dữ liệu mà chưa có bất kỳ luật nào bao phủ (ví dụ Nhỏ + Đắt tiền), hệ thống sẽ không thể giải mờ và trả về 0. Do đó, tập luật phải bao phủ toàn bộ các tổ hợp logic có thể xảy ra (Ví dụ: 3 biến, mỗi biến 3 trạng thái => Cần có đủ 27 luật để phủ kín).
- **Điểm biên**: Nhờ sự tối ưu hóa của Hệ thống, khi người dùng chọn điểm tuyệt đối (0 hoặc 10), hệ thống vẫn tự động nội suy độ phụ thuộc hoàn hảo (1.0) để đảm bảo luật được kích hoạt nhạy bén nhất.

Tóm lại, sự thông minh của hệ thống này phụ thuộc hoàn toàn vào **Chất lượng và Số lượng của Tập Luật** do các Chuyên gia pháp lý nạp vào. Thuật toán Fuzzy Engine chỉ đóng vai trò xử lý toán học để chuyển đổi cảm quan của chuyên gia thành những con số chính xác.
