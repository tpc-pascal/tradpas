#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$REPO_DIR/.venv"
SERVICE_NAME="tradpas.service"

echo "==> tradpas installer"
echo ""

# 1. Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Install it first."
    exit 1
fi
echo "[OK] python3 found: $(python3 --version)"

# 2. Create venv
if [ ! -d "$VENV_DIR" ]; then
    echo "==> Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi
echo "[OK] venv at $VENV_DIR"

# 3. Install dependencies
echo "==> Installing Python packages..."
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -r "$REPO_DIR/requirements.txt"
echo "[OK] Dependencies installed"

# 4. Config
if [ ! -f "$REPO_DIR/config.yaml" ]; then
    echo "==> Creating config.yaml from example..."
    cp "$REPO_DIR/config.example.yaml" "$REPO_DIR/config.yaml"
    echo "[!] Edit $REPO_DIR/config.yaml with your Telegram credentials"
else
    echo "[OK] config.yaml exists"
fi

# 5. Systemd service
SERVICE_DIR="$HOME/.config/systemd/user"
mkdir -p "$SERVICE_DIR"
if [ -f "$REPO_DIR/$SERVICE_NAME" ]; then
    cp "$REPO_DIR/$SERVICE_NAME" "$SERVICE_DIR/$SERVICE_NAME"
    systemctl --user daemon-reload
    echo "[OK] Service installed: $SERVICE_NAME"
    echo "    Run: systemctl --user enable --now tradpas"
else
    echo "[!] $SERVICE_NAME not found, skipping"
fi

# 6. Check Ollama
if command -v ollama &>/dev/null; then
    echo "[OK] Ollama found"
    MODEL=$(grep -A2 'ollama:' "$REPO_DIR/config.yaml" 2>/dev/null | grep 'model:' | awk '{print $2}' || echo "qwen2.5-coder")
    echo "    Model: $MODEL"
else
    echo "[!] Ollama not found. Install it: https://ollama.ai"
fi

echo ""
echo "==> Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Edit config.yaml:"
echo "     vim $REPO_DIR/config.yaml"
echo "  2. Start the service:"
echo "     systemctl --user enable --now tradpas"
echo "  3. Check logs:"
echo "     journalctl --user -u tradpas -f"
