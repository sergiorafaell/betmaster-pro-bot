import telebot
from telebot import types
import os
import time
from flask import Flask
import threading

# ================= CONFIGURAÇÃO =================
TOKEN = '8255460383:AAG1znCT140k8Kidh7LXFtops4F0n77ckVo'
ADMIN_ID = 5125563829

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

print(f"🤖 Bot inicializado com token: {TOKEN[:10]}...")

# ================= COMANDOS =================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(f"📥 Recebido /start de {message.from_user.id}")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎯 GERAR CÓDIGO", callback_data="gerar"),
        types.InlineKeyboardButton("💎 VER VIP", callback_data="vip")
    )
    markup.add(
        types.InlineKeyboardButton("📞 SUPORTE", url="https://t.me/AiltonArmindo"),
        types.InlineKeyboardButton("💰 PAGAR", callback_data="pagar")
    )
    
    try:
        bot.send_message(
            message.chat.id,
            f"""🏆 <b>BET MASTER PRO</b>

👋 Olá <b>{message.from_user.first_name}</b>!
🆔 ID: <code>{message.from_user.id}</code>

✅ <b>Bot online e funcionando!</b>

🎯 <b>Comandos:</b>
/gerar - Gerar código (2 GRÁTIS/dia)
/vip - Ver planos VIP
/suporte - Falar com suporte

💎 <b>VIP:</b> 150MT a 5000MT

📞 <b>Suporte:</b> @AiltonArmindo""",
            reply_markup=markup,
            parse_mode='HTML'
        )
        print(f"✅ Respondido para {message.from_user.id}")
    except Exception as e:
        print(f"❌ Erro ao responder: {e}")

@bot.message_handler(commands=['gerar'])
def gerar_codigo(message):
    import random
    import string
    from datetime import datetime
    
    codigo = 'BM' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    bot.reply_to(
        message,
        f"""✅ <b>CÓDIGO GERADO!</b>

🔢 <code>{codigo}</code>
📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}

🏠 <b>Usar em:</b>
• Betway
• 1xBet  
• PremierBet
• ElephantBet

⚠️ Válido 24 horas""",
        parse_mode='HTML'
    )

@bot.message_handler(commands=['vip'])
def vip_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("💰 DIÁRIO 150MT", callback_data="diario"),
        types.InlineKeyboardButton("🏆 SEMANAL 800MT", callback_data="semanal")
    )
    markup.add(
        types.InlineKeyboardButton("👑 MENSAL 2500MT", callback_data="mensal"),
        types.InlineKeyboardButton("🚀 PREMIUM 5000MT", callback_data="premium")
    )
    
    bot.send_message(
        message.chat.id,
        """💎 <b>PLANOS VIP</b>

1. <b>Diário</b> - 150MT
   • 10 códigos/dia
   • 24 horas

2. <b>Semanal</b> - 800MT  
   • 15 códigos/dia
   • 7 dias

3. <b>Mensal</b> - 2500MT
   • 20 códigos/dia
   • 30 dias

4. <b>Premium</b> - 5000MT
   • 30 códigos/dia
   • 90 dias

📲 <b>Pagamento:</b>
• Emola: 870612404
• M-Pesa: 848568229
• PayPal: ayltonanna@gmail.com""",
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text:
        bot.reply_to(message, f"📝 Recebido: {message.text}\n\nUse /start para menu")

# ================= CALLBACKS =================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "gerar":
        gerar_codigo(call.message)
    elif call.data == "vip":
        vip_info(call.message)
    elif call.data == "pagar":
        bot.send_message(
            call.message.chat.id,
            """💰 <b>PAGAMENTO</b>

📱 <b>Para pagar:</b>
1. Emola: 870612404
2. M-Pesa: 848568229  
3. PayPal: ayltonanna@gmail.com

📞 <b>Envie comprovante para:</b>
• Telegram: @AiltonArmindo
• WhatsApp: +258848568229

⚡ Ativação em 5 minutos!""",
            parse_mode='HTML'
        )

# ================= WEB SERVER (KEEP-ALIVE) =================
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bet Master Pro - ONLINE ✅"

@app.route('/health')
def health():
    return "OK", 200

def run_web():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# ================= INICIAR =================
if __name__ == '__main__':
    print("🚀 Iniciando servidor web...")
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    
    print("🤖 Iniciando bot Telegram...")
    print("⏳ Aguarde 5 segundos...")
    time.sleep(5)
    
    while True:
        try:
            print("🔄 Iniciando polling...")
            bot.polling(none_stop=True, interval=1, timeout=30)
        except Exception as e:
            print(f"⚠️ Erro: {e}")
            print("🔄 Reiniciando em 10 segundos...")
            time.sleep(10)
