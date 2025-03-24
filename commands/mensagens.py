import discord
import os
import asyncio
import google.generativeai as genai
from collections import deque
from gtts import gTTS
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

GENAI_API_KEY = os.getenv('GENAI_API_KEY')
genai.configure(api_key= GENAI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

message_history = {}
async def on_message(message):
    print(f'Mensagem recebida no canal {message.channel.name}: {message.content}') 
    if message.author.bot or len(message.content) > 200:
        return
    channel_id = message.channel.id

    if "alice" in message.content.lower():
        # contextualiza pelo histórico de mensagens
        if channel_id not in message_history:
            message_history[channel_id] = deque(maxlen=5) # Máximo de 5 mensagens

        message_history[channel_id].append(f"Usuário: {message.content}")
        context = "\n".join(message_history[channel_id])
        
        prompt = (
                "Você é Alice, uma vampira inteligente e espirituosa no Discord. Filha de Muriel, também conhecido como Quasartioon. "
                f"Seja breve e direta em suas respostas, utilizando no máximo 50 palavras."
                f"Aqui está o contexto recente da conversa:\n{context}\n"
                f"Responda à última mensagem que o usuário mandou: {message.content.lower()}"
            )
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                generated_response = response.text.strip()
                message_history[channel_id].append(f"Alice: {generated_response}")
            else:
                generated_response = "Hmm, parece que não consegui pensar em nada agora."
            await message.channel.send(generated_response)
        except Exception as e:
            await message.channel.send('Meu programador é tão burro que não consegue me possibilitar de comunicar...')
            print(f'Erro ao gerar a resposta: {e}')

    # Garantia o processamento
    

async def ping(ctx):
    await ctx.send('Pong! 🏓')


async def contar(ctx, inicio: int):
    if inicio <= 0: 
        await ctx.send('Ai cê me quebrea... Digita um número maior que zero pô')
        return
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client:
        for i in range (inicio, 0, -1):
            tts_path = "output.mp3"
            tts = gTTS(str(i), lang='pt')
            tts.save(tts_path)

            ctx.voice_client.stop()
            source = discord.FFmpegPCMAudio(tts_path)
            ctx.voice_client.play(source, after=lambda e: print('Audio finalizado :', e))
            while ctx.voice_client.is_playing():
                await asyncio.sleep(0.5)
        for member in voice_channel.members:
            try:
                await member.move_to(None)
            except discord.Forbidden:
                await ctx.send(f'To sendo oprimida, não consigo tirar o {member.mention} da call')
            except discord.HTTPException as e:
                await ctx.send(f'Erro ao desconectar {member.mention}: {e}')
        
        await ctx.send('Boa noite rapaziada! @everyone')
    else:
        await ctx.send('Me coloca no canal primeiro, poxa.')

async def contar_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Isso nem sequer é um número, cara...')


async def boa_noite(ctx):
    await ctx.send('Boa noite, lindinho... 💋💋')

async def entrar(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await ctx.send('To entrando...')
        await channel.connect()
    else:
        await ctx.send('Entra numa call primeiro, né mano.')


async def falar(ctx, *, texto):
    if ctx.voice_client:
        tts_path = "output.mp3"
        tts = gTTS(texto, lang='pt')
        tts.save(tts_path)

        ctx.voice_client.stop()
        source = discord.FFmpegPCMAudio(tts_path)
        ctx.voice_client.play(source, after=lambda e: print('Audio finalizado :', e))
        print(f'Falando: {texto}')
    else:
        await ctx.send('Primeiro eu preciso estar em um canal de voz...')


async def sair(ctx):
    if ctx.voice_client:
        await ctx.send('To saindo, pera ai...')
        await ctx.voice_client.disconnect()
    else:
        await ctx.send('Mas eu nem to em um canal de voz, cara.')