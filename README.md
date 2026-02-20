# 🤖 AI Dev Setup Guide

> Hướng dẫn toàn diện thiết lập môi trường AI coding với **nhiều subscription** trong một workflow thống nhất.

## Kiến trúc tổng quan

```
┌─────────────────────────────────────────────────────────┐
│                   AI Dev Workflow                        │
├──────────────────┬──────────────────┬───────────────────┤
│   claude-anti    │   claude-real    │    opencode       │
│  (Gemini Ultra)  │  (Claude Team)   │  (GPT + Copilot)  │
│                  │                  │                   │
│  Antigravity     │  Anthropic API   │  OpenAI OAuth     │
│  Port :8045      │  Real Account    │  GitHub OAuth     │
└──────────────────┴──────────────────┴───────────────────┘
```

| Tool | Provider | Subscription | Dùng khi nào |
|---|---|---|---|
| `claude-anti` | Gemini Ultra (Antigravity) | Google free quota | Coding hàng ngày, agentic tasks |
| `claude-real` | Claude Opus 4.6 | Claude Team | Cần real Claude, billing tracking |
| `opencode` | GPT-4o + Copilot Pro | ChatGPT Plus + GitHub | GPT perspective, Copilot completions |

---

## Yêu cầu

- macOS 13+ (Ventura trở lên)
- [Antigravity Manager](https://github.com/lbjlaq/Antigravity-Manager) v4.0+ (chạy port `8045`)
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) v2.1+
- [OpenCode](https://opencode.ai) (terminal AI coding assistant)
- Python 3.8+

---

## Quick Start

```bash
# Clone repo
git clone https://github.com/hutune/claude-code-switch-guide
cd claude-code-switch-guide

# Setup shell functions
curl -o ~/.claude-switch.py https://raw.githubusercontent.com/hutune/claude-code-switch-guide/main/claude-switch.py
# Thêm functions vào ~/.zshrc (xem hướng dẫn chi tiết bên dưới)

# Chạy tool theo nhu cầu
claude-anti    # Gemini Ultra qua Antigravity
claude-real    # Real Claude Team
opencode       # GPT + Copilot
```

---

## Claude Code: Switching giữa Antigravity và Real

### `claude-anti` — Antigravity (Gemini Ultra)

```bash
# Chạy Claude Code qua Antigravity proxy
ANTHROPIC_API_KEY="sk-antigravity" \
ANTHROPIC_BASE_URL="http://127.0.0.1:8045" \
claude
```

**Indicator**: Header hiển thị `claude-opus-4-6-thinking · API Usage Billing`  
**Nguồn model**: Gemini Ultra (rotate nhiều Google account tự động)

### `claude-real` — Real Claude Team

```bash
# Chạy Claude Code với real Anthropic account
claude
```

**Indicator**: Header hiển thị tên account + `Claude Team`

### Shell Functions (`~/.zshrc`)

```bash
# Thêm vào ~/.zshrc
claude-anti() {
  python3 ~/.claude-switch.py anti && \
  ANTHROPIC_API_KEY="sk-antigravity" \
  ANTHROPIC_BASE_URL="http://127.0.0.1:8045" \
  claude "$@"
}

claude-real() {
  python3 ~/.claude-switch.py real && claude "$@"
}
```

### Quy tắc switching

> ⚠️ **QUAN TRỌNG**: Luôn dùng `/exit` để thoát — **KHÔNG** dùng `/logout`

```
claude-anti → /exit → claude-real   ✅
claude-anti → /logout               ❌ (xóa token, mất auth)
```

---

## OpenCode: GPT Plus + GitHub Copilot

OpenCode kết nối với nhiều AI providers qua OAuth — không cần API key riêng.

### Xem providers đang kết nối

```bash
opencode auth list
```

### Kết nối provider mới (OAuth)

```bash
opencode auth login [url]
```

Ví dụ:
```bash
opencode auth login          # Interactive — chọn provider từ menu
opencode auth login github   # Kết nối GitHub Copilot Pro trực tiếp
opencode auth login openai   # Kết nối OpenAI / ChatGPT Plus
```

Sau khi chạy lệnh, browser sẽ mở để đăng nhập OAuth. Không cần nhập API key.

### Logout provider

```bash
opencode auth logout
```

### Chạy OpenCode

```bash
cd your-project
opencode
```

Trong OpenCode TUI, dùng phím tắt để switch model giữa GPT-4o và Copilot.

---

## Antigravity Manager

Antigravity Manager cần **chạy trước** khi dùng `claude-anti`.

- **Port**: `8045`
- **API Key**: `sk-antigravity`
- **Config**: `~/.antigravity_tools/gui_config.json`

### Kiểm tra Antigravity đang chạy

```bash
lsof -i :8045
# hoặc
curl http://127.0.0.1:8045/v1/models \
  -H "Authorization: Bearer sk-antigravity"
```

---

## Cấu trúc file

```
.
├── README.md                    # File này
├── claude-switch.py             # Script backup/restore OAuth token
└── .claude/
    └── settings.local.json      # Claude Code permissions config
```

### `.claude/settings.local.json`

```json
{
  "permissions": {
    "allow": [
      "WebSearch",
      "Bash(brew install:*)",
      "Bash(opencode)"
    ]
  }
}
```

---

## Thêm AI Provider mới

### Thêm vào OpenCode (GLM, Kimi, Minimax...)

```bash
opencode auth login
# Chọn provider hoặc "Custom (OpenAI-compatible)"
# Nhập API Base URL và API Key
```

Ví dụ các provider OpenAI-compatible:
| Provider | Base URL | 
|---|---|
| GLM-4 | `https://open.bigmodel.cn/api/paas/v4/` |
| Kimi | `https://api.moonshot.cn/v1` |
| Minimax | `https://api.minimax.chat/v1` |

---

## Xử lý lỗi thường gặp

### Claude-anti: 403 / Connection refused

```bash
# 1. Kiểm tra Antigravity có đang chạy không
lsof -i :8045

# 2. Nếu không có process → mở Antigravity Manager GUI → bật Proxy
# 3. Kiểm tra config
cat ~/.antigravity_tools/gui_config.json
```

### Claude-anti: Hỏi "Do you want to use this API key?"

→ Chọn `1. Yes` (lần đầu chạy)

### OpenCode: OAuth token hết hạn

```bash
opencode auth logout
opencode auth login
```

---

## License

MIT
