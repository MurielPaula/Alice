⚙️ Bot Configurado com:

- ( ex : )discord.pycom prefixo "a "(ex: a comando)

- comandos comUso de comandos slash comclient.tree.sync()

- Permissões amplas viaIntents.all()

🔐 APIs Integradas:
- Google Gemini ( genai.Client) para IA conversacional

- Laboratórios Eleven para geração de voz ( texto para fala ) .para geração de voz (texto para fala).

- Leitura de tokens usando o arquivo , com a biblioteca .usando o arquivo .env, com a biblioteca dotenv.

🤖 Nome do bot: Alice

# 🤖 Alice - Bot de Discord com IA e TTS

Alice é um bot de Discord desenvolvido em Python que integra:
- Geração de respostas contextuais com IA (Google Gemini)
- Conversão de texto em fala (TTS com `pyttsx3`)
- Interações por comandos e mensagens.
- Controle de canal autorizado para interação.

---

## 🚀 Funcionalidades

- 🧠 **Geração de respostas inteligentes** com base nas mensagens dos usuários usando o modelo Gemini.
- 🔊 **Leitura das respostas com voz**, utilizando a biblioteca `pyttsx3`.
- 🎯 **Restrição de comandos e mensagens** a um canal autorizado pelo comando `/configurar`.
- 🛠️ **Comando de teste** para validar se o bot está operando no canal correto.
- 🖼️ (Em desenvolvimento) Suporte a **análise de imagens** via URL.
- 🍷 Contador de quantas vezes a IA menciona a palavra "vinho" — por diversão ou estatística.

---

## 🧩 Requisitos

- Python 3.9+
- Um bot de Discord criado via [Discord Developer Portal](https://discord.com/developers/applications)
- Chave de API do [Google Gemini](https://ai.google.com/)

---

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/alice-discord-bot.git
cd alice-discord-bot
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```
| Exemplo de dependências necessárias: |
| ----|
```txt
discord.py
pyttsx3
requests
google-generativeai
```
3. Crie (ou edite) um arquivo .env com as variáveis necessárias:
```ini
DISCORD_TOKEN=seu_token_do_discord
GEMINI_API_KEY=sua_chave_gemini
```

## ⚙️ Uso
1. Execute o bot com:
```bash
python bot.py
```
2. No Discord, utilize o comando:
```bash
/configurar
```
Para definir o canal em que o bot poderá interagir com mensagens e comandos.
3. Mande uma mensagem mencionando a Alice:
```less
@Alice O que você acha de vinho?
```
A Alice responderá e, se estiver ativado, lerá a resposta em voz alta.

## 💡 Comandos Disponíveis

| Comando       | Descrição                                                      |
|---------------|----------------------------------------------------------------|
| `/configurar` | Define o canal atual como autorizado para interações.         |
| `/teste`      | (Opcional) Comando de exemplo para testar a funcionalidade TTS(texto para fala).        |


## 🎙️ Text-to-Speech (TTS)
Utiliza a biblioteca pyttsx3 para conversão de texto em voz. O áudio é reproduzido localmente — ideal para interações em tempo real ou streaming.

## 📸 Imagens com IA (em construção)

A estrutura está pronta para permitir envio de imagens via URL e processar via Gemini:
```
def verificar_conteudo_imagem(url_imagem):
    # Converte imagem em base64 e envia como parte do prompt
```
## 🔐 Canal Autorizado
O bot só responde a comandos e mensagens no canal autorizado via /configurar.

Isso evita que Alice interaja fora do contexto desejado ou em canais aleatórios.

## 📚 Arquitetura
- on_ready: Notifica que o bot está online.

- on_message: Lida com mensagens recebidas.

- @bot.command: Comandos manuais como /configurar.

- generate_response: Chama o Gemini com o prompt montado.

- falar: Converte resposta em fala usando TTS.

## 🧙 Sobre a Alice
Alice é uma IA misteriosa e elegante. Ela pode ser personalizada com diferentes personalidades ou modos de fala.
Você pode modificar o prompt base para ajustar o comportamento dela ao seu estilo.



