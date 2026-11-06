# Windows full21 建置

指定來源維持 `assets/illustrations/v1.1-full21/` 與 `content/handbook.json`，不生成圖片、不呼叫 API。Windows 測試輸出另存 `output/v1.1-full21-windows/`，保留所有歷史版本。

## PowerShell 指令

在專案根目錄執行。從 Mac 複製的 `.venv` 不可沿用，請另建 Windows 環境。

```powershell
py -3 -m venv .venv-windows
.\.venv-windows\Scripts\python.exe -m pip install -r requirements-full21-windows.txt
.\.venv-windows\Scripts\python.exe -m playwright install chromium
powershell -NoProfile -ExecutionPolicy Bypass -File .\build-full21-windows.ps1 -Python .\.venv-windows\Scripts\python.exe -Pdftoppm 'C:\tools\poppler\Library\bin\pdftoppm.exe'
```

Poppler 路徑依實際安裝位置調整；也可把其 bin 加入 PATH，或設定 `PDFTOPPM` 環境變數後直接執行 Python 腳本。工具須來自受信任的安裝來源。若無 Poppler，可明確選擇既有 PyMuPDF 渲染器：

```powershell
.\.venv-windows\Scripts\python.exe scripts/build_full21.py --browser --output-dir output/v1.1-full21-windows --renderer pymupdf
```

兩種方式皆輸出 A4 200 dpi；QA 記錄實際 renderer，不混稱 Poppler 結果。聯絡表字型自動偵測 Windows 微軟正黑體／Mac Arial Unicode／Linux DejaVu Sans，可用 `--font` 指定。網頁加入微軟正黑體備援；所有文字檔明確以 UTF-8 讀寫。

建置包含 21 頁、離線圖片、搜尋後全書列印、390／768 px、溢出與完整 PDF 內文檢查。另以執行前 SHA-256 快照確認素材及其他既有產物未變更，不再依賴 Mac 的 Git 執行環境。這是本次執行的保留檢查，並非歷史 commit 比對。產出後仍須檢視聯絡表及完整頁面；腳本不再自動宣稱人工視覺驗收完成。

## 2026-11-06 實測

- Python 語法、CLI 參數、所有文字讀寫明確指定 UTF-8：通過。
- 21 張原圖對 manifest、2 張官方角色 master 雜湊：通過；既有離線 HTML 頁碼 cover／P01–P20：通過。
- 新建置實際執行：停在缺少 Pillow；未產生新 PDF／頁面 PNG，未覆寫原交付。
- 本機僅找到 Google Cloud SDK 的 Python 3.14.7 可啟動；原附 Windows venv 指向不存在的 Python312，repo venv 為 Mac ARM。
- 嘗試在交接根目錄 `.venv-windows` 安裝免費本機建置套件，連線 PyPI 被環境拒絕（WinError 10013）。Poppler／Git 亦未找到，所以沒有本地 commit。
- 完整紀錄與現有成果雜湊：`qa/windows-compatibility-report.json`。此報告不把舊 QA 當成本次 Windows 輸出驗收。

依賴安裝完成後重跑上述指令，再檢視 `output/v1.1-full21-windows/contact-*.png` 與全頁 PNG。工程／安全審查狀態延續原版。
