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

## Fix Vietnamese Input (Telex/VNI)

Claude Code CLI mặc định xử lý sai input từ Vietnamese IME (Unikey, OpenKey, EVKey). Cần patch để gõ tiếng Việt bình thường.

### Nguyên lý lỗi

Vietnamese IME gửi input dạng:
```
v → i → e [DEL] ê → t [DEL] ệ → t    (gõ "việt")
```
Claude Code chỉ xử lý ký tự `DEL` rồi return, **mất ký tự thay thế** → text bị vỡ.

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

> ⚠️ **QUAN TRỌNG**: Dù gọi bản NPM đã patch, Claude Code có hệ thống "tengu" tự **delegate sang native binary** (chưa patch). Cần vô hiệu hóa:

```bash
# Rename native binary (giữ backup)
mv ~/.local/bin/claude ~/.local/bin/claude-native-backup

# Verify: which claude phải trỏ đến bản NPM
which claude
# Output: /usr/local/bin/claude (hoặc path NPM của bạn)
```

### Env vars cần thiết

Thêm vào shell functions (xem mục Shell Functions bên dưới):

```bash
export CLAUDE_CODE_DISABLE_AUTO_MIGRATE_TO_NATIVE=true
export DISABLE_INSTALLATION_CHECKS=true
```

### Khôi phục native binary

```bash
# Nếu muốn quay lại native binary (không có Vietnamese fix)
mv ~/.local/bin/claude-native-backup ~/.local/bin/claude
```

### Lưu ý

- Patch cần **re-apply** sau mỗi lần update Claude Code (`sudo cc-vietnamese install`)
- Xem thêm: [cc-vietnamese](https://www.npmjs.com/package/cc-vietnamese)

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

## Antigravity IDE — Multi-Instance (Multi-Account)

Mặc định chỉ chạy được **1 Antigravity IDE** vì Electron enforce single-instance lock. Trick: chạy binary trực tiếp với `--user-data-dir` riêng để bypass.

### Tạo instance thứ 2

```bash
# Tạo AppleScript app wrapper
osacompile -o "/Applications/Antigravity 2.app" -e \
  'do shell script "\"/Applications/Antigravity.app/Contents/MacOS/Electron\" --user-data-dir=\"" & (POSIX path of (path to home folder)) & "Library/Application Support/Antigravity2\" &"'
```

→ App **Antigravity 2** xuất hiện trong `/Applications`, click mở như app bình thường.

### Shell aliases (thêm vào `~/.zshrc`)

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

### Workflow 2 accounts song song

```
Antigravity IDE (Account 1)    → Project A: code, implement
Antigravity 2   (Account 2)    → Project B: check, review
Terminal: claude-anti           → Agentic tasks (dùng proxy, rotate cả 2 accounts)
```

### Lưu ý

- Mỗi instance có **data directory riêng** → login Google account khác nhau
- Lần đầu mở `Antigravity 2` sẽ cần **login Google** (instance mới, chưa có session)
- Cả 2 dùng cùng binary gốc → **tự động update** khi Antigravity update
- Có thể tạo thêm `anti3`, `anti4`... nếu cần nhiều accounts hơn

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

### Claude-anti: `effortLevel` API Error 400

```
API Error: 400 Unknown name "effortLevel" at 'request.generation_config': Cannot find field.
```

**Nguyên nhân**: Claude Code gửi tham số `effortLevel` (cho thinking models) mà Gemini API không hỗ trợ.

**Fix**: Update Antigravity Manager lên bản mới nhất, hoặc đổi model mapping trong `~/.antigravity_tools/gui_config.json`:

```json
"custom_mapping": {
  "claude-opus-4-*": "gemini-3-pro"  // thay vì claude-opus-4-5-thinking
}
```

### Claude-anti: Vietnamese input bị lỗi

→ Xem mục [Fix Vietnamese Input](#fix-vietnamese-input-telexvni) ở trên

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
