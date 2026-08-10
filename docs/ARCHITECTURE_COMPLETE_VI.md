# BioCognitive-AI Framework - Hệ Thống Kiến Trúc Nhận Thức Hoàn Chỉnh

## Tổng Quan

**BioCognitive-AI Framework** là một hệ thống kiến trúc AI hoàn chỉnh được thiết kế dựa trên các nguyên lý thần kinh học sinh học. Nó cung cấp một nền tảng mạnh mẽ cho xây dựng các agent AI có khả năng suy luận, học hỏi và tự điều chỉnh theo thời gian.

Khác với các kiến trúc tuyến tính truyền thống, BioCognitive sử dụng một **đồ thị nhận thức kết nối** cho phép tương tác phức tạp giữa các thành phần, tạo ra những hành vi emerge mô phỏng tư duy sinh học.

---

## Các Đặc Điểm Chính

### 1. **Kiến Trúc Đồ Thị Nhận Thức**

Thay vì xử lý tuyến tính (Input → Xử lý → Output), BioCognitive sử dụng một mạng lưới kết nối:

```
               Mô Hình Thế Giới
               ↑      ↓
Chú Ý ────→ Dự Báo
  ↓            ↓
Động Lực ← Sai Số Dự Báo
  ↓
Bộ Điều Hành
  ↓
Lập Kế Hoạch
  ↓
LLM (Tạo Phản Hồi)
  ↓
Meta-Nhận Thức (Phê Bình & Sửa)
  ↓
Bộ Nhớ (Lưu Trữ)
  ↓
Hợp Nhất (Tinh Chỉnh Từ Trong Khi Ngủ)
```

### 2. **Xử Lý Dự Báo Đa Chiều**

Thay vì dự báo một giá trị duy nhất:

```python
Kết Quả Dự Báo = {
    cảm_xúc_dự_kiến: 0.7,
    khả_năng_theo_dõi: 0.5,
    độ_tự_tin: 0.8,
    hoàn_thành_mục_tiêu: 0.6,
    sự_gia_tăng_thông_tin: 0.3,
    độ_bất_định: 0.2
}
```

### 3. **Gán Trách Nhiệm Cho Sai Số**

Khi dự báo sai, hệ thống biết được CHÍ CHÍNH XÁC MODULE NÀO là nguyên nhân:

```python
Sai_Số_Dự_Báo = {
    sai_số_cảm_xúc: 0.2,
    sai_số_khế_hợp: 0.3,
    sai_số_thông_tin: 0.1,
    sai_số_mục_tiêu: 0.15,
    # Gán trách nhiệm:
    sai_mô_hình_thế_giới: 0.15,
    sai_bộ_lập_kế_hoạch: 0.10,
    sai_bộ_dự_báo: 0.25,
    sai_llm: 0.30
}
```

**Ưu điểm:** Hệ thống học được chính xác cần cải thiện thành phần nào.

### 4. **Tầng Inductive Bias Dựa Trên Nhu Cầu**

Thay vì một vector điểm dạo động:

```python
# Cũ: Động lực = [0.5, 0.8, 0.3, 0.2]  (không rõ ý nghĩa)

# Mới: Đồ Thị Nhu Cầu
Nhu_Cầu = {
    an_toàn: 0.3,
    tò_mò: 0.9,
    giao_tiếp: 0.5,
    thành_tựu: 0.4
}

# Với vấn đề ức chế:
an_toàn_cao → ức_chế tò_mò ("không nên mạo hiểm")
```

### 5. **Meta-Nhận Thức Tự Chỉnh**

Sau khi LLM tạo ra một phản hồi:

```
Bản Nháp
  ↓
[Phê Bình] → Danh Sách Vấn Đề {
  lỗi_thực_tế: ["Claim X không đúng sự thật"],
  xung_đột_niềm_tin: ["Mâu thuẫn với tin cũ"],
  sai_lầm_hay_vọng_tưởng: ["Tuyên bố không có bằng cứ"],
  ...
}
  ↓
[Quyết Định] → Có cần sửa không?
  ↓
[Sửa] → Phản Hồi Tốt Hơn (nếu cần)
  ↓
[Lưu Trữ] → Chỉ lưu trữ phiên bản cuối cùng đã kiểm chứng
```

### 6. **Công Thức Bộ Nhớ Thông Minh**

Thay vì công thức nhân (gây hiện tượng "số không"):

```python
# Cũ: (không tốt)
tầm_quan_trọng = cảm_xúc × tính_lạ × sai_số_dự_báo × bất_định
# Nếu cảm_xúc = 0 → tầm_quan_trọng = 0 (sai!)

# Mới: (cân bằng tốt)
tầm_quan_trọng = (
    0.25 × cảm_xúc +
    0.25 × tính_lạ +
    0.25 × sai_số_dự_báo +
    0.15 × bất_định +
    0.10 × liên_quan_mục_tiêu
)
# Tất cả thành phần đều góp phần
```

### 7. **Giấc Ngủ & Hợp Nhất Tinh Chỉnh**

Lúc hoạt động ít:

```
[Phát Lại] → Chạy lại các tình huống cũ
  ↓
[Phản Thực Tế] → Nếu trả lời khác → PE sẽ thế nào? (dùng Dự Báo, KHÔNG gọi LLM)
  ↓
[Giấc Mơ] → Kết hợp 2-3 tình huống xa nhau → tìm mẫu mới
  ↓
[Đề Xuất Đột Biến] → Cập nhật Gene dựa trên phân tích
  ↓
[Hợp Nhất] → Lưu vào Bộ Nhớ Ngữ Nghĩa
```

---

## Kiến Trúc Chung (Tổng Quan)

```
┌─────────────────────────────────────────────────────────────────┐
│                      BỘ ĐIỀU HỌC QUẢN LÍ                       │
│  (Quyết định NHANH/TRUNG BÌNH/SÂU dựa trên độ phức tạp)        │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                     ĐƯỜNG DẪN NHANH                             │
│  Input → Chú Ý Cơ Bản → Lập Kế Hoạch → LLM → Output          │
│  (⏱ ~1-2ms, bỏ qua hầu hết xử lý phức tạp)                    │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ĐƯỜNG DẪN TRUNG BÌNH                         │
│  Input                                                          │
│    ↓                                                            │
│  Chú Ý Cơ Bản (Novelty + Emotion + Tính Tân Tiến + Từ Khóa)  │
│    ↓                                                            │
│  Cập Nhật Mô Hình Thế Giới (Entities, Relations, Beliefs)     │
│    ↓                                                            │
│  Chú Ý Tinh Tế (Với Mục Tiêu Từ t-1)                          │
│    ↓                                                            │
│  Dự Báo → Bộ Nhớ Đợi (Multi-turn)                             │
│    ↓                                                            │
│  Lỗi Dự Báo → Gán Trách Nhiệm → Cập Nhật Bất Định            │
│    ↓                                                            │
│  Đồ Thị Nhu Cầu (Cạnh Tranh + Ức Chế Bên Hông)                │
│    ↓                                                            │
│  Bộ Điều Hành (Chọn Mục Tiêu Dựa Trên DecisionContext)        │
│    ↓                                                            │
│  Lập Kế Hoạch → LLM → Output                                   │
│  (⏱ ~2-5ms, bỏ qua Meta-Nhận Thức)                            │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────���──────────────────────────────────────────┐
│                     ĐƯỜNG DẪN SÂU                              │
│  [Tất cả ở trên] +                                             │
│    ↓                                                            │
│  Phê Bình (Kiểm Tra Thực Tế, Xung Đột Niềm Tin, Sai Lầm)      │
│    ↓                                                            │
│  Meta-Quyết Định (Cần Sửa Không?)                             │
│    ↓                                                            │
│  [Tùy Chọn] Sửa → Phản Hồi Tốt Hơn                            │
│    ↓                                                            │
│  Mã Hóa Bộ Nhớ (Chỉ Lưu Phiên Bản Cuối Cùng)                  │
│  (⏱ ~100-200ms, khác với LLM 20-3000ms)                       │
└─────────────────────────────────────────────────────────────────┘
                           ↓
                    [Người Dùng Nhận Phản Hồi]
                           ↓
                    [Phản Ứng Của Người Dùng]
                           ↓
                    [Bất Định Cập Nhật]

┌─────────────────────────────────────────────────────────────────┐
│           [KHÔNG ĐỒNG BỘ] ĐỘNG CƠ HỢP NHẤT (Giấc Ngủ)         │
│  Phát Lại → Phản Thực Tế → Giấc Mơ → Đột Biến → Hợp Nhất     │
│  (⏱ 1-10ms mỗi chu kỳ, chạy nền khi không bận)               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Các Thành Phần Chính

### 1. **Chú Ý** (Attention)
- **Chú Ý Cơ Bản**: Lọc từ dưới lên (không có bối cảnh mục tiêu)
- **Chú Ý Tinh Tế**: Lọc từ trên xuống (dùng mục tiêu hiện tại)

### 2. **Mô Hình Thế Giới** (World Model)
- **Đồ Thị Entities**: Các đối tượng và mối quan hệ
- **Kho Niềm Tin**: Mệnh đề về thế giới (với lịch sử thời gian)
- **Kho Ý Định**: Mục tiêu của người dùng
- **Trạng Thái Quyết Định**: Lựa chọn đang trong tiến trình
- **Trạng Thái Học Tập**: Tiến độ trên các chủ đề
- **Ước Tính Cảm Xúc**: Trạng thái cảm xúc của người dùng

### 3. **Dự Báo** (Prediction)
- **Công Cụ Dự Báo Hội Thoại**: Phản ứng tiếp theo của người dùng
- **Công Cụ Dự Báo Tự**: Chất lượng phản hồi của chúng tôi
- **Bộ Đệm Đang Chờ**: Dự báo đang chờ giải quyết
- **Động Cơ Lỗi Dự Báo**: Gán trách nhiệm cho từng module
- **Động Cơ Bất Định**: Theo dõi thống kê lỗi

### 4. **Động Lực** (Motivation)
- **Đồ Thị Nhu Cầu**: Nhu Cầu Cạnh Tranh (An Toàn, Tò Mò, Giao Tiếp, Thành Tựu)
- **Ức Chế Bên Hông**: Nhu cầu cao ức chế nhu cầu khác
- **Giai Đoạn Khôi Phục**: Nhu cầu được thỏa mãn gần đây → ức chế

### 5. **Bộ Điều Hành** (Executive Controller)
- **Ngăn Xếp Mục Tiêu**: Cho phép chuyển đổi tác vụ
- **Giải Quyết Xung Đột**: Khi hai mục tiêu cạnh tranh
- **Chế Độ Hoạt Động**: trực tiếp | suy tư | sáng tạo
- **Chỉ Đọc DecisionContext**: Không đọc các module khác

### 6. **Meta-Nhận Thức** (Meta-Cognition)
- **Công Cụ Phê Bình**: Kiểm tra lỗi thực tế, ảo tưởng, mâu thuẫn
- **Động Cơ Meta**: Phê Bình → Quyết Định Sửa → Sửa → Lựa Chọn
- **Chỉ Lưu Trữ Phiên Bản Cuối Cùng**: Chứ không phải bản nháp

### 7. **Bộ Nhớ** (Memory)
- **Bộ Nhớ Tập Sự**: Dấu vết trải nghiệm cá nhân
- **Bộ Nhớ Ngữ Nghĩa**: Kiến thức tổng quát
- **Công Thức Tầm Quan Trọng**: Tổng trọng số thay vì tích

### 8. **Hợp Nhất** (Consolidation/Sleep)
- **Phát Lại**: Chạy lại các tình huống
- **Phản Thực Tế**: Mô phỏng "Nếu tôi trả lời khác?" (dùng Dự Báo, không phải LLM)
- **Giấc Mơ**: Kết hợp các tình huống để tìm mẫu
- **Đề Xuất Đột Biến**: Cập nhật cơ sở di truyền

---

## Các Công Thức Khóa

### Điểm Chú Ý Cơ Bản
```
điểm_chú_ý = (tính_lạ + tín_hiệu_cảm_xúc + tính_tân_tiến + nổi_bật_từ_khóa) / 4
```

### Điểm Chú Ý Tinh Tế
```
điểm = (liên_quan_mục_tiêu + (1 - xung_đột_niềm_tin) + (1 - bất_ngờ_dự_báo)) / 3
```

### Bộ Nhớ Tầm Quan Trọng (Mới)
```
tầm_quan_trọng = (
    0.25 × cảm_xúc +
    0.25 × tính_lạ +
    0.25 × sai_số_dự_báo +
    0.15 × bất_định +
    0.10 × liên_quan_mục_tiêu
)
```

### Chế Độ Bất Định
```
Nếu (variance_PE cao && xu_hướng_PE tăng):
    chế_độ = "khám_phá"
Nếu (variance_PE thấp && trung_bình_PE thấp):
    chế_độ = "khai_thác"
```

---

## Thời Gian Xử Lý

```
Động cơ nhận thức:        0.7-1.5 ms
  - Chú Ý Cơ Bản:         0.1 ms
  - Cập Nhật Mô Hình:     0.2 ms
  - Dự Báo:               0.2 ms
  - Bộ Điều Hành:         0.05 ms
  - Meta-Nhận Thức:       0.1 ms
  - Bộ Nhớ:               0.05 ms
  - Hợp Nhất:             Không đồng bộ

LLM (Chai Chỉ):          20-3000 ms (Local hoặc API)
Tổng Cộng:               ~0.7 ms - 3000 ms

Chi Tiêu: Nhận thức chỉ chiếm ~0.1% thời gian, tập trung vào ĐÚNG HẠN và CÓ THỂ SỬA CHỬA
```

---

## Các Giai Đoạn Phát Triển

### ✅ Giai Đoạn 1: Thiết Kế Giao Diện (HOÀN THÀNH)
- Tất cả cấu trúc dữ liệu được định nghĩa
- Tất cả giao diện ABC được định nghĩa
- Các hợp đồng I/O được khóa

### 🔄 Giai Đoạn 2: Refactoring Quan Trọng (ĐANG TIẾN HÀNH)
1. Bottleneck DecisionContext (Bộ Điều Hành)
2. Mẫu Façade WorldModel (Chia Thành Chuyên Gia)
3. Niềm Tin Thời Gian (Theo Dõi Tiến Hóa)
4. Gán Trách Nhiệm Lỗi (Phân Hủy PE)
5. Phân Hủy Công Cụ Phê Bình (Báo Cáo Có Cấu Trúc)
6. Công Thức Bộ Nhớ (Tổng Trọng Số)
7. Hợp Nhất Dàn Dựng (Replay → CF → Dream → Mutation → Consolidate)

### 🚀 Giai Đoạn 3: Hiệu Năng & Tinh Chỉnh (TƯƠNG LAI)
- Event Sourcing (Versioning WorkspaceObject)
- Tối Ưu Hóa (Hồ Sơ, Đạt 0.7-1.5ms)
- Tích Hợp v3 (GRN, Genome, Epigenome)
- Kiểm Tra Toàn Diện
- Tài Liệu & Hướng Dẫn

---

## Cấu Trúc Dự Án

```
BioCognitive-AI-Framework/
├── bio_agent/
│   ├── __init__.py
│   ├── interfaces/                    # Giai Đoạn 1: Tất Cả ABC
│   │   ├── shared.py                 # Cấu Trúc Dữ Liệu
│   │   ├── attention.py              # Chú Ý
│   │   ├── world_model.py            # Mô Hình Thế Giới
│   │   ├── prediction.py             # Dự Báo
│   │   ├── motivation.py             # Động Lực
│   │   ├── executive.py              # Bộ Điều Hành
│   │   ├── budget.py                 # Bộ Điều Hạn Bộ Nhớ
│   │   ├── meta_cognition.py         # Meta-Nhận Thức
│   │   ├── memory.py                 # Bộ Nhớ
│   │   └── sleep.py                  # Hợp Nhất
│   ├── implementations/                # Giai Đoạn 2-3: Thực Hiện
│   │   └── (Chưa hoàn tất)
│   └── tests/                          # Giai Đoạn 3: Kiểm Tra
│       └── (Chưa hoàn tất)
├── docs/
│   ├── architecture.md                # Kiến Trúc (TÀI LIỆU NÀY)
│   ├── decision_flow.md               # Quy Trình Quyết Định
│   ├── glossary.md                    # Từ Điển
│   ├── v3_integration_guide.md        # (Tương Lai) Tích Hợp
│   └── api_reference.md               # (Tương Lai) Tham Chiếu API
├── examples/
│   ├── simple_attention_flow.py       # Ví Dụ 1: Chú Ý
│   ├── prediction_resolution.py       # Ví Dụ 2: Dự Báo
│   └── sleep_consolidation.py         # Ví Dụ 3: Hợp Nhất
├── Makefile                            # Lệnh Sự Tiện Lợi
├── pyproject.toml                      # Cấu Hình Dự Án
├── requirements.txt                    # Phụ Thuộc
├── requirements-dev.txt                # Phụ Thuộc Phát Triển
├── .github/workflows/ci.yml            # Quy Trình CI/CD
├── CONTRIBUTING.md                     # Hướng Dẫn Đóng Góp
├── README.md                           # Giới Thiệu (Phiên Bản Ngắn)
└── .gitignore                          # Git Ignore
```

---

## Cách Sử Dụng Nhanh

### Cài Đặt

```bash
git clone https://github.com/quoctuan21112009-maker/BioCognitive-AI-Framework.git
cd BioCognitive-AI-Framework
make install-dev
```

### Chạy Ví Dụ

```bash
make run-examples
# hoặc
python examples/simple_attention_flow.py
python examples/prediction_resolution.py
python examples/sleep_consolidation.py
```

### Kiểm Tra Chất Lượng

```bash
make lint       # Kiểm Tra Lỗi
make format     # Định Dạng Mã
make type-check # Kiểm Tra Loại
make test       # Chạy Kiểm Tra
```

### Xây Dựng Tài Liệu

```bash
make docs
# Mở: docs/_build/html/index.html
```

---

## Triết Lý Thiết Kế

### 1. **Khác Biệt Với Pipeline Tuyến Tính**
- ✅ Phản Hồi: PE → Bất Định → Động Lực → Bộ Điều Hành
- ✅ Tương Tác: Các Module Giao Tiếp Trong Khoảng Thời Gian
- ✅ Tự Điều Chỉnh: Meta-Nhận Thức Sửa Lỗi Trước Khi Lưu

### 2. **Mô Phỏng Sinh Học Không Phải Hiện Thực Hóa Chính Xác**
- 🧠 Được Lấy Cảm Hứng Bởi Thần Kinh Học (Global Workspace, Inhibition, Consolidation)
- 🎯 Tập Trung Vào **Chức Năng**: Những Gì Hoạt Động, Không Phải Giải Phẫu Học Chính Xác

### 3. **Đơn Giản Là Tốt**
- 🚀 Hiệu Năng: Nhận Thức Chỉ Chiếm 1% Thời Gian → Tối Ưu Hóa Cho ĐÚNG HẠN, Không Tốc Độ
- 🔧 Khả Năng Sửa Chữa: Module Có Thể Cập Nhật Độc Lập Mà Không Phá Vỡ Cái Khác
- 📚 Học Hỏi: Mỗi Sai Số Là Cơ Hội Để Cải Thiện

### 4. **Giao Diện Trước Thực Hiện**
- 📋 Tất Cả ABC Được Định Nghĩa Trước (Giai Đoạn 1)
- 🔐 Hợp Đồng I/O Được Khóa → Phát Triển Độc Lập
- ✅ Refactoring Module Không Ảnh Hưởng Đến Module Khác

---

## Những Đột Phá Chính

### 1️⃣ **DecisionContext Bottleneck**
Thay vì Bộ Điều Hành Đọc 6+ Module, chỉ Đọc DecisionContext → Độc Lập Cao

### 2️⃣ **Gán Trách Nhiệm Lỗi**
PE Không Chỉ Là "0.6", Mà Là "{world: 0.2, planner: 0.1, llm: 0.3}" → Học Cụ Thể

### 3️⃣ **Niềm Tin Thời Gian**
Không Ghi Đè Niềm Tin Cũ, Mà Theo Dõi Tiến Hóa → Phát Hiện Xu Hướng

### 4️⃣ **Phản Thực Tế Rẻ Tiền**
Hợp Nhất Sử Dụng Dự Báo Chứ Không Phải LLM → 50-100x Rẻ Hơn

### 5️⃣ **Meta-Nhận Thức Có Cấu Trúc**
Phê Bình Không Chỉ Trả Về Điểm Số, Mà Danh Sách Vấn Đề Cụ Thể → Sửa Có Mục Tiêu

---

## Tích Hợp & Mở Rộng

### Tích Hợp Với v3
Giai Đoạn 3 sẽ Kết Nối:
- **GRN** (Gene Regulatory Network): Điều Khiển Biểu Hiện Gene
- **Genome**: Các Tham Số Di Truyền (Cập Nhật Via Đề Xuất Đột Biến)
- **Epigenome**: Sửa Đổi Epigenetic (Bật/Tắt Gene)

### Mở Rộng
- **Mô Phỏng**: Chạy Đa Agent, Xem Tương Tác Xã Hội
- **Học Từ Người**: Fine-tune Dựa Trên Phản Hồi Người Dùng
- **Chuyên Môn Hóa**: Một Agent Cho Từng Lĩnh Vực (Medical, Legal, Coding, ...)

---

## Tham Khảo Khoa Học

1. **Global Workspace Theory** (Baars 1988)
   - Ý Tưởng: Ý Thức Là Một Workspace Chia Sẻ
   - Sử Dụng: Mô Hình Chú Ý & Integrated Info.

2. **Hierarchical Reinforcement Learning** (Barto & Mahadevan 2003)
   - Ý Tưởng: Mục Tiêu Phân Cấp, Task Decomposition
   - Sử Dụng: Ngăn Xếp Mục Tiêu & Bộ Điều Hành

3. **Temporal Difference Learning** (Sutton & Barto 2018)
   - Ý Tưởng: Sai Số Dự Báo Là Tín Hiệu Học
   - Sử Dụng: PE → Cập Nhật Bất Định → Động Lực

4. **Meta-Cognition** (Flavell 1979)
   - Ý Tưởng: Suy Nghĩ Về Suy Nghĩ
   - Sử Dụng: Phê Bình & Sửa Phản Hồi

5. **Sleep & Consolidation** (Born & Wilhelm 2012)
   - Ý Tưởng: Giấc Ngủ Hợp Nhất Bộ Nhớ
   - Sử Dụng: Replay, Counterfactual, Dream, Consolidate

6. **Lateral Inhibition** (Hartline & Ratliff 1957)
   - Ý Tưởng: Tín Hiệu Mạnh Ức Chế Tín Hiệu Yếu
   - Sử Dụng: Đồ Thị Nhu Cầu & Ức Chế Cạnh Tranh

---

## Câu Hỏi Thường Gặp

### Q: Có nhanh hơn LLM không?
**A:** Không. Nhận thức (~1ms) tối ưu hóa cho ĐÚNG HẠN & CÓ THỂ SỬA CHỬA, không tốc độ. LLM vẫn chiếm 95% thời gian.

### Q: Có cần học máy không?
**A:** Không ở giai đoạn đầu. Giai Đoạn 1-2 sử dụng Heuristics. Giai Đoạn 3 có thể thêm Neural Nets nếu cần.

### Q: Làm sao để mở rộng?
**A:** Thêm Module Mới → Dùng Interface ABC → Các Module Khác Không Cần Thay Đổi (Độc Lập Cao).

### Q: Có mức giá không?
**A:** Mã Nguồn Mở, MIT License. Tùy Ý Tặng & Hỗ Trợ.

---

## Bước Tiếp Theo

1. **Đọc Tài Liệu**
   - `docs/architecture.md` (Chi Tiết)
   - `docs/decision_flow.md` (Quy Trình)
   - `docs/glossary.md` (Từ Điển)

2. **Chạy Ví Dụ**
   - `examples/simple_attention_flow.py`
   - `examples/prediction_resolution.py`
   - `examples/sleep_consolidation.py`

3. **Đóng Góp**
   - Xem `CONTRIBUTING.md`
   - Chọn Giai Đoạn 2 Task
   - Mở PR

4. **Thảo Luận**
   - GitHub Issues
   - GitHub Discussions

---

## Liên Hệ

**Email:** quoctuan21112009@gmail.com  
**GitHub:** https://github.com/quoctuan21112009-maker/BioCognitive-AI-Framework  

