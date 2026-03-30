import streamlit as st
from server import start_server, stop_server, is_server_running
from config import MEU_NOME, TAILSCALE_IPS, MINECRAFT_PORT

st.set_page_config(page_title="Minecraft Server", page_icon="🎮")

st.title("🎮 Servidor de Minecraft")

# status
running = is_server_running()

if running:
    meu_ip = TAILSCALE_IPS.get(MEU_NOME, "?")
    st.success("🟢 Servidor **online**")
    st.code(f"{meu_ip}:{MINECRAFT_PORT}", language=None)
else:
    st.error("🔴 Servidor **offline**")

st.divider()

# ip fo grupo
with st.expander("📋 IPs Tailscale do grupo"):
    for nome, ip in TAILSCALE_IPS.items():
        st.code(f"{nome}: {ip}:{MINECRAFT_PORT}", language=None)

st.divider()

# logs
log_area = st.empty()
logs = []

def log(msg):
    logs.append(msg)
    log_area.text("\n".join(logs))

# botões
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Ligar servidor", disabled=running, use_container_width=True):
        with st.spinner("Iniciando..."):
            ok = start_server(log)
        if ok:
            st.success("Servidor no ar! Recarregue a página para atualizar o status.")
        else:
            st.error("Algo deu errado. Veja os logs acima.")

with col2:
    if st.button("⏹️ Desligar servidor", disabled=not running, use_container_width=True):
        with st.spinner("Encerrando e salvando mundo..."):
            stop_server(log)
        st.success("Servidor encerrado e mundo salvo!")

st.divider()
st.caption("Recarregue a página para atualizar o status.")