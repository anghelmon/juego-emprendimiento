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

    .badge-hard {
        background: #dc2626 !important;
        box-shadow: 0px 3px 0px #991b1b !important;
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

# BANCO MODO FÁCIL (Precios Visibles)
BANCO_FACIL = [
    {
        "titulo": "Lanzamiento del Producto",
        "situacion": "Tienes $1,500 de ahorros iniciales. ¿Cómo vas a salir al mercado?",
        "opciones": [
            ("🚀 Lanzar un Producto Mínimo Viable (PMV) Básico [Inversión: -$500]", -500, 15, 10, "Lanzó PMV Básico"),
            ("🧪 Hacer un testeo con una Versión Beta Gratuita [Inversión: -$100]", -100, 5, 2, "Lanzó Beta Gratuito"),
            ("⭐ Lanzar el Producto Completo con todo incluido [Inversión: -$1,400]", -1400, 40, 25, "Lanzó Producto Completo"),
        ],
    },
    {
        "titulo": "Estrategia de Crecimiento",
        "situacion": "Necesitas conseguir tus primeros usuarios de forma constante.",
        "opciones": [
            ("🔥 Invertir en Pauta Pagada Masiva en Redes Sociales [Inversión: -$600]", -600, 50, 10, "Pauta Pagada Masiva"),
            ("📱 Ejecutar una Campaña de Publicidad Moderada [Inversión: -$150]", -150, 20, 5, "Pauta Moderada"),
            ("🌱 Apostar por Crecimiento Orgánico y Recomendaciones [Costo: $0]", 0, 10, 15, "Crecimiento Orgánico"),
        ],
    },
    {
        "titulo": "Incidencia de Entrega del Producto",
        "situacion": "Un cliente importante reporta que su paquete figura como entregado pero nunca llegó a sus manos.",
        "opciones": [
            ("🔍 Hablar directamente con la persona e investigar la situación a fondo con la logística [Costo: -$150]", -150, 5, 15, "Investigación personalizada con el cliente"),
            ("💰 Emitir un reembolso inmediato e indemnización sin investigar [Costo: -$400]", -400, 0, 10, "Reembolso automático"),
            ("📄 Indicarle que abra un reclamo directamente con la empresa de envíos [Costo: $0]", 0, -10, -25, "Desentenderse del reclamo"),
        ],
    },
    {
        "titulo": "Retroalimentación del Cliente",
        "situacion": "Los usuarios están pidiendo una nueva función muy solicitada.",
        "opciones": [
            ("🛠️ Desarrollar e integrar la nueva función de inmediato [Inversión: -$400]", -400, 15, 10, "Nueva función desarrollada"),
            ("📊 Hacer una encuesta y lanzar una Demo previa sencilla [Inversión: -$100]", -100, 5, 2, "Demo Sencilla"),
            ("⏸️ Mantener el producto actual sin cambios por ahora [Costo: $0]", 0, -5, -10, "Mantuvo producto actual"),
        ],
    },
    {
        "titulo": "Contratación de Personal",
        "situacion": "El crecimiento está aumentando la carga de trabajo en el equipo.",
        "opciones": [
            ("👔 Contratar a un perfil Senior con mucha experiencia [Costo: -$500]", -500, 10, 5, "Contrató perfil Senior"),
            ("🤝 Contratar un apoyo Freelance de forma temporal [Costo: -$200]", -200, 4, 2, "Contrató apoyo Freelance"),
            ("💪 Exigir un esfuerzo extra al equipo actual sin contratar [Costo: $0]", 0, -5, -15, "Sin nuevas contrataciones"),
        ],
    },
    {
        "titulo": "Estrategia ante la Competencia",
        "situacion": "Aparece un competidor directo ofreciendo un producto similar a menor precio.",
        "opciones": [
            ("🏷️ Reducir tus precios para competir agresivamente [Costo: -$200]", -200, 15, 0, "Redujo precios"),
            ("🎧 Reforzar la Atención y Soporte al Cliente [Inversión: -$50]", -50, 3, 5, "Reforzó servicio al cliente"),
            ("💎 Apostar por la Diferenciación de Alta Calidad [Inversión: -$300]", -300, 8, 15, "Diferenció por Calidad"),
        ],
    },
    {
        "titulo": "Oferta de Inversionista",
        "situacion": "Un inversionista ángel ofrece un capital adicional para acelerar el negocio.",
        "opciones": [
            ("📈 Aceptar la Inversión Total a cambio de ceder participación [Ingreso: +$1,500]", 1500, 10, 0, "Aceptó Inversión externa"),
            ("🤝 Aceptar una Inversión Parcial más conservadora [Ingreso: +$500]", 500, 3, 2, "Aceptó Inversión parcial"),
            ("🛡️ Rechazar la oferta y mantener el control total del negocio [Costo: $0]", 0, 0, 5, "Mantuvo Control total"),
        ],
    },
    {
        "titulo": "Capacidad Operativa",
        "situacion": "La demanda está aumentando y comienzan a generarse cuellos de botella.",
        "opciones": [
            ("🏭 Invertir fuertemente en Infraestructura y Tecnología [Inversión: -$600]", -600, 20, 10, "Invirtió en Capacidad"),
            ("📦 Subcontratar parte de la producción o logística [Costo: -$250]", -250, 5, 2, "Subcontrató producción"),
            ("⚠️ Mantener la capacidad actual procesando a ritmo lento [Costo: $0]", 0, -10, -20, "Mantuvo Capacidad"),
        ],
    },
    {
        "titulo": "Alianza Estratégica",
        "situacion": "Otra startup complementaria propone promocionar ambos productos juntos.",
        "opciones": [
            ("🤝 Firmar una Alianza Estratégica y co-branding completo [Inversión: -$200]", -200, 20, 5, "Aceptó Alianza Estratégica"),
            ("🌐 Realizar una Colaboración Digital Puntual en redes [Inversión: -$50]", -50, 8, 2, "Colaboración Puntual"),
            ("🚶‍♂️ Rechazar y continuar operando de forma independiente [Costo: $0]", 0, 0, 0, "Continuó Individualmente"),
        ],
    },
    {
        "titulo": "Crisis de Redes Sociales",
        "situacion": "Un cliente referente publica una crítica negativa que empieza a hacerse viral.",
        "opciones": [
            ("🎁 Contactar al cliente, disculparse públicamente y compensarlo [Costo: -$250]", -250, 0, 10, "Respondió y Compensó"),
            ("📢 Emitir un Comunicado Oficial aclarando la situación [Costo: -$50]", -50, -2, 2, "Comunicado Oficial"),
            ("🔇 Ignorar la publicación para no darle más visibilidad [Costo: $0]", 0, -10, -25, "Ignóro la Crítica"),
        ],
    },
]

# BANCO MODO DIFÍCIL (Precios ocultos, balances económicos más ajustados y alcanzables, 15 preguntas para mayor aleatoriedad)
BANCO_DIFICIL = [
    {
        "titulo": "Caída Crítica de Servidores",
        "situacion": "Tu servidor principal cayó durante la hora pico de ventas. Los clientes no pueden completar compras.",
        "opciones": [
            ("🚨 Migrar de inmediato a servidores Cloud de Alta Disponibilidad", -350, 20, 15, "Migración Cloud"),
            ("🛠️ Reiniciar servidores e intentar una reparación manual rápida", -100, -5, -10, "Reparación manual"),
            ("📢 Poner pantalla de mantenimiento y esperar a que pase el pico", 0, -20, -20, "Mantenimiento pasivo"),
        ],
    },
    {
        "titulo": "Demanda Legal por Propiedad Intelectual",
        "situacion": "Una gran corporación te exige retirar una marca registrada alegando similitud en el logo.",
        "opciones": [
            ("⚖️ Contratar un bufete de abogados experto para defender la marca", -300, 0, 10, "Defensa legal especialista"),
            ("🎨 Aceptar hacer un Rebranding completo rápido de la marca", -150, -10, -5, "Rebranding de emergencia"),
            ("🙈 Ignorar la notificación esperando que no escalen el proceso", 0, -5, -30, "Ignoró demanda legal"),
        ],
    },
    {
        "titulo": "Fuga de Talento Clave",
        "situacion": "Tu Desarrollador Principal recibe una oferta del doble de sueldo en una gran empresa.",
        "opciones": [
            ("💰 Igualar la oferta salarial y ofrecer participación en la empresa", -250, 5, 10, "Retención con equity"),
            ("🤝 Dejarlo ir y contratar a un apoyo temporal de reemplazo", -120, -10, -5, "Reemplazo temporal"),
            ("⌛ Absorber su trabajo entre los fundadores restantes", 0, -15, -15, "Sobrecarga de trabajo"),
        ],
    },
    {
        "titulo": "Auditoría Tributaria Inesperada",
        "situacion": "El ministerio de hacienda requiere una revisión completa de contabilidad de tus primeros meses.",
        "opciones": [
            ("📋 Contratar una auditoría contable externa para dejar todo en regla", -200, 0, 10, "Auditoría Contable Externa"),
            ("📁 Revisar y presentar los papeles por tu propia cuenta", -50, 0, -10, "Revisión Interna"),
            ("⏳ Solicitar prórrogas consecutivas para ganar tiempo", 0, 0, -20, "Prórroga Tributaria"),
        ],
    },
    {
        "titulo": "Ronda de Inversión Agresiva",
        "situacion": "Un fondo de Venture Capital ofrece capital adicional, pero exigen participación activa.",
        "opciones": [
            ("🚀 Aceptar la inversión perdiendo parte del control", 800, 25, -10, "Aceptó VC Agresivo"),
            ("🤝 Negociar una ronda más pequeña reteniendo la mayoría", 350, 10, 5, "Negoció Ronda Moderada"),
            ("🚫 Rechazar y continuar financiado por ventas", 0, 0, 10, "Rechazó VC"),
        ],
    },
    {
        "titulo": "Defecto de Calidad en Lote Masivo",
        "situacion": "El último lote enviado a 100 clientes llegó con una falla importante de funcionamiento.",
        "opciones": [
            ("🚚 Retirar el lote completo, reemplazar gratis y pedir disculpas", -400, 10, 20, "Retiro y Reemplazo Total"),
            ("🔧 Ofrecer un cupón de descuento para la próxima compra", -100, -15, -15, "Cupón de Compensación"),
            ("❓ Atribuir el problema a un mal uso por parte del usuario", 0, -35, -30, "Negación de Responsabilidad"),
        ],
    },
    {
        "titulo": "Ataque de Ciberseguridad",
        "situacion": "Detectas que intentan vulnerar la base de datos de usuarios.",
        "opciones": [
            ("🔒 Contratar expertos en ciberseguridad para blindar el sistema", -300, 0, 15, "Blindaje Ciberseguridad"),
            ("💾 Aplicar parches de seguridad recomendados de forma interna", -100, -5, -5, "Parches Internos"),
            ("🙈 Confiar en que los firewalls actuales resistan la amenaza", 0, -15, -25, "Sin acciones de seguridad"),
        ],
    },
    {
        "titulo": "Expansión Regional Arriesgada",
        "situacion": "Surge la opción de abrir mercado en una zona vecina con costumbres distintas.",
        "opciones": [
            ("🌐 Crear estrategia e invertir en localización de marca", -350, 30, 10, "Expansión Localizada"),
            ("📦 Exportar envíos directos sin mayor inversión local", -120, 10, 0, "Ventas Directas"),
            ("🛑 Cancelar expansión por el momento", 0, 0, 0, "Canceló Expansión"),
        ],
    },
    {
        "titulo": "Campaña Boicoteada en Redes",
        "situacion": "Una campaña publicitaria fue malinterpretada y se convirtió en tendencia negativa.",
        "opciones": [
            ("🕊️ Retirar la campaña de inmediato y hacer un ajuste público", -150, 5, 15, "Ajuste Público"),
            ("📝 Publicar una aclaración justificando el mensaje original", -30, -10, -10, "Aclaración Pública"),
            ("🔥 Ignorar las críticas y dejar corriendo los anuncios", 0, 10, -25, "Ignoró Boicot"),
        ],
    },
    {
        "titulo": "Cambio de Algoritmo en Canal Principal",
        "situacion": "La plataforma donde consigues la mayoría de tus clientes cambió sus reglas.",
        "opciones": [
            ("Diversificar de inmediato invirtiendo en 2 canales nuevos", -300, 20, 10, "Diversificación de Canales"),
            ("Pagar las nuevas tarifas exigidas por la plataforma actual", -150, 5, 0, "Pago de Tarifas Plazas"),
            ("Reducir presupuesto de publicidad y confiar en la base actual", 0, -20, -10, "Reducción de Publicidad"),
        ],
    },
    {
        "titulo": "Retraso en Cadena de Suministro",
        "situacion": "Tu proveedor principal retuvo los insumos esenciales por problemas aduaneros.",
        "opciones": [
            ("✈️ Contratar envío exprés prioritario con un proveedor secundario", -250, 10, 10, "Envío Exprés Proveedor Secundario"),
            ("✉️ Explicar el retraso a los clientes ofreciendo un pequeño regalo futuro", -50, -5, 5, "Comunicado con atención a clientes"),
            ("🤐 Mantener silencio hasta que se resuelva la aduana", 0, -20, -20, "Silencio ante retraso"),
        ],
    },
    {
        "titulo": "Fuga de Información Confidencial",
        "situacion": "Se filtró un borrador preliminar de tus nuevos planes comerciales.",
        "opciones": [
            ("📢 Adelantar el lanzamiento oficial para ganar el mercado", -200, 20, 10, "Lanzamiento Adelantado"),
            ("🔒 Reforzar los acuerdos de confidencialidad internos", -60, 0, 5, "Refuerzo NDA"),
            ("🤷‍♂️ No hacer nada y considerar que fue publicidad gratuita", 0, -5, -15, "Inacción por filtración"),
        ],
    },
    {
        "titulo": "Comentarios Negativos de la Prensa local",
        "situacion": "Un blog especializado publicó un artículo cuestionando la viabilidad de tu servicio.",
        "opciones": [
            ("📰 Organizar un evento demostrativo en vivo para la prensa", -180, 15, 15, "Demostración a Prensa"),
            ("💬 Responder en la sección de comentarios del artículo", 0, -5, -5, "Respuesta en comentarios"),
            ("🚫 Bloquear y vetar al medio de tus canales oficiales", 0, -15, -20, "Veto a Medio de Prensa"),
        ],
    },
    {
        "titulo": "Aumento Inesperado en Alquiler/Infraestructura",
        "situacion": "Los costos fijos de tu espacio operativo o servidores aumentaron un 25%.",
        "opciones": [
            ("🏠 Reubicar la operación a un esquema totalmente remoto/virtual", -150, 5, 5, "Migración a Trabajo Remoto"),
            ("🤝 Absorber el aumento y renegociar el contrato a largo plazo", -250, 0, 0, "Renegociación de Contrato"),
            ("✂️ Reducir beneficios al equipo para compensar el costo", 0, -10, -20, "Recorte de Beneficios"),
        ],
    },
    {
        "titulo": "Llegada de una Copia Barata",
        "situacion": "Un clon de tu servicio aparece vendiendo una versión defectuosa pero muy barata.",
        "opciones": [
            ("🏅 Crear una campaña destacando los sellos de garantía y calidad", -150, 15, 15, "Campaña de Garantía y Calidad"),
            ("💸 Bajar tus precios temporalmente para frenar su entrada", -200, 10, -5, "Guerra de precios temporal"),
            ("🤫 Ignorarlos confiando en la lealtad de tus usuarios", 0, -10, -10, "Inacción ante clon"),
        ],
    },
]

# Inicialización de modo de juego
if "modo_dificultad" not in st.session_state:
    st.session_state.modo_dificultad = None


def iniciar_partida(modo):
    st.session_state.modo_dificultad = modo
    st.session_state.dinero = 1500
    st.session_state.clientes = 10
    st.session_state.reputacion = 50
    st.session_state.fase = 0
    st.session_state.historial = []

    if modo == "Fácil":
        st.session_state.preguntas_juego = random.sample(BANCO_FACIL, 10)
    else:
        st.session_state.preguntas_juego = random.sample(BANCO_DIFICIL, 10)


# Selección de Modo de Juego inicial
if st.session_state.modo_dificultad is None:
    st.markdown(
        """
        <div class="question-card" style="text-align: center;">
            <div class="question-title">🎯 SELECCIONA TU MODO DE JUEGO</div>
            <div class="question-text">¿Qué tan preparado te sientes para administrar tu empresa?</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col_facil, col_dificil = st.columns(2)
    with col_facil:
        if st.button("🟢 Modo Normal / Fácil\n(Precios e inversiones visibles)"):
            iniciar_partida("Fácil")
            st.rerun()

    with col_dificil:
        if st.button("🔴 Modo Difícil / Experto\n(Situaciones críticas sin precios)"):
            iniciar_partida("Difícil")
            st.rerun()

else:
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
        st.error("💥 ¡QUIEBRA TÉCNICA! Te quedaste sin capital suficiente para continuar operando.")
        game_over = True
    elif st.session_state.reputacion <= 30:
        st.error("💥 ¡CRISIS SEVERA DE REPUTACIÓN! Tu reputación cayó a 30 o menos y la empresa perdió total credibilidad.")
        game_over = True

    fase_actual = st.session_state.fase

    # Renderizado de Pregunta Actual
    if not game_over and fase_actual < 10:
        datos = st.session_state.preguntas_juego[fase_actual]
        badge_class = "question-badge badge-hard" if st.session_state.modo_dificultad == "Difícil" else "question-badge"

        st.markdown(
            f"""
            <div class="question-card">
                <span class="{badge_class}">PASO {fase_actual + 1} DE 10 • MODO {st.session_state.modo_dificultad.upper()}</span>
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
            st.success("🏆 ¡FELICIDADES! Llegaste a la meta manteniendo una empresa rentable y con excelente reputación.")

        st.markdown("</div>", unsafe_allow_html=True)

        # Generación únicamente del archivo descargable
        if st.session_state.historial:
            df_historial = pd.DataFrame(st.session_state.historial)
            csv_data = df_historial.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Descargar Registro de Decisiones (CSV)",
                data=csv_data,
                file_name=f"historial_emprendimiento_{st.session_state.modo_dificultad.lower()}.csv",
                mime="text/csv",
            )

    # Botón para cambiar de modo o reiniciar
    if game_over or fase_actual >= 10:
        if st.button("🔄 Jugar Otra Vez / Cambiar Modo", use_container_width=True):
            st.session_state.clear()
            st.rerun()