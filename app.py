import random
import pandas as pd
import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Startup Life - El Juego de la Vida Emprendedora",
    page_icon="🎲",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Estilos CSS estilo Juego de Mesa (The Game of LIFE)
st.markdown(
    """
<style>
    /* Fondo estilo tablero de juego */
    .stApp {
        background: #f0fdf4;
        background-image: radial-gradient(#cbd5e1 1px, transparent 1px);
        background-size: 20px 20px;
        color: #1e293b;
        font-family: 'Fredoka', 'Nunito', 'Segoe UI', sans-serif;
    }

    /* Logo estilo bloques de colores "The Game of LIFE" */
    .board-title-container {
        text-align: center;
        margin-bottom: 20px;
    }
    .game-subhead {
        font-size: 1.1rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .life-blocks {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        margin-bottom: 10px;
    }
    .block {
        width: 55px;
        height: 55px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.2rem;
        font-weight: 900;
        color: white;
        box-shadow: 0px 6px 0px rgba(0,0,0,0.2), inset 0px 3px 0px rgba(255,255,255,0.4);
        text-shadow: 2px 2px 0px rgba(0,0,0,0.3);
    }
    .b-l { background-color: #ec4899; } /* Rosa */
    .b-i { background-color: #0284c7; } /* Azul */
    .b-f { background-color: #16a34a; } /* Verde */
    .b-e { background-color: #eab308; } /* Amarillo */

    .game-subtitle {
        font-size: 1rem;
        font-weight: 700;
        color: #475569;
        margin-bottom: 15px;
    }

    /* Tarjetas de Métricas estilo Tablero */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 12px;
        text-align: center;
        box-shadow: 0px 6px 0px #cbd5e1, 0px 10px 15px rgba(0,0,0,0.08);
        border: 3px solid #64748b;
    }
    .card-capital { border-color: #22c55e; }
    .card-clientes { border-color: #0284c7; }
    .card-reputacion { border-color: #eab308; }

    .metric-label {
        font-size: 0.85rem;
        font-weight: 800;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 900;
        margin-top: 2px;
    }

    /* Tarjeta de Pregunta / Escenario */
    .question-card {
        background: white;
        border-radius: 20px;
        padding: 22px;
        margin-top: 15px;
        margin-bottom: 20px;
        border: 4px solid #0f172a;
        box-shadow: 0px 8px 0px #0f172a, 0px 12px 20px rgba(0,0,0,0.1);
    }

    .question-badge {
        display: inline-block;
        background: #0284c7;
        color: white;
        font-weight: 800;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-bottom: 10px;
        box-shadow: 0px 3px 0px #0369a1;
    }

    .question-title {
        color: #0f172a;
        font-size: 1.4rem;
        font-weight: 900;
        margin-bottom: 10px;
    }

    .question-text {
        font-size: 1.1rem;
        color: #334155;
        line-height: 1.5;
        font-weight: 600;
    }

    /* Botones de Opciones estilo Fichas de Juego 3D */
    div.stButton > button {
        width: 100%;
        border-radius: 14px !important;
        padding: 14px 20px !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        background: #ffffff !important;
        color: #0f172a !important;
        border: 3px solid #0f172a !important;
        box-shadow: 0px 6px 0px #0f172a !important;
        transition: all 0.1s ease !important;
        margin-bottom: 12px !important;
        text-align: left !important;
    }

    div.stButton > button:hover {
        background: #f1f5f9 !important;
        transform: translateY(2px) !important;
        box-shadow: 0px 4px 0px #0f172a !important;
        color: #0284c7 !important;
    }

    div.stButton > button:active {
        transform: translateY(6px) !important;
        box-shadow: 0px 0px 0px #0f172a !important;
    }

    /* Botón de descarga estilo premio */
    div.stDownloadButton > button {
        width: 100%;
        border-radius: 14px !important;
        padding: 14px 20px !important;
        font-size: 1.1rem !important;
        font-weight: 900 !important;
        background: #22c55e !important;
        color: white !important;
        border: 3px solid #15803d !important;
        box-shadow: 0px 6px 0px #15803d !important;
    }
    div.stDownloadButton > button:hover {
        background: #16a34a !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Encabezado visual estilo "The Game of LIFE"
st.markdown(
    """
    <div class="board-title-container">
        <div class="game-subhead">EL JUEGO DE LA</div>
        <div class="life-blocks">
            <div class="block b-l">S</div>
            <div class="block b-i">T</div>
            <div class="block b-f">A</div>
            <div class="block b-e">R</div>
            <div class="block b-l">T</div>
            <div class="block b-i">U</div>
            <div class="block b-f">P</div>
        </div>
        <div class="game-subtitle">🎲 Toma decisiones, cuida tu reputación (mínimo 30) y evita la quiebra.</div>
    </div>
""",
    unsafe_allow_html=True,
)

# Banco total de preguntas (con montos visibles y sin revelar impacto en clientes/reputación)
BANCO_PREGUNTAS = [
    {
        "titulo": "Lanzamiento del Producto",
        "situacion": (
            "Tienes $1,500 de ahorros iniciales. ¿Cómo vas a salir al mercado?"
        ),
        "opciones": [
            (
                "🚀 Lanzar un Producto Mínimo Viable (PMV) Básico [Inversión:"
                " -$500]",
                -500,
                15,
                10,
                "Lanzó PMV Básico",
            ),
            (
                "🧪 Hacer un testeo con una Versión Beta Gratuita [Inversión:"
                " -$100]",
                -100,
                5,
                2,
                "Lanzó Beta Gratuito",
            ),
            (
                "⭐ Lanzar el Producto Completo con todo incluido [Inversión:"
                " -$1,400]",
                -1400,
                40,
                25,
                "Lanzó Producto Completo",
            ),
        ],
    },
    {
        "titulo": "Estrategia de Crecimiento",
        "situacion": (
            "Necesitas conseguir tus primeros usuarios de forma constante."
        ),
        "opciones": [
            (
                "🔥 Invertir en Pauta Pagada Masiva en Redes Sociales [Inversión:"
                " -$600]",
                -600,
                50,
                10,
                "Pauta Pagada Masiva",
            ),
            (
                "📱 Ejecutar una Campaña de Publicidad Moderada [Inversión:"
                " -$150]",
                -150,
                20,
                5,
                "Pauta Moderada",
            ),
            (
                "🌱 Apostar por Crecimiento Orgánico y Recomendaciones [Costo:"
                " $0]",
                0,
                10,
                15,
                "Crecimiento Orgánico",
            ),
        ],
    },
    {
        "titulo": "Incidencia de Entrega del Producto",
        "situacion": (
            "Un cliente importante reporta que su paquete figura como entregado"
            " pero nunca llegó a sus manos."
        ),
        "opciones": [
            (
                "🔍 Hablar directamente con la persona e investigar la"
                " situación a fondo con la logística [Costo: -$150]",
                -150,
                5,
                15,
                "Investigación personalizada con el cliente",
            ),
            (
                "💰 Emitir un reembolso inmediato e indemnización sin investigar"
                " [Costo: -$400]",
                -400,
                0,
                10,
                "Reembolso automático",
            ),
            (
                "📄 Indicarle que abra un reclamo directamente con la empresa"
                " de envíos [Costo: $0]",
                0,
                -10,
                -25,
                "Desentenderse del reclamo",
            ),
        ],
    },
    {
        "titulo": "Retroalimentación del Cliente",
        "situacion": (
            "Los usuarios están pidiendo una nueva función muy solicitada."
        ),
        "opciones": [
            (
                "🛠️ Desarrollar e integrar la nueva función de inmediato"
                " [Inversión: -$400]",
                -400,
                15,
                10,
                "Nueva función desarrollada",
            ),
            (
                "📊 Hacer una encuesta y lanzar una Demo previa sencilla"
                " [Inversión: -$100]",
                -100,
                5,
                2,
                "Demo Sencilla",
            ),
            (
                "⏸️ Mantener el producto actual sin cambios por ahora [Costo:"
                " $0]",
                0,
                -5,
                -10,
                "Mantuvo producto actual",
            ),
        ],
    },
    {
        "titulo": "Contratación de Personal",
        "situacion": (
            "El crecimiento está aumentando la carga de trabajo en el equipo."
        ),
        "opciones": [
            (
                "👔 Contratar a un perfil Senior con mucha experiencia [Costo:"
                " -$500]",
                -500,
                10,
                5,
                "Contrató perfil Senior",
            ),
            (
                "🤝 Contratar un apoyo Freelance de forma temporal [Costo:"
                " -$200]",
                -200,
                4,
                2,
                "Contrató apoyo Freelance",
            ),
            (
                "💪 Exigir un esfuerzo extra al equipo actual sin contratar"
                " [Costo: $0]",
                0,
                -5,
                -15,
                "Sin nuevas contrataciones",
            ),
        ],
    },
    {
        "titulo": "Estrategia ante la Competencia",
        "situacion": (
            "Aparece un competidor directo ofreciendo un producto similar a"
            " menor precio."
        ),
        "opciones": [
            (
                "🏷️ Reducir tus precios para competir agresivamente [Costo:"
                " -$200]",
                -200,
                15,
                0,
                "Redujo precios",
            ),
            (
                "🎧 Reforzar la Atención y Soporte al Cliente [Inversión:"
                " -$50]",
                -50,
                3,
                5,
                "Reforzó servicio al cliente",
            ),
            (
                "💎 Apostar por la Diferenciación de Alta Calidad [Inversión:"
                " -$300]",
                -300,
                8,
                15,
                "Diferenció por Calidad",
            ),
        ],
    },
    {
        "titulo": "Oferta de Inversionista",
        "situacion": (
            "Un inversionista ángel ofrece un capital adicional para acelerar"
            " el negocio."
        ),
        "opciones": [
            (
                "📈 Aceptar la Inversión Total a cambio de ceder participación"
                " [Ingreso: +$1,500]",
                1500,
                10,
                0,
                "Aceptó Inversión externa",
            ),
            (
                "🤝 Aceptar una Inversión Parcial más conservadora [Ingreso:"
                " +$500]",
                500,
                3,
                2,
                "Aceptó Inversión parcial",
            ),
            (
                "🛡️ Rechazar la oferta y mantener el control total del negocio"
                " [Costo: $0]",
                0,
                0,
                5,
                "Mantuvo Control total",
            ),
        ],
    },
    {
        "titulo": "Capacidad Operativa",
        "situacion": (
            "La demanda está aumentando y comienzan a generarse cuellos de"
            " botella."
        ),
        "opciones": [
            (
                "🏭 Invertir fuertemente en Infraestructura y Tecnología"
                " [Inversión: -$600]",
                -600,
                20,
                10,
                "Invirtió en Capacidad",
            ),
            (
                "📦 Subcontratar parte de la producción o logística [Costo:"
                " -$250]",
                -250,
                5,
                2,
                "Subcontrató producción",
            ),
            (
                "⚠️ Mantener la capacidad actual procesando a ritmo lento"
                " [Costo: $0]",
                0,
                -10,
                -20,
                "Mantuvo Capacidad",
            ),
        ],
    },
    {
        "titulo": "Alianza Estratégica",
        "situacion": (
            "Otra startup complementaria propone promocionar ambos productos"
            " juntos."
        ),
        "opciones": [
            (
                "🤝 Firmar una Alianza Estratégica y co-branding completo"
                " [Inversión: -$200]",
                -200,
                20,
                5,
                "Aceptó Alianza Estratégica",
            ),
            (
                "🌐 Realizar una Colaboración Digital Puntual en redes"
                " [Inversión: -$50]",
                -50,
                8,
                2,
                "Colaboración Puntual",
            ),
            (
                "🚶‍♂️ Rechazar y continuar operando de forma independiente"
                " [Costo: $0]",
                0,
                0,
                0,
                "Continuó Individualmente",
            ),
        ],
    },
    {
        "titulo": "Crisis de Redes Sociales",
        "situacion": (
            "Un cliente referente publica una crítica negativa que empieza a"
            " hacerse viral."
        ),
        "opciones": [
            (
                "🎁 Contactar al cliente, disculparse públicamente y compensarlo"
                " [Costo: -$250]",
                -250,
                0,
                10,
                "Respondió y Compensó",
            ),
            (
                "📢 Emitir un Comunicado Oficial aclarando la situación"
                " [Costo: -$50]",
                -50,
                -2,
                2,
                "Comunicado Oficial",
            ),
            (
                "🔇 Ignorar la publicación para no darle más visibilidad"
                " [Costo: $0]",
                0,
                -10,
                -25,
                "Ignoró la Crítica",
            ),
        ],
    },
    {
        "titulo": "Ciberseguridad y Datos",
        "situacion": (
            "Se detectó un intento de acceso no autorizado a la plataforma."
        ),
        "opciones": [
            (
                "🔒 Contratar una Auditoría Completa de Ciberseguridad [Costo:"
                " -$450]",
                -450,
                0,
                15,
                "Auditoría de Seguridad",
            ),
            (
                "🛡️ Aplicar Parches y Actualizaciones de seguridad básicas"
                " [Costo: -$100]",
                -100,
                0,
                5,
                "Parches Básicos",
            ),
            (
                "⚠️ Ignorar la alerta al no registrarse pérdidas graves"
                " [Costo: $0]",
                0,
                -15,
                -30,
                "Ignoró Alerta Ciberseguridad",
            ),
        ],
    },
    {
        "titulo": "Campaña de Influencers",
        "situacion": (
            "Un creador de contenido relevante en tu sector ofrece"
            " promocionarte."
        ),
        "opciones": [
            (
                "🌟 Contratar una Campaña Exclusiva de recomendación"
                " [Inversión: -$500]",
                -500,
                35,
                10,
                "Campaña Influencer Exclusiva",
            ),
            (
                "🎁 Enviar Muestras Gratis del producto esperando mención"
                " [Costo: -$120]",
                -120,
                12,
                3,
                "Muestras Gratis",
            ),
            (
                "❌ Rechazar la propuesta y mantener el enfoque actual [Costo:"
                " $0]",
                0,
                0,
                0,
                "Rechazó Influencer",
            ),
        ],
    },
    {
        "titulo": "Regulaciones e Impuestos",
        "situacion": (
            "Se aprueba un ajuste normativo que requiere adecuar tu modelo"
            " comercial."
        ),
        "opciones": [
            (
                "📜 Contratar Asesoría Jurídica Completa para estar en regla"
                " [Costo: -$350]",
                -350,
                0,
                10,
                "Asesoría Jurídica Completa",
            ),
            (
                "📝 Realizar un Trámite Interno Básico de adecuación [Costo:"
                " -$100]",
                -100,
                0,
                2,
                "Trámite Interno Básico",
            ),
            (
                "⏳ Postergar la adecuación hasta recibir una notificación"
                " [Costo: $0]",
                0,
                0,
                -20,
                "Postergó Ajuste Legal",
            ),
        ],
    },
    {
        "titulo": "Expansión Geográfica",
        "situacion": (
            "Aparece la oportunidad de abrir ventas en una nueva provincia."
        ),
        "opciones": [
            (
                "🌍 Iniciar una Expansión Total e inmediata en la nueva zona"
                " [Inversión: -$600]",
                -600,
                25,
                0,
                "Expansión Total",
            ),
            (
                "🏙️ Hacer una Prueba Piloto Regional con presupuesto acotado"
                " [Inversión: -$250]",
                -250,
                10,
                3,
                "Prueba Piloto Regional",
            ),
            (
                "🏛️ Consolidar primero el Mercado Actual antes de expandirse"
                " [Inversión: -$100]",
                -100,
                5,
                5,
                "Consolidó Mercado Actual",
            ),
        ],
    },
    {
        "titulo": "Adopción de Inteligencia Artificial",
        "situacion": (
            "Puedes integrar herramientas de IA para automatizar la operación."
        ),
        "opciones": [
            (
                "🤖 Implementar IA Avanzada en la atención y ventas [Inversión:"
                " -$400]",
                -400,
                20,
                10,
                "Implementación IA Avanzada",
            ),
            (
                "💬 Integrar un Chatbot Sencillo de respuestas automáticas"
                " [Inversión: -$100]",
                -100,
                5,
                2,
                "Chatbot Sencillo",
            ),
            (
                "📞 Mantener el esquema de atención manual tradicional [Costo:"
                " $0]",
                0,
                -5,
                0,
                "Atención Manual",
            ),
        ],
    },
    {
        "titulo": "Innovación de Producto",
        "situacion": (
            "El mercado exige renovar el diseño y la interfaz general de tu"
            " servicio."
        ),
        "opciones": [
            (
                "🚀 Invertir en un Rediseño Total de la plataforma [Inversión:"
                " -$700]",
                -700,
                30,
                15,
                "Rediseño Total",
            ),
            (
                "📈 Aplicar Ajustes Visuales Menores sin alterar la estructura"
                " [Inversión: -$200]",
                -200,
                8,
                5,
                "Ajustes Menores",
            ),
            (
                "🔒 Mantener la Versión Actual sin gastar recursos [Costo: $0]",
                0,
                -10,
                -10,
                "Mantuvo Versión Actual",
            ),
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
    st.session_state.preguntas_juego = random.sample(BANCO_PREGUNTAS, 10)


def tomar_decision(
    fase_nombre, eleccion, costo_capital, delta_clientes, delta_reputacion
):
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
        "Reputación Restante": f"{st.session_state.reputacion}",
    })

    st.session_state.fase += 1
    st.rerun()


# Panel visual de métricas del jugador
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"""
        <div class="metric-card card-capital">
            <span class="metric-label" style="color: #16a34a;">💵 Capital</span>
            <div class="metric-value" style="color: #15803d;">${st.session_state.dinero}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card card-clientes">
            <span class="metric-label" style="color: #0284c7;">👥 Clientes</span>
            <div class="metric-value" style="color: #0369a1;">{max(0, st.session_state.clientes)}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card card-reputacion">
            <span class="metric-label" style="color: #ca8a04;">⭐ Reputación</span>
            <div class="metric-value" style="color: #a16207;">{max(0, st.session_state.reputacion)}/100</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

st.write("")

# Validación de Game Over (Pérdida por Capital <= 0 o Reputación <= 30)
game_over = False
if st.session_state.dinero <= 0:
    st.error(
        "💥 ¡QUIEBRA TÉCNICA! Te quedaste sin capital suficiente para continuar"
        " operando."
    )
    game_over = True
elif st.session_state.reputacion <= 30:
    st.error(
        "💥 ¡CRISIS SEVERA DE REPUTACIÓN! Tu reputación cayó a 30 o menos y la"
        " empresa perdió total credibilidad."
    )
    game_over = True

fase_actual = st.session_state.fase

# Renderizado de Pregunta Actual
if not game_over and fase_actual < 10:
    datos = st.session_state.preguntas_juego[fase_actual]

    st.markdown(
        f"""
        <div class="question-card">
            <span class="question-badge">PASO {fase_actual + 1} DE 10</span>
            <div class="question-title">{datos['titulo']}</div>
            <div class="question-text">{datos['situacion']}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    for texto, capital, clientes, reputacion, log in datos["opciones"]:
        if st.button(texto, use_container_width=True):
            tomar_decision(datos["titulo"], log, capital, clientes, reputacion)

# Pantalla de Fin de Juego
elif game_over or fase_actual >= 10:
    st.markdown(
        '<div class="question-card" style="text-align: center;">',
        unsafe_allow_html=True,
    )
    st.subheader("🏁 ¡FIN DE LA PARTIDA!")

    if not game_over and st.session_state.dinero > 0:
        st.balloons()
        st.success(
            "🏆 ¡FELICIDADES! Llegaste a la meta manteniendo una empresa"
            " rentable y con excelente reputación."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Generación únicamente del archivo descargable (sin tabla visible)
    if st.session_state.historial:
        df_historial = pd.DataFrame(st.session_state.historial)
        csv_data = df_historial.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Descargar Registro de Decisiones (CSV)",
            data=csv_data,
            file_name="historial_emprendimiento.csv",
            mime="text/csv",
        )

# Botón para reiniciar partida
if game_over or fase_actual >= 10:
    if st.button("🔄 Jugar Otra Vez", use_container_width=True):
        st.session_state.clear()
        st.rerun()