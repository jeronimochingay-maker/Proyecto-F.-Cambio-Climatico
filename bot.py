import os
import discord
from discord.ext import commands
from openai import OpenAI

client = OpenAI(
    api_key = ('TOKEN'),
base_url="https://api.groq.com/openai/v1"
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    description="Bot experto en cambio climático"
)

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")

@bot.command()
async def preguntar(ctx, *, pregunta):

    async with ctx.typing():

        try:
            respuesta = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Eres un experto en cambio climático. "
                            "Responde de forma clara, educativa y precisa. "
                            "Si la pregunta no está relacionada con cambio climático "
                            "o medio ambiente, indica que el bot solo responde "
                            "sobre esos temas."
                        )
                    },
                    {
                        "role": "user",
                        "content": pregunta
                    }
                ]
            )

            texto = respuesta.choices[0].message.content

            if len(texto) > 1900:
                texto = texto[:1900] + "..."

            await ctx.send(texto)

        except Exception as e:
            print(e)
            await ctx.send("Error al consultar la IA.")

bot.run('TOKEN_DISCORD')
