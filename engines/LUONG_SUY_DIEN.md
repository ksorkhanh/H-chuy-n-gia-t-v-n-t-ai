# KIẾN TRÚC SUY DIỄN VÀ LUỒNG DỮ LIỆU HỆ THỐNG

Tài liệu này mô tả chi tiết cách hệ thống nạp dữ liệu từ tri thức chuyên gia (Luật) và thực hiện suy diễn mờ để đưa ra tư vấn pháp lý.

---

## 1. QUÁ TRÌNH NẠP DỮ LIỆU (DATA LOADING)

Quá trình này xảy ra khi người dùng bắt đầu một phiên tư vấn cho một Module cụ thể (ví dụ: Thuế đất đai).

### Bước 1: Nạp cấu hình biến mờ (Tĩnh)
- **File:** `modules/[module_name]/config.json`
- **Hàm thực hiện:** `FuzzyEngine.load_config(config)`
- **Nội dung:** 
    - Định nghĩa các biến đầu vào (ví dụ: `dien_tich`, `loai_dat`).
    - Định nghĩa các hàm liên thuộc (Membership Functions) như `Thấp`, `Trung bình`, `Cao`.
    - Thiết lập các thông số hình học [a, b, c] cho Tam giác hoặc [a, b, c, d] cho Hình thang.

### Bước 2: Nạp tập luật suy diễn (Động)
- **File:** `models/rule.py` & `expert_system.db`
- **Hàm thực hiện:** `Rule.get_by_module(module_name)` sau đó nạp vào `FuzzyEngine.load_rules_from_db(rule_models)`.
- **Nội dung:** 
    - Lấy các luật thật từ Cơ sở dữ liệu SQLite.
    - Cấu trúc luật: `IF (Biến A là Tập X) AND (Biến B là Tập Y) THEN (Kết luận là Tập Z)`.
    - Mỗi luật liên kết với một ID điều khoản pháp lý (`legal_article_id`).

---

## 2. QUY TRÌNH SUY DIỄN CHI TIẾT (INFERENCE PROCESS)

Khi người dùng nhấn nút "Chạy tư vấn", luồng xử lý sẽ đi qua 3 lớp chính:

### Lớp 1: Giao diện (Views)
- **File:** `views/consultation_view.py`
- **Hàm:** `_on_run()`
- **Nhiệm vụ:** Thu thập giá trị rõ (Crisp input) từ các thanh trượt/combo box và gửi đến Controller.

### Lớp 2: Điều phối (Controllers)
- **File:** `controllers/consultation_controller.py`
- **Hàm:** `run_consultation(module_name, inputs)`
- **Nhiệm vụ:**
    1. Khởi tạo `FuzzyEngine`.
    2. Nạp Config và Rules (như mô tả ở phần 1).
    3. Gọi `fuzzy.run(inputs)` để lấy điểm số mờ.
    4. Gọi `LegalEngine.get_articles_for_rules()` để lấy trích dẫn luật dựa trên các luật đã khớp.

### Lớp 3: Động cơ cốt lõi (Engines)
Đây là nơi thực hiện tính toán toán học tại `engines/fuzzy_engine.py`:

| Giai đoạn | Hàm trong `fuzzy_engine.py` | Mô tả toán học |
|:---|:---|:---|
| **1. Mờ hóa** | `fuzzify(inputs)` | Chuyển giá trị thực (ví dụ: 50m2) thành độ liên thuộc [0, 1] cho các tập mờ (ví dụ: Rộng: 0.8, Vừa: 0.2). |
| **2. Đánh giá luật** | `evaluate_rules()` | Sử dụng toán tử **MIN** (And) để tính độ kích hoạt (Firing Strength) của từng luật. |
| **3. Tổng hợp** | `aggregate()` | Sử dụng toán tử **MAX** (Or) để kết hợp các kết quả của tất cả luật đã kích hoạt thành một hình học mờ duy nhất. |
| **4. Giải mờ** | `defuzzify()` | Sử dụng phương pháp **Trọng tâm (Centroid)**: Tính toán điểm cân bằng của hình học tổng hợp để đưa ra điểm số cuối cùng (0-100). |

---

## 3. SƠ ĐỒ LUỒNG DỮ LIỆU (FLOWCHART)

```mermaid
graph TD
    A[Người dùng nhập liệu] -->|Giá trị rõ| B(ConsultationController)
    
    subgraph "Nạp Tri Thức"
        C[(Database - Rules)] --> B
        D[config.json - Variables] --> B
    end

    B --> E{FuzzyEngine}
    
    subgraph "Quy trình Fuzzy"
        E --> F[Fuzzify]
        F --> G[Rule Evaluation - MIN]
        G --> H[Aggregation - MAX]
        H --> I[Defuzzify - Centroid]
    end
    
    I -->|Điểm số| J(LegalEngine)
    J -->|Tìm điều khoản| K[Kết quả & Trích dẫn Luật]
    K --> L[Hiển thị cho người dùng]
```

---

## 4. VÍ DỤ THỰC TẾ
Nếu hệ thống có luật: `IF (Diện tích là Lớn) AND (Vị trí là Đẹp) THEN (Mức bồi thường là Cao)`

1. **Nạp dữ liệu:** Hệ thống nạp luật này từ DB và định nghĩa "Lớn", "Đẹp", "Cao" từ file json.
2. **Mờ hóa:** Diện tích 100m2 $\rightarrow$ "Lớn" đạt 0.9. Vị trí loại 1 $\rightarrow$ "Đẹp" đạt 1.0.
3. **Suy diễn:** Độ kích hoạt = `min(0.9, 1.0) = 0.9`.
4. **Kết quả:** Tập mờ "Cao" sẽ bị cắt ở mức 0.9 và đưa vào tính toán trọng tâm để ra số tiền bồi thường cụ thể.
