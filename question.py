import discord

client = discord.Client()  # 接続に使用するオブジェクト


# 起動時
@client.event
async def on_ready():
    print('ログイン成功')


# メッセージを監視
@client.event
async def on_message(message):
    # 「/box」が頭についたメッセージならオウム返しする
    if message.content.startswith('/box'):
        # 文字から「/box」を抜く
        question = message.content[len('/box'):].strip()
        # 質問させたいチャンネルのid
        target_channel_id = getTargetChannelId()

        # id=0なら質問者にエラー報告DM
        # idが0以外なら匿名質問する
        if target_channel_id == 0:
            dm = await message.author.create_dm()  # 質問者へDM作成
            await dm.send(
                'Sorry, メッセージを送信できませんでした．'
                'もう1度試してみてください．\n'
                '【質問文】' + question)
        else:
            # 匿名質問させたいチャンネル
            target_channel = client.get_channel(target_channel_id)
            # チャンネルに質問メッセージ送信
            await target_channel.send(question)


# 匿名質問させたいチャンネルのidを取得
# 指定したカテゴリにある最初のTextチャンネル＝質問させたいチャンネルとみなす
# ただしカテゴリにチャンネルが無い時は0を返す
def getTargetChannelId() -> int:
    # 質問させたいチャンネル(対象チャンネル)
    target_channel = {'id': 0, 'position': 99999999}
    # ***********************************************************
    # 指定カテゴリ(対象チャンネルが含まれたカテゴリ)の名前

    category_id = INT_ID_OF_YOUR_CATEGORY  # カテゴリidを指定
    target_category_name = client.get_channel(category_id).name

    # ***********************************************************
    # 指定したサーバにある全てのTextチャンネル一覧
    all_channels = client.get_guild(INT_ID_OF_SERVER).text_channels

    # 全てのTextチャンネルから「指定カテゴリに属する最初のチャンネル」を探す
    for channel in all_channels:
        # 指定カテゴリに属する場合だけ対象チャンネル候補とみなす
        if str(channel.category) == target_category_name:
            # positionが小さいほうを「より対象チャンネルに近い」として交換
            # 初期値はpositionが大きい(99999999)ので，必ず入れ替わる想定
            # 繰り返せば，最後にはpositionが最も小さいチャンネルを代入できる
            if target_channel['position'] > int(channel.position):
                target_channel['id'] = int(channel.id)
                target_channel['position'] = int(channel.position)
    # 最終的に代入されたidを返す
    return target_channel['id']


# botとしてDiscordに接続(botのトークンを指定)
client.run('TOKEN_OF_YOUR_BOT')
