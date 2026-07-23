# tradpas

<p align="center">
  <img src="assets/logo.svg" alt="tradpas logo" width="200">
</p>

> Giao dịch thông minh, tự do tài chính.
> Bot giao dịch Telegram: đọc tín hiệu → Ollama phân tích → gửi kết quả qua bot.
> Android chỉ dùng Telegram app — không cài thêm gì.

------------------------------------------------------------------------

## Tính năng

- **Telegram Signal Listener** — Telethon đọc channel tín hiệu real-time
- **AI Analysis** — Ollama (qwen2.5-coder) phân tích thị trường + tin tức → confidence %
- **Telegram Bot** — Gửi kết quả vào DM + inline keyboard (Vào lệnh / Bỏ qua)
- **Free 100%** — Local LLM (Ollama), không cần API key trả phí
- **Android nhẹ** — Chỉ dùng Telegram app, không cài thêm app
- **Systemd Service** — Chạy nền trên Arch Linux, auto-restart

------------------------------------------------------------------------

## Cấu trúc thư mục

```
tradpas/
├── src/
│   ├── main.py                  # Entry point
│   ├── telegram/                # Telegram listener + parser + bot
│   ├── core/                    # Order dataclass + processor + history
│   └── analysis/                # News + market data + Ollama
├── prompts/                     # Prompt templates
├── tests/                       # Unit tests
├── assets/                      # Logo, images
├── tradpas.service              # systemd unit
├── install.sh                   # Installation script
├── config.example.yaml          # Config mẫu
├── Makefile                     # Build automation
└── *.md                         # Documentation
```

------------------------------------------------------------------------

## Tech Stack

| Layer              | Công nghệ               |
|--------------------|--------------------------|
| Core               | Python 3.12+             |
| Telegram Read      | Telethon                 |
| Telegram Bot       | python-telegram-bot      |
| Local LLM          | Ollama (qwen2.5-coder)   |
| Market Data        | ccxt (Binance public)    |
| News               | feedparser (RSS)         |
| Database           | SQLite                   |
| Service            | systemd                  |

------------------------------------------------------------------------

## Quick Start

```bash
# 1. Clone
git clone https://github.com/tpc-pascal/tradpas.git
cd tradpas

# 2. Cài đặt
./install.sh

# 3. Cấu hình
vim config.yaml
# Điền API Telegram, bot token, channel...

# 4. Chạy
systemctl --user start tradpas
journalctl --user -u tradpas -f
```

Xem chi tiết tại [GUIDE.md](GUIDE.md).

------------------------------------------------------------------------

## License

MIT — xem [LICENSE](LICENSE)
