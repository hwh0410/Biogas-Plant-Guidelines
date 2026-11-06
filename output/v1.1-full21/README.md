# 沼氣場健康檢查手冊｜封面＋20 頁圖解版

先開啟 `handbook.html` 或 `Biogas-Plant-v1.1-full21.pdf`。

- `pages/cover.png`、`pages/P01.png` 至 `pages/P20.png`：21 張完整頁面圖片，A4 200 dpi。
- `all-21-illustrations.png`：21 張獨立生成原圖的總覽。
- `contact-1.png` 至 `contact-3.png`：全書分組校樣。
- `21-original-illustrations.zip`：21 張原生 PNG、提示詞、生成紀錄與來源 manifest。
- `21-complete-pages.zip`：21 張含完整中文的逐頁 PNG。
- `Biogas-Plant-v1.1-full21-bundle.zip`：完整交付包，包含 PDF、離線 HTML、頁面 PNG、原圖及說明。
- `qa-report.json`：實際建置與檢查結果。

21 張原圖都是本輪獨立生成，每次以兩張官方角色原圖維持角色一致性。中文正文、表格、公式與安全警語由原 JSON 後製，保留正確且可編輯的內容。

原 v1、第一輪及第二輪四頁樣板均保留。工程與工安審查待完成，非施工圖或正式操作程序；不宣稱主圖為原生 300 dpi。圖中儀表色帶與曲線皆為情境示意，不可作安全判斷。

根目錄重建：
```
.venv/bin/python scripts/build_full21.py --browser
.venv/bin/python scripts/build_full21.py --package
```
需要 Pillow、PyMuPDF、Playwright/Chromium、Poppler。瀏覽器啟動與本機伺服器如受沙盒限制，依核准流程執行。
