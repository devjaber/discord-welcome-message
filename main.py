import discord
from PIL import Image, ImageDraw, ImageFont
from config import TOKEN, CHANNEL_ID, FONT_PATH
import requests
#jaberkohistani.com

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_member_join(member):
    username = member.name
    user_mention = member.mention

    avatar_url = member.avatar.url
    avatar_image = Image.open(requests.get(avatar_url, stream=True).raw).convert('L') 

    mask = Image.new("L", avatar_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + avatar_image.size, fill=255)
    avatar_image.putalpha(mask)
    background_image = Image.open('background_image.png').convert('RGBA')

    welcome_message = f'{username}'
    preview_image = Image.alpha_composite(background_image, Image.new('RGBA', background_image.size, (0, 0, 0, 0)))

    avatar_image = avatar_image.resize((650, 790))
    preview_image.paste(avatar_image, (620, 65), avatar_image)

    font = ImageFont.truetype(FONT_PATH, 70)
    draw = ImageDraw.Draw(preview_image)
    draw.text((200, 200), welcome_message, fill=(48, 48, 48), font=font)

    preview_image_path = f'user-img/{username}.png'
    preview_image.save(preview_image_path)

    channel = client.get_channel(CHANNEL_ID)
    await channel.send(file=discord.File(preview_image_path))

    send_welcome_message = f'||{user_mention}||'
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(send_welcome_message)

client.run(TOKEN)
