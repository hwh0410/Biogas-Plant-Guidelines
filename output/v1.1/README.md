# 沼氣場健康檢查手冊 v1.1 四頁樣板

- 開啟 `samples.html`：封面、P03、P05、P10，圖片已內嵌，離線可看。
- `Biogas-Plant-Health-Check-v1.1-samples.pdf`：A4 四頁原生文字 PDF，字型已內嵌。
- `contact-sheet.png`：四頁總覽；`cover.png` / `P03.png` / `P05.png` / `P10.png` 為逐頁預覽。
- `qa-report.json`：本次實測結果，離線與 Chromium 瀏覽器 QA 已通過，專業審查待完成。
- `browser/report.json`：四頁版面、列印、390/768 px 捲動與 v1 搜尋換頁回歸報告。
- `browser/samples-browser-print.pdf`：Chromium 的四頁 A4 列印結果。
- `v1.1-samples-bundle.zip`：可攜式交付包，含圖片原檔、提示詞、審查記錄。

PDF 由共用版面資料原生輸出；HTML 的瀏覽器列印可能有字型差異，正式評估請使用提供的 PDF。HTML 小螢幕可於頁面區左右捲動，390/768 px 捲動已實測，手機流動版尚未製作。

原 v1 封面＋20 頁、PDF、Word、網頁均保留。此版只交付優先四頁樣板，非完整新版全書，亦非正式操作程序。設備與取樣位置示意需工程／工安審查。原圖最低有效約 201 dpi，正式高解析印刷需更高原生解析度素材。

建置（根目錄，已安裝 Pillow/PyMuPDF 的 Python）：
```
python scripts/build.py --v11
python scripts/browser_qa_v11.py
python scripts/qa_v11.py
```

本次建置使用既有 `/Users/huangwenfu/Downloads/pptx_env/bin/python`；瀏覽器測試使用專案 `.venv/bin/python`。專案測試套件與 Chromium 已備妥。瀏覽器與本機測試伺服器在本工作階段需要額外權限核准。
