import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Startup Life", page_icon="🚀", layout="centered")

st.title("🚀 Startup Life: Simulador de Emprendimiento")
st.write(
    "Toma decisiones estratégicas para hacer crecer tu empresa o llevarla a la quiebra."
)

# Inicializar variables en la sesión del usuario
if "dinero" not in st.session_state:
    st.session_state.dinero = 1500
    st.session_state.clientes = 10
    st.session_state.reputacion = 50
    st.session_state.fase = 1
    st.session_state.game_over = False
    st.session_state.mensaje = ""

# Mostrar indicadores visuales
col1, col2, col3 = st.columns(3)
col1.metric("💰 Capital", f"${st.session_state.dinero}")
col2.metric("👥 Clientes", st.session_state.clientes)
col3.metric("⭐ Reputación", f"{st.session_state.reputacion}/100")

st.divider()

# Verificar condiciones de quiebra
if st.session_state.dinero <= 0:
    st.error("❌ ¡QUIEBRA TÉCNICA! Te quedaste sin flujo de caja operativo.")
    st.session_state.game_over = True
elif st.session_state.reputacion <= 0:
    st.error("❌ ¡CRISIS DE MARCA! Perdiste la confianza del mercado.")
    st.session_state.game_over = True

# --- FASE 1 ---
if st.session_state.fase == 1 and not st.session_state.game_over:
    st.subheader("Fase 1: Lanzamiento del Producto")
    st.write("Tienes $1,500 de ahorros. ¿Cómo vas a salir al mercado?")

    if st.button(
        "1. Producto Mínimo Viable (PMV) básico ($500)", use_container_width=True
    ):
        st.session_state.dinero -= 500
        st.session_state.clientes += 15
        st.session_state.reputacion += 10
        st.session_state.fase = 2
        st.rerun()

    if st.button(
        "2. Lanzar el producto 'perfecto' e impecable ($1,400)",
        use_container_width=True,
    ):
        st.session_state.dinero -= 1400
        st.session_state.clientes += 40
        st.session_state.reputacion += 25
        st.session_state.fase = 2
        st.rerun()

# --- FASE 2 ---
elif st.session_state.fase == 2 and not st.session_state.game_over:
    st.subheader("Fase 2: Estrategia de Crecimiento")
    st.write("Necesitas más usuarios. ¿Qué estrategia de marketing aplicas?")

    if st.button(
        "1. Invertir en pauta y anuncios digitales ($600)",
        use_container_width=True,
    ):
        st.session_state.dinero -= 600
        st.session_state.clientes += 50
        st.session_state.reputacion += 10
        st.session_state.fase = 3
        st.rerun()

    if st.button(
        "2. Marketing orgánico y alianzas sin costo ($0)",
        use_container_width=True,
    ):
        st.session_state.clientes += 10
        st.session_state.reputacion += 15
        st.session_state.fase = 3
        st.rerun()

# --- FASE 3 ---
elif st.session_state.fase == 3 and not st.session_state.game_over:
    st.subheader("Fase 3: Gestión de Crisis")
    st.write(
        "Un proveedor falló y el 20% de tus envíos llegaron defectuosos a los clientes."
    )

    if st.button(
        "1. Reembolsar e indemnizar de inmediato ($500)",
        use_container_width=True,
    ):
        st.session_state.dinero -= 500
        st.session_state.reputacion += 20
        st.session_state.fase = 4
        st.rerun()

    if st.button(
        "2. Ignorar reclamos y culpar a la empresa de envíos ($0)",
        use_container_width=True,
    ):
        st.session_state.reputacion -= 45
        st.session_state.clientes -= 20
        st.session_state.fase = 4
        st.rerun()

# --- RESULTADO FINAL ---
elif st.session_state.fase == 4 and not st.session_state.game_over:
    st.subheader("🏁 Resultado de tu Emprendimiento")
    if st.session_state.dinero >= 1000 and st.session_state.reputacion >= 60:
        st.balloons()
        st.success(
            "🏆 ¡ÉXITO TOTAL! Tu startup es rentable y lista para escalar."
        )
    elif st.session_state.dinero > 0 and st.session_state.reputacion >= 40:
        st.warning(
            "⚖️ ¡SOBREVIVISTE! Mantienes operación pero vives al día con las ventas."
        )
    else:
        st.error("📉 ¡FRACASO! Perdiste la confianza de los clientes.")

# Botón para reiniciar
if st.session_state.game_over or st.session_state.fase == 4:
    if st.button("🔄 Reiniciar juego", use_container_width=True):
        st.session_state.clear()
        st.rerun()