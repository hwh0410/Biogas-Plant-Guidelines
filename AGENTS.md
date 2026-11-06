# AGENTS.md — Biogas Plant Handbook (Mac Codex)

## 任務與工作環境
此 repo 是《沼氣場健康檢查手冊》。使用者要求將 v1 文字與功能完整保留，改做專業但親民、設備造型半寫實的 v1.1 高品質圖解出版版面。重要程度：圖片真實感、專業圖解、吉祥物連貫、頁面設計；絕對不要用幾何 SVG 和純文字框假裝完成 AI 高品質主視覺。

## 必須先讀
- `CODEX_TASK.md`、`LOCAL_SETUP.md`
- `README.md`、`docs/visual-redesign-v1.1.md`、`docs/outline-v0.1.md`
- `docs/mascot-spec-v0.2.md`、`docs/visual-spec-v0.2.md`
- `docs/review-checklist.md`、`content/handbook.json`
- `qa/report.json`、`scripts/build.py`、`web/`

## 固定角色圖（本地已具備）
- `assets/mascot/reference/mascot-character-sheet-v0.1.png`
- `assets/mascot/reference/mascot-pose-sheet-v0.1.png`
不得改寫、重繪成別的機器人或覆蓋 master。導出新姿態、透明圖可保存至 `assets/mascot/poses/`。

## 原始技術來源
`reference/109年度沼氣再利用(發電)推廣與沼氣發電機操作手冊.pdf`。此為內容參考，不等於所有老舊設定可作當代標準。技術及安全須明示待專業審查。

## 改版原則
- 封面、P03、P05、P10 四頁設計樣板先行，再擴展其餘頁。
- AI 生成設備插畫須提供可用原圖檔；沒有圖片生成工具就誠實說明，不要用簡單 SVG 假冒。
- AI 負責設備情境，中文字、管線箭頭與量測點由 HTML/SVG/CSS 疊加可編輯內容。
- 設備須具工業結構可信度，不能引入不可靠的安全操作步驟。
- 先查目前程式的架構，不破壞 v1 的輸出和測試。
- 不自動 push 或部署公開版本；完成本地檢查後提示使用者確認（除非用戶在 Codex 當次明確授權）。
- 用 git 留存階段 checkpoint，但不要把原始大型 PDF 推送到 GitHub，除非明確確認授權和需要；可以將 reference/ 加入 .gitignore。

## 交付與驗收
v1.1 新目錄/檔名，包含封面+3頁樣板 HTML/PDF、可追溯的生成圖片、來源與提示詞、排版 QA、後續20頁對應表。後續再組完整 A4 21 頁 PDF/可編輯 DOCX。

## 最新使用者修正：第二輪視覺樣板
使用者明確指出「同一隻」不等於直接裁切原圖；角色必須有情境互動，並調整整體風格與排版。自 v1.1-r2 起，每張角色圖須以兩張 master PNG 作參考重新生成動作及情境，不以 poses/ 裁切圖作成品。此項使用者修正優先於 CODEX_TASK.md 先前「優先裁切」策略。詳見 docs/v1.1-r2-design-review.md；第一輪成品保留供比較。

## 最新交付範圍：全書 21 張
使用者進一步授權直接按 20 頁內容各自生成圖片，另加封面。最新完整版本為 assets/illustrations/v1.1-full21/ 與 output/v1.1-full21/；原生插畫與含完整正文的頁面 PNG 分開保存。中文、表格、公式及警語由既有 JSON 後製保持正確。舊版不覆蓋。
