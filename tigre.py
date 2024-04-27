import telebot
from datetime import datetime, timedelta
from random import randint, uniform
import time
import json

bot = telebot.TeleBot('6841364767:AAEY-tYOAK-CR7TygnGTYxtPcbX35OQLrRk')
admin = '6646834549'
chats_file = 'chats.json'

fortuneTiger = 'Fortune Tiger'
site = 'Bet7K.com'
valorPlano = 50
envio_ativo = False

def getRandomNumber(min, max):
    return randint(min, max)

def displayMessage(chatId, validUntil):
    normalValue = getRandomNumber(4, 7)
    turboValue = getRandomNumber(4, 7)
    respinsValue = getRandomNumber(2, 4)

    message = f"""
🎊*OPORTUNIDADE CONFIRMADA* 🎊
    
🐅 *{fortuneTiger}*
💻 *Site:* *{site}*
⏳ *Válido até:* *{validUntil}*
    
👉 *{normalValue}x Normal*
⚡ *{turboValue}x Turbo*
🚥 Intercalando
🔄 SE Não VIER, Repita *{respinsValue}x*
🏆 USE O CÓDIGO: *NETCOM* E GANHE R$20 NO CADASTRO 
    """

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('🤑ENTRE AGORA NO JOGO🤑', url='https://bet7k.com/?ref=98d1afafbc6c'))

    try:
        bot.send_message(chatId, message, parse_mode='Markdown', reply_markup=keyboard)
        print(f'Sinal enviado ao chat [{chatId}] - Válido até: {validUntil}')
    except Exception as error:
        print(f'Erro ao enviar o sinal: {error}')

def enviar_sinais_junior_netcom():
    global envio_ativo
    try:
        while envio_ativo:
            with open(chats_file, 'r') as file:
                chats = json.load(file)
                for chat_id in chats:
                    intervalo_valid_until = uniform(4, 6)  # Intervalo aleatório entre 4 e 6
                    validUntil = (datetime.now() + timedelta(minutes=intervalo_valid_until)).strftime('%H:%M')
                    displayMessage(chat_id, validUntil)
                    time.sleep(7)  # Enviar todos os sinais simultaneamente para os chats
                time.sleep(7 * 60)  # Ativar o tempo para enviar novamente após o envio para todos os chats
    except Exception as error:
        print(f'Erro ao enviar a mensagem de sinal: {error}')

def save_chats(chats):
    with open(chats_file, 'w') as file:
        json.dump(chats, file, indent=4)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bem-vindo(a) Sou o Bot de sinais 🐯TIGER Apenas funciono onde meu mestre permitir.")

@bot.message_handler(commands=['ativar'])
def ativar_netcom(message):
    global envio_ativo
    if str(message.from_user.id) == admin:
        if not envio_ativo:
            envio_ativo = True
            bot.reply_to(message, "Envio de sinais ativado com sucesso!")
            enviar_sinais_junior_netcom()
        else:
            bot.reply_to(message, "O envio de sinais já está ativo.")
    else:
        bot.reply_to(message, "Você não e admin.")

@bot.message_handler(commands=['desativar'])
def desativar_netcom(message):
    global envio_ativo
    if str(message.from_user.id) == admin:
        if envio_ativo:
            envio_ativo = False
            bot.reply_to(message, "Envio de sinais desativado com sucesso!")
        else:
            bot.reply_to(message, "O envio de sinais já está desativado.")
    else:
        bot.reply_to(message, "Você não e admin.")

@bot.message_handler(commands=['adicionar'])
def adicionar_chat_netcom(message):
    if str(message.from_user.id) == admin:
        text = message.text.split(' ', 1)
        if len(text) > 1 and text[1].startswith('-id'):
            chat_id = text[1][3:]
            with open(chats_file, 'r') as file:
                chats = json.load(file)
                if chat_id not in chats:
                    chats.append(chat_id)
                    save_chats(chats)
                    bot.reply_to(message, "Chat ID adicionado com sucesso!")
                else:
                    bot.reply_to(message, "Este Chat ID já está na lista.")
        else:
            bot.reply_to(message, "Formato inválido! Use: /adicionar -id[ChatID]")
    else:
        bot.reply_to(message, "Você não e admin.")

@bot.message_handler(commands=['remover'])
def remover_chat_netcom(message):
    if str(message.from_user.id) == admin:
        text = message.text.split(' ', 1)
        if len(text) > 1 and text[1].startswith('-id'):
            chat_id = text[1][3:]
            with open(chats_file, 'r') as file:
                chats = json.load(file)
                if chat_id in chats:
                    chats.remove(chat_id)
                    save_chats(chats)
                    bot.reply_to(message, "Chat ID removido com sucesso!")
                else:
                    bot.reply_to(message, "Este Chat ID não está na lista.")
        else:
            bot.reply_to(message, "Formato inválido! Use: /remover -id[ChatID]")
    else:
        bot.reply_to(message, "Você não e admin.")

@bot.message_handler(commands=['listar'])
def listar_chats_netcom(message):
    if str(message.from_user.id) == admin:
        with open(chats_file, 'r') as file:
            chats = json.load(file)
            bot.reply_to(message, f"Chat IDs na lista: {', '.join(str(chat) for chat in chats)}")
    else:
        bot.reply_to(message, "Você não e admin.")

def polling():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Erro: {str(e)}")
            time.sleep(15)

print("VAI TIGRINHO!!")
if __name__ == "__main__":
    enviar_sinais_junior_netcom()
    polling()
