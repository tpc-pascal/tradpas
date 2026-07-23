# Hướng dẫn sử dụng tradpas

> Phiên bản mới nhất: v1.0.0 — Cài đặt tự động, tích hợp Ollama

------------------------------------------------------------------------

## Yêu cầu

| Thành phần | Yêu cầu |
|------------|---------|
| OS | Arch Linux (hoặc distro có systemd) |
| Python | 3.12+ |
| Ollama | Đã cài, model `qwen2.5-coder` (hoặc tương tự) |
| Telegram API | API ID + API Hash từ [my.telegram.org](https://my.telegram.org/apps) |
| Bot Token | Tạo từ [@BotFather](https://t.me/BotFather) |
| Khác | Git, pip, virtualenv |

------------------------------------------------------------------------

## Cài đặt

### Tự động (khuyên dùng)

```bash
bash <(curl -s https://raw.githubusercontent.com/tpc-pascal/tradpas/main/install.sh)
```

Quy trình:

| Bước | Mô tả |
|------|-------|
| `install.sh` | Kiểm tra Python → tạo venv → pip install → copy config mẫu → cài systemd service |
| Sau đó | Sửa `config.yaml` → `systemctl --user enable --now tradpas` |

### Thủ công

```bash
# 1. Clone
git clone https://github.com/tpc-pascal/tradpas.git
cd tradpas

# 2. Python venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Kiểm tra Ollama
ollama pull qwen2.5-coder
ollama list

# 4. Cấu hình
cp config.example.yaml config.yaml
vim config.yaml

# 5. Systemd service
mkdir -p ~/.config/systemd/user
cp tradpas.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable tradpas
systemctl --user start tradpas
```

------------------------------------------------------------------------

## Cấu hình

```yaml
telegram:
  api_id: 12345
  api_hash: ""
  phone: "+84123456789"
  bot_token: "123456:ABC-DEF..."
  watch_channels:
    - "@signal_channel_1"

analysis:
  ollama:
    model: qwen2.5-coder
    host: http://localhost:11434
  confidence_threshold: 60
  cache_ttl: 300

notify:
  target: ""
```

### Tham số

| Tham số | Mô tả | Mặc định |
|---------|-------|----------|
| `telegram.api_id` | API ID từ my.telegram.org | — |
| `telegram.api_hash` | API Hash từ my.telegram.org | — |
| `telegram.phone` | Số điện thoại (+84...) | — |
| `telegram.bot_token` | Token từ @BotFather | — |
| `telegram.watch_channels` | Danh sách channel tín hiệu | `[]` |
| `analysis.ollama.model` | Model Ollama | `qwen2.5-coder` |
| `analysis.ollama.host` | Địa chỉ Ollama server | `http://localhost:11434` |
| `analysis.confidence_threshold` | Ngưỡng confidence tối thiểu (%) | `60` |
| `analysis.cache_ttl` | Cache TTL (giây) | `300` |
| `notify.target` | Username Telegram nhận kết quả | — |

------------------------------------------------------------------------

## Cách dùng

### Chạy nền (production)

```bash
systemctl --user enable --now tradpas
systemctl --user status tradpas
journalctl --user -u tradpas -f
```

### Chạy debug

```bash
cd tradpas
source .venv/bin/activate
python src/main.py --debug
```

### Dừng

```bash
systemctl --user stop tradpas
systemctl --user disable tradpas
```

### Xem lịch sử lệnh

```bash
cd tradpas
source .venv/bin/activate
python -c "from src.database import db; print(db.get_recent(10))"
```

------------------------------------------------------------------------

## Luồng hoạt động

```
Telegram channel tín hiệu
       │
       ▼
Telethon đọc message real-time
       │
       ▼
Parser → Order { symbol, entry, tp, sl, direction }
       │
       ▼
Ollama phân tích thị trường + tin tức → confidence %
       │
       ▼
Nếu confidence >= threshold ──▶ Bot gửi DM + inline keyboard
       │                               │
       ▼                               ▼
Bỏ qua (log)                 Android nhận notification Telegram
                                  [✅ Vào lệnh]  [❌ Bỏ qua]
```

### Message Bot gửi

```
🟢 BTCUSDT LONG
Entry: 65,000.00
TP:   67,000.00 (+3.08%)
SL:   64,000.00 (-1.54%)
R:R:  2.0
Confidence: 78%

Xu hướng tăng ngắn hạn, khối lượng giao dịch cao.

[✅ Vào lệnh]  [❌ Bỏ qua]
```

------------------------------------------------------------------------

## Fix lỗi thường gặp

### Bot không gửi được message

```bash
# Kiểm tra bot token
curl https://api.telegram.org/bot<TOKEN>/getMe

# Kiểm tra log tradpas
journalctl --user -u tradpas -n 50 --no-pager

# Kiểm tra target username đã đúng chưa
grep target config.yaml
```

### Ollama không chạy

```bash
# Kiểm tra service
systemctl --user status ollama

# Pull model
ollama pull qwen2.5-coder

# Test gọi Ollama
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-coder",
  "prompt": "Hello",
  "stream": false
}'
```

### Permission denied với systemd

```bash
# Dùng user service (không cần sudo)
loginctl enable-linger $USER
systemctl --user enable --now tradpas
```

### Không parse được lệnh

```bash
# Bật debug để xem log chi tiết
python src/main.py --debug
# Kiểm tra format message từ channel có đúng không
```

------------------------------------------------------------------------

## Tác giả

**tpc-pascal** — [GitHub](https://github.com/tpc-pascal)
