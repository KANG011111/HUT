# LINE Bot + Google Sheets 專案

這是一個 LINE Bot 應用程式，能夠接收用戶訊息並將其儲存至 Google Sheets。

## 功能特色

- 接收 LINE 用戶訊息
- 自動儲存訊息到 Google Sheets
- 用戶資訊獲取（姓名、ID）
- 訊息時間戳記記錄
- 錯誤處理與日誌記錄
- 支援 Zeabur 部署

## 技術架構

- **後端**: Python 3.9 + Flask
- **LINE SDK**: line-bot-sdk
- **Google API**: gspread + google-auth
- **部署**: Zeabur

## 專案結構

```
linebot-project/
├── app/
│   ├── __init__.py              # Flask 應用程式工廠
│   ├── config.py                # 配置管理
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── line_controller.py   # LINE Webhook 控制器
│   ├── services/
│   │   ├── __init__.py
│   │   ├── line_service.py      # LINE 訊息處理服務
│   │   └── google_sheets_service.py  # Google Sheets 整合
│   └── utils/
│       ├── __init__.py
│       └── logger.py            # 日誌記錄工具
├── main.py                      # 應用程式進入點
├── requirements.txt             # Python 依賴套件
├── runtime.txt                  # Python 版本指定
├── .env.example                 # 環境變數範本
├── .gitignore                   # Git 忽略檔案
└── README.md                    # 專案文檔
```

## 環境設定

### 1. 複製環境變數範本

```bash
cp .env.example .env
```

### 2. 設定環境變數

編輯 `.env` 檔案，填入實際的設定值：

```env
# LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here
LINE_CHANNEL_SECRET=your_channel_secret_here

# Google Sheets 設定
GOOGLE_SHEET_ID=your_google_sheet_id_here
GOOGLE_SERVICE_ACCOUNT_EMAIL=your_service_account_email_here
GOOGLE_PRIVATE_KEY=your_private_key_here

# 伺服器設定
PORT=5000
NODE_ENV=development
```

### 3. 建立虛擬環境

```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境 (Mac/Linux)
source venv/bin/activate

# 啟動虛擬環境 (Windows)
venv\Scripts\activate
```

### 4. 安裝依賴套件

```bash
pip install -r requirements.txt
```

## 本地開發

### 啟動開發伺服器

```bash
python main.py
```

伺服器將在 `http://localhost:5000` 啟動。

### API 端點

- **健康檢查**: `GET /api/health`
- **LINE Webhook**: `POST /api/line/webhook`
- **根路由**: `GET /`

## Google Sheets 設定

### 1. 建立 Google Cloud Project

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用 Google Sheets API 和 Google Drive API

### 2. 建立服務帳戶

1. 前往「IAM 和管理」>「服務帳戶」
2. 建立服務帳戶
3. 下載 JSON 金鑰檔案
4. 從 JSON 檔案中取得 `client_email` 和 `private_key`

### 3. 設定 Google Sheets

1. 建立新的 Google Sheets 試算表
2. 與服務帳戶的 email 分享試算表（編輯權限）
3. 從 URL 取得 Sheet ID

### 4. 工作表結構

| 時間 | 用戶ID | 用戶名稱 | 訊息內容 | 訊息類型 |
|------|--------|----------|----------|----------|
| 2024-01-15 14:30:25 | U1234567890 | 張三 | 你好 | text |

## LINE Bot 設定

### 1. 建立 LINE Bot

1. 前往 [LINE Developers](https://developers.line.biz/)
2. 建立新的 Provider 和 Channel
3. 取得 Channel Access Token 和 Channel Secret

### 2. 設定 Webhook

1. 在 LINE Developers 控制台中
2. 設定 Webhook URL: `https://your-app.zeabur.app/api/line/webhook`
3. 啟用 Webhook

## 部署到 Zeabur

### 1. 推送到 Git Repository

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin your-repo-url
git push -u origin main
```

### 2. 在 Zeabur 控制台部署

1. 登入 [Zeabur](https://zeabur.com/)
2. 選擇「Deploy from Git」
3. 連接 GitHub/GitLab repository
4. 選擇 `main` 分支
5. 設定環境變數
6. 部署完成後獲得 HTTPS URL

### 3. 更新 LINE Webhook URL

使用 Zeabur 提供的 URL 更新 LINE Bot 的 Webhook 設定。

## 日誌記錄

應用程式會自動建立日誌檔案：

- `logs/linebot_YYYY-MM-DD.log` - 一般日誌
- `logs/linebot_error_YYYY-MM-DD.log` - 錯誤日誌

## 故障排除

### 常見問題

1. **環境變數錯誤**
   - 檢查 `.env` 檔案是否正確設定
   - 確認所有必要的環境變數都已設定

2. **Google Sheets 連線失敗**
   - 確認服務帳戶有試算表的編輯權限
   - 檢查 `GOOGLE_PRIVATE_KEY` 是否正確（注意換行符號）

3. **LINE Webhook 驗證失敗**
   - 確認 `LINE_CHANNEL_SECRET` 設定正確
   - 檢查 Webhook URL 是否正確

### 開發除錯

```bash
# 檢查日誌
tail -f logs/linebot_$(date +%Y-%m-%d).log

# 測試 API 端點
curl http://localhost:5000/api/health
```

## 貢獻指南

1. Fork 專案
2. 建立功能分支: `git checkout -b feature/new-feature`
3. 提交變更: `git commit -m 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 建立 Pull Request

## 授權

本專案使用 MIT 授權。

## 聯絡資訊

如有問題或建議，請透過以下方式聯絡：

- GitHub Issues
- Email: your-email@example.com