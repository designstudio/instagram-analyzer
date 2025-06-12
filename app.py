import streamlit as st
import instaloader
import pandas as pd
import re
import os

# CONFIGURAÇÕES DA PÁGINA
st.set_page_config(page_title="Instagram Post Analyzer", layout="centered")
st.title("📊 Analisador de Post do Instagram")

# EXTRAI O SHORTCODE DO LINK
def extract_shortcode(url):
    match = re.search(r"instagram\.com/p/([A-Za-z0-9_-]+)/?", url)
    return match.group(1) if match else url

# ENTRADA DO USUÁRIO
post_input = st.text_input("Cole o link do post ou apenas o shortcode (ex: DKPS0vitjSq):", "")

if post_input:
    shortcode = extract_shortcode(post_input)
    try:
        st.info("🔍 Conectando ao Instagram...")

        # LOGIN USANDO SEGREDOS DO STREAMLIT
        L = instaloader.Instaloader()
        L.login(st.secrets["IG_USER"], st.secrets["IG_PASS"])

        st.info("📥 Buscando dados do post...")
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # MOSTRA OS DADOS DO POST
        st.success("✅ Dados coletados com sucesso!")
        st.markdown(f"**📌 Dono do post:** `{post.owner_username}`")
        st.markdown(f"**❤️ Curtidas:** `{post.likes}`")
        st.markdown(f"**💬 Comentários:** `{post.comments}`")
        st.markdown(f"**👥 Seguidores do perfil:** `{post.owner_profile.followers}`")

        # COLETA E EXIBE COMENTÁRIOS
        comments_data = []
        for comment in post.get_comments():
            comments_data.append({
                "Usuário": comment.owner.username,
                "Comentário": comment.text,
                "Data": comment.created_at_utc.strftime("%Y-%m-%d %H:%M:%S")
            })

        if comments_data:
            df = pd.DataFrame(comments_data)
            st.markdown("### 💾 Comentários extraídos:")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Baixar CSV",
                data=csv,
                file_name=f"comentarios_{shortcode}.csv",
                mime='text/csv',
            )
        else:
            st.warning("Este post não possui comentários.")

    except Exception as e:
        st.error(f"❌ Erro ao buscar o post: {str(e)}")
