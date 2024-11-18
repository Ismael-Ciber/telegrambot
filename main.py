from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import subprocess

# Cargar variables de entorno
load_dotenv()
API_KEY = os.getenv("API_KEY")
AUTHORIZED_TELEGRAM_ID = int(os.getenv("AUTHORIZED_TELEGRAM_ID"))

# Decorador para verificar autorización
# Este decorador verifica que el usuario que ha introducido el comando somos nosotros (haciendo uso de AUTHORIZED_TELEGRAM_ID)
# para todos los próximos comandos del bot
def require_authorization(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != AUTHORIZED_TELEGRAM_ID:
            await update.message.reply_text("No estás autorizado para usar este bot.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

# Comandos del bot
@require_authorization
async def saludo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hola!")

@require_authorization
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Por favor, proporciona un dominio.")
        return

    domain = context.args[0]
    try:
        resultados = subprocess.run(
            ["./scan.sh", domain],
            capture_output=True,
            text=True,
            check=True
        )
        await update.message.reply_text(resultados.stdout)
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"Error al ejecutar el escaneo: {e}")

# Configuración principal del bot
def main():
    app = ApplicationBuilder().token(API_KEY).build()
    app.add_handler(CommandHandler("saludo", saludo))
    app.add_handler(CommandHandler("scan", scan))
    print("Bot iniciado")
    app.run_polling()

if __name__ == "__main__":
    main()
