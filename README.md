# 🤖 AI Dev Setup Guide

> Hướng dẫn toàn diện thiết lập môi trường AI coding với **nhiều subscription** trong một workflow thống nhất.

## Kiến trúc tổng quan

```
┌──────────────────────────────────────────────────────────────────┐
│                        AI Dev Workflow                            │
├──────────────┬──────────────────┬──────────────┬────────────────┤
│  Anti IDE    │   claude-anti    │ claude-real  │   opencode     │
│ (All-in-One) │ (Gemini Ultra)   │(Claude Team) │(GPT + Copilot) │
│              │                  │              │                │
│ IDE + Chat   │ Antigravity      │ Anthropic    │ OpenAI OAuth   │
│ + Terminal   │ Port :8045       │ Real Account │ GitHub OAuth   │
└──────────────┴──────────────────┴──────────────┴────────────────┘
```

| Tool | Provider | Subscription | Dùng khi nào |
|---|---|---|---|
| **Antigravity IDE** | Gemini (Antigravity Tools) | Google Gemini | **All-in-one**: code + chat + terminal |
| `claude-anti` | Gemini Ultra (Antigravity) | Google free quota | Terminal coding, agentic tasks |
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

### Kết nối provider (trong TUI)

Sau khi chạy `opencode`, gõ `/connect` để mở menu kết nối provider:

```
/connect    # Connect provider
/models     # Switch model
/agents     # Switch agent
/mcps       # Toggle MCPs
/exit       # Thoát
```

Browser sẽ mở để đăng nhập OAuth — không cần nhập API key thủ công.

### Chạy OpenCode

```bash
cd your-project
opencode
```

### Xem / xóa providers đã kết nối (CLI)

```bash
opencode auth list      # Xem danh sách providers
opencode auth logout    # Logout provider
```

---

## Antigravity IDE — All-in-One Setup

**Antigravity IDE** (tức là editor này) là setup all-in-one nhất — trong một cửa sổ duy nhất bạn có:

| Tính năng | Mô tả |
|---|---|
| 📂 **Code Editor** | Xem và chỉnh sửa file trực tiếp |
| 💬 **AI Chat** | Chat với Gemini subscription qua Antigravity Tools |
| 🖥️ **Integrated Terminal** | Chạy `claude-anti`, `claude-real`, `opencode` song song |
| 🔧 **Tool Execution** | AI có thể chạy lệnh, đọc file, tìm kiếm web |

### Workflow all-in-one trong Antigravity IDE

```
Antigravity IDE
│
├── Chat panel    → Gemini Ultra (qua Antigravity Tools)
│
├── Terminal 1    → claude-anti (Gemini Ultra cho agentic tasks)
├── Terminal 2    → claude-real (Real Claude Team)
├── Terminal 3    → opencode (GPT Plus + Copilot Pro)
│
└── Editor        → Xem code, diff, review
```

### Khi nào dùng Anti IDE vs terminal tools?

- **Anti IDE** → Chat nhanh, hỏi về code đang mở, brainstorm, review diff
- **claude-anti** → Agentic task dài (viết nhiều file, refactor lớn)
- **claude-real** → Cần track API usage, billing, real Claude output
- **opencode** → Muốn GPT-4o hoặc Copilot completions

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
