# 🤖 AI Dev Setup Guide

> Hướng dẫn toàn diện thiết lập môi trường AI coding với **nhiều subscription** trong một workflow thống nhất.

## 📑 Mục lục

1. [Kiến trúc tổng quan](#kiến-trúc-tổng-quan)
2. [Yêu cầu](#yêu-cầu)
3. [Quick Start](#quick-start)
4. [Antigravity IDE](#antigravity-ide)
   - [All-in-One Setup](#all-in-one-setup)
   - [Multi-Instance (Multi-Account)](#multi-instance-multi-account)
5. [Antigravity Manager (Proxy)](#antigravity-manager)
6. [Claude Code: Switching Antigravity ↔ Real](#claude-code-switching-giữa-antigravity-và-real)
   - [Shell Functions](#shell-functions-zshrc)
   - [Quy tắc switching](#quy-tắc-switching)
7. [Fix Vietnamese Input (Telex/VNI)](#fix-vietnamese-input-telexvni)
8. [OpenCode: GPT Plus + GitHub Copilot](#opencode-gpt-plus--github-copilot)
9. [Thêm AI Provider mới](#thêm-ai-provider-mới)
10. [Cấu trúc file](#cấu-trúc-file)
11. [Xử lý lỗi thường gặp](#xử-lý-lỗi-thường-gặp)

---

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

## Antigravity IDE

### All-in-One Setup

**Antigravity IDE** là setup all-in-one nhất — trong một cửa sổ duy nhất:

| Tính năng | Mô tả |
|---|---|
| 📂 **Code Editor** | Xem và chỉnh sửa file trực tiếp |
| 💬 **AI Chat** | Chat với Gemini subscription qua Antigravity Tools |
| 🖥️ **Integrated Terminal** | Chạy `claude-anti`, `claude-real`, `opencode` song song |
| 🔧 **Tool Execution** | AI có thể chạy lệnh, đọc file, tìm kiếm web |

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

**Khi nào dùng gì?**

- **Anti IDE** → Chat nhanh, hỏi về code đang mở, brainstorm, review diff
- **claude-anti** → Agentic task dài (viết nhiều file, refactor lớn)
- **claude-real** → Cần track API usage, billing, real Claude output
- **opencode** → Muốn GPT-4o hoặc Copilot completions

### Multi-Instance (Multi-Account)

Chạy **2+ Antigravity IDE** song song với Google accounts khác nhau. Electron enforce single-instance lock → bypass bằng `--user-data-dir` riêng.

#### Tạo instance thứ 2

```bash
osacompile -o "/Applications/Antigravity 2.app" -e \
  'do shell script "\"/Applications/Antigravity.app/Contents/MacOS/Electron\" --user-data-dir=\"" & (POSIX path of (path to home folder)) & "Library/Application Support/Antigravity2\" &"'
```

→ App **Antigravity 2** xuất hiện trong `/Applications`, click mở như app bình thường.

#### Shell aliases (thêm vào `~/.zshrc`)

```bash
# ===== Antigravity IDE Multi-Instance =====
ANTI_BIN="/Applications/Antigravity.app/Contents/MacOS/Electron"

anti1() {
  echo '🚀 Opening Antigravity IDE (Account 1)...'
  "$ANTI_BIN" --user-data-dir="$HOME/Library/Application Support/Antigravity" "$@" &
}

anti2() {
  echo '🚀 Opening Antigravity IDE (Account 2)...'
  "$ANTI_BIN" --user-data-dir="$HOME/Library/Application Support/Antigravity2" "$@" &
}
```

#### Workflow

```
Antigravity IDE (Account 1)    → Project A: code, implement
Antigravity 2   (Account 2)    → Project B: check, review
Terminal: claude-anti           → Agentic tasks (proxy, rotate accounts)
```

> **Lưu ý**: Lần đầu mở `Antigravity 2` cần login Google. Cả 2 dùng chung binary → tự update. Có thể tạo thêm `anti3`, `anti4`...

---

## Antigravity Manager

Antigravity Manager cần **chạy trước** khi dùng `claude-anti`.

- **Port**: `8045`
- **API Key**: `sk-antigravity`
- **Config**: `~/.antigravity_tools/gui_config.json`

```bash
# Kiểm tra Antigravity đang chạy
lsof -i :8045
# hoặc
curl http://127.0.0.1:8045/v1/models \
  -H "Authorization: Bearer sk-antigravity"
```

---

## Claude Code: Switching giữa Antigravity và Real

### `claude-anti` — Antigravity (Gemini Ultra)

```bash
ANTHROPIC_API_KEY="sk-antigravity" \
ANTHROPIC_BASE_URL="http://127.0.0.1:8045" \
claude
```

**Indicator**: Header hiển thị `claude-opus-4-6-thinking · API Usage Billing`
**Nguồn model**: Gemini Ultra (rotate nhiều Google account tự động)

### `claude-real` — Real Claude Team

```bash
claude
```

**Indicator**: Header hiển thị tên account + `Claude Team`

### Shell Functions (`~/.zshrc`)

```bash
# ===== Claude Code Switch =====
# Dùng bản NPM đã patch Vietnamese (cc-vietnamese)
# Thay path dưới đây bằng output của: which claude (sau khi rename native binary)
CLAUDE_NPM="$(which claude)"
unalias claude-anti claude-real 2>/dev/null

claude-anti() {
  export ANTHROPIC_API_KEY="sk-antigravity"
  export CLAUDE_CODE_DISABLE_AUTO_MIGRATE_TO_NATIVE=true
  export DISABLE_INSTALLATION_CHECKS=true
  python3 ~/.claude-switch.py anti
  echo '{"env":{"ANTHROPIC_BASE_URL":"http://127.0.0.1:8045","ANTHROPIC_API_KEY":"sk-antigravity"},"model":"claude-opus-4-6-thinking"}' > ~/.claude/settings.json
  echo '✅ Switched to Antigravity proxy (Vietnamese patched)'
  "$CLAUDE_NPM" "$@"
}

claude-real() {
  export CLAUDE_CODE_DISABLE_AUTO_MIGRATE_TO_NATIVE=true
  export DISABLE_INSTALLATION_CHECKS=true
  python3 ~/.claude-switch.py real
  echo '{}' > ~/.claude/settings.json
  unset ANTHROPIC_API_KEY ANTHROPIC_BASE_URL
  echo '✅ Switched to Claude Team (Vietnamese patched)'
  "$CLAUDE_NPM" "$@"
}
```

### Quy tắc switching

> ⚠️ **QUAN TRỌNG**: Luôn dùng `/exit` để thoát — **KHÔNG** dùng `/logout`

```
claude-anti → /exit → claude-real   ✅
claude-anti → /logout               ❌ (xóa token, mất auth)
```

---

## Fix Vietnamese Input (Telex/VNI)

Claude Code CLI xử lý sai input từ Vietnamese IME (Unikey, OpenKey, EVKey). Cần patch để gõ tiếng Việt bình thường.

### Nguyên lý lỗi

Vietnamese IME gửi: `v → i → e [DEL] ê → t [DEL] ệ → t` (gõ "việt")
Claude Code chỉ xử lý `DEL` rồi return, **mất ký tự thay thế** → text bị vỡ.

### Cài đặt

```bash
# 1. Cài cc-vietnamese CLI
npm install -g cc-vietnamese

# 2. Cài Claude Code bản NPM (song song với native binary)
sudo npm install -g @anthropic-ai/claude-code@latest

# 3. Apply patch vào bản NPM
sudo cc-vietnamese install

# 4. Kiểm tra patch
cc-vietnamese status
# Output: Status: Patched ✓
```

### Bypass Native Binary

> ⚠️ **QUAN TRỌNG**: Claude Code có hệ thống "tengu" tự **delegate sang native binary** (chưa patch). Cần vô hiệu hóa:

```bash
# Rename native binary (giữ backup)
mv ~/.local/bin/claude ~/.local/bin/claude-native-backup

# Verify: which claude phải trỏ đến bản NPM
which claude
# Output: /usr/local/bin/claude (hoặc path NPM của bạn)
```

### Env vars cần thiết

Đã có sẵn trong [Shell Functions](#shell-functions-zshrc):

```bash
export CLAUDE_CODE_DISABLE_AUTO_MIGRATE_TO_NATIVE=true
export DISABLE_INSTALLATION_CHECKS=true
```

### Khôi phục native binary

```bash
mv ~/.local/bin/claude-native-backup ~/.local/bin/claude
```

> **Lưu ý**: Patch cần **re-apply** sau mỗi lần update Claude Code (`sudo cc-vietnamese install`). Xem thêm: [cc-vietnamese](https://www.npmjs.com/package/cc-vietnamese)

---

## OpenCode: GPT Plus + GitHub Copilot

OpenCode kết nối với nhiều AI providers qua OAuth — không cần API key riêng.

```bash
cd your-project
opencode
```

| Lệnh | Mô tả |
|---|---|
| `/connect` | Connect provider |
| `/models` | Switch model |
| `/agents` | Switch agent |
| `/mcps` | Toggle MCPs |
| `/exit` | Thoát |

```bash
# Quản lý providers
opencode auth list      # Xem danh sách
opencode auth logout    # Logout provider
```

---

## Thêm AI Provider mới

### Thêm vào OpenCode (GLM, Kimi, Minimax...)

```bash
opencode auth login
# Chọn provider hoặc "Custom (OpenAI-compatible)"
# Nhập API Base URL và API Key
```

| Provider | Base URL |
|---|---|
| GLM-4 | `https://open.bigmodel.cn/api/paas/v4/` |
| Kimi | `https://api.moonshot.cn/v1` |
| Minimax | `https://api.minimax.chat/v1` |

---

## Cấu trúc file

```
.
├── README.md                    # File này
├── claude-switch.py             # Script backup/restore OAuth token
└── .claude/
    └── settings.local.json      # Claude Code permissions config
```

```json
// .claude/settings.local.json
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

## Xử lý lỗi thường gặp

### Claude-anti: 403 / Connection refused

```bash
# 1. Kiểm tra Antigravity có đang chạy không
lsof -i :8045

# 2. Nếu không có process → mở Antigravity Manager GUI → bật Proxy
# 3. Kiểm tra config
cat ~/.antigravity_tools/gui_config.json
```

### Claude-anti: `effortLevel` API Error 400

```
API Error: 400 Unknown name "effortLevel" at 'request.generation_config'
```

**Nguyên nhân**: Claude Code gửi tham số `effortLevel` mà Gemini API không hỗ trợ.
**Fix**: Update Antigravity Manager lên bản mới nhất, hoặc đổi model mapping:

```json
"custom_mapping": {
  "claude-opus-4-*": "gemini-3-pro"  // thay vì claude-opus-4-5-thinking
}
```

### Claude-anti: Vietnamese input bị lỗi

→ Xem mục [Fix Vietnamese Input](#fix-vietnamese-input-telexvni)

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
