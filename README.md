# Hệ Thống Chuyên Gia Tư Vấn Pháp Lý

> Hệ thống tư vấn pháp lý thông minh sử dụng **Fuzzy Logic (Mamdani)**, giao diện **PyQt6**, kiến trúc **MVC**, thiết kế **plugin-based** có khả năng mở rộng.

## 📋 Tổng Quan

Hệ thống hỗ trợ tư vấn pháp lý cho 3 nghiệp vụ trong lĩnh vực **Luật Đất đai 2024**:

| Module | Mô tả | Biến đầu vào |
|--------|--------|--------------|
| 🔄 Chuyển nhượng QSD đất | Đánh giá tính khả thi chuyển nhượng | Pháp lý, Giá trị, Diện tích, Vị trí, Nghĩa vụ TC |
| 💰 Bồi thường thu hồi đất | Đánh giá mức bồi thường | Loại đất, Thời gian SD, Diện tích, Hệ số K, Tái định cư |
| ⚖️ Vi phạm hành chính | Đánh giá mức xử phạt | Mức độ VP, Diện tích VP, Thời gian, Tái phạm, Thiệt hại |

## 🏗️ Kiến Trúc

```
┌─────────────────────────────────────────────────────┐
│                Presentation Layer (PyQt6)            │
│  Login │ Dashboard │ Consultation │ Management       │
├─────────────────────────────────────────────────────┤
│                Controllers (MVC)                     │
│  Auth │ Consultation │ Legal │ Rule │ User │ History │
├─────────────────────────────────────────────────────┤
│              Application Layer (Modules)             │
│  Transfer │ Compensation │ Violation │ [Extensible]  │
├────────────────────┬────────────────────────────────┤
│   Fuzzy Engine     │      Legal Engine              │
│   (Mamdani)        │      (Citations)               │
├────────────────────┴────────────────────────────────┤
│              Core Layer                              │
│  Database (SQLite) │ Auth │ Config                   │
└─────────────────────────────────────────────────────┘
```

## 🚀 Cài Đặt & Chạy

### 1. Yêu cầu
- Python 3.10+
- pip

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy ứng dụng
```bash
python main.py
```

### 4. Đăng nhập mặc định
| Username | Password | Role |
|----------|----------|------|
| admin | 123456 | Quản trị viên |
| staff01 | 123456 | Nhân viên |
| expert01 | 123456 | Chuyên gia |

## 📁 Cấu Trúc Project

```
JOB_01/
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── config/settings.py       # Cấu hình hệ thống
├── core/
│   ├── database.py          # SQLite manager (singleton)
│   └── auth.py              # Authentication service
├── models/                  # Data models (ORM-like)
│   ├── user.py, legal.py, rule.py, case.py
├── engines/
│   ├── fuzzy_engine.py      # Fuzzy Logic Engine (Mamdani)
│   └── legal_engine.py      # Legal citation engine
├── modules/                 # Plugin-based modules
│   ├── base_module.py       # Abstract base class
│   ├── module_loader.py     # Dynamic loader
│   ├── transfer/            # Chuyển nhượng QSD đất
│   ├── compensation/        # Bồi thường thu hồi
│   └── violation/           # Vi phạm hành chính
├── controllers/             # MVC controllers
├── views/                   # PyQt6 views
│   ├── styles.py            # QSS dark theme
│   ├── login_view.py
│   ├── main_window.py       # Sidebar + stacked views
│   ├── dashboard_view.py
│   ├── consultation_view.py # Dynamic form + results
│   ├── legal_management_view.py
│   ├── rule_management_view.py
│   ├── user_management_view.py
│   └── history_view.py
├── data/
│   ├── schema.sql           # Database schema
│   ├── seed_data.sql        # Sample data
│   └── sample_rules.json    # Import example
└── utils/helpers.py         # Utilities
```

## 📖 Hướng Dẫn Sử Dụng Hệ Thống

### 1. Quản Lý Văn Bản Pháp Lý (Dành cho Admin/Chuyên gia)
Mục này cho phép bạn quản lý các tài liệu, nghị định, bộ luật để làm cơ sở trích dẫn cho kết quả tư vấn.
- **Thêm Văn Bản Mới**:
  - Chọn nút **Thêm Văn Bản** ở cột trái.
  - Điền thông tin: Mã số (vd: `LDD2024`), Tên văn bản (vd: `Luật Đất đai 2024`), Cơ quan ban hành, Ngày có hiệu lực, và Mô tả (hoặc Link tra cứu).
  - Nhấn **Lưu thay đổi** để cập nhật vào hệ thống.
- **Quản Lý Điều Luật chi tiết**:
  - Khi click chọn một Văn bản bên danh sách trái, cột phải sẽ hiển thị các Điều luật thuộc văn bản đó. 
  - Nhấn **Thêm Điều Luật** để bổ sung chi tiết (vd: Mã điều: `D15`, Tên: `Điều 15`, Nội dung: `Quy định về...`).
- **Sửa / Xóa**: 
  - Chọn văn bản/điều luật cần thao tác. Nhấn **Xóa** (nút màu đỏ) để loại bỏ. Để sửa, chỉ cần thay đổi thông tin trên Form và nhấn **Lưu**.

### 2. Quản Lý Luật Suy Diễn (Fuzzy Rules Management)
Hệ chuyên gia hoạt động dựa trên các quy tắc Logic mờ (Nếu A và B thì C). Bạn có thể toàn quyền tùy chỉnh bộ não của hệ thống tại đây.
- **Cấu trúc của một Luật (Rule)**:
  - **Module**: Nghiệp vụ áp dụng (vd: `tax`, `transfer`, `compensation`).
  - **Mã luật (Rule ID)**: Mã định danh duy nhất (vd: `R001_Tax`).
  - **Kết luận (Conclusion)**: Tập mờ đầu ra (vd: `high`, `low`, `medium`).
  - **Trọng số (Weight)**: Độ mạnh/ưu tiên của luật (từ `0.1` đến `1.0`).
- **Cách viết Điều Kiện (JSON Format)**:
  - Tập hợp các điều kiện đầu vào (Mệnh đề IF) phải được viết dưới chuẩn **JSON Array**.
  - Ví dụ: Để thiết lập quy tắc *"NẾU Vị trí là Nông thôn VÀ Diện tích Nhỏ"*, bạn điền vào ô **Điều kiện (JSON)** như sau:
    ```json
    [
      {"variable": "location_type", "term": "rural"},
      {"variable": "area_size", "term": "small"}
    ]
    ```
    *(Lưu ý: Thuộc tính `variable` và `term` phải khớp chính xác với các biến đã được cấu hình trong file `config.json` của từng Module).*
- **Thêm / Trạng Thái Luật**:
  - Nhấn **Thêm Luật** -> Nhập đầy đủ thông tin (JSON hợp lệ) -> **Lưu Luật**.
  - Nút **Tắt / Bật (Toggle)**: Bạn có thể tạm thời vô hiệu hóa một luật thay vì xóa bỏ nó, hệ thống sẽ bỏ qua luật này khi tư vấn.

## 🔧 Mở Rộng Module Mới

### Ví dụ: Thêm module "Thuế đất đai"

1. **Tạo thư mục module:**
```
modules/tax/
├── __init__.py
├── config.json
└── module.py
```

2. **Tạo config.json:**
```json
{
  "module": "tax",
  "display_name": "Thuế đất đai",
  "icon": "💲",
  "input_variables": [
    {
      "name": "land_value",
      "label": "Giá trị đất",
      "range": [0, 10],
      "membership_functions": [
        {"name": "low", "type": "triangular", "params": [0, 0, 5]},
        {"name": "high", "type": "triangular", "params": [5, 10, 10]}
      ]
    }
  ],
  "output_variable": {
    "name": "tax_rate",
    "label": "Thuế suất",
    "range": [0, 100],
    "membership_functions": [
      {"name": "low_tax", "type": "triangular", "params": [0, 0, 50]},
      {"name": "high_tax", "type": "triangular", "params": [50, 100, 100]}
    ]
  },
  "input_fields": [
    {"name": "land_value", "label": "Giá trị đất", "type": "slider",
     "min": 0, "max": 10, "step": 0.5, "default": 5}
  ]
}
```

3. **Tạo module.py:**
```python
from modules.base_module import BaseModule
import os, json

class TaxModule(BaseModule):
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = json.load(f)

    def get_name(self): return "tax"
    def get_display_name(self): return "Thuế đất đai"
    def get_description(self): return "Tư vấn thuế đất đai"
    def get_icon(self): return "💲"
    def get_config(self): return self._config
    def get_input_fields(self): return self._config["input_fields"]

    def interpret_result(self, score, conclusion):
        return {
            "level": "medium",
            "title": f"Thuế suất: {score:.1f}%",
            "color": "#f39c12",
            "description": f"Mức thuế đánh giá: {score:.1f}/100",
            "recommendations": ["Tham khảo cơ quan thuế"]
        }
```

4. **Thêm rules vào database** (hoặc import từ JSON)
5. **Khởi động lại ứng dụng** - Module sẽ tự động được phát hiện!

## 📊 Fuzzy Logic Engine

### Quy trình xử lý
1. **Fuzzification**: Chuyển giá trị crisp → fuzzy (triangular/trapezoidal MFs)
2. **Rule Evaluation**: AND (min), weighted rules
3. **Aggregation**: MAX operator
4. **Defuzzification**: Centroid method

### Membership Functions
- **Triangular**: `[a, b, c]` - tam giác
- **Trapezoidal**: `[a, b, c, d]` - hình thang

## 📜 Cơ Sở Pháp Lý

- Luật Đất đai 2024 (Luật số 31/2024/QH15)
- Nghị định 88/2024/NĐ-CP (Bồi thường, tái định cư)
- Nghị định 91/2019/NĐ-CP (Xử phạt VPHC đất đai)
- Luật Công chứng 2014

## 🔮 Kế Hoạch Mở Rộng

- [ ] Tích hợp FastAPI cho web service
- [ ] Chatbot pháp lý (NLP)
- [ ] Nâng cấp PostgreSQL
- [ ] Thêm module: Dân sự, Hợp đồng, Lao động
- [ ] Export PDF báo cáo tư vấn
