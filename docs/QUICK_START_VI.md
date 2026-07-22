# 📘 BioCognitive AI Framework - Tóm Tắt Thực Hành

## 🎯 5 Phút Hiểu Rõ Ràng

### Vấn Đề Cũ (Linear Pipeline)
```
Input → Xử Lý → Output
       (Tuyến tính, không phản hồi, khó sửa)
```

### Giải Pháp Mới (Cognitive Graph)
```
       Mô Hình Thế Giới
       ↑      ↓
Chú Ý ← → Dự Báo
↓      ↓
Động Lực ← Sai Số
↓
Bộ Điều Hành ← Meta-Nhận Thức Sửa Lỗi
↓
Output
```

**Ưu Điểm:**
- ✅ Phản Hồi: Lỗi → Cải Thiện
- ✅ Tự Sửa: Phê Bình → Sửa Trước Khi Lưu
- ✅ Học Cụ Thể: Biết Chính Xác Module Nào Cần Cải

---

## 🧠 8 Thành Phần Chính

| # | Thành Phần | Chức Năng | Đầu Ra |
|---|-----------|----------|--------|
| 1 | 👁️ **Chú Ý Cơ Bản** | Lọc Input từ dưới lên | Điểm Saliency |
| 2 | 👁️ **Chú Ý Tinh Tế** | Lọc dùng mục tiêu hiện tại | Điểm Relevance |
| 3 | 🌍 **Mô Hình Thế Giới** | Lưu Entities, Beliefs, Intents | Snapshot |
| 4 | 🔮 **Dự Báo** | Dự đoán Sentiment, Followup, Confidence, Goal, Info | PredictionResult |
| 5 | 🎲 **Sai Số & Bất Định** | Compute PE, attribute to module, track stats | Error + Attribution |
| 6 | 💪 **Động Lực** | Cạnh tranh Need (Safety, Curiosity, ...) | Dominant Need |
| 7 | 🎛️ **Bộ Điều Hành** | Chọn Goal & Mode (direct/reflective/creative) | Executive Decision |
| 8 | 🏠 **Meta-Nhận Thức** | Phê Bình → Quyết Định Sửa → Sửa → Finalize | Final Response |
| 9 | 💾 **Bộ Nhớ** | Lưu trữ phản hồi cuối cùng (không bản nháp) | Episode ID |
| 10 | 😴 **Hợp Nhất** | Phát Lại, Phản Thực Tế, Giấc Mơ, Đột Biến | Gene Mutations |

---

## ⚡ 3 Chế Độ Xử Lý

### 🏃 NHANH (~1-2ms)
Input đơn giản → Chú Ý Cơ Bản → LLM → Output
```
💡 Ví dụ: "2+2=", "hi", "what time is it?"
⏱️ Bỏ qua hầu hết xử lý phức tạp
```

### 🚶 TRUNG BÌNH (~2-5ms)
Như NHANH + Mô Hình Thế Giới + Dự Báo + Động Lực + Bộ Điều Hành
```
💡 Ví dụ: Hỏi bình thường, bao gồm context
⏱️ Bao gồm xử lý nhận thức đầy đủ
```

### 🧑‍🏫 SÂU (~100-200ms)
Như TRUNG BÌNH + Meta-Nhận Thức (Phê Bình + Sửa)
```
💡 Ví dụ: Câu hỏi phức tạp, độ bất định cao
⏱️ LLM có thể gọi lại để sửa (50-100ms thêm)
```

**Auto-Routing:**
```
Bộ Điều Hạn Bộ Nhớ quyết định:
- Đơn Giản? → NHANH
- Bình Thường? → TRUNG BÌNH
- Phức Tạp/Không Chắc? → SÂU
```

---

## 🔑 5 Đột Phá Chính

### 1️⃣ DecisionContext Bottleneck
```python
# Cũ: Bộ Điều Hành Đọc Tất Cả
active_goal = ExecutiveController.current_goal()
needs = MotivationNetwork.snapshot()
world = WorldModel.snapshot()  
uncertainty = UncertaintyEngine.get()
# ❌ Phụ Thuộc Quá Nhiều

# Mới: Bộ Điều Hành Đọc Chỉ DecisionContext
context = DecisionContext(
    active_goal = ...,
    dominant_need = ...,
    uncertainty = ...,
    candidate_actions = ...,
    ...
)
exec_decision = ExecutiveController.decide(context)
# ✅ Phụ Thuộc Rõ Ràng, Dễ Thay Đổi
```

### 2️⃣ Gán Trách Nhiệm Lỗi
```python
# Cũ: PE Là Một Số
error = 0.6  # Sai từ đâu?

# Mới: PE Phân Hủy
error = PredictionError(
    sentiment=0.2,
    followup=0.3,
    info=0.1,
    goal=0.15,
    # Gán Trách Nhiệm:
    world_error=0.15,      # Mô Hình Thế Giới Sai
    planner_error=0.10,    # Lập Kế Hoạch Sai
    prediction_error=0.25, # Dự Báo Sai
    llm_error=0.30         # LLM Sai
)
# ✅ Genome Biết Cần Cập Nhật Gì
```

### 3️⃣ Niềm Tin Thời Gian
```python
# Cũ: Ghi Đè
User.favorite = "Python"  # turn 0
User.favorite = "Rust"    # turn 100 (mất lịch sử)
User.favorite = "Go"      # turn 200

# Mới: Lịch Sử
beliefs = [
    ("Python", turn=0),
    ("Rust", turn=100),
    ("Go", turn=200)
]
# ✅ Dự Báo Thấy Xu Hướng: "Thích Ngôn Ngữ Mới Mỗi 100 Turn"
```

### 4️⃣ Công Thức Bộ Nhớ Thông Minh
```python
# Cũ: Tích (gây Zero-Out)
importance = emotion × novelty × PE × uncertainty
# Nếu emotion=0 → importance=0 (sai!)

# Mới: Tổng Trọng Số
importance = (
    0.25 × emotion +
    0.25 × novelty +
    0.25 × PE +
    0.15 × uncertainty +
    0.10 × goal_relevance
)
# ✅ Tất Cả Thành Phần Đều Góp Phần
```

### 5️⃣ Phản Thực Tế Rẻ Tiền
```python
# Cũ: Hợp Nhất Gọi LLM (3000ms/lần)
for episode in sleep_episodes:
    alt_response = llm.generate_alternative(episode)
    # 💸 3000ms × 100 episodes = 300 giây = 5 phút/đêm

# Mới: Dùng Dự Báo (0.2ms/lần)
for episode in sleep_episodes:
    alt_pe = prediction_engine.estimate_pe(episode, alt_response)
    # 💚 0.2ms × 100 episodes = 20ms = Cực Rẻ
```

---

## 📊 Công Thức Nhanh

### Chú Ý Cơ Bản
```
Score = (Novelty + Emotion + Recency + Keyword) / 4
Lọc top-k → tiếp tục
```

### Chú Ý Tinh Tế (Với Mục Tiêu)
```
Score = (Goal_Relevance + (1-Belief_Conflict) + (1-Prediction_Surprise)) / 3
Cao → Xử Lý Sâu
```

### Sai Số Dự Báo (Magnitude)
```
Magnitude = √((sentiment²+followup²+info²+goal²)/4) / 2
Cao → Tăng Bất Định → Tăng Khám Phá
```

### Bộ Nhớ Tầm Quan Trọng
```
Importance = 0.25×emotion + 0.25×novelty + 0.25×PE + 0.15×uncertainty + 0.10×goal
Kết Quả: [0..1]
```

### Chế Độ Bất Định
```
Nếu variance_PE > 0.1 AND trend_PE > 0:
    mode = "explore"  (thử cái mới)
Nếu variance_PE < 0.1 AND mean_PE < 0.2:
    mode = "exploit"  (tin cái cũ)
```

---

## 🚀 Bắt Đầu

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

### Kiểm Tra Code
```bash
make lint      # Lỗi
make format    # Định Dạng
make type-check # Loại
make test      # Kiểm Tra
```

---

## 📚 Tài Liệu Thêm

| File | Nội Dung |
|------|----------|
| `docs/architecture.md` | Kiến Trúc Đầy Đủ (5000 từ) |
| `docs/decision_flow.md` | Quy Trình Turn-by-Turn |
| `docs/glossary.md` | Từ Điển & Khái Niệm |
| `CONTRIBUTING.md` | Hướng Dẫn Đóng Góp |
| `examples/*.py` | Mã Ví Dụ Chạy Được |

---

## 🎓 Học Hỏi Thêm

- **Global Workspace Theory**: Baars 1988
- **Hierarchical RL**: Barto & Mahadevan 2003
- **Temporal Difference**: Sutton & Barto 2018
- **Meta-Cognition**: Flavell 1979
- **Sleep Consolidation**: Born & Wilhelm 2012

---

## ❓ FAQ

**Q: Có nhanh hơn LLM không?**
A: Không. Nhận thức ~1ms vs LLM 20-3000ms. Tối ưu cho ĐÚNG HẠN, không tốc độ.

**Q: Có phải học máy không?**
A: Không bắt buộc. Giai Đoạn 1-2 dùng Heuristics. Giai Đoạn 3 có thể thêm.

**Q: Có thể mở rộng không?**
A: Dễ. Thêm Module → Dùng Interface → Các Module Khác Không Đổi (Độc Lập Cao).

**Q: Giá tiền?
A: Mã Nguồn Mở, MIT License. Tùy Ý Hỗ Trợ.

---

## 📞 Liên Hệ

**Email:** quoctuan21112009@gmail.com  
**GitHub:** https://github.com/quoctuan21112009-maker/BioCognitive-AI-Framework  


---


