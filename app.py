import random
import pandas as pd
import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Startup Life - Simulador",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Estilos CSS corregidos para alta legibilidad y contraste
st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: #f8fafc;
    }

    .main-title {
        text-align: center;
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 20px;
    }

    .metric-card {
        background: #1e293b;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        border: 1px solid #334155;
    }
    .card-capital { border-top: 4px solid #4ade80; }
    .card-clientes { border-top: 4px solid #38bdf8; }
    .card-reputacion { border-top: 4px solid #facc15; }

    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 4px;
    }

    .question-card {
        background: #1e293b;
        border-radius: 16px;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 20px;
        border: 1px solid #475569;
    }

    /* Botones oscuros con texto claro contrastado */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 14px 18px;
        font-size: 1rem;
        font-weight: 600;
        background-color: #334155 !important;
        color: #ffffff !important;
        border: 1px solid #64748b !important;
        transition: all 0.2s ease;
        margin-bottom: 8px;
        text-align: left;
    }

    div.stButton > button:hover {
        background-color: #475569 !important;
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
    }

    /* Botón de descarga */
    div.stDownloadButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 12px 18px;
        font-size: 1rem;
        font-weight: 700;
        background-color: #0284c7 !important;
        color: #ffffff !important;
        border: none !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #0369a1 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Encabezado visual
st.markdown(
    '<h1 class="main-title">🚀 Startup Life: Simulador</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-title">Toma decisiones estratégicas. Mantén tu reputación'
    " sobre 30 y evita la quiebra.</p>",
    unsafe_allow_html=True,
)

# Banco total de preguntas (16 escenarios sin revelar impactos en la interfaz)
BANCO_PREGUNTAS = [
    {
        "titulo": "Lanzamiento del Producto",
        "situacion": (
            "Tienes $1,500 de ahorros iniciales. ¿Cómo vas a salir al mercado?"
        ),
        "opciones": [
            ("🚀 Lanzar un Producto Mínimo Viable (PMV) Básico", -500, 15, 10, "Lanzó PMV Básico"),
            ("🧪 Hacer un testeo interno con una Versión Beta Gratuita", -100, 5, 2, "Lanzó Beta Gratuito"),
            ("⭐ Lanzar el Producto Completo con todas sus funcionalidades", -1400, 40, 25, "Lanzó Producto Completo"),
        ],
    },
    {
        "titulo": "Estrategia de Crecimiento",
        "situacion": (
            "Necesitas conseguir tus primeros usuarios de forma constante."
        ),
        "opciones": [
            ("🔥 Invertir en Pauta Pagada Masiva en Redes Sociales", -600, 50, 10, "Pauta Pagada Masiva"),
            ("📱 Ejecutar una Campaña de Publicidad Moderada", -150, 20, 5, "Pauta Moderada"),
            ("🌱 Apostar por Crecimiento Orgánico y Recomendaciones", 0, 10, 15, "Crecimiento Orgánico"),
        ],
    },
    {
        "titulo": "Gestión de Crisis Inicial",
        "situacion": (
            "Un proveedor falló y el 20% de los primeros pedidos llegaron con"
            " retraso."
        ),
        "opciones": [
            ("💰 Ofrecer Reembolso e Indemnización Total a los afectados", -500, 0, 20, "Reembolso Total"),
            ("🎟️ Enviar un Cupón de Descuento para la próxima compra", -100, -5, 5, "Cupón de Descuento"),
            ("🤷‍♂️ Ignorar los Reclamos y enfocarse en los clientes nuevos", 0, -20, -35, "Ignorar Reclamos"),
        ],
    },
    {
        "titulo": "Retroalimentación del Cliente",
        "situacion": (
            "Los usuarios están pidiendo una nueva función muy solicitada."
        ),
        "opciones": [
            ("🛠️ Desarrollar e integrar la nueva función de inmediato", -400, 15, 10, "Nueva función desarrollada"),
            ("📊 Hacer una encuesta y lanzar una Demo previa muy sencilla", -100, 5, 2, "Demo Sencilla"),
            ("⏸️ Mantener el producto actual sin cambios por ahora", 0, -5, -10, "Mantuvo producto actual"),
        ],
    },
    {
        "titulo": "Contratación de Personal",
        "situacion": "El crecimiento está aumentando la carga de trabajo en el equipo.",
        "opciones": [
            ("👔 Contratar a un perfil Senior con mucha experiencia", -500, 10, 5, "Contrató perfil Senior"),
            ("🤝 Contratar un apoyo Freelance de forma temporal", -200, 4, 2, "Contrató apoyo Freelance"),
            ("💪 Exigir un esfuerzo extra al equipo actual sin contratar", 0, -5, -15, "Sin nuevas contrataciones"),
        ],
    },
    {
        "titulo": "Estrategia ante la Competencia",
        "situacion": (
            "Aparece un competidor directo ofreciendo un producto similar a menor precio."
        ),
        "opciones": [
            ("🏷️ Reducir tus precios para competir agresivamente", -200, 15, 0, "Redujo precios"),
            ("🎧 Reforzar la Atención y Soporte al Cliente", -50, 3, 5, "Reforzó servicio al cliente"),
            ("💎 Apostar por la Diferenciación de Alta Calidad", -300, 8, 15, "Diferenció por Calidad"),
        ],
    },
    {
        "titulo": "Oferta de Inversionista",
        "situacion": "Un inversionista ángel ofrece un capital adicional para acelerar el negocio.",
        "opciones": [
            ("📈 Aceptar la Inversión Total a cambio de ceder participación", 1500, 10, 0, "Aceptó Inversión externa"),
            ("🤝 Aceptar una Inversión Parcial más conservadora", 500, 3, 2, "Aceptó Inversión parcial"),
            ("🛡️ Rechazar la oferta y mantener el control total del negocio", 0, 0, 5, "Mantuvo Control total"),
        ],
    },
    {
        "titulo": "Capacidad Operativa",
        "situacion": "La demanda está aumentando y comienzan a generarse cuellos de botella.",
        "opciones": [
            ("🏭 Invertir fuertemente en Infraestructura y Tecnología", -600, 20, 10, "Invirtió en Capacidad"),
            ("📦 Subcontratar parte de la producción o logística", -250, 5, 2, "Subcontrató producción"),
            ("⚠️ Mantener la capacidad actual y procesar pedidos a ritmo lento", 0, -10, -20, "Mantuvo Capacidad"),
        ],
    },
    {
        "titulo": "Alianza Estratégica",
        "situacion": (
            "Otra startup complementaria propone promocionar ambos productos juntos."
        ),
        "opciones": [
            ("🤝 Firmar una Alianza Estratégica y co-branding completo", -200, 20, 5, "Aceptó Alianza Estratégica"),
            ("🌐 Realizar una Colaboración Digital Puntual en redes", -50, 8, 2, "Colaboración Puntual"),
            ("🚶‍♂️ Rechazar y continuar operando de forma independiente", 0, 0, 0, "Continuó Individualmente"),
        ],
    },
    {
        "titulo": "Crisis de Redes Sociales",
        "situacion": (
            "Un cliente referente publica una crítica negativa que empieza a hacerse viral."
        ),
        "opciones": [
            ("🎁 Contactar al cliente, disculparse públicamente y compensarlo", -250, 0, 10, "Respondió y Compensó"),
            ("📢 Emitir un Comunicado Oficial aclarando la situación", -50, -2, 2, "Comunicado Oficial"),
            ("🔇 Ignorar la publicación para no darle más visibilidad", 0, -10, -25, "Ignoró la Crítica"),
        ],
    },
    {
        "titulo": "Ciberseguridad y Datos",
        "situacion": (
            "Se detectó un intento de acceso no autorizado a la plataforma."
        ),
        "opciones": [
            ("🔒 Contratar una Auditoría Completa de Ciberseguridad", -450, 0, 15, "Auditoría de Seguridad"),
            ("🛡️ Aplicar Parches y Actualizaciones de seguridad básicas", -100, 0, 5, "Parches Básicos"),
            ("⚠️ Ignorar la alerta al no registrarse pérdidas graves", 0, -15, -30, "Ignoró Alerta Ciberseguridad"),
        ],
    },
    {
        "titulo": "Campaña de Influencers",
        "situacion": (
            "Un creador de contenido relevante en tu sector ofrece promocionarte."
        ),
        "opciones": [
            ("🌟 Contratar una Campaña Exclusiva de recomendación", -500, 35, 10, "Campaña Influencer Exclusiva"),
            ("🎁 Enviar Muestras Gratis del producto esperando mención orgánica", -120, 12, 3, "Muestras Gratis"),
            ("❌ Rechazar la propuesta y mantener el enfoque actual", 0, 0, 0, "Rechazó Influencer"),
        ],
    },
    {
        "titulo": "Regulaciones e Impuestos",
        "situacion": (
            "Se aprueba un ajuste normativo que requiere adecuar tu modelo comercial."
        ),
        "opciones": [
            ("📜 Contratar Asesoría Jurídica Completa para estar 100% en regla", -350, 0, 10, "Asesoría Jurídica Completa"),
            ("📝 Realizar un Trámite Interno Básico de adecuación", -100, 0, 2, "Trámite Interno Básico"),
            ("⏳ Postergar la adecuación hasta recibir una notificación formal", 0, 0, -20, "Postergó Ajuste Legal"),
        ],
    },
    {
        "titulo": "Expansión Geográfica",
        "situacion": "Aparece la oportunidad de abrir ventas en una nueva provincia.",
        "opciones": [
            ("🌍 Iniciar una Expansión Total e inmediata en la nueva zona", -600, 25, 0, "Expansión Total"),
            ("🏙️ Hacer una Prueba Piloto Regional con presupuesto acotado", -250, 10, 3, "Prueba Piloto Regional"),
            ("🏛️ Consolidar primero el Mercado Actual antes de expandirse", -100, 5, 5, "Consolidó Mercado Actual"),
        ],
    },
    {
        "titulo": "Adopción de Inteligencia Artificial",
        "situacion": (
            "Puedes integrar herramientas de IA para automatizar la operación."
        ),
        "opciones": [
            ("🤖 Implementar IA Avanzada en la atención y ventas", -400, 20, 10, "Implementación IA Avanzada"),
            ("💬 Integrar un Chatbot Sencillo de respuestas automáticas", -100, 5, 2, "Chatbot Sencillo"),
            ("📞 Mantener el esquema de atención manual tradicional", 0, -5, 0, "Atención Manual"),
        ],
    },
    {
        "titulo": "Innovación de Producto",
        "situacion": "El mercado exige renovar el diseño y la interfaz general de tu servicio.",
        "opciones": [
            ("🚀 Invertir en un Rediseño Total de la plataforma", -700, 30, 15, "Rediseño Total"),
            ("📈 Aplicar Ajustes Visuales Menores sin alterar la estructura", -200, 8, 5, "Ajustes Menores"),
            ("🔒 Mantener la Versión Actual sin gastar recursos", 0, -10, -10, "Mantuvo Versión Actual"),
        ],
    },
]

# Inicialización del juego y selección aleatoria de 10 preguntas
if "dinero" not in st.session_state:
    st.session_state.dinero = 1500
    st.session_state.clientes = 10
    st.session_state.reputacion = 50
    st.session_state.fase = 0
    st.session_state.historial = []
    # Selecciona 10 preguntas al azar del banco
    st.session_state.preguntas_juego = random.sample(BANCO_PREGUNTAS, 10)


def tomar_decision(fase_nombre, eleccion, costo_capital, delta_clientes, delta_reputacion):
    st.session_state.dinero += costo_capital
    st.session_state.clientes += delta_clientes
    st.session_state.reputacion += delta_reputacion

    st.session_state.historial.append({
        "Fase": f"Paso {st.session_state.fase + 1}: {fase_nombre}",
        "Decisión": eleccion,
        "Cambio Capital": f"${costo_capital:+d}",
        "Cambio Clientes": f"{delta_clientes:+d}",
        "Cambio Reputación": f"{delta_reputacion:+d}",
        "Capital Restante": f"${st.session_state.dinero}",
        "Reputación Restante": f"{st.session_state.reputacion}"
    })

    st.session_state.fase += 1
    st.rerun()


# Panel visual de métricas del jugador
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
        <div class="metric-card card-capital">
            <span style="font-size: 0.85rem; color: #4ade80;">💵 CAPITAL</span>
            <div class="metric-value" style="color: #4ade80;">${st.session_state.dinero}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card card-clientes">
            <span style="font-size: 0.85rem; color: #38bdf8;">👥 CLIENTES</span>
            <div class="metric-value" style="color: #38bdf8;">{max(0, st.session_state.clientes)}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card card-reputacion">
            <span style="font-size: 0.85rem; color: #facc15;">⭐ REPUTACIÓN</span>
            <div class="metric-value" style="color: #facc15;">{max(0, st.session_state.reputacion)}/100</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# Validación de Game Over (Pérdida por Capital <= 0 o Reputación <= 30)
game_over = False
if st.session_state.dinero <= 0:
    st.error("💥 ¡QUIEBRA TÉCNICA! Te quedaste sin capital suficiente para continuar operando.")
    game_over = True
elif st.session_state.reputacion <= 30:
    st.error("💥 ¡CRISIS SEVERA DE REPUTACIÓN! Tu reputación cayó a 30 o menos y la empresa perdió total credibilidad.")
    game_over = True

fase_actual = st.session_state.fase

# Renderizado de Pregunta Actual
if not game_over and fase_actual < 10:
    datos = st.session_state.preguntas_juego[fase_actual]
    
    st.markdown(f"""
        <div class="question-card">
            <h3 style="color: #38bdf8; margin-bottom: 8px;">Paso {fase_actual + 1} de 10: {datos['titulo']}</h3>
            <p style="font-size: 1.05rem; color: #f8fafc; line-height: 1.5; margin: 0;">{datos['situacion']}</p>
        </div>
    """, unsafe_allow_html=True)

    for texto, capital, clientes, reputacion, log in datos["opciones"]:
        if st.button(texto, use_container_width=True):
            tomar_decision(datos['titulo'], log, capital, clientes, reputacion)

# Pantalla de Fin de Juego
elif game_over or fase_actual >= 10:
    st.markdown('<div class="question-card" style="text-align: center;">', unsafe_allow_html=True)
    st.subheader("🏁 Fin de la Partida")
    
    if not game_over and st.session_state.dinero > 0:
        st.balloons()
        st.success("🏆 ¡FELICIDADES! Completaste exitosamente las 10 etapas manteniendo una empresa rentable y con buena reputación.")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Generación únicamente del archivo descargable (sin tabla visible)
    if st.session_state.historial:
        df_historial = pd.DataFrame(st.session_state.historial)
        csv_data = df_historial.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Descargar Registro de Respuestas (CSV)",
            data=csv_data,
            file_name="historial_emprendimiento.csv",
            mime="text/csv"
        )

# Botón para reiniciar partida
if game_over or fase_actual >= 10:
    if st.button("🔄 Reiniciar Nueva Partida", use_container_width=True):
        st.session_state.clear()
        st.rerun()