# 沼氣場健康檢查手冊｜第二輪視覺樣板

- `samples.html`：離線四頁預覽，手機會直向重排。
- `Biogas-Plant-Health-Check-v1.1-r2.pdf`：與 HTML 同來源的 A4 四頁 PDF。
- `contact-sheet.png`：四頁總覽；`cover.png`、`P03.png`、`P05.png`、`P10.png` 為逐頁瀏覽器預覽。
- `mobile-390.png`、`mobile-768.png`：實際手機寬度截圖。
- `qa-report.json`：版面、完整原文與前版保留檢查。
- `v1.1-r2-bundle.zip`：含成品、四張原圖、兩張角色參考、原始提示詞及製作文件。

本輪以每次帶入兩張官方 PNG 重新生成角色參與情境；未使用裁切姿態圖。角色會導覽場區、指引模型、看槽外儀表及記錄量測。前版仍在 output/v1.1/，可比較。

在專案根目錄重建（需要已安裝的 Pillow、PyMuPDF、Playwright 及 Chromium）：
```
.venv/bin/python scripts/build_v11_r2.py --browser
```
沙盒若限制 Chromium／本機伺服器，需透過既有額外權限核准流程執行。

原圖約 194–232 有效 dpi；這是美術與內容溝通樣板，不是 300 dpi 印刷定稿、施工圖或正式操作程序。工程與工安審查仍待完成。
