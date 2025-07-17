from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Inventario como lista de diccionarios
inventario = []

# Función para buscar por código
def buscar_por_codigo(codigo):
    for producto in inventario:
        if producto["codigo"] == codigo:
            return producto
    return None

# Función para buscar por nombre
def buscar_por_nombre(nombre):
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return producto
    return None

# Agregar producto
def agregar_producto(nombre, cantidad, precio, codigo):
    if buscar_por_codigo(codigo):
        return "❌ Ya existe un producto con ese código."
    
    inventario.append({
        "nombre": nombre,
        "cantidad": int(cantidad),
        "precio": float(precio),
        "codigo": codigo
    })
    return "✅ Producto agregado correctamente."

# Mostrar inventario
def mostrar_inventario():
    if not inventario:
        return "📦 El inventario está vacío."
    texto = "📋 Inventario:\n"
    for p in inventario:
        texto += f"{p['codigo']} | {p['nombre']} | Cantidad: {p['cantidad']} | Precio: ${p['precio']:.2f}\n"
    return texto

# Calcular valor total
def calcular_valor_total():
    total = sum(p["cantidad"] * p["precio"] for p in inventario)
    return f"💰 Valor total del inventario: ${total:.2f}"

# Actualizar cantidad
def actualizar_cantidad(codigo, nueva_cantidad):
    producto = buscar_por_codigo(codigo)
    if producto:
        producto["cantidad"] = int(nueva_cantidad)
        return "✅ Cantidad actualizada."
    return "❌ Producto no encontrado."

# -------------------
# Funciones del BOT
# -------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy tu bot de inventario 🛒\n"
        "Usa estos comandos:\n"
        "/agregar nombre cantidad precio codigo\n"
        "/ver - ver inventario\n"
        "/buscar nombre\n"
        "/buscarcodigo codigo\n"
        "/actualizarcodigo codigo nueva_cantidad\n"
        "/valor - ver valor total"
    )

async def agregar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        nombre, cantidad, precio, codigo = context.args
        mensaje = agregar_producto(nombre, cantidad, precio, codigo)
    except:
        mensaje = "⚠️ Formato incorrecto. Usa: /agregar nombre cantidad precio codigo"
    await update.message.reply_text(mensaje)

async def ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(mostrar_inventario())

async def buscar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        nombre = " ".join(context.args)
        producto = buscar_por_nombre(nombre)
        if producto:
            mensaje = f"✅ Encontrado:\n{producto}"
        else:
            mensaje = "❌ Producto no encontrado."
    except:
        mensaje = "⚠️ Usa: /buscar nombre"
    await update.message.reply_text(mensaje)

async def buscarcodigo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        codigo = context.args[0]
        producto = buscar_por_codigo(codigo)
        if producto:
            mensaje = f"✅ Encontrado:\n{producto}"
        else:
            mensaje = "❌ Producto no encontrado."
    except:
        mensaje = "⚠️ Usa: /buscarcodigo código"
    await update.message.reply_text(mensaje)

async def actualizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        codigo, nueva_cantidad = context.args
        mensaje = actualizar_cantidad(codigo, nueva_cantidad)
    except:
        mensaje = "⚠️ Usa: /actualizarcodigo código nueva_cantidad"
    await update.message.reply_text(mensaje)

async def valor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(calcular_valor_total())

# -------------------
# Iniciar el bot
# -------------------

app = ApplicationBuilder().token("7583734984:AAGGjQU71QierMh8kvI8RYWNSg3Zq_20arI").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("agregar", agregar))
app.add_handler(CommandHandler("ver", ver))
app.add_handler(CommandHandler("buscar", buscar))
app.add_handler(CommandHandler("buscarcodigo", buscarcodigo))
app.add_handler(CommandHandler("actualizarcodigo", actualizar))
app.add_handler(CommandHandler("valor", valor))

print("🤖 Bot ejecutándose...")
app.run_polling()
