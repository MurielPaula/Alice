# 🤖 Alice - Bot de Discord com IA e TTS
Alice é uma assistente IA para Discord, equipada com geração de respostas inteligentes e conversão de texto em fala (TTS). Ideal para comunidades que buscam uma interação diferenciada e divertida.

## ⚙️ Bot Configurado com:
- discord.py com suporte a comandos tradicionais e comandos slash (client.tree.sync()).

- Permissões amplas ativadas com Intents.all().

- Prefixo opcional: a (ex: a comando).

## 🔐 APIs Integradas
- Google Gemini (genai.Client) para IA conversacional.

- Eleven Labs para geração de voz (texto para fala).

- dotenv para leitura de tokens e configurações a partir do arquivo .env.

## 🚀 Funcionalidades
- 🧠 Respostas inteligentes com IA (Google Gemini).

- 🔊 Conversão de texto em fala, utilizando pyttsx3.

- 🎯 Canal autorizado: o bot só interage em um canal definido com /configurar.

- 🛠️ Comando de teste para validar o funcionamento.

- 🖼️ (Em construção) Suporte a análise de imagens via URL.

- 🍷 Contador de vinho: acompanha quantas vezes a IA menciona a palavra "vinho".

## 🧩 Requisitos
- Python 3.9+

- Um bot criado no Discord Developer Portal

- Chave de API do Google Gemini

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
| `/teste`      | Testa o funcionamento do bot e da voz.        |


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

## 🧪 Exemplo de uso
No canal autorizado:

```bash
@Alice Olá! Você gosta de vinho?
```
A Alice irá:

- Gerar uma resposta com IA
- Falar a resposta (TTS ativo)

Resultado:

```mathematica
Claro! O vinho é uma bebida com muita história e complexidade. 🍷
```

## 📚 Arquitetura
- on_ready: Notifica que o bot está online.

- on_message: Lida com mensagens recebidas.

- @bot.command: Comandos manuais como /configurar.

- generate_response: Chama o Gemini com o prompt montado.

- falar: Converte resposta em fala usando TTS.

## 🧙 Sobre a Alice
Alice é uma IA misteriosa e elegante. Ela pode ser personalizada com diferentes personalidades ou modos de fala.
Você pode modificar o prompt base para ajustar o comportamento dela ao seu estilo.



