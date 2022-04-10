import simplematrixbotlib as botlib
from wallbox_control import get_status_str, exec_enable_auto, exec_activate, exec_deactivate
 
creds = botlib.Creds("matrixserver", "username", "password")
bot = botlib.Bot(creds)
PREFIX = '!'


@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command("help"):
        
        message = (f"""
        Help
        ============================
        Simple bot for controlling wallbox
        Commands?
            {PREFIX}help - show this message
            {PREFIX}auto - activate auto mode
            {PREFIX}on - turn permanently on
            {PREFIX}off - turn permanently off
            {PREFIX}status - show current status
        """)
        
        await bot.api.send_text_message(room.room_id, message)
        
        
        
@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
        
    if match.is_not_from_this_bot() and match.prefix() and match.command("status"):
        
        status = get_status_str()
        msg = "Wallbox and battery status: \n{}".format(status)
        await bot.api.send_text_message(room.room_id, msg)
        img_path = '/home/pi/wallbox_controller/www/soc_over_time.png'
        await bot.api.send_image_message(room_id=room.room_id, image_filepath=img_path)
        

@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
        
    if match.is_not_from_this_bot() and match.prefix() and match.command("on"):
        
        res = exec_activate()
        if res == "1":
            await bot.api.send_text_message(room.room_id, "wallbox successfully activated")
        else:
            await bot.api.send_text_message(room.room_id, "I am sorry there was an error")
        
        
@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
        
    if match.is_not_from_this_bot() and match.prefix() and match.command("off"):
        
        res = exec_deactivate()
        if res == "0":
            await bot.api.send_text_message(room.room_id, "wallbox successfully dectivated")
        else:
            await bot.api.send_text_message(room.room_id, "I am sorry there was an error")
        
        
@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
        
    if match.is_not_from_this_bot() and match.prefix() and match.command("auto"):
        
        exec_enable_auto()
        status = get_status_str()
        await bot.api.send_text_message(room.room_id, "Auto mode enabled")
        msg = "Wallbox and battery status: \n{}".format(status)
        await bot.api.send_text_message(room.room_id, msg)
        
bot.run()
