# bheringbot/freelancer_auto_reply/main.py

import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import API_ID, API_HASH, BOT_TOKEN, RESPONDER_EM_GRUPO
from respostas import respostas

app = Client("freelancer_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Mensagem de boas-vindas com botões
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    nome = message.from_user.first_name or "amigo"
    texto = (
        f"👋 Olá, {nome}!\n\n"
        "Sou o assistente automático de freelancers da Bhering Bots.\n\n"
        "Escolha uma opção abaixo:"
    )
    botoes = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📁 Portfólio", callback_data="btn_portfolio"),
            InlineKeyboardButton("💲 Preço", callback_data="btn_preco")
        ],
        [
            InlineKeyboardButton("💳 Pagamento", callback_data="btn_pagamento")
        ],
        [
            InlineKeyboardButton("💬 Falar com Bhering", url="https://t.me/bheringbot1")
        ]
    ])
    await message.reply(texto, reply_markup=botoes)

# Função que responde aos botões
@app.on_callback_query()
async def callback_handler(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    nome = callback_query.from_user.first_name or "amigo"

    await callback_query.answer()  # <-- IMPORTANTE para evitar falha silenciosa

    if data == "btn_portfolio":
        resposta = respostas.get("portfólio", "Portfólio não disponível.")
        await callback_query.message.reply(f"👨‍💻 {nome}, aqui está meu portfólio:\n{resposta}")
    elif data == "btn_preco":
        resposta = respostas.get("preço", "Preços sob consulta.")
        await callback_query.message.reply(f"💰 {nome}, {resposta}")
    elif data == "btn_pagamento":
        resposta = respostas.get("pagamento", "Aceito Pix, boleto e cartão.")
        await callback_query.message.reply(f"💳 {nome}, {resposta}")
    else:
        await callback_query.message.reply("⚠️ Botão desconhecido.")

# (Opcional) resposta automática em grupo
if RESPONDER_EM_GRUPO:
    @app.on_message(filters.group & filters.text)
    async def responder_grupo(client, message):
        texto = message.text.lower()
        for chave, resposta in respostas.items():
            if chave in texto:
                nome = message.from_user.first_name or "amigo"
                await message.reply(f"👋 {nome}, {resposta}")
                break

app.run()
