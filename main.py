faarom dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import subprocess

# Cargar variables de entorno
load_dotenv()
API_KEY = os.getenv("API_KEY")
AUTHORIZED_TELEGRAM_ID = int(os.getenv("AUTHORIZED_TELEGRAM_ID"))

# Decorador para verificar autorización
def require_authorization(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != AUTHORIZED_TELEGRAM_ID:
            await update.message.reply_text("No estás autorizado para usar este bot.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

# Comando para saludar al usuario
@require_authorization
async def saludo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hola!")

# Comando para escanear y enviar el PDF
@require_authorization
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Por favor, proporciona un dominio.")
        return

    domain = context.args[0]
    try:
        # Ejecutar el script de escaneo
        subprocess.run(
            ["./scan.sh", domain],
            text=True,
            check=True
        )
        await update.message.reply_text("Escaneo completado con éxito. Enviando resultados...")

        # Ruta al archivo PDF generado por el escaneo
        ruta_pdf = f"./resultado_{domain}.pdf"

        # Enviar el archivo PDF
        with open(ruta_pdf, "rb") as pdf:
            await update.message.reply_document(document=pdf, filename=f"./resultado_{domain}.pdf")

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
