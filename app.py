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

# BANCO MODO FÁCIL (50 Preguntas - Precios e impactos cuantitativos visibles)
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
            ("🔍 Hablar directamente con la persona e investigar con la logística [Costo: -$150]", -150, 5, 15, "Investigación personalizada"),
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
            ("📈 Aceptar la Inversión Total a cambio de participación [Ingreso: +$1,500]", 1500, 10, 0, "Aceptó Inversión externa"),
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
    {
        "titulo": "Optimización del Sitio Web",
        "situacion": "El sitio web se cae constantemente debido a la lentitud del servidor.",
        "opciones": [
            ("⚡ Rediseñar el sitio y migrar a servidores de alto rendimiento [Inversión: -$350]", -350, 15, 8, "Rediseño Web Completo"),
            ("🔧 Aplicar optimizaciones básicas y limpiar la base de datos [Inversión: -$80]", -80, 5, 2, "Optimización básica"),
            ("⏳ No realizar cambios hasta que haya más presupuesto [Costo: $0]", 0, -8, -12, "Sin mejoras web"),
        ],
    },
    {
        "titulo": "Programa de Fidelización",
        "situacion": "Quieres asegurar que los clientes actuales vuelvan a comprar regularmente.",
        "opciones": [
            ("💳 Lanzar un Programa de Puntos y Recompensas Exclusivas [Inversión: -$300]", -300, 12, 12, "Programa de Puntos"),
            ("📧 Enviar un boletín mensual con cuentos y descuentos [Inversión: -$50]", -50, 4, 3, "Boletín mensual"),
            ("❌ No implementar ningún beneficio de fidelización [Costo: $0]", 0, -2, -5, "Sin programa fidelización"),
        ],
    },
    {
        "titulo": "Participación en Feria de Innovación",
        "situacion": "Existe la posibilidad de colocar un stand en una importante expo del sector.",
        "opciones": [
            ("🎪 Contratar un Stand Premium y material promocional [Inversión: -$500]", -500, 30, 15, "Stand Premium Expo"),
            ("🎟️ Asistir únicamente como visitante para hacer networking [Inversión: -$100]", -100, 8, 5, "Networking Visitante"),
            ("🏠 Dejar pasar el evento para no incurrir en gastos [Costo: $0]", 0, 0, 0, "No asistió a Feria"),
        ],
    },
    {
        "titulo": "Certificación de Calidad",
        "situacion": "Obtener una acreditación oficial de calidad le daría mucho respaldo al producto.",
        "opciones": [
            ("🏅 Iniciar el proceso completo de auditoría y certificación ISO [Inversión: -$600]", -600, 10, 25, "Certificación Oficial ISO"),
            ("📄 Implementar un manual de buenas prácticas interno [Inversión: -$150]", -150, 3, 8, "Manual Interno"),
            ("🚫 Continuar operando sin ningún sello de garantía [Costo: $0]", 0, 0, -5, "Sin certificado"),
        ],
    },
    {
        "titulo": "Estrategia de Email Marketing",
        "situacion": "Tienes una lista de correos de potenciales interesados.",
        "opciones": [
            ("📩 Automatizar secuencias personalizadas de ventas [Inversión: -$200]", -200, 18, 5, "Email Marketing Automatizado"),
            ("✉️ Enviar un correo promocional directo de forma manual [Inversión: -$30]", -30, 5, 1, "Correo promocional manual"),
            ("🗑️ Descartar la lista por falta de tiempo [Costo: $0]", 0, 0, 0, "Lista ignorada"),
        ],
    },
    {
        "titulo": "Suscripción de Software Operativo",
        "situacion": "Herramientas avanzadas de gestión pueden ahorrar muchas horas de trabajo.",
        "opciones": [
            ("💻 Adquirir licencias del software ERP empresarial [Inversión: -$400]", -400, 8, 5, "Licencias ERP"),
            ("📊 Utilizar herramientas gratuitas y plantillas de Excel [Costo: $0]", 0, 0, 0, "Uso de Excel gratuito"),
            ("📝 Llevar el registro manual en cuadernos y notas [Costo: $0]", 0, -5, -10, "Registro manual"),
        ],
    },
    {
        "titulo": "Estudio de Mercado",
        "situacion": "Dudas si lanzar una nueva línea de productos o enfocarte en la existente.",
        "opciones": [
            ("🔬 Contratar una agencia experta para un estudio formal [Inversión: -$450]", -450, 10, 10, "Estudio Agencia Profesional"),
            ("📋 Diseñar encuestas propias y entrevistar a 50 usuarios [Inversión: -$50]", -50, 4, 3, "Encuestas Propias"),
            ("🎲 Lanzar según la intuición de los fundadores [Costo: $0]", 0, 2, -8, "Decisión por intuición"),
        ],
    },
    {
        "titulo": "Capacitación del Equipo",
        "situacion": "Surgieron nuevas tecnologías que el equipo no domina adecuadamente.",
        "opciones": [
            ("🎓 Inscribir al equipo en un Boot Camp intensivo especializado [Inversión: -$350]", -350, 5, 12, "Boot Camp Especializado"),
            ("📚 Comprar libros de estudio y cursos grabados [Inversión: -$80]", -80, 2, 4, "Cursos Grabados"),
            ("⌛ Pedir que aprendan de forma autodidacta en tiempo libre [Costo: $0]", 0, -2, -6, "Aprendizaje Autodidacta"),
        ],
    },
    {
        "titulo": "Packaging y Embalaje",
        "situacion": "El empaque actual del producto es sencillo y sin marca.",
        "opciones": [
            ("📦 Diseñar cajas personalizadas sostenibles y atractivas [Inversión: -$300]", -300, 10, 15, "Packaging Sostenible"),
            ("🏷️ Agregar stickers con la marca sobre las cajas estándar [Inversión: -$60]", -60, 3, 4, "Stickers de marca"),
            ("🟫 Enviar en sobres de papel genéricos sin diseño [Costo: $0]", 0, -2, -8, "Empaque Genérico"),
        ],
    },
    {
        "titulo": "Reducción de Plazos de Pago",
        "situacion": "Los clientes corporativos piden pagar a 60 días, pero necesitas liquidez.",
        "opciones": [
            ("🏦 Contratar servicio de Factoring pagando una comisión [Costo: -$150]", -150, 8, 2, "Uso de Factoring"),
            ("🏷️ Ofrecer un 5% de descuento por Pago Contado Inmediato [Costo: -$80]", -80, 5, 3, "Descuento Pronto Pago"),
            ("⏳ Aceptar el plazo de 60 días sin negociar [Costo: $0]", 0, 2, 0, "Aceptó 60 días"),
        ],
    },
    {
        "titulo": "Contratación de Asesor Legal",
        "situacion": "Debes redactar los términos y condiciones del servicio y proteger contratos.",
        "opciones": [
            ("⚖️ Contratar un abogado especialista en startups [Inversión: -$300]", -300, 0, 10, "Abogado Especialista"),
            ("📄 Usar una plantilla legal estandarizada de internet [Inversión: -$30]", -30, 0, 0, "Plantilla de Internet"),
            ("✍️ Redactar el documento internamente sin asesoría [Costo: $0]", 0, 0, -10, "Redacción propia informal"),
        ],
    },
    {
        "titulo": "Estrategia con Influenciadores",
        "situacion": "Quieres llegar a un público más joven a través de creadores de contenido.",
        "opciones": [
            ("🌟 Contratar 2 Influencers reconocidos del sector [Inversión: -$500]", -500, 35, 8, "Influencers Reconocidos"),
            ("🎁 Enviar productos gratis a 10 Micro-influencers [Inversión: -$120]", -120, 12, 5, "Regalos Micro-influencers"),
            ("🚫 Evitar el marketing con creadores de contenido [Costo: $0]", 0, 0, 0, "Sin Influencers"),
        ],
    },
    {
        "titulo": "Rediseño de Identidad Visual",
        "situacion": "La imagen gráfica actual luce poco profesional en comparación con la competencia.",
        "opciones": [
            ("🎨 Contratar una agencia de branding para renovar la marca [Inversión: -$400]", -400, 10, 15, "Renovación Branding"),
            ("💻 Ajustar el logo e iconografía en plataformas gratuitas [Inversión: -$50]", -50, 3, 3, "Ajustes básicos logo"),
            ("🖌️ Mantener el logo original hecho al inicio [Costo: $0]", 0, -2, -5, "Mantener logo antiguo"),
        ],
    },
    {
        "titulo": "Patrocinio de Evento Local",
        "situacion": "Un congreso educativo local busca patrocinadores.",
        "opciones": [
            ("🥇 Ser Patrocinador Principal con espacio en tarima [Inversión: -$450]", -450, 20, 18, "Patrocinio Principal"),
            ("🥉 Aparecer en el catálogo del evento como colaborador [Inversión: -$100]", -100, 5, 5, "Patrocinio Catálogo"),
            ("❌ Decline la oportunidad de patrocinio [Costo: $0]", 0, 0, 0, "Rechazó Patrocinio"),
        ],
    },
    {
        "titulo": "Adquisición de Equipamiento",
        "situacion": "Las computadoras del equipo están viejas y ralentizan las entregas.",
        "opciones": [
            ("💻 Renovar el equipo de cómputo con procesadores modernos [Inversión: -$600]", -600, 5, 5, "Renovación Computadoras"),
            ("🛠️ Comprar memoria RAM adicional y discos sólidos [Inversión: -$150]", -150, 2, 2, "Mantenimiento Equipos"),
            ("⌛ Seguir trabajando con los equipos actuales [Costo: $0]", 0, -3, -5, "Sin renovación técnica"),
        ],
    },
    {
        "titulo": "Estrategia de Ventas B2B",
        "situacion": "Buscas cerrar acuerdos directos con colegios y centros de capacitación.",
        "opciones": [
            ("👔 Contratar un Ejecutivo de Ventas con cartera de clientes [Inversión: -$500]", -500, 25, 5, "Ejecutivo B2B Dedicated"),
            ("📞 Asignar días de llamadas en frío al equipo interno [Inversión: -$50]", -50, 8, 1, "Llamadas en frío"),
            ("🌐 Esperar a que las instituciones lleguen por la web [Costo: $0]", 0, 1, -2, "Ventas pasivas"),
        ],
    },
    {
        "titulo": "Implementación de Soporte 24/7",
        "situacion": "Clientes extranjeros preguntan por soporte fuera del horario de oficina.",
        "opciones": [
            ("🤖 Configurar un Chatbot inteligente con respuesta instantánea [Inversión: -$250]", -250, 10, 8, "Chatbot Automatizado"),
            ("📱 Responder mensajes desde el celular según disponibilidad [Costo: $0]", 0, 2, -3, "Soporte informal"),
            ("🕔 Establecer un mensaje indicando atención en horas hábiles [Costo: $0]", 0, -2, 2, "Horario limitado claro"),
        ],
    },
    {
        "titulo": "Apertura de Punto Físico Demo",
        "situacion": "Te proponen habilitar un pequeño showroom de prueba para clientes.",
        "opciones": [
            ("🏬 Alquilar un espacio temporal en un centro comercial [Inversión: -$650]", -650, 30, 12, "Showroom Temporal"),
            ("🤝 Colocar productos en consignación en una tienda aliada [Inversión: -$100]", -100, 8, 4, "Consignación Tienda"),
            ("🌐 Mantenerse exclusivamente como tienda digital [Costo: $0]", 0, 0, 0, "Modelo 100% Digital"),
        ],
    },
    {
        "titulo": "Promoción de Black Friday",
        "situacion": "Se acerca la temporada de altas ventas a nivel mundial.",
        "opciones": [
            ("💥 Lanzar descuentos del 40% respaldados por publicidad [Inversión: -$350]", -350, 40, 5, "Campaña Black Friday"),
            ("🏷️ Ofrecer envío gratis por compras superiores a cierto monto [Inversión: -$80]", -80, 12, 4, "Envío Gratis Promocional"),
            ("🚫 No participar en campañas de descuentos [Costo: $0]", 0, -5, 0, "Sin promociones"),
        ],
    },
    {
        "titulo": "Renovación de Contrato de Dominio y Cloud",
        "situacion": "Corresponde renovar las plataformas y servidores para el próximo año.",
        "opciones": [
            ("🔒 Pagar la suscripción anual anticipada con descuento [Inversión: -$200]", -200, 0, 5, "Suscripción Anual Cloud"),
            ("📅 Pagar la cuota mes a mes con recargo adicional [Inversión: -$30]", -30, 0, 0, "Pago Mensual Servidores"),
            ("⚠️ Trasladar a un hosting barato pero inestable [Inversión: -$10]", -10, -5, -15, "Hosting Inestable"),
        ],
    },
    {
        "titulo": "Desarrollo de Aplicación Móvil",
        "situacion": "Los usuarios solicitan ingresar al servicio desde una App propia.",
        "opciones": [
            ("📲 Desarrollar una App nativa para Android e iOS [Inversión: -$700]", -700, 35, 15, "App Nativa Desarrollada"),
            ("🌐 Adaptar la página web a un formato móvil (PWA) [Inversión: -$150]", -150, 10, 5, "Versión PWA Móvil"),
            ("🖥️ Mantener acceso únicamente para computadoras de escritorio [Costo: $0]", 0, -8, -10, "Sin acceso móvil"),
        ],
    },
    {
        "titulo": "Gestión de Desechos / Sostenibilidad",
        "situacion": "Se busca mejorar el perfil ecológico del proceso productivo.",
        "opciones": [
            ("♻️ Implementar un proceso de basura cero e insumos reciclables [Inversión: -$250]", -250, 5, 20, "Proceso Basura Cero"),
            ("📦 Reemplazar plástico por papel en envíos sencillos [Inversión: -$50]", -50, 2, 5, "Insumos de Papel"),
            ("🗑️ Mantener los insumos plásticos económicos tradicionales [Costo: $0]", 0, 0, -10, "Sin iniciativa ecológica"),
        ],
    },
    {
        "titulo": "Seguro contra Contingencias",
        "situacion": "Aparece la opción de asegurar los activos contra robos o daños.",
        "opciones": [
            ("🛡️ Adquirir una Póliza de Seguro Empresarial Todo Riesgo [Inversión: -$300]", -300, 0, 10, "Póliza Empresarial"),
            ("🔒 Reforzar las cerraduras y alarmas locales [Inversión: -$80]", -80, 0, 2, "Seguridad Física Básica"),
            ("🎲 Operar asumir los riesgos de cualquier accidente [Costo: $0]", 0, 0, -5, "Sin seguro"),
        ],
    },
    {
        "titulo": "Traducción y Localización de Idioma",
        "situacion": "Recibes visitas de clientes angloparlantes en la web.",
        "opciones": [
            ("🇬🇧 Traducir profesionalmente el sistema al inglés [Inversión: -$200]", -200, 15, 8, "Traducción Profesional"),
            ("🤖 Colocar un botón de traducción automática de Google [Costo: $0]", 0, 3, -2, "Traducción Automática"),
            ("🇪🇸 Mantener el servicio exclusivamente en español [Costo: $0]", 0, -2, 0, "Solo Español"),
        ],
    },
    {
        "titulo": "Campaña de Referidos",
        "situacion": "Quieres que los clientes actuales inviten a sus conocidos.",
        "opciones": [
            ("🎁 Entregar $10 en saldo al usuario y su amigo referido [Inversión: -$250]", -250, 25, 6, "Programa de Referidos Bivalente"),
            ("🏷️ Regalar un sticker promocional por cada invitación [Inversión: -$30]", -30, 4, 1, "Regalo sencillo referidos"),
            ("❌ No entregar incentivos por recomendar [Costo: $0]", 0, 0, 0, "Sin programa de recomendación"),
        ],
    },
    {
        "titulo": "Creación de Canal de YouTube / Blog",
        "situacion": "Crear contenido educativo puede posicionar la marca como experta.",
        "opciones": [
            ("🎥 Contratar edición de video profesional para tutoriales [Inversión: -$300]", -300, 15, 12, "Videos Educativos Pro"),
            ("✍️ Grabar explicaciones sencillas desde el teléfono [Inversión: -$20]", -20, 5, 3, "Videos Celular"),
            ("🚫 No dedicar tiempo a la creación de contenidos [Costo: $0]", 0, 0, 0, "Sin contenidos"),
        ],
    },
    {
        "titulo": "Registro Oficial de Patente / Propiedad",
        "situacion": "Quieres asegurar la propiedad sobre la metodología usada.",
        "opciones": [
            ("📜 Tramitar el registro formal de marca y patente [Inversión: -$400]", -400, 0, 15, "Registro Oficial Patente"),
            ("📝 Guardar evidencias de autoría en registros digitales [Inversión: -$40]", -40, 0, 2, "Registro Digital Básico"),
            ("🔓 Dejar el desarrollo abierto sin protección jurídica [Costo: $0]", 0, 0, -8, "Propiedad sin proteger"),
        ],
    },
    {
        "titulo": "Renovación de Contratos con Proveedores",
        "situacion": "Tu proveedor clave aumentó sus precios un 15%.",
        "opciones": [
            ("🤝 Firmar contrato exclusivo a largo plazo reteniendo precio [Inversión: -$200]", -200, 5, 5, "Contrato Exclusivo Proveedor"),
            ("🔍 Buscar y evaluar un proveedor alternativo más económico [Inversión: -$50]", -50, -2, 0, "Cambio Proveedor Económico"),
            ("💸 Aceptar el incremento sin negociar nada [Costo: $0]", 0, -5, -2, "Aceptó aumento precio"),
        ],
    },
    {
        "titulo": "Validación con Grupo Focal (Focus Group)",
        "situacion": "Tienes dudas sobre el diseño del empaque y la propuesta visual.",
        "opciones": [
            ("👥 Contratar un grupo focal con clientes potenciales [Inversión: -$300]", -300, 8, 10, "Focus Group Profesional"),
            ("☕ Invitar un café a 5 amigos para escuchar su opinión [Inversión: -$20]", -20, 2, 1, "Reunión Informal Amigos"),
            ("🚀 Lanzar sin consultar a ningún grupo [Costo: $0]", 0, 0, -5, "Sin validación previa"),
        ],
    },
    {
        "titulo": "Integración de Pasarelas de Pago",
        "situacion": "Clientes abandonan las compras porque faltan medios de pago.",
        "opciones": [
            ("💳 Integrar cobro con tarjeta, transferencia y billeteras [Inversión: -$250]", -250, 20, 5, "Múltiples Pasarelas Pago"),
            ("🏦 Aceptar únicamente transferencias bancarias directas [Costo: $0]", 0, 2, -2, "Solo Transferencias"),
            ("💵 Cobrar únicamente contra entrega en efectivo [Costo: $0]", 0, -10, -10, "Solo Efectivo"),
        ],
    },
    {
        "titulo": "Optimización del Checkout",
        "situacion": "El proceso de compra en la tienda requiere completar muchos campos.",
        "opciones": [
            ("🛒 Contratar un rediseño del carrito a 1 solo clic [Inversión: -$200]", -200, 18, 5, "Checkout 1-Clic"),
            ("📋 Eliminar 2 campos innecesarios del formulario actual [Costo: $0]", 0, 5, 2, "Simplificación formulario"),
            ("🔒 Exigir registro completo previo para poder ver precios [Costo: $0]", 0, -12, -8, "Registro obligatorio estricto"),
        ],
    },
    {
        "titulo": "Lanzamiento de Edición Limitada",
        "situacion": "Es el aniversario de la empresa y se planea una edición especial.",
        "opciones": [
            ("✨ Producir un lote exclusivo con caja conmemorativa [Inversión: -$350]", -350, 15, 12, "Edición Aniversario Especial"),
            ("🎉 Aplicar un banner festivo en las redes sociales [Inversión: -$20]", -20, 2, 2, "Banner Celebración"),
            ("📅 Dejar pasar el aniversario como un día normal [Costo: $0]", 0, 0, 0, "Aniversario ignorado"),
        ],
    },
    {
        "titulo": "Participación en Podcast del Sector",
        "situacion": "Te invitan a hablar de tu negocio en un programa de radio digital popular.",
        "opciones": [
            ("🎙️ Preparar una presentación impecable con asesoría [Inversión: -$150]", -150, 12, 15, "Entrevista Podcast Asesorada"),
            ("📱 Asistir a la llamada de forma improvisada [Costo: $0]", 0, 4, 2, "Entrevista Improvisada"),
            ("🚫 Rechazar la invitación por pena o falta de tiempo [Costo: $0]", 0, 0, -2, "Rechazó Podcast"),
        ],
    },
    {
        "titulo": "Evaluación del Clima Laboral",
        "situacion": "El equipo se nota cansado tras las jornadas de entregas.",
        "opciones": [
            ("🌴 Organizar un día de integración (Team Building) pagado [Inversión: -$250]", -250, 0, 10, "Jornada Team Building"),
            ("🍕 Invitar una tarde de pizza durante la reunión semanal [Inversión: -$40]", -40, 0, 3, "Tarde de Pizza"),
            ("📢 Exigir mantener el rendimiento sin distracciones [Costo: $0]", 0, -5, -15, "Presión laboral"),
        ],
    },
    {
        "titulo": "Encuesta de Satisfacción (NPS)",
        "situacion": "Quieres medir la lealtad real de tus compradores.",
        "opciones": [
            ("📊 Contratar plataforma interactiva de retroalimentación [Inversión: -$180]", -180, 5, 8, "Plataforma NPS Profesional"),
            ("📧 Enviar un formulario gratuito de Google Forms [Costo: $0]", 0, 2, 2, "Google Forms Gratis"),
            ("❌ No preguntar la opinión de los clientes [Costo: $0]", 0, -4, -6, "Sin medición de satisfacción"),
        ],
    },
    {
        "titulo": "Implementación de Certificado de Seguridad SSL",
        "situacion": "El navegador web marca la tienda como 'Sitio No Seguro'.",
        "opciones": [
            ("🔒 Comprar e instalar el certificado de seguridad avanzado [Inversión: -$150]", -150, 10, 10, "Certificado SSL Avanzado"),
            ("🛠️ Instalar la versión gratuita de certificación básica [Costo: $0]", 0, 4, 3, "SSL Básico Gratuito"),
            ("⚠️ Dejar la web sin certificado de seguridad [Costo: $0]", 0, -20, -30, "Sitio No Seguro"),
        ],
    },
    {
        "titulo": "Campaña de Remarketing",
        "situacion": "Muchas personas ven los productos pero no completan la compra.",
        "opciones": [
            ("🎯 Invertir en anuncios dirigidos a quienes abandonaron el carrito [Inversión: -$200]", -200, 20, 2, "Campaña Remarketing"),
            ("📧 Configurar un correo de recordatorio de carrito olvidado [Inversión: -$30]", -30, 6, 1, "Email Carrito Olvidado"),
            ("🤷‍♂️ Confiar en que los clientes regresen solos [Costo: $0]", 0, 0, 0, "Sin remarketing"),
        ],
    },
    {
        "titulo": "Pruebas de Usabilidad con Usuarios",
        "situacion": "Dudas si a los clientes mayores les cuesta navegar en el sistema.",
        "opciones": [
            ("🧪 Realizar sesiones observadas de prueba de uso [Inversión: -$220]", -220, 6, 8, "Pruebas Usabilidad Profesional"),
            ("👀 Observar a un familiar usando la plataforma [Costo: $0]", 0, 1, 1, "Prueba casera"),
            ("🚀 Asumir que la interfaz es perfecta para todos [Costo: $0]", 0, -4, -5, "Sin pruebas usabilidad"),
        ],
    },
    {
        "titulo": "Asistencia a Convención Internacional",
        "situacion": "Oportunidad de viajar para representar a la startup en el extranjero.",
        "opciones": [
            ("✈️ Comprar pasajes y participar en la rueda de negocios [Inversión: -$800]", -800, 40, 20, "Viaje Convención Internacional"),
            ("💻 Participar únicamente de las conferencias en modalidad virtual [Inversión: -$100]", -100, 8, 4, "Convención Virtual"),
            ("❌ Dejar pasar la oportunidad internacional [Costo: $0]", 0, 0, 0, "No asistió a Convención"),
        ],
    },
    {
        "titulo": "Cierre del Ejercicio Anual",
        "situacion": "Es momento de hacer el balance final de la empresa ante los socios.",
        "opciones": [
            ("📊 Contratar un informe financiero detallado con proyecciones [Inversión: -$250]", -250, 0, 12, "Balance Financiero Detallado"),
            ("📝 Presentar una hoja de resumen de ingresos y egresos [Costo: $0]", 0, 0, 2, "Resumen Básico"),
            ("🙈 Postergar la reunión de resultados por tiempo indefinido [Costo: $0]", 0, -5, -15, "Informe de resultados omitido"),
        ],
    },
]

# BANCO MODO DIFÍCIL (50 Preguntas - Escenarios de crisis, precios ocultos e información incompleta)
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
            ("🔥 Ignorar las críticas y dejar corriendo los anuncios", 0, 10, -25, "Ignóro Boicot"),
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
            ("✈️ Contratar envío exprés prioritario con un proveedor secundario", -250, 10, 10, "Envío Exprés Secundario"),
            ("✉️ Explicar el retraso a los clientes ofreciendo un pequeño regalo futuro", -50, -5, 5, "Comunicado con Atención"),
            ("🤐 Mantener silencio hasta que se resuelva la aduana", 0, -20, -20, "Silencio ante Retraso"),
        ],
    },
    {
        "titulo": "Fuga de Información Confidencial",
        "situacion": "Se filtró un borrador preliminar de tus nuevos planes comerciales.",
        "opciones": [
            ("📢 Adelantar el lanzamiento oficial para ganar el mercado", -200, 20, 10, "Lanzamiento Adelantado"),
            ("🔒 Reforzar los acuerdos de confidencialidad internos", -60, 0, 5, "Refuerzo NDA"),
            ("🤷‍♂️ No hacer nada y considerar que fue publicidad gratuita", 0, -5, -15, "Inacción por Filtración"),
        ],
    },
    {
        "titulo": "Comentarios Negativos de la Prensa local",
        "situacion": "Un blog especializado publicó un artículo cuestionando la viabilidad de tu servicio.",
        "opciones": [
            ("📰 Organizar un evento demostrativo en vivo para la prensa", -180, 15, 15, "Demostración a Prensa"),
            ("💬 Responder en la sección de comentarios del artículo", 0, -5, -5, "Respuesta en comentarios"),
            ("🚫 Bloquear y vetar al medio de tus canales oficiales", 0, -15, -20, "Veto a Medio"),
        ],
    },
    {
        "titulo": "Aumento Inesperado en Alquiler/Infraestructura",
        "situacion": "Los costos fijos de tu espacio operativo o servidores aumentaron un 25%.",
        "opciones": [
            ("🏠 Reubicar la operación a un esquema totalmente remoto/virtual", -150, 5, 5, "Migración Trabajo Remoto"),
            ("🤝 Absorber el aumento y renegociar el contrato a largo plazo", -250, 0, 0, "Renegociación Contrato"),
            ("✂️ Reducir beneficios al equipo para compensar el costo", 0, -10, -20, "Recorte Beneficios"),
        ],
    },
    {
        "titulo": "Llegada de una Copia Barata",
        "situacion": "Un clon de tu servicio aparece vendiendo una versión defectuosa pero muy barata.",
        "opciones": [
            ("🏅 Crear una campaña destacando los sellos de garantía y calidad", -150, 15, 15, "Campaña Garantía y Calidad"),
            ("💸 Bajar tus precios temporalmente para frenar su entrada", -200, 10, -5, "Guerra Precios Temporal"),
            ("🤫 Ignorarlos confiando en la lealtad de tus usuarios", 0, -10, -10, "Inacción ante Clon"),
        ],
    },
    {
        "titulo": "Renuncia Inesperada del Socio Fundador",
        "situacion": "Tu socio decide abandonar el proyecto por motivos personales exigiendo vender sus acciones.",
        "opciones": [
            ("💰 Comprar su participación de contado con ahorros de la empresa", -400, 0, 5, "Compra Acciones Socio"),
            ("🤝 Buscar un inversionista sustituto que asuma su paquete accionario", -100, 5, -5, "Inversionista Sustituto"),
            ("⚖️ Iniciar un arbitraje legal para congelar la salida", -180, -5, -15, "Arbitraje Legal Salida"),
        ],
    },
    {
        "titulo": "Vulnerabilidad en Datos de Pago",
        "situacion": "Un investigador externo detectó un fallo potencial en el sistema de facturación.",
        "opciones": [
            ("🛡️ Auditar y reparar el sistema pagando una recompensa ética al investigador", -220, 0, 15, "Recompensa Ciberseguridad"),
            ("🛠️ Parchear internamente el error de forma rápida", -50, 0, 0, "Parche Interno Rápido"),
            ("🤷‍♂️ Desestimar el reporte acusando al investigador de chantaje", 0, -15, -25, "Desestimación Reporte"),
        ],
    },
    {
        "titulo": "Quiebra del Proveedor Principal",
        "situacion": "La empresa que te abastece del insumo crítico cerró sorpresivamente sus puertas.",
        "opciones": [
            ("🌍 Importar los insumos con tarifa exprés desde un mercado extranjero", -350, 10, 10, "Importación Exprés"),
            ("🤝 Firmar contrato de urgencia con un proveedor local de menor calidad", -120, -5, -5, "Proveedor Local Alternativo"),
            ("🛑 Detener los despachos hasta encontrar una solución económica", 0, -25, -20, "Pausa de Despachos"),
        ],
    },
    {
        "titulo": "Sanción Regulatoria Sorpresiva",
        "situacion": "Una entidad estatal impone una multa por falta de un permiso administrativo reciente.",
        "opciones": [
            ("🏛️ Pagar la multa de inmediato y gestionar la licencia correspondiente", -280, 0, 10, "Pago Multa y Regularización"),
            ("⚖️ Apelar la sanción en tribunales contenciosos", -120, 0, -5, "Apelación Legal Sanción"),
            ("🙈 Continuar operando sin pagar esperando que no cierren el negocio", 0, 0, -30, "Manejo Informal Sanción"),
        ],
    },
    {
        "titulo": "Estafa en Transacción Internacional",
        "situacion": "Un cliente extranjero pagó con una tarjeta clonada y el banco retuvo los fondos entregados.",
        "opciones": [
            ("🔒 Implementar un software anti-fraude para transacciones futuras", -200, 0, 10, "Software Anti-Fraude"),
            ("📊 Absorber la pérdida contable como gasto de operación", -150, 0, 0, "Absorción Pérdida"),
            ("😡 Exigir al cliente el pago bajo amenaza de denuncia internacional", 0, -5, -10, "Reclamo Agresivo"),
        ],
    },
    {
        "titulo": "Pérdida Masiva de Información (Sin Backup)",
        "situacion": "Un fallo de disco eliminó el registro de clientes del último mes.",
        "opciones": [
            ("🚑 Contratar una empresa especializada en recuperación forense de datos", -300, 5, 10, "Recuperación Forense Datos"),
            ("📧 Pedir amablemente a los clientes que reingresen sus datos en la web", -20, -15, -10, "Reingreso Manual Clientes"),
            ("📝 Reconstruir la información a partir de comprobantes en papel", 0, -10, -15, "Reconstrucción Manual"),
        ],
    },
    {
        "titulo": "Huelga de Transportistas",
        "situacion": "Un paro nacional de transporte impide entregar los productos por más de una semana.",
        "opciones": [
            ("🚁 Contratar servicios de mensajería privada especializada de costo elevado", -280, 12, 12, "Mensajería Privada Exprés"),
            ("🎁 Notificar a los clientes y ofrecer un cupón de regalo por la espera", -60, -2, 8, "Notificación con Regalo"),
            ("🤐 Apagar la atención a clientes hasta que se levante el paro", 0, -20, -25, "Atención Apagada"),
        ],
    },
    {
        "titulo": "Infiltración de Espionaje Industrial",
        "situacion": "Un ex-empleado vendió tu lista de prospectos calificados a la competencia.",
        "opciones": [
            ("⚖️ Iniciar acciones legales por violación de secreto comercial", -250, 0, 10, "Acción Legal Secreto Comercial"),
            ("🚀 Lanzar una oferta relámpago a esa lista para ganar la venta primero", -100, 15, -5, "Oferta Relámpago Lista"),
            ("🤷‍♂️ Dejar pasar la filtración y enfocarse en prospectos nuevos", 0, 0, -10, "Inacción Espionaje"),
        ],
    },
    {
        "titulo": "Retiro de Insumo del Mercado",
        "situacion": "El gobierno prohibió un componente químico/digital que usas en tu servicio.",
        "opciones": [
            ("🧪 Reformular la propuesta con componentes certificados de mayor costo", -320, 8, 15, "Reformulación Certificada"),
            ("⚙️ Reemplazar por un sustituto básico que altera ligeramente el resultado", -100, -8, -10, "Sustituto Básico"),
            ("⚠️ Agotar las existencias almacenadas antes de acatar la prohibición", 0, 5, -35, "Venta de Existencias Prohibidas"),
        ],
    },
    {
        "titulo": "Sabotaje en Servidores por Ex-Empleado",
        "situacion": "Un trabajador despedido desconfiguró la base de datos antes de salir.",
        "opciones": [
            ("💻 Contratar un equipo externo de restauración de emergencia", -280, 0, 10, "Restauración de Emergencia"),
            ("🛠️ Detener operaciones 2 días para reparar la configuración", -80, -10, -5, "Pausa de Reparación"),
            ("🙈 Tratar de disimular los errores de sistema ante los usuarios", 0, -18, -20, "Disimulo de Fallas"),
        ],
    },
    {
        "titulo": "Aumento Drástico de Inflación",
        "situacion": "Los costos de insumos subieron un 30% de un mes a otro en el país.",
        "opciones": [
            ("📈 Ajustar las tarifas de inmediato para proteger el margen de ganancia", 0, -12, 2, "Aumento de Tarifas"),
            ("🤝 Reducir el margen absorbiendo parte del impacto financiero", -200, 5, 8, "Absorción de Inflación"),
            ("✂️ Reducir el tamaño o contenido del producto manteniendo el precio", -50, -10, -15, "Reducción de Producto"),
        ],
    },
    {
        "titulo": "Falla de Integración con Pasarela de Pago",
        "situacion": "Durante todo el fin de semana los cobros se duplicaron a 50 compradores.",
        "opciones": [
            ("💰 Reembolsar automáticamente y regalar un bono de compensación", -350, 5, 20, "Reembolso con Bono"),
            ("🏦 Devolver solo el saldo duplicado tras revisión de cuentas", -120, -5, 5, "Devolución Estándar"),
            ("📄 Pedir que cada cliente gestione la devolución directamente con su banco", 0, -30, -30, "Reclamo Bancario Cliente"),
        ],
    },
    {
        "titulo": "Ocupación de Espacio / Conflicto Local",
        "situacion": "Vecinos o comercios colindantes reclaman por el ruido o logística de tu negocio.",
        "opciones": [
            ("🔇 Insonorizar y acondicionar las instalaciones con aislamiento", -250, 0, 12, "Acondicionamiento Técnico"),
            ("🤝 Negociar horarios de trabajo reducidos para no molestar", -50, -5, 2, "Horarios Reducidos"),
            ("📣 Ignorar los reclamos afirmando contar con patente comercial", 0, -2, -20, "Enfrentamiento Comunitario"),
        ],
    },
    {
        "titulo": "Plagio de Campaña Publicitaria",
        "situacion": "Una marca reconocida copió exactamente tu eslogan y piezas gráficas.",
        "opciones": [
            ("📢 Exponer el caso en redes sociales de forma creativa y viral", -80, 25, 15, "Exposición Viral Creativa"),
            ("⚖️ Enviar una carta de cese y desista legal formal", -180, 0, 5, "Carta Cese y Desista"),
            ("🤦‍♂️ Dejarlo pasar considerando que no se puede luchar contra un gigante", 0, -5, -10, "Inacción ante Plagio"),
        ],
    },
    {
        "titulo": "Fuga de Agua o Incendio Menor en Oficina",
        "situacion": "Un siniestro arruinó el mobiliario y papelería de trabajo.",
        "opciones": [
            ("🏢 Remodelar y reparar los daños con cobertura de seguro", -250, 0, 8, "Reparación Instalaciones"),
            ("🏠 Enviar a todo el equipo a teletrabajo de forma improvisada", -60, -2, -2, "Teletrabajo Improvisado"),
            ("📦 Trabajar entre los escombros hasta juntar dinero", 0, -8, -15, "Trabajo en Malas Condiciones"),
        ],
    },
    {
        "titulo": "Error en el Precio Publicado",
        "situacion": "Por un error tipográfico se vendieron 30 productos a un 10% de su valor real.",
        "opciones": [
            ("🎁 Honrar los pedidos asumiendo la pérdida como costo de imagen", -400, 15, 25, "Honrar Pedidos Error"),
            ("❌ Cancelar las compras solicitando disculpas y dando un 20% de descuento", -80, -10, 0, "Cancelación con Descuento"),
            ("🚫 Cancelar los pedidos unilateralmente sin dar explicaciones", 0, -25, -25, "Cancelación Unilateral"),
        ],
    },
    {
        "titulo": "Bloqueo de Cuenta Publicitaria",
        "situacion": "La plataforma de anuncios bloqueó tu cuenta por un error de revisión automática.",
        "opciones": [
            ("👨‍⚖️ Contratar una agencia certificada para apelar y recuperar la cuenta", -200, 5, 5, "Agencia Certificada Apelación"),
            ("📱 Crear una cuenta nueva y empezar desde cero la pauta", -100, -8, -5, "Cuenta Nueva Pauta"),
            ("⏳ Esperar la resolución del soporte automatizado sin presionar", 0, -15, -10, "Espera Pasiva Soporte"),
        ],
    },
    {
        "titulo": "Contaminación de Insumos",
        "situacion": "Un lote de materia prima vino defectuoso de origen provocando malos olores o fallas.",
        "opciones": [
            ("🗑️ Destruir el lote completo e iniciar reclamo al proveedor", -300, 0, 10, "Destrucción de Lote Defectuoso"),
            ("🔧 Intentar filtrar o arreglar el insumo para no perder la inversión", -100, -12, -15, "Filtro Insumo Defectuoso"),
            ("📦 Utilizar el lote para los pedidos de menor prioridad", 0, -30, -35, "Uso de Lote Contaminado"),
        ],
    },
    {
        "titulo": "Cambio en la Ley de Protección de Datos",
        "situacion": "Una nueva normativa exige consentimiento explícito firmado para guardar datos.",
        "opciones": [
            ("📋 Adaptar el sistema con una firma de abogados especializada", -220, 0, 10, "Adaptación Legal RGPD"),
            ("📧 Enviar un correo masivo pidiendo confirmación de datos", -30, -5, 0, "Correo Masivo Datos"),
            ("🙈 Ignorar la ley hasta recibir una inspección formal", 0, 0, -25, "Incumplimiento Normativo"),
        ],
    },
    {
        "titulo": "Extorsión Digital (Ransomware)",
        "situacion": "Ciberdelincuentes encriptaron los archivos del servidor pidiendo rescate.",
        "opciones": [
            ("🛡️ Contratar a un equipo informático especializado para limpiar el sistema", -350, 0, 10, "Limpieza Ciberseguridad"),
            ("💾 Formatear los equipos y restaurar un respaldo antiguo", -120, -8, -5, "Restauración Respaldo"),
            ("💸 Pagar el rescate solicitado por los atacantes", -450, 0, -20, "Pago Rescate Ransomware"),
        ],
    },
    {
        "titulo": "Pérdida de Contrato con Cliente Grande",
        "situacion": "Tu cliente principal que representaba el 40% de ingresos no renovó contrato.",
        "opciones": [
            ("💼 Lanzar una ofensiva comercial para captar 3 clientes medianos", -250, 18, 5, "Ofensiva Comercial B2B"),
            ("✂️ Reducir la plantilla de empleados para ajustar los costos", -50, -5, -10, "Recorte de Personal"),
            ("📉 Solicitar un crédito bancario para cubrir el déficit temporal", -150, 0, -5, "Crédito Bancario Déficit"),
        ],
    },
    {
        "titulo": "Falta de Liquidez para Planilla",
        "situacion": "A 3 días de pagar sueldos, la cuenta bancaria no tiene fondos suficientes.",
        "opciones": [
            ("💳 Inyectar un préstamo personal de los fundadores a la empresa", -300, 0, 10, "Inyección Préstamo Personal"),
            ("🤝 Negociar un pago diferido en 2 partes con los trabajadores", 0, -5, -15, "Pago Diferido Planilla"),
            ("⌛ Retrasar el pago sin avisar al equipo hasta cobrar facturas", 0, -10, -25, "Retraso Pago Sin Aviso"),
        ],
    },
    {
        "titulo": "Cierre Inesperado de Vías de Acceso",
        "situacion": "Obras públicas frente a tu local impiden el acceso de clientes por 2 meses.",
        "opciones": [
            ("🚚 Implementar servicio de entrega a domicilio gratuita para la zona", -200, 12, 10, "Delivery Gratuito Zona"),
            ("📢 Colocar señalización informativa en las avenidas principales", -50, 2, 2, "Señalización Obras"),
            ("🛋️ Esperar a que concluyan las obras públicas", 0, -15, -10, "Inacción por Obras"),
        ],
    },
    {
        "titulo": "Escándalo de Declaraciones de un Embajador de Marca",
        "situacion": "El rostro público de tu marca hizo comentarios ofensivos en sus redes.",
        "opciones": [
            ("✂️ Cancelar el contrato de inmediato y emitir desvinculación pública", -150, 2, 18, "Desvinculación Embajador"),
            ("📝 Pedir al embajador que disculpe públicamente sin romper contrato", -30, -5, -5, "Disculpa Pública Embajador"),
            ("🤫 Mantener silencio esperando que se olvide la polémica", 0, -15, -25, "Silencio Polémica Embajador"),
        ],
    },
    {
        "titulo": "Acusación Falsa de Defecto por Competidor",
        "situacion": "Crearon cuentas falsas para llenar tu perfil con reseñas de 1 estrella.",
        "opciones": [
            ("🔍 Documentar el ataque y solicitar la eliminación formal a la plataforma", -100, 5, 12, "Reclamación Reseñas Falsas"),
            ("💬 Responder cada reseña falsa desmintiendo con pruebas", -20, 2, 5, "Respuesta Proactiva Reseñas"),
            ("🔥 Discutir agresivamente con las cuentas falsas", 0, -10, -20, "Discusión en Reseñas"),
        ],
    },
    {
        "titulo": "Falla del Sistema de Aire Acondicionado / Confort",
        "situacion": "En plena ola de calor la ventilación de la tienda dejó de funcionar.",
        "opciones": [
            ("❄️ Comprar e instalar un equipo industrial nuevo el mismo día", -280, 5, 10, "Aire Acondicionado Nuevo"),
            ("🌬️ Alquilar ventiladores portátiles como solución temporal", -70, 0, 0, "Ventiladores Portátiles"),
            ("🔥 Obligar a trabajar en altas temperaturas sin climatización", 0, -10, -20, "Sin Climatización"),
        ],
    },
    {
        "titulo": "Incompatibilidad de Actualización de Software",
        "situacion": "La última actualización del sistema operativo volvió inoperable tu App.",
        "opciones": [
            ("👨‍💻 Contratar horas de desarrollo urgente de fin de semana", -300, 10, 10, "Desarrollo Urgente Fin de Semana"),
            ("⏪ Volver a la versión anterior perdiendo las nuevas funciones", -50, -5, -2, "Rollback Versión Anterior"),
            ("⏳ Pedir paciencia a los usuarios mientras el equipo interno lo resuelve", 0, -18, -15, "Espera Resolución Interna"),
        ],
    },
    {
        "titulo": "Perdida de Licencia Comercial",
        "situacion": "Un inspector clausuró temporalmente por falta de un rótulo de emergencia.",
        "opciones": [
            ("🚨 Instalar la señalética en 24 horas y pagar inspección exprés", -200, 0, 10, "Inspección Exprés Señalética"),
            ("📝 Hacer el trámite regular esperando 10 días hábiles", -50, -10, -5, "Trámite Regular Clausura"),
            ("🚪 Abrir a puerta cerrada de manera clandestina", 0, -5, -35, "Operación Clandestina"),
        ],
    },
    {
        "titulo": "Nuevos Impuestos al Comercio Electrónico",
        "situacion": "El gobierno aprobó una tasa del 8% a todas las transacciones digitales.",
        "opciones": [
            ("💡 Absorber el impuesto eficientizando procesos de costo", -180, 5, 10, "Absorción Eficiente Impuesto"),
            ("🏷️ Trasladar el impuesto de forma transparente al precio final", 0, -10, -2, "Traslado Transparente Impuesto"),
            ("❓ Ocultar el recargo bajo el concepto de 'gastos administrativos'", 0, -15, -20, "Ocultamiento Recargo"),
        ],
    },
    {
        "titulo": "Caída del Proveedor de Correo Electrónico",
        "situacion": "Los correos de confirmación de compra dejaron de enviarse por 24 horas.",
        "opciones": [
            ("✉️ Contratar un servicio SMTP alternativo de contingencia", -150, 5, 8, "Servidor SMTP Contingencia"),
            ("📲 Notificar a los compradores mediante un mensaje SMS", -40, 2, 3, "Notificación SMS Masiva"),
            ("🤐 Dejar que los clientes pregunten por el estado de sus compras", 0, -15, -15, "Inacción Correo"),
        ],
    },
    {
        "titulo": "Deterioro de la Calidad por Subcontratación",
        "situacion": "El taller externo entregó un lote con costuras/acabados deficiente.",
        "opciones": [
            ("🔍 Inspeccionar y corregir cada pieza manualmente antes de vender", -200, 2, 10, "Control y Corrección Manual"),
            ("🏷️ Vender el lote como mercancía de segunda selección con descuento", -50, 5, -5, "Segunda Selección Descuento"),
            ("📦 Despachar los productos defectuosos a precio normal", 0, -25, -30, "Despacho Defectuoso"),
        ],
    },
    {
        "titulo": "Demanda por Accidente de Trabajo",
        "situacion": "Un colaborador sufrió una caída por un cable suelto en la oficina.",
        "opciones": [
            ("🏥 Cubrir los gastos médicos completos e indemnización justa", -300, 0, 15, "Indemnización Médica Completa"),
            ("⚖️ Dejar el asunto en manos del seguro social básico", -80, 0, -5, "Gestión Seguro Básico"),
            ("🙅‍♂️ Negar responsabilidad argumentando negligencia del trabajador", 0, -5, -25, "Negación Responsabilidad Accidente"),
        ],
    },
    {
        "titulo": "Cierre del Canal de Pagos Digital Preferido",
        "situacion": "La aplicación de cobros móviles más usada en el país sufrió una intervención.",
        "opciones": [
            ("💳 Migrar de urgencia e integrar 2 alternativas de cobro web", -220, 12, 5, "Integración Urgente Alternativas"),
            ("🏦 Pedir pagos por transferencia bancaria directa", 0, -5, -2, "Transferencias Directas"),
            ("🛑 Suspender ventas hasta que reabra la plataforma principal", 0, -25, -15, "Suspensión Temporal Ventas"),
        ],
    },
    {
        "titulo": "Robo de Mercancía en Depósito",
        "situacion": "Sujetos desconocidos sustrajeron el 20% del stock acumulado.",
        "opciones": [
            ("🛡️ Reponer la mercancía e instalar cámaras de alta seguridad", -350, 0, 10, "Reposición y Cámaras"),
            ("📋 Presentar la denuncia y esperar los resultados policiales", -50, -8, -2, "Denuncia Policial"),
            ("🙈 Disimular la falta de stock cancelando pedidos al azar", 0, -20, -20, "Cancelación Pedidos Azar"),
        ],
    },
    {
        "titulo": "Desacuerdo entre Inversionistas y Fundadores",
        "situacion": "Los socios exigen recortar el gasto en calidad para aumentar dividendos.",
        "opciones": [
            ("🧠 Presentar una defensa técnica del valor del cliente a largo plazo", -100, 5, 12, "Defensa Técnica Valor"),
            ("🤝 Ceder parcialmente recortando un 5% de la inversión en empaque", -50, -2, -2, "Recorte Parcial Calidad"),
            ("📉 Aceptar todos los recortes exigidos para evitar conflictos", 0, -15, -20, "Recorte Total Exigido"),
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

    # Se seleccionan exactamente 6 preguntas al azar para cada partida de los bancos de 50
    if modo == "Fácil":
        st.session_state.preguntas_juego = random.sample(BANCO_FACIL, 6)
    else:
        st.session_state.preguntas_juego = random.sample(BANCO_DIFICIL, 6)


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

    # Renderizado de Pregunta Actual (hasta 6 preguntas elegidas de entre las 50)
    if not game_over and fase_actual < 6:
        datos = st.session_state.preguntas_juego[fase_actual]
        badge_class = "question-badge badge-hard" if st.session_state.modo_dificultad == "Difícil" else "question-badge"

        st.markdown(
            f"""
            <div class="question-card">
                <span class="{badge_class}">PASO {fase_actual + 1} DE 6 • MODO {st.session_state.modo_dificultad.upper()}</span>
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
    elif game_over or fase_actual >= 6:
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
    if game_over or fase_actual >= 6:
        if st.button("🔄 Jugar Otra Vez / Cambiar Modo", use_container_width=True):
            st.session_state.clear()
            st.rerun()