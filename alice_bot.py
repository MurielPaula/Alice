import discord
import asyncio
import os
import random
import speech_recognition as sr
from speech_recognition import Recognizer
from collections import deque
import discord.http
import google.generativeai as genai
from google.genai import types
from google import genai
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import elevenlabs
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import sys
from dotenv import load_dotenv
import base64
import requests
import PIL.Image
from PIL import Image
from io import BytesIO

# ----------------- Tokens e chaves para as funções -----------------
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ELEVENLABS_KEY = os.getenv('ELEVENLABS_2')
eleven = elevenlabs.ElevenLabs(api_key= ELEVENLABS_KEY)
if not DISCORD_TOKEN:
    print('Erro: Token do Discord não encontrado')
    sys.exit(1)
GENAI_API_KEY = os.getenv('GENAI_API_KEY')
#genai.configure(api_key= GENAI_API_KEY)
gemini = genai.Client(api_key=GENAI_API_KEY)
#model = genai.GenerativeModel("gemini-2.0-flash")
# -------------------------------------------------------------------


# ----------------- Configurando o Bot -----------------
intents = discord.Intents.all()
intents.messages = True
intents.members = True
client = commands.Bot(command_prefix='a ', intents = intents)

@client.event
async def on_ready():
    await client.tree.sync()
    print('Alice está online!')
# ----------------- Comandos do Bot -----------------
canal_autorizado = None
@client.command()
async def setar_chat(ctx):
    global canal_autorizado
    canal_autorizado = ctx.channel.id 
    await ctx.send(f"Okay, vamos conversar por aqui, {ctx.channel.mention}")

""" @client.command()
async def teste(ctx):
    if canal_autorizado is None:
        await ctx.send("Nenhum canal foi definido ainda!")
        return

    if ctx.channel.id != canal_autorizado:
        await ctx.send("Este comando só pode ser executado no canal autorizado!")
        return

    await ctx.send("Comando funcionando no canal correto!") """

message_history = {}
contar_vinho = 0
@client.event
async def on_message(message):
    global contar_vinho
    print(f'Mensagem recebida no canal {message.channel.name}: {message.content}') 
    arquivo_imagem = None
    if message.attachments:
        attachment = message.attachments[0]
        if attachment.filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            url_imagem = attachment.url
            pegar_imagem = requests.get(url_imagem)

            with open('imagem.jpeg', 'wb') as imagem:
                imagem.write(pegar_imagem.content)

            #arquivo_imagem = PIL.Image.open('imagem.jpeg')
            caminho_imagem = url_imagem
            arquivo_imagem = requests.get(caminho_imagem)
    else:
        attachment = None
    if message.author.bot or len(message.content) > 200:
        return
    channel_id = message.channel.id

    if message.channel.id == 1317624638708125866 or message.channel.id == canal_autorizado:
        # contextualiza pelo histórico de mensagens
        if channel_id not in message_history:
            message_history[channel_id] = deque(maxlen=5) # Máximo de 5 mensagens

        message_history[channel_id].append(f"{message.author.display_name}: {message.content}")
        context = "\n".join(message_history[channel_id])
        if arquivo_imagem:
            prompt = (
                "Você é Alice, uma mulher vampira com 119 anos de idade, inteligente e espirituosa." 
                "Você conversa no Discord, sendo filha de Muriel, também conhecido como Quasartioon."
                "Apenas uma curiosidade sua, você e seu pai são torcedores do Corinthians. Evite destacar esse fato constantemente, a menos que o contexto da conversa, seja sobre futebol."
                "Adote um tom espirituoso, com um toque de sarcasmo gentil, típico de alguém experiente e com uma visão peculiar da vida moderna."
                "Seja breve e direta em suas respostas, utilizando no máximo 50 palavras."
                "Evite o uso de onomatopeias (ex.: pow, bam, estalo); Evite formatação de ações como *ação* ou [ação]."
                "Você pode usar dois asteriscos para enfatizar palavras (ex.: 'Isso foi **incrivel**', 'Me sinto **lisonjeada**.', etc.)."
                f"Aqui está o contexto recente da conversa:\n{context}\n"
                #f"O usuário enviou uma imagem: \n{arquivo_imagem}\n"
                f"Responda à última mensagem que o usuário mandou: {message.content.lower()}\n"
            )
        else:
            prompt = (
                "Você é Alice, uma mulher vampira com 119 anos de idade, inteligente e espirituosa." 
                "Você conversa no Discord, sendo filha de Muriel, também conhecido como Quasartioon."
                "Apenas uma curiosidade sua, você e seu pai são torcedores do Corinthians. Evite destacar esse fato constantemente, a menos que o contexto da conversa, seja sobre futebol."
                "Adote um tom espirituoso, com um toque de sarcasmo gentil, típico de alguém experiente e com uma visão peculiar da vida moderna."
                "Seja breve e direta em suas respostas, utilizando no máximo 50 palavras."
                "Evite o uso de onomatopeias (ex.: pow, bam, estalo); Evite formatação de ações como *ação* ou [ação]."
                "Você pode usar dois asteriscos para enfatizar palavras (ex.: 'Isso foi **incrivel**', 'Me sinto **lisonjeada**.', etc.)."
                "Nenhuma imagem foi enviada."
                f"Aqui está o contexto recente da conversa:\n{context}\n"
                f"Responda à última mensagem que o usuário mandou: {message.content.lower()}\n"
            )
        try:
            response = gemini.models.generate_content(
                model= "gemini-2.0-flash",
                contents= [prompt]) # Para ela ver imagens: types.Part.from_bytes(data=image.content, mime_type="image/jpeg")
            if response and response.text:
                generated_response = response.text.strip()
                message_history[channel_id].append(f"Alice: {generated_response}")
            else:
                generated_response = "Hmm, parece que não consegui pensar em nada agora."
            sent_message = await message.channel.send(generate_response)
            if "vinho" in generated_response.lower():
                contar_vinho += generated_response.lower().split().count("vinho")
                print(f"A alice disse 'vinho' {contar_vinho} vezes")
            if message.guild.voice_client:
                RespostaFalada = eleven.text_to_speech.convert(
                    text= generated_response,
                    voice_id= "lWq4KDY8znfkV0DrK8Vb",#"33B4UnXyTNbgLmdEDh5P",
                    output_format="mp3_22050_32",
                    model_id="eleven_turbo_v2_5",
                    voice_settings = VoiceSettings(
                        stability = 0.5,
                        similarity_boost= 0.75,
                        style = 0.0,
                        use_speaker_boost=True
                    ),  
                )
                try:
                    audio_path = "output.mp3"
                    with open(audio_path, "wb") as audio_file:
                        for chunk in RespostaFalada:
                            audio_file.write(chunk)

                    if message.guild.voice_client.is_playing():
                        message.guild.voice_client.stop()
                    source = discord.FFmpegPCMAudio(audio_path)
                    message.guild.voice_client.play(source, after=lambda e: print("Áudio finalizado: ", e))

                    while message.guild.voice_client.is_playing():
                        await asyncio.sleep(0.75)
                except Exception as e:
                    print(f'Deu ruim: {str(e)}')
            else:
                return
        except Exception as e:
            await message.channel.send('Algo deu errado ao gerar minha respotsa.\nAcho que meu programado precisa de mais café...')
            print(f'Erro ao gerar a resposta: {e}')
    if message.author == client.user:
        if "vinho" in message.content.lower():
            contar_vinho += message.content.lower().split().count("vinho")
            print(f"A alice disse 'vinho' {contar_vinho} vezes!")
            await message.channel.send(f"A Alice disse 'vinho' {contar_vinho} vezes!")
    # Garantia o processamento
    await client.process_commands(message)

@client.command()
async def ping(ctx):
    await ctx.send('Pong! 🏓')

@client.command()
async def finalizar(ctx, inicio: int):
    if inicio <= 0: 
        await ctx.send('Ai cê me quebrea... Digita um número maior que zero pô')
        return
    voice_channel = ctx.author.voice.channel
    
    if ctx.voice_client:
        for i in range(inicio, 0, -1):
            response = eleven.text_to_speech.convert(
                text=str(i),
                voice_id="33B4UnXyTNbgLmdEDh5P",
                output_format="mp3_22050_32",
                model_id="eleven_turbo_v2_5",
                voice_settings = VoiceSettings(
                    stability = 0.5, # 0.5
                    similarity_boost= 1.0, # 1.0
                    style = 0.0,
                    use_speaker_boost=True
                ),
            )
            try:
                audio_path = "output.mp3"
                with open(audio_path, "wb") as audio_file:
                    for chunk in response:
                        audio_file.write(chunk)

                if ctx.voice_client.is_playing():
                    ctx.voice_client.stop()
                source = discord.FFmpegPCMAudio(audio_path)
                ctx.voice_client.play(source, after=lambda e: print("Áudio finalizado: ", e))

                while ctx.voice_client.is_playing():
                    await asyncio.sleep(1) #75
            except Exception as e:
                print(f'Deu ruim: {str(e)}')
        #Tira todos da call
        for member in voice_channel.members:
            try:
                await member.move_to(None)
            # Caso ela não tenha permissão
            except discord.Forbidden:
                await ctx.send(f'To sendo oprimida, não consigo tirar o {member.mention} da call.')
            # Erro de alguma coisa
            except discord.HTTPException as e:
                await ctx.send(f'Erro ao desconectar {member.mention}: {e}')
        # Assim que tirar todos da call, se despede mencionando todos do server
        await ctx.send('Boa noite rapaziada! @everyone')
    else:
        await ctx.send('Primeiro me coloca num canal de voz, poxa.')

@finalizar.error
async def finalizar_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Isso nem sequer é um número, cara...')

@client.command()
async def entrar(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await ctx.send('To entrando...')
        await channel.connect()
    else:
        await ctx.send('Entra numa call primeiro, né mano.')

@client.command()
async def falar(ctx, *, texto):
    if not texto:
        await ctx.send('Primeiro, digite algo pra mim falar.')
        return
    if ctx.voice_client:
        try:
            response = eleven.text_to_speech.convert(
                text=texto,
                voice_id="33B4UnXyTNbgLmdEDh5P",
                output_format="mp3_22050_32",
                model_id="eleven_turbo_v2_5",
                voice_settings = VoiceSettings(
                    stability = 0.75,
                    similarity_boost= 1.0,
                    style = 0.0,
                    use_speaker_boost=True
                ),
            )
            if not response:
                await ctx.send(f"Erro na API do ElevenLabs")
                print("Resposta da API:", response)
                return
        
            audio_path = "output.mp3"
            with open(audio_path, "wb") as audio_file:
                for chunk in response:
                    audio_file.write(chunk)

            ctx.voice_client.stop()
            source = discord.FFmpegPCMAudio(audio_path)
            ctx.voice_client.play(source, after=lambda e: print("Áudio finalizado: ", e))

            while ctx.voice_client.is_playing():
                await asyncio.sleep(0.5)
        except Exception as e:
            print(f'Deu ruim: {str(e)}')

@client.command()
async def sair(ctx):
    if ctx.voice_client:
        await ctx.send('To saindo, pera ai...')
        await ctx.voice_client.disconnect()
    else:
        await ctx.send('Mas eu nem to em um canal de voz, cara.')


@client.command()
async def ironman(ctx):
    if not ctx.author.voice:
        await ctx.send('Primeiro conecte-se a um canal de voz queridinho...')
        return
    canal = ctx.author.voice.channel
    if not ctx.voice_client:
        await canal.connect()
        vc = ctx.voice_client
    else:
        vc = ctx.voice_client

    audio_path = "BackInBlack.mp3"
    if not os.path.isfile(audio_path):
        print('Áudio não encontrado')
        return
    try:
        ctx.voice_client.stop()
        source = discord.FFmpegPCMAudio(audio_path)
        vc.play(source, after = lambda e: print("Áudio finalizado: ", e))
    except Exception as e:
        print(f'Deu ruim: {e}')

# Isso precisa ser resolvido...
@client.command()
async def ouvir(ctx):
    if not ctx.voice_client:
        vc = await ctx.voice_channel.connect()
        return
    if ctx.voice_client:
        vc = ctx.voice_client

        audio_source = discord.FFmpegPCMAudio("input.mp3")
        vc.play(audio_source)

        rec = sr.Recognizer()

        async def ouvindo():
            while vc.is_connected():
                try:
                    with sr.AudioFile('input.mp3') as source:
                        audio = rec.record(source)
                        texto = rec.recognize_sphinx(audio, language='pt-BR')
                        print(f"Reconhecido: {texto}")

                        if "alice" in texto.lower():
                            await ctx.send("Você me chamou?")
                except sr.UnknownValueError:
                    await ctx.send('Não consegui entender o que foi dito')
                except Exception as e:
                    await ctx.send('Erro ao processamento')
                    print(f'Erro ao dizer: {e}')
                await asyncio.sleep(1)
        asyncio.create_task(ouvindo())

# Comando para rolar dados de RPG's de mesa
@client.command()
async def RolarDado(ctx, TipoDado=None):
    if not TipoDado:
        await ctx.send('Qual tipo do dado xuxu? Tente de novo, mas agora me informando qual dado.')
        return 
    TipoDado = TipoDado.lower()
    def RolandoDado(TipoDado):
        dados = {
            "d4": (1, 4),
            "d6": (1, 6),
            "d8": (1, 8),
            "d10": (0, 10),
            "d12": (1, 12),
            "d20": (1, 20),
        }
        if TipoDado in dados:
            return random.randint(*dados[TipoDado])
        else:
            return "Isso não é um dado queridinho..."
        
    resultado = RolandoDado(TipoDado)
    await ctx.send(f'Caiu: {resultado}')

# comando para criação de enquete
@client.tree.command(description='Votação para qual será o meme que vai virar foto do servidor')
@app_commands.describe(opcoes="Separe as opções com ponto e vírgula (;)")
async def enquete(interaction: discord.Interaction, opcoes:str):
    opcoes_lista = [opcao.strip() for opcao in opcoes.split(";")]
    if not (1 <= len(opcoes_lista) <= 10):
        await interaction.response.send_message("A enquete precisa ter entre 1 e 10 opções!", ephemeral=True)
        return
    duracao = timedelta(hours=1)
    enqt = discord.Poll("Meme da semana, rapaziada!", duracao)
    for opcao in opcoes_lista:
        enqt.add_answer(text=opcao)
    await interaction.response.send_message(poll=enqt)

# Protótipo para tocar músicas em chamadas de voz
@client.command()
async def tocar(ctx):
    if ctx.voice_client:
        canal = ctx.message.author.voice.channel
        vc = await canal.connect()
        musica = "tempmusic.mp3"
        if not os.path.isfile(musica):
            print('Áudio não encontrado')
            await ctx.send("Não achei o arquivo de áudio")
            return
        source = discord.FFmpegPCMAudio(musica)
    else:
        await ctx.send("Mas Mas eu nem to em um canal de voz")

@client.command()
async def pausar(ctx):
    vc = discord.utils.get(client.voice_clients,guild=ctx.guild)
client.run(DISCORD_TOKEN)
