import streamlit as st
from server import start_server, stop_server, is_server_running
from config import MEU_NOME, TAILSCALE_IPS, MINECRAFT_PORT

st.set_page_config(page_title="Minecraft Server", page_icon="🎮")

st.title("🎮 Minecraft Server")

# status
running = is_server_running()

if running:
    meu_ip = TAILSCALE_IPS.get(MEU_NOME, "?")
    st.success("🟢 Server **online**")
    st.code(f"{meu_ip}:{MINECRAFT_PORT}", language=None)
else:
    st.error("🔴 Server **offline**")

st.divider()

# ip fo grupo
with st.expander("📋 Tailscale IPs from the group"):
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
    if st.button("▶️ Start server", disabled=running, use_container_width=True):
        with st.spinner("Starting..."):
            ok = start_server(log)
        if ok:
            st.success("Server is running! Reload the page to update the status.")
        else:
            st.error("Something went wrong. See the logs above.")

with col2:
    if st.button("⏹️ Stop server", disabled=not running, use_container_width=True):
        with st.spinner("Stopping and saving world..."):
            stop_server(log)
        st.success("Server stopped and world saved!")

st.divider()
st.caption("Reload the page to update the status.")