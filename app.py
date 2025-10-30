from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TemplateMessage,
    ButtonsTemplate,
    PostbackAction,
    PushMessageRequest,
    BroadcastRequest,
    MulticastRequest,
    TextMessage,
    Emoji,
    VideoMessage,
    AudioMessage,
    LocationMessage,
    StickerMessage,
    ImageMessage,
    ConfirmTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    FlexMessage,
    FlexBubble,
    FlexImage,
    FlexMessage,
    FlexBox,
    FlexText,
    FlexIcon,
    FlexButton,
    FlexSeparator,
    FlexContainer,
    ImagemapArea,
    ImagemapBaseSize,
    ImagemapExternalLink,
    ImagemapMessage,
    ImagemapVideo,
    URIImagemapAction,
    MessageImagemapAction,
    QuickReply,
    QuickReplyItem,
    MessagingApiBlob,
    RichMenuSize,
    RichMenuRequest,
    RichMenuArea,
    RichMenuBounds
)
from linebot.v3.webhooks import (
    MessageEvent,
    FollowEvent,
    PostbackEvent,
    TextMessageContent,
    JoinEvent
)

from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

import requests
import json
import os
import threading
import re
import base64

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#加入好友事件
@line_handler.add(FollowEvent)
def handle_follow(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        welcome_msg = TextMessage(text="歡迎加入！請輸入指令開始使用。")
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[welcome_msg]
            )
        )

@line_handler.add(JoinEvent)
def handle_join(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        welcome_msg = TextMessage(text="大家好！我是精靈Genie\n\n以下是我的點餐功能:\n✅ 開始點餐\n輸入「早餐」、「午餐」、「晚餐」，我就會啟動點餐流程\n\n📝 點餐過程\n各位輸入的訊息都會被我記錄為餐點內容並即時回覆目前的點餐紀錄\n\n🛑 結束點餐\n輸入「結束點餐」，我會統整出餐點清單並結束點餐流程。")
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[welcome_msg]
            )
        )



# Google Sheets 設定
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1SI-w08r6nHoTndKPvP2aWSl3J7CnZJzUPEu3MHTOrFM'  # ← 你的試算表 ID
RANGE_NAME = '工作表1!A:C' # ← 工作表名稱與範圍
# 從 Vercel 環境變數讀取並解碼 Base64 的 JSON 憑證
json_str = base64.b64decode(os.getenv('GOOGLE_CREDENTIALS_BASE64')).decode('utf-8')
json_data = json.loads(json_str)

# 建立憑證物件
credentials = service_account.Credentials.from_service_account_info(json_data, scopes=SCOPES)

# 建立 Google Sheets API 服務
sheets_service = build('sheets', 'v4', credentials=credentials)

#訊息傳送(點餐)
# 記錄每個群組的回覆訊息與點餐狀態
group_replies = {}
group_active = {}

def is_valid_meal(text):
    # 排除 URL 或非餐點內容
    if re.search(r'https?://|\.com|\.tw|\.net|\.org', text):
        return False
    return True

def append_to_sheet(values):
    app.logger.info(f"寫入試算表：{values}")
    body = {
        'values': [values]
    }
    sheets_service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()

def auto_end_order(group_id, line_bot_api):
    if group_active.get(group_id, False):
        if group_id not in group_replies or not group_replies[group_id]:
            summary_text = '點餐結束。此次無任何餐點紀錄。'
        else:
            summary_text = '點餐結束！以下是這次的餐點：\n' + '\n'.join(group_replies[group_id])

        group_replies[group_id] = []
        group_active[group_id] = False

        line_bot_api.push_message(
            PushMessageRequest(
                to=group_id,
                messages=[TextMessage(text=summary_text)]
            )
        )

@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text.strip()
    group_id = event.source.group_id if event.source.type == 'group' else 'private'

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # 開始點餐
        if any(keyword in text for keyword in ['早餐', '午餐', '晚餐']):
            group_active[group_id] = True

            timer = threading.Timer(1800, auto_end_order, args=(group_id, line_bot_api))
            timer.start()

            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='請開始點餐（30分鐘後自動結束）')]
                )
            )
            return

        # 結束點餐
        if text == '結束點餐':
            group_active[group_id] = False

            try:
                result = sheets_service.spreadsheets().values().get(
                    spreadsheetId=SPREADSHEET_ID,
                    range=RANGE_NAME
                ).execute()

                rrows = result.get('values', [])[1:]  # 跳過標題列
                group_meals = [row[1] for row in rows if len(row) >= 2 and str(row[0]).strip() == str(group_id).strip()]

                if not group_meals:
                    summary_text = '點餐結束！此次無任何餐點紀錄。'
                else:
                    summary_text = '點餐結束！以下是這次的餐點：\n' + '\n'.join(group_meals)

                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=summary_text)]
                    )
                )

            except Exception as e:
                app.logger.error(f"結束點餐回覆失敗：{e}")
            return

        # 非點餐狀態下忽略訊息
        if not group_active.get(group_id, False):
            return

        # 餐點處理流程
        if is_valid_meal(text):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            try:
                append_to_sheet([group_id, text, timestamp])
            except Exception as e:
                app.logger.error(f"寫入試算表失敗：{e}")
            
        try:
            result = sheets_service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME
            ).execute()

            rows = result.get('values', [])
            app.logger.info(f"讀取試算表資料：{rows}")

            group_meals = [row[1] for row in rows if len(row) >= 2 and str(row[0]).strip() == str(group_id).strip()]
            current_summary = '\n'.join(group_meals)

            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f'目前點餐紀錄如下：\n{current_summary}')]
                )
            )
        except Exception as e:
            app.logger.error(f"回覆訊息失敗：{e}")

        else:
            try:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text='此內容未被記錄，請輸入餐點名稱')]
                    )
                )
            except Exception as e:
                app.logger.error(f"非餐點內容回覆失敗：{e}")

if __name__ == "__main__":
    app.run()