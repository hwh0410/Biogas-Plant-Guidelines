# Mac 本機啟動、依賴與排錯

Windows 最新封面＋20 頁版請見 [Windows full21 建置](docs/windows-full21-build.md)。使用獨立環境及輸出目錄，勿沿用 Mac `.venv`。

## 一鍵合併
雙擊 `setup-mac.command`，或在解壓目錄中執行：

```bash
bash setup-mac.command
```

它會從 `https://github.com/itribioenergy/Biogas-Plant-Guidelines.git` 下載 main 最新版本，複製官方 PNG + 109 年原始 PDF、AGENTS.md、CODEX_TASK.md 到新資料夾 `Biogas-Plant-Guidelines/`。

**重要：本 ZIP 沒有內含 GitHub 最新程式碼本體**，因封包製作環境無法連線 GitHub。Mac 第一次執行時必須能連到 GitHub；如果私有化或需要登入，請先完成 GitHub 憑證授權。

## 安裝 Codex CLI
參照官方 https://github.com/openai/codex 或 https://learn.chatgpt.com/docs/codex/cli ，可在 macOS 使用：

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

或已安裝 npm 時：

```bash
npm install -g @openai/codex
```

然後：

```bash
cd "~/Downloads/Biogas-Plant-Codex-Mac-Handoff/Biogas-Plant-Guidelines"  # 依實際解壓位置調整
codex
```

Codex 第一次開啟依指示用新的 ChatGPT 帳號登入。輸入：

`請讀取 CODEX_TASK.md 和 AGENTS.md，直接開始執行。`

## 網頁預覽
```bash
cd Biogas-Plant-Guidelines
python3 -m http.server 8000
```
瀏覽 `http://localhost:8000/web/`。或直接雙擊 `output/standalone.html`。

## PDF/Word 建置
原 repo `requirements.txt`、`scripts/build.py`、`.github/workflows/handbook.yml` 為主要線索。macOS 的系統字型與瀏覽器環境不同，請 Codex 先閱讀腳本再決定要裝什麼套件。

## 有關 AI 圖像生成
Codex CLI 是程式代理，不保證在任意環境自動具備圖片生成 API；請先查可用工具或外部圖片生成服務及費用，經使用者確認後使用。若沒有工具，先把圖像生成 prompts、資產位置與匯入流程實作完成。

## 請勿
- 不要一開始就 push 或覆蓋 v1。
- 不要把 PDF 中舊年代參數當現行法規或所有設備通用設定。
- 不要在沒有工程審查下把 AI 畫的設備接管當作施工圖。
