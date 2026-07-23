# Hướng dẫn đóng góp

Vui lòng đọc kỹ các hướng dẫn dưới đây trước khi bắt đầu đóng góp.

------------------------------------------------------------------------

## 1. Thiết lập môi trường

```bash
git clone https://github.com/tpc-pascal/tradpas.git
cd tradpas
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

------------------------------------------------------------------------

## 2. Quy trình gửi đóng góp

1. **Fork** dự án về tài khoản cá nhân
2. **Tạo branch mới:**
   - Tính năng mới: `git checkout -b feat/ten-tinh-nang`
   - Sửa lỗi: `git checkout -b fix/ten-loi`
   - Tài liệu: `git checkout -b docs/ten-tai-lieu`
3. **Commit:** Một commit duy nhất cho một feature — title format:
   ```
   feat: v<version> - <mô tả>
   fix: v<version> - <mô tả>
   docs: v<version> - <mô tả>
   ```
4. **Push & PR:** Đẩy branch lên GitHub, tạo Pull Request vào nhánh `main`.

------------------------------------------------------------------------

## 3. Quy chuẩn viết mã

- **Python 3.12+** — Type hints bắt buộc
- **Snake_case** — Function, biến: `snake_case`; Class: `PascalCase`; Hằng: `UPPER_CASE`
- **Ruff** format + lint — Kiểm tra trước commit
- **Không comment giải thích code** — Trừ khi thật sự cần thiết
- **Idempotent** — Hàm có thể chạy lại nhiều lần không gây lỗi
- **Error handling** — Dùng logger, không `print()`
- **Config** — Mọi tham số qua `config.yaml`, không hardcode

### Ví dụ

```python
def parse_order(raw: str) -> Order | None:
    try:
        ...
        return Order(...)
    except ValueError:
        logger.error("Cannot parse order: %s", raw)
        return None
```

------------------------------------------------------------------------

## 4. Cấu trúc thư mục

```
tradpas/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── logger.py
│   ├── database.py
│   ├── telegram/
│   │   ├── listener.py
│   │   ├── parser.py
│   │   └── bot.py
│   ├── core/
│   │   ├── order.py
│   │   ├── processor.py
│   │   └── history.py
│   └── analysis/
│       ├── news.py
│       ├── market.py
│       └── analyzer.py
├── prompts/
│   └── analyze.txt
├── tests/
├── tradpas.service
├── install.sh
├── config.example.yaml
├── requirements.txt
├── Makefile
└── *.md
```

------------------------------------------------------------------------

## 5. Kiểm thử

```bash
# Chạy tất cả tests
pytest

# Coverage
pytest --cov=src tests/

# Kiểm tra lint
ruff check src/
ruff format --check src/
```

Trước khi gửi PR, đảm bảo:
- Code chạy không lỗi trên máy cá nhân
- `pytest` pass
- `ruff check` không lỗi
- Không ảnh hưởng tính năng cũ

------------------------------------------------------------------------

## 6. Build

```bash
make build    # Tạo distributable package
make install  # Cài đặt local
```

------------------------------------------------------------------------

## Liên hệ

- [Mở Issue](https://github.com/tpc-pascal/tradpas/issues)
- [Discussions](https://github.com/tpc-pascal/tradpas/discussions)
