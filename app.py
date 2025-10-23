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
    TextMessageContent
)

import requests
import json
import os

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

# # 訊息事件(輸入postback, linebot回覆按鈕)
# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         if event.message.text == 'postback':
#             buttons_template = ButtonsTemplate(
#                 title='Postback Sample',
#                 text='Postback Action',
#                 actions=[
#                     PostbackAction(label='Postback Action', text='Postback Action Button Clicked!', data='postback'),
#                 ])
#             template_message = TemplateMessage(
#                 alt_text='Postback Sample',
#                 template=buttons_template
#             )
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[template_message]
#                 )
#             )
        
# @handler.add(PostbackEvent)
# def handle_postback(event):
#     if event.postback.data == 'postback':
#         print('Postback event is triggered')

# 訊息事件(訊息推送以及回覆功能)
# @handler.add(MessageEvent, message=TextMessageContent)
# def message_text(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
        
        # Reply message

        # line_bot_api.reply_message(
        #     ReplyMessageRequest(
        #         reply_token=event.reply_token,
        #         messages=[TextMessage(text ='reply message')]
        #     )
        # )

        # result = line_bot_api.reply_message_with_http_info(
        #     ReplyMessageRequest(
        #         reply_token=event.reply_token,
        #         messages=[TextMessage(text = "reply message with http info")]
        #     )
        # )

        # Push message
        # line_bot_api.push_message_with_http_info(
        #     PushMessageRequest(
        #         to=event.source.user_id,
        #         messages=[TextMessage(text='PUSH!')]
        #     )
        # )

        # Broadcast message
        # line_bot_api.broadcast_with_http_info(
        #     BroadcastRequest(
        #         messages=[TextMessage(text='BROADCAST!')]
        #     )
        # )

        # Multicast message
        # line_bot_api.multicast_with_http_info(
        #     MulticastRequest(
        #         to=['U2523f12efc62a10443c93abb089a432f'],
        #         messages=[TextMessage(text='MULTICAST!')],
        #         notificationDisabled=True #是否靜音傳送
        #     )
        # )

#訊息回覆(各類型訊息)
# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     text = event.message.text
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)

#         if text == '文字':
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[TextMessage(text="這是文字訊息")]
#                 )
#             )
#         elif text == '表情符號':
#             emojis = [
#                 Emoji(index=0, product_id="5ac1bfd5040ab15980c9b435", emoji_id="001"),
#                 Emoji(index=12, product_id="5ac1bfd5040ab15980c9b435", emoji_id="002")
#             ]
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[TextMessage(text='$ LINE 表情符號 $', emojis=emojis)]
#                 )
#             )
#         elif text == '貼圖':
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[StickerMessage(package_id="446", sticker_id="1988")]
#                 )
#             )
#         elif text == '圖片':
#             url = request.url_root + 'static/Logo.jpg'
#             url = url.replace("http", "https")
#             app.logger.info("url=" + url)
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[
#                         ImageMessage(original_content_url=url, preview_image_url=url)
#                     ]
#                 )
#             )
#         elif text == '影片':
#             url = request.url_root + 'static/video.mp4'
#             url = url.replace("http", "https")
#             app.logger.info("url=" + url)
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[
#                         VideoMessage(original_content_url=url, preview_image_url=url)
#                     ]
#                 )
#             )
#         elif text == '音訊':
#             url = request.url_root + 'static/music.mp3'
#             url = url.replace("http", "https")
#             app.logger.info("url=" + url)
#             duration = 60000  # in milliseconds
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[
#                         AudioMessage(original_content_url=url, duration=duration)
#                     ]
#                 )
#             )
#         elif text == '位置':
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[
#                         LocationMessage(title='Location', address="Taipei", latitude=25.0475, longitude=121.5173)
#                     ]
#                 )
#             )
#         else:
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[TextMessage(text=event.message.text)]
#                 )
#             )

#訊息傳送(Template)
# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     text = event.message.text
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         # Confirm Template
#         if text == 'Confirm':
#             confirm_template = ConfirmTemplate(
#                 text='今天學程式了嗎?',
#                 actions=[
#                     MessageAction(label='是', text='是!'),
#                     MessageAction(label='否', text='否!')
#                 ]
#             )
#             template_message = TemplateMessage(
#                 alt_text='Confirm alt text',
#                 template=confirm_template
#             )
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[template_message]
#                 )
#             )
#         # Buttons Template
#         elif text == 'Buttons':
#             url = request.url_root + 'static/Logo.jpg'
#             url = url.replace("http", "https")
#             app.logger.info("url=" + url)
#             buttons_template = ButtonsTemplate(
#                 thumbnail_image_url=url,
#                 title='示範',
#                 text='詳細說明',
#                 actions=[
#                     # URIAction(label='連結', uri='https://www.facebook.com/NTUEBIGDATAEDU'),
#                     # PostbackAction(label='回傳值', data='ping', displayText='傳了'),
#                     # MessageAction(label='傳"哈囉"', text='哈囉'),
#                     # DatetimePickerAction(label="選擇時間", data="時間", mode="datetime"),
#                     CameraAction(label='拍照'),
#                     CameraRollAction(label='選擇相片'),
#                     LocationAction(label='選擇位置')
#                 ]
#             )
#             template_message = TemplateMessage(
#                 alt_text="This is a buttons template",
#                 template=buttons_template
#             )
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[template_message]
#                 )
#             )
#         # Carousel Template
#         elif text == 'Carousel':
#             url = request.url_root + 'static/Logo.jpg'
#             url = url.replace("http", "https")
#             app.logger.info("url=" + url)
#             carousel_template = CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url=url,
#                         title='第一項',
#                         text='這是第一項的描述',
#                         actions=[
#                             URIAction(
#                                 label='按我前往 Google',
#                                 uri='https://www.google.com'
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url=url,
#                         title='第二項',
#                         text='這是第二項的描述',
#                         actions=[
#                             URIAction(
#                                 label='按我前往 Yahoo',
#                                 uri='https://www.yahoo.com'
#                             )
#                         ]
#                     )
#                 ]
#             )

#             carousel_message = TemplateMessage(
#                 alt_text='這是 Carousel Template',
#                 template=carousel_template
#             )

#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages =[carousel_message]
#                 )
#             )
#         # ImageCarousel Template
#         elif text == 'ImageCarousel':
#             url = request.url_root + 'static/'
#             url = url.replace("http", "https")
#             app.logger.info("url=" + url)
#             image_carousel_template = ImageCarouselTemplate(
#                 columns=[
#                     ImageCarouselColumn(
#                         image_url=url+'facebook.png',
#                         action=URIAction(
#                             label='造訪FB',
#                             uri='https://www.facebook.com/NTUEBIGDATAEDU'
#                         )
#                     ),
#                     ImageCarouselColumn(
#                         image_url=url+'instagram.png',
#                         action=URIAction(
#                             label='造訪IG',
#                             uri='https://instagram.com/ntue.bigdata?igshid=YmMyMTA2M2Y='
#                         )
#                     ),
#                     ImageCarouselColumn(
#                         image_url=url+'youtube.png',
#                         action=URIAction(
#                             label='造訪YT',
#                             uri='https://www.youtube.com/@bigdatantue'
#                         )
#                     ),
#                 ]
#             )

#             image_carousel_message = TemplateMessage(
#                 alt_text='圖片輪播範本',
#                 template=image_carousel_template
#             )

#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[image_carousel_message]
#                 )
#             )

#訊息傳送(Flex)
# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     text = event.message.text
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         if text == 'flex':
#             url = request.url_root + 'static/Logo.jpg'
#             url = url.replace("http", "https")
#             app.logger.info("url=" + url)
#             bubble = FlexBubble(
#                 direction='ltr',
#                 hero=FlexImage(
#                     url=url,
#                     size='full',
#                     aspect_ratio='20:13',
#                     aspect_mode='cover',
#                     action=URIAction(uri='https://www.facebook.com/NTUEBIGDATAEDU', label='label')
#                 ),
#                 body=FlexBox(
#                     layout='vertical',
#                     contents=[
#                         # title
#                         FlexText(text='教育大數據', weight='bold', size='xl'),
#                         # review
#                         FlexBox(
#                             layout='baseline',
#                             margin='md',
#                             contents=[
#                                 FlexIcon(size='sm', url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"),
#                                 FlexIcon(size='sm', url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"),
#                                 FlexIcon(size='sm', url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"),
#                                 FlexIcon(size='sm', url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"),
#                                 FlexIcon(size='sm', url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"),
#                                 FlexText(text='5.0', size='sm', color='#999999', margin='md', flex=0)
#                             ]
#                         ),
#                         # info
#                         FlexBox(
#                             layout='vertical',
#                             margin='lg',
#                             spacing='sm',
#                             contents=[
#                                 FlexBox(
#                                     layout='baseline',
#                                     spacing='sm',
#                                     contents=[
#                                         FlexText(
#                                             text='Place',
#                                             color='#aaaaaa',
#                                             size='sm',
#                                             flex=1
#                                         ),
#                                         FlexText(
#                                             text='Da\'an District, Taipei ',
#                                             wrap=True,
#                                             color='#666666',
#                                             size='sm',
#                                             flex=5
#                                         )
#                                     ],
#                                 ),
#                                 FlexBox(
#                                     layout='baseline',
#                                     spacing='sm',
#                                     contents=[
#                                         FlexText(
#                                             text='Time',
#                                             color='#aaaaaa',
#                                             size='sm',
#                                             flex=1
#                                         ),
#                                         FlexText(
#                                             text="10:00 - 23:00",
#                                             wrap=True,
#                                             color='#666666',
#                                             size='sm',
#                                             flex=5,
#                                         ),
#                                     ],
#                                 ),
#                             ],
#                         )
#                     ],
#                 ),
#                 footer=FlexBox(
#                     layout='vertical',
#                     spacing='sm',
#                     contents=[
#                         # callAction
#                         FlexButton(
#                             style='link',
#                             height='sm',
#                             action=URIAction(label='CALL', uri='tel:0911880932'),
#                         ),
#                         # separator
#                         FlexSeparator(),
#                         # websiteAction
#                         FlexButton(
#                             style='link',
#                             height='sm',
#                             action=URIAction(label='WEBSITE', uri='https://www.facebook.com/NTUEBIGDATAEDU')
#                         )
#                     ]
#                 ),
#             )
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[FlexMessage(alt_text="hello", contents=bubble)]
#                 )
#             )

#         elif text == 'flex message':
#             line_flex_json = {
#                 "type": "bubble",
#                 "hero": {
#                     "type": "image",
#                     "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
#                     "size": "full",
#                     "aspectRatio": "20:13",
#                     "aspectMode": "cover",
#                     "action": {
#                     "type": "uri",
#                     "uri": "http://linecorp.com/"
#                     }
#                 },
#                 "body": {
#                     "type": "box",
#                     "layout": "vertical",
#                     "contents": [
#                     {
#                         "type": "text",
#                         "text": "Brown Cafe",
#                         "weight": "bold",
#                         "size": "xl"
#                     },
#                     {
#                         "type": "box",
#                         "layout": "baseline",
#                         "margin": "md",
#                         "contents": [
#                         {
#                             "type": "icon",
#                             "size": "sm",
#                             "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                         },
#                         {
#                             "type": "icon",
#                             "size": "sm",
#                             "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                         },
#                         {
#                             "type": "icon",
#                             "size": "sm",
#                             "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                         },
#                         {
#                             "type": "icon",
#                             "size": "sm",
#                             "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                         },
#                         {
#                             "type": "icon",
#                             "size": "sm",
#                             "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
#                         },
#                         {
#                             "type": "text",
#                             "text": "4.0",
#                             "size": "sm",
#                             "color": "#999999",
#                             "margin": "md",
#                             "flex": 0
#                         }
#                         ]
#                     },
#                     {
#                         "type": "box",
#                         "layout": "vertical",
#                         "margin": "lg",
#                         "spacing": "sm",
#                         "contents": [
#                         {
#                             "type": "box",
#                             "layout": "baseline",
#                             "spacing": "sm",
#                             "contents": [
#                             {
#                                 "type": "text",
#                                 "text": "Place",
#                                 "color": "#aaaaaa",
#                                 "size": "sm",
#                                 "flex": 1
#                             },
#                             {
#                                 "type": "text",
#                                 "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
#                                 "wrap": True,
#                                 "color": "#666666",
#                                 "size": "sm",
#                                 "flex": 5
#                             }
#                             ]
#                         },
#                         {
#                             "type": "box",
#                             "layout": "baseline",
#                             "spacing": "sm",
#                             "contents": [
#                             {
#                                 "type": "text",
#                                 "text": "Time",
#                                 "color": "#aaaaaa",
#                                 "size": "sm",
#                                 "flex": 1
#                             },
#                             {
#                                 "type": "text",
#                                 "text": "10:00 - 23:00",
#                                 "wrap": True,
#                                 "color": "#666666",
#                                 "size": "sm",
#                                 "flex": 5
#                             }
#                             ]
#                         }
#                         ]
#                     }
#                     ]
#                 },
#                 "footer": {
#                     "type": "box",
#                     "layout": "vertical",
#                     "spacing": "sm",
#                     "contents": [
#                     {
#                         "type": "button",
#                         "style": "link",
#                         "height": "sm",
#                         "action": {
#                         "type": "uri",
#                         "label": "CALL",
#                         "uri": "https://www.facebook.com/NTUEBIGDATAEDU"
#                         }
#                     },
#                     {
#                         "type": "button",
#                         "style": "link",
#                         "height": "sm",
#                         "action": {
#                         "type": "uri",
#                         "label": "WEBSITE",
#                         "uri": "https://www.facebook.com/NTUEBIGDATAEDU"
#                         }
#                     },
#                     {
#                         "type": "box",
#                         "layout": "vertical",
#                         "contents": [],
#                         "margin": "sm"
#                     }
#                     ],
#                     "flex": 0
#                 }
#             }
#             line_flex_str = json.dumps(line_flex_json)
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[FlexMessage(alt_text='詳細說明', contents=FlexContainer.from_json(line_flex_str))]
#                 )
#             )

#         else:
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[TextMessage(text=event.message.text)]
#                 )
#             )

#訊息傳送(點餐)
# 記錄每個群組的回覆訊息與點餐狀態
group_replies = {}
group_active = {}

@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text.strip()
    group_id = event.source.group_id if event.source.type == 'group' else 'private'

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # 點餐開始：初始化回覆列表與狀態
        if any(keyword in user_text for keyword in ["早餐", "午餐", "晚餐"]):
            group_replies[group_id] = []
            group_active[group_id] = True
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='請開始點餐')]
                )
            )
            return

        # 結束點餐：回覆所有收集到的訊息並關閉狀態
        if text == '結束點餐':
            if group_id not in group_replies or not group_replies[group_id]:
                summary_text = '目前尚無任何回覆。'
            else:
                summary_text = '點餐結束！以下是這次的餐點：\n' + '\n'.join(group_replies[group_id])

            # 清除資料並關閉狀態
            group_replies[group_id] = []
            group_active[group_id] = False

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=summary_text)]
                )
            )
            return

        # 若群組未啟動點餐，不做任何回覆
        if not group_active.get(group_id, False):
            return
        # 收集回覆訊息（非指令）
        group_replies[group_id].append(text)

        # 組合目前所有回覆
        current_summary = '\n'.join(group_replies[group_id])

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=f'目前點餐紀錄如下：\n{current_summary}')
                ]
            )
        )



#訊息回覆(image map)
# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     text = event.message.text
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         if text == 'imagemap':
#             url1 = request.url_root + 'static/imagemap'
#             url1 = url1.replace("http", "https")
#             app.logger.info("url=" + url1)
#             url2 = request.url_root + 'static/video.mp4'
#             url2 = url2.replace("http", "https")
#             app.logger.info("url=" + url2)
#             url3 = request.url_root + 'static/preview_image.png'
#             url3 = url3.replace("http", "https")
#             app.logger.info("url=" + url3)
#             imagemap_message = ImagemapMessage(
#                 base_url=url1,
#                 alt_text='this is an imagemap',
#                 base_size=ImagemapBaseSize(height=1040, width=1040),
#                 video=ImagemapVideo(
#                     original_content_url=url2,
#                     preview_image_url=url3,
#                     area=ImagemapArea(
#                         x=0, y=0, width=1040, height=520
#                     ),
#                     external_link=ImagemapExternalLink(
#                         link_uri='https://www.youtube.com/@bigdatantue',
#                         label='點我看更多',
#                     ),
#                 ),
#                 actions=[
#                     URIImagemapAction(
#                         type = "uri",
#                         linkUri='https://instagram.com/ntue.bigdata?igshid=YmMyMTA2M2Y=',
#                         area=ImagemapArea(
#                             x=0, y=520, width=520, height=520
#                         )
#                     ),
#                     MessageImagemapAction(
#                         type ="message",
#                         text='這是fb網頁https://www.facebook.com/NTUEBIGDATAEDU',
#                         area=ImagemapArea(
#                             x=520, y=520, width=520, height=520
#                         )
#                     )
#                 ]
#             )
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[imagemap_message]
#                 )
#             )

# 訊息回覆(quick reply)
# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     text = event.message.text
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         if text == 'quick_reply':
#             postback_icon = request.url_root + 'static/postback.png'
#             postback_icon = postback_icon.replace("http", "https")
#             message_icon = request.url_root + 'static/message.png'
#             message_icon = message_icon.replace("http", "https")
#             datetime_icon = request.url_root + 'static/calendar.png'
#             datetime_icon = datetime_icon.replace("http", "https")
#             date_icon = request.url_root + 'static/calendar.png'
#             date_icon = date_icon.replace("http", "https")
#             time_icon = request.url_root + 'static/time.png'
#             time_icon = time_icon.replace("http", "https")

#             quickReply = QuickReply(
#                 items=[
#                     QuickReplyItem(
#                         action=PostbackAction(
#                             label="Postback",
#                             data="postback",
#                             display_text="postback"
#                         ),
#                         image_url=postback_icon
#                     ),
#                     QuickReplyItem(
#                         action=MessageAction(
#                             label="Message",
#                             text="message"
#                         ),
#                         image_url=message_icon
#                     ),
#                     QuickReplyItem(
#                         action=DatetimePickerAction(
#                             label="Date",
#                             data="date",
#                             mode="date"
#                         ),
#                         image_url=date_icon
#                     ),
#                     QuickReplyItem(
#                         action=DatetimePickerAction(
#                             label="Time",
#                             data="time",
#                             mode="time"
#                         ),
#                         image_url=time_icon
#                     ),
#                     QuickReplyItem(
#                         action=DatetimePickerAction(
#                             label="Datetime",
#                             data="datetime",
#                             mode="datetime",
#                             initial="2024-01-01T00:00",
#                             max="2025-01-01T00:00",
#                             min="2023-01-01T00:00"
#                         ),
#                         image_url=datetime_icon
#                     ),
#                     QuickReplyItem(
#                         action=CameraAction(label="Camera")
#                     ),
#                     QuickReplyItem(
#                         action=CameraRollAction(label="Camera Roll")
#                     ),
#                     QuickReplyItem(
#                         action=LocationAction(label="Location")
#                     )
#                 ]
#             )
            
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[TextMessage(
#                         text='請選擇項目',
#                         quick_reply=quickReply
#                     )]
#                 )
#             )

# @handler.add(PostbackEvent)
# def handle_postback(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         postback_data = event.postback.data
#         if postback_data == 'postback':
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[TextMessage(text='Postback')]
#                 )
#             )
#         elif postback_data == 'date':
#             date = event.postback.params['date']
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[TextMessage(text=date)]
#                 )
#             )
#         elif postback_data == 'time':
#             time = event.postback.params['time']
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[TextMessage(text=time)]
#                 )
#             )
#         elif postback_data == 'datetime':
#             datetime = event.postback.params['datetime']
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[TextMessage(text=datetime)]
#                 )
#             )

#menu
# def create_rich_menu_1():
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         line_bot_blob_api = MessagingApiBlob(api_client)

#         areas = [
#             RichMenuArea(
#                 bounds=RichMenuBounds(
#                     x=0,
#                     y=0,
#                     width=833,
#                     height=843
#                 ),
#                 action=MessageAction(text='A')
#             ),
#             RichMenuArea(
#                 bounds=RichMenuBounds(
#                     x=834,
#                     y=0,
#                     width=833,
#                     height=843
#                 ),
#                 action=MessageAction(text='B')
#             ),
#             RichMenuArea(
#                 bounds=RichMenuBounds(
#                     x=1663,
#                     y=0,
#                     width=834,
#                     height=843
#                 ),
#                 action=MessageAction(text='C')
#             ),
#             RichMenuArea(
#                 bounds=RichMenuBounds(
#                     x=0,
#                     y=843,
#                     width=833,
#                     height=843
#                 ),
#                 action=MessageAction(text='D')
#             ),
#             RichMenuArea(
#                 bounds=RichMenuBounds(
#                     x=834,
#                     y=843,
#                     width=833,
#                     height=843
#                 ),
#                 action=MessageAction(text='E')
#             ),
#             RichMenuArea(
#                 bounds=RichMenuBounds(
#                     x=1662,
#                     y=843,
#                     width=834,
#                     height=843
#                 ),
#                 action=MessageAction(text='F')
#             )
#         ]

#         rich_menu_to_create = RichMenuRequest(
#             size=RichMenuSize(
#                 width=2500,
#                 height=1686,
#             ),
#             selected=True,
#             name="圖文選單1",
#             chat_bar_text="查看更多資訊",
#             areas=areas
#         )

#         rich_menu_id = line_bot_api.create_rich_menu(
#             rich_menu_request=rich_menu_to_create
#         ).rich_menu_id

#         with open('./public/richmenu-a.png', 'rb') as image:
#             line_bot_blob_api.set_rich_menu_image(
#                 rich_menu_id=rich_menu_id,
#                 body=bytearray(image.read()),
#                 _headers={'Content-Type': 'image/png'}
#             )

#         line_bot_api.set_default_rich_menu(rich_menu_id)


# def create_rich_menu_2():
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         line_bot_blob_api = MessagingApiBlob(api_client)

#         # Create rich menu
#         headers = {
#             'Authorization': 'Bearer ' + CHANNEL_ACCESS_TOKEN,
#             'Content-Type': 'application/json'
#         }
#         body = {
#             "size": {
#                 "width": 2500,
#                 "height": 1686
#             },
#             "selected": True,
#             "name": "圖文選單 1",
#             "chatBarText": "查看更多資訊",
#             "areas": [
#                 {
#                     "bounds": {
#                         "x": 0,
#                         "y": 0,
#                         "width": 833,
#                         "height": 843
#                     },
#                     "action": {
#                         "type": "message",
#                         "text": "A"
#                     }
#                 },
#                 {
#                     "bounds": {
#                         "x": 834,
#                         "y": 0,
#                         "width": 833,
#                         "height": 843
#                     },
#                     "action": {
#                         "type": "message",
#                         "text": "B"
#                     }
#                 },
#                 {
#                     "bounds": {
#                         "x": 1663,
#                         "y": 0,
#                         "width": 834,
#                         "height": 843
#                     },
#                     "action": {
#                         "type": "message",
#                         "text": "C"
#                     }
#                 },
#                 {
#                     "bounds": {
#                         "x": 0,
#                         "y": 843,
#                         "width": 833,
#                         "height": 843
#                     },
#                     "action": {
#                         "type": "message",
#                         "text": "D"
#                     }
#                 },
#                 {
#                     "bounds": {
#                         "x": 834,
#                         "y": 843,
#                         "width": 833,
#                         "height": 843
#                     },
#                     "action": {
#                         "type": "message",
#                         "text": "E"
#                     }
#                 },
#                 {
#                     "bounds": {
#                         "x": 1662,
#                         "y": 843,
#                         "width": 838,
#                         "height": 843
#                     },
#                     "action": {
#                         "type": "message",
#                         "text": "F"
#                     }
#                 }
#             ]
#         }

#         response = requests.post('https://api.line.me/v2/bot/richmenu', headers=headers, data=json.dumps(body).encode('utf-8'))
#         response = response.json()
#         print(response)
#         rich_menu_id = response["richMenuId"]
        
#         # Upload rich menu image
#         with open('static/richmenu-1.jpg', 'rb') as image:
#             line_bot_blob_api.set_rich_menu_image(
#                 rich_menu_id=rich_menu_id,
#                 body=bytearray(image.read()),
#                 _headers={'Content-Type': 'image/jpeg'}
#             )

#         line_bot_api.set_default_rich_menu(rich_menu_id)

# create_rich_menu_2()

if __name__ == "__main__":
    app.run()