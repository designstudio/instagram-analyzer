import streamlit as st
import instaloader
import re

st.set_page_config(page_title="Análise de Post", layout="centered")
st.title("📊 Analisador de Performance de Post do Instagram")

def extract_shortcode(url):
    match = re.search(r"instagram\.com/p/([A-Za-z0-9_-]+)/?", url)
    return match.group(1) if match else url

post_input = st.text_input("Cole o link do post ou apenas o shortcode:")

if post_input:
    shortcode = extract_shortcode(post_input)
    try:
        st.info("🔍 Buscando dados públicos do post...")

        L = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        likes = post.likes
        comments = post.comments
        followers = post.owner_profile.followers

        engagement = ((likes + comments) / followers) * 100 if followers > 0 else 0

        st.success("✅ Dados encontrados com sucesso!")
        st.markdown(f"**👤 Perfil:** `{post.owner_username}`")
        st.markdown(f"**❤️ Curtidas:** `{likes}`")
        st.markdown(f"**💬 Comentários:** `{comments}`")
        st.markdown(f"**👥 Seguidores:** `{followers}`")

        st.markdown("---")
        st.markdown("### 📈 Taxa de Engajamento")
        st.metric("Engajamento", f"{engagement:.2f}%")

        if engagement >= 5:
            st.success("🔥 Alto engajamento! Post de destaque.")
        elif engagement >= 2:
            st.info("👍 Bom engajamento. Post está performando bem.")
        else:
            st.warning("📉 Engajamento baixo. Reavalie conteúdo e timing.")

    except Exception as e:
        st.error(f"❌ Erro ao buscar os dados: {e}")
