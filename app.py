import pandas as pd
import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Startup Life - Simulador",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- ESTILOS PERSONALIZADOS (CSS) PARA DARLE COLOR Y DISEÑO ---
st.markdown(
    """
<style>
    /* Fondo con degradado colorido */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #0d1b2a 50%, #1b263b 100%);
        color: #ffffff;
    }

    /* Título Principal */
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff7e5f, #feb47b, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        color: #e0e6ed;
        margin-bottom: 25px;
    }

    /* Tarjetas del Dashboard / Métricas */
    .metric-card {
        background: rgba(255, 255, 255, 0.07);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-3px);
    }
    .card-capital { border-top: 4px solid #00e676; }
    .card-clientes { border-top: 4px solid #00b0ff; }
    .card-reputacion { border-top: 4px solid #ffea00; }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 5px;
    }

    /* Tarjeta de la Situación Actual */
    .question-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.03) 100%);
        border-radius: 20px;
        padding: 25px;
        margin-top: 15px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    /* Personalización de los Botones de Opción */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: auto;
        padding: 14px 20px;
        font-size: 1rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        margin-bottom: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Estilos dinámicos para los botones según su posición */
    div.row-widget.stButton:nth-child(1) > button {
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        color: white;
    }
    div.row-widget.stButton:nth-child(2) > button {
        background: linear-gradient(90deg, #4776e6, #8e54e9);
        color: white;
    }
    div.row-widget.stButton:nth-child(3) > button {
        background: linear-gradient(90deg, #11998e, #38ef7d);
        color: #0d1b2a;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 7px 20px rgba(255,255,255,0.3);
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
    '<p class="sub-title">Toma decisiones estratégicas, cuida tu capital y'
    " lleva tu emprendimiento al éxito.</p>",
    unsafe_allow_html=True,
)

# Inicializar variables de estado
if "dinero" not in st.session_state:
    st.session_state.dinero = 1500
    st.session_state.clientes = 10
    st.session_state.reputacion = 50
    st.session_state.fase = 1
    st.session_state.historial = []


def tomar_decision(
    fase_nombre,
    eleccion,
    costo_capital,
    delta_clientes,
    delta_reputacion,
    siguiente_fase,
):
    st.session_state.dinero += costo_capital
    st.session_state.clientes += delta_clientes
    st.session_state.reputacion += delta_reputacion

    st.session_state.historial.append({
        "Fase": fase_nombre,
        "Decisión": eleccion,
        "Cambio Capital": f"${costo_capital:+d}",
        "Cambio Clientes": f"{delta_clientes:+d}",
        "Cambio Reputación": f"{delta_reputacion:+d}",
        "Capital Restante": f"${st.session_state.dinero}",
    })

    st.session_state.fase = siguiente_fase
    st.rerun()


# Panel visual de indicadores (Dashboard Colorido)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"""
        <div class="metric-card card-capital">
            <span style="font-size: 1rem; color: #00e676;">💵 CAPITAL</span>
            <div class="metric-value" style="color: #00e676;">${st.session_state.dinero}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card card-clientes">
            <span style="font-size: 1rem; color: #00b0ff;">👥 CLIENTES</span>
            <div class="metric-value" style="color: #00b0ff;">{max(0, st.session_state.clientes)}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card card-reputacion">
            <span style="font-size: 1rem; color: #ffea00;">⭐ REPUTACIÓN</span>
            <div class="metric-value" style="color: #ffea00;">{max(0, st.session_state.reputacion)}/100</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

st.write("")

# Comprobar quiebra o pérdida de reputación
game_over = False
if st.session_state.dinero <= 0:
    st.error(
        "💥 ¡QUIEBRA TÉCNICA! Te quedaste sin capital para continuar operando."
    )
    game_over = True
elif st.session_state.reputacion <= 0:
    st.error(
        "💥 ¡CRISIS DE MARCA! Tu reputación cayó a 0 y perdiste el mercado."
    )
    game_over = True

# Base de datos de las 12 Fases
fases_datos = {
    1: {
        "titulo": "Fase 1: Lanzamiento del Producto",
        "situacion": (
            "Tienes $1,500 de ahorros iniciales. ¿Cómo vas a salir al mercado?"
        ),
        "opciones": [
            (
                "🚀 Lanzar PMV Básico (-$500) | +15 Clientes, +10 Reputación",
                -500,
                15,
                10,
                "Lanzó PMV Básico",
            ),
            (
                "🧪 Testeo/Versión Beta (-$100) | +5 Clientes, +2 Reputación",
                -100,
                5,
                2,
                "Lanzó Beta Gratuito (Neutro)",
            ),
            (
                "⭐ Lanzar Producto 'Perfecto' (-$1,400) | +40 Clientes, +25"
                " Reputación",
                -1400,
                40,
                25,
                "Lanzó Producto Perfecto",
            ),
        ],
    },
    2: {
        "titulo": "Fase 2: Estrategia de Crecimiento",
        "situacion": (
            "Necesitas conseguir tus primeros usuarios de forma constante."
        ),
        "opciones": [
            (
                "🔥 Invertir en Pauta Masiva (-$600) | +50 Clientes, +10"
                " Reputación",
                -600,
                50,
                10,
                "Pauta Pagada masiva",
            ),
            (
                "📱 Publicidad Moderada (-$150) | +20 Clientes, +5 Reputación",
                -150,
                20,
                5,
                "Pauta Moderada (Neutro)",
            ),
            (
                "🌱 Marketing Orgánico / Voz a voz ($0) | +10 Clientes, +15"
                " Reputación",
                0,
                10,
                15,
                "Crecimiento Orgánico",
            ),
        ],
    },
    3: {
        "titulo": "Fase 3: Gestión de Crisis Inicial",
        "situacion": (
            "Un proveedor falló y el 20% de los primeros pedidos llegaron con"
            " retraso."
        ),
        "opciones": [
            (
                "💰 Reembolso e Indemnización (-$500) | +20 Reputación",
                -500,
                0,
                20,
                "Reembolso Total",
            ),
            (
                "🎟️ Ofrecer Cupón Descuento (-$100) | -5 Clientes, +5"
                " Reputación",
                -100,
                -5,
                5,
                "Cupón de Descuento (Neutro)",
            ),
            (
                "🤷‍♂️ Ignorar Reclamos ($0) | -20 Clientes, -45 Reputación",
                0,
                -20,
                -45,
                "Ignorar Reclamos",
            ),
        ],
    },
    4: {
        "titulo": "Fase 4: Retroalimentación del Cliente",
        "situacion": (
            "Los primeros usuarios piden una nueva función, pero desarrollarla"
            " cuesta dinero."
        ),
        "opciones": [
            (
                "🛠️ Desarrollar función ya (-$400) | +15 Clientes, +10"
                " Reputación",
                -400,
                15,
                10,
                "Nueva función implementada",
            ),
            (
                "📊 Encuesta y Demo sencilla (-$100) | +5 Clientes, +2"
                " Reputación",
                -100,
                5,
                2,
                "Versión preliminar sencilla (Neutro)",
            ),
            (
                "⏸️ Mantener producto actual ($0) | -5 Clientes, -5 Reputación",
                0,
                -5,
                -5,
                "Mantuvo producto actual",
            ),
        ],
    },
    5: {
        "titulo": "Fase 5: Contratación",
        "situacion": "El crecimiento está aumentando la carga de trabajo.",
        "opciones": [
            (
                "👔 Contratar perfil Senior (-$500) | +10 Clientes, +5"
                " Reputación",
                -500,
                10,
                5,
                "Contrató senior experimentado",
            ),
            (
                "🤝 Apoyo Freelance temporal (-$200) | +4 Clientes, +2"
                " Reputación",
                -200,
                4,
                2,
                "Contrató apoyo temporal (Neutro)",
            ),
            (
                "💪 Trabajar solo con el equipo actual ($0) | Sin cambios",
                0,
                0,
                0,
                "Sin nuevas contrataciones",
            ),
        ],
    },
    6: {
        "titulo": "Fase 6: Competencia",
        "situacion": (
            "Aparece una empresa ofreciendo un producto similar a menor precio."
        ),
        "opciones": [
            ("🏷️ Reducir tus precios (-$200) | +15 Clientes", -200, 15, 0, "Redujo precio"),
            (
                "🎧 Reforzar Soporte al Cliente (-$50) | +3 Clientes, +5"
                " Reputación",
                -50,
                3,
                5,
                "Reforzó servicio (Neutro)",
            ),
            (
                "💎 Diferenciarte por Calidad (-$300) | +8 Clientes, +15"
                " Reputación",
                -300,
                8,
                15,
                "Diferenció por Calidad",
            ),
        ],
    },
    7: {
        "titulo": "Fase 7: Inversionista",
        "situacion": "Un inversionista ofrece $1,500 para acelerar el crecimiento.",
        "opciones": [
            (
                "📈 Aceptar inversión total (+$1,500) | +10 Clientes",
                1500,
                10,
                0,
                "Aceptó Inversión externa",
            ),
            (
                "🤝 Inversión parcial / Menor capital (+$500) | +3 Clientes, +2"
                " Reputación",
                500,
                3,
                2,
                "Inversión parcial (Neutro)",
            ),
            (
                "🛡️ Rechazar y mantener control total ($0) | +5 Reputación",
                0,
                0,
                5,
                "Mantuvo Control total",
            ),
        ],
    },
    8: {
        "titulo": "Fase 8: Capacidad de Producción",
        "situacion": "La demanda está aumentando y comienzas a tener retrasos.",
        "opciones": [
            (
                "🏭 Invertir en infraestructura (-$600) | +20 Clientes, +10"
                " Reputación",
                -600,
                20,
                10,
                "Invirtió en Capacidad",
            ),
            (
                "📦 Subcontratar producción temporal (-$250) | +5 Clientes, +2"
                " Reputación",
                -250,
                5,
                2,
                "Subcontrató producción (Neutro)",
            ),
            (
                "⚠️ Mantener capacidad actual ($0) | -10 Clientes, -10"
                " Reputación",
                0,
                -10,
                -10,
                "Mantuvo Capacidad",
            ),
        ],
    },
    9: {
        "titulo": "Fase 9: Alianza Estratégica",
        "situacion": (
            "Otra startup propone promocionar ambos productos juntos."
        ),
        "opciones": [
            (
                "🤝 Aceptar Alianza Estratégica (-$200) | +20 Clientes, +5"
                " Reputación",
                -200,
                20,
                5,
                "Aceptó Alianza Estratégica",
            ),
            (
                "🌐 Colaboración Digital Puncual (-$50) | +8 Clientes, +2"
                " Reputación",
                -50,
                8,
                2,
                "Colaboración puntual (Neutro)",
            ),
            (
                "🚶‍♂️ Continuar individualmente ($0) | Sin cambios",
                0,
                0,
                0,
                "Continuó Individualmente",
            ),
        ],
    },
    10: {
        "titulo": "Fase 10: Crisis de Reputación",
        "situacion": (
            "Un cliente publica una crítica negativa que se empieza a volver"
            " viral."
        ),
        "opciones": [
            (
                "🎁 Responder y Compensar (-$250) | +10 Reputación",
                -250,
                0,
                10,
                "Respondió y Compensó",
            ),
            (
                "📢 Emitir Comunicado Oficial (-$50) | -2 Clientes, +2"
                " Reputación",
                -50,
                -2,
                2,
                "Comunicado Oficial (Neutro)",
            ),
            (
                "🔇 Ignorar la Crítica ($0) | -10 Clientes, -20 Reputación",
                0,
                -10,
                -20,
                "Ignoró la Crítica",
            ),
        ],
    },
    11: {
        "titulo": "Fase 11: Expansión",
        "situacion": (
            "Tu negocio funciona bien y aparece la oportunidad de entrar en"
            " otro mercado."
        ),
        "opciones": [
            ("🌍 Expansión Agresiva (-$700) | +30 Clientes", -700, 30, 0, "Expansión agresiva"),
            (
                "🏙️ Prueba Piloto Regional (-$350) | +12 Clientes, +4"
                " Reputación",
                -350,
                12,
                4,
                "Prueba piloto regional (Neutro)",
            ),
            (
                "🏛️ Consolidar Mercado Actual (-$200) | +10 Clientes, +10"
                " Reputación",
                -200,
                10,
                10,
                "Consolidó mercado actual",
            ),
        ],
    },
    12: {
        "titulo": "Fase 12: Innovación Final",
        "situacion": (
            "Una nueva tecnología podría transformar tu producto, pero requiere"
            " fuerte inversión."
        ),
        "opciones": [
            (
                "🚀 Innovación Tecnológica Total (-$800) | +25 Clientes, +20"
                " Reputación",
                -800,
                25,
                20,
                "Innovación total",
            ),
            (
                "📈 Adopción Gradual (-$300) | +10 Clientes, +8 Reputación",
                -300,
                10,
                8,
                "Adopción gradual (Neutro)",
            ),
            (
                "🔒 Mantener producto actual ($0) | +2 Clientes",
                0,
                2,
                0,
                "Mantuvo producto actual",
            ),
        ],
    },
}

fase_actual = st.session_state.fase

# Renderizado de Pregunta
if not game_over and fase_actual in fases_datos:
    datos = fases_datos[fase_actual]

    st.markdown(
        f"""
        <div class="question-card">
            <h3 style="color: #feb47b; margin-bottom: 10px;">{datos['titulo']}</h3>
            <p style="font-size: 1.15rem; color: #f0f3f6; line-height: 1.5;">{datos['situacion']}</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    for texto, capital, clientes, reputacion, log in datos["opciones"]:
        if st.button(texto, use_container_width=True):
            tomar_decision(
                datos["titulo"], log, capital, clientes, reputacion, fase_actual + 1
            )

# Pantalla de Fin de Juego
elif game_over or fase_actual > 12:
    st.markdown(
        '<div class="question-card" style="text-align: center;">',
        unsafe_allow_html=True,
    )
    st.subheader("🏁 Fin de la Partida")

    if not game_over and st.session_state.dinero > 0:
        st.balloons()
        st.success(
            "🏆 ¡FELICIDADES! Lograste completar todas las fases y consolidar"
            " tu empresa."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.historial:
        st.write("### 📋 Registro de Tus Decisiones:")
        df_historial = pd.DataFrame(st.session_state.historial)
        st.dataframe(df_historial, use_container_width=True)

        csv_data = df_historial.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Descargar Reporte de Respuestas (CSV)",
            data=csv_data,
            file_name="historial_emprendimiento.csv",
            mime="text/csv",
        )

if game_over or fase_actual > 12:
    if st.button("🔄 Reiniciar Juego", use_container_width=True):
        st.session_state.clear()
        st.rerun()