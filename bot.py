import os
import google.generativeai as genai
from telegram.ext import ApplicationBuilder, MessageHandler, filters

TOKEN = "8100198477:AAH-tqk77L2rSXG51wsppetdaB7_4bYvVAE"
API_KEY = "AQ.Ab8RN6ItXaEgx5e_x7s9VMCzHM_Ho5r8brK8YmVbeGWQY33AlwAQ.Ab8RN6ItXaEgx5e_x7s9VMCzHM_Ho5r8brK8YmVbeGWQY33Alw "
KULLANICI_ID = "-1002017528631" 

SOURCE_CHANNELS = [
    "firsatz", "yaniyocom", "TAZEFIRSAT", "Cuzdown", "onual_firsat", 
    "indirimlisinerede", "linkledinn", "indirimbakanligi", "amazonozel", 
    "ozelfirsat", "indirimpare", "anlikindirimbotu", "firsatlar_onemli", 
    "TAZEFIRSATmini", "firsatavcilari01", "butcedostu", "indirim", 
    "trendindirimlerim", "indirimz", "indirimc", "indiriim", 
    "alisverishaberleri", "indirimbultenicom", "firsatikacirmakanal", 
    "firsattdiyari", "indirimfirsatburada", "dhsicak_firsatlar"
]

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def mesaj_isleyici(update, context):
    
    if update.channel_post and update.channel_post.text:
        kanal_adi = update.channel_post.chat.username
        
        # Eğer mesaj SOURCE_CHANNELS listesindeki bir kanaldan geldiyse işle
        if kanal_adi in SOURCE_CHANNELS:
            mesaj = update.channel_post.text
            prompt = f"Mesajı analiz et: {mesaj}. Sadece 'Ürün | Fiyat | Link' formatında ver."
            
            try:
                yanit = model.generate_content(prompt).text
                await context.bot.send_message(chat_id=KULLANICI_ID, text=f"🔍 Analiz:\n{yanit}")
            except Exception as e:
                print(f"Gemini veya Mesaj Gönderme Hatası: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Kanallardaki yeni gönderileri (postları) dinlemek için filtre
    app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POSTS, mesaj_isleyici))
    
    print("Bot başlatıldı, kanallar dinleniyor...")
    app.run_polling()
