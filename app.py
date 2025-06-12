import streamlit as st
import instaloader
import pandas as pd
import re

st.set_page_config(page_title="Instagram Post Analyzer", layout="centered")
st.title("📊 Analisador de Post do Instagram (sem login)")

def extract_shortcode(url):
    match = re.search(r"instagram\.com/p/([A-Za-z0-9_-]+)/?", url)
    return match.group(1) if match else url

post_input = st.text_input("Cole o link do post ou o shortcode:", "")

if post_input:
    shortcode = extract_shortcode(post_input)
    try:
        st.info("🔍 Buscando dados do post...")
        L = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        st.success("✅ Dados coletados com sucesso!")
        st.markdown(f"**📌 Dono do post:** `{post.owner_username}`")
        st.markdown(f"**❤️ Curtidas:** `{post.likes}`")
        st.markdown(f"**💬 Comentários:** `{post.comments}`")
        st.markdown(f"**👥 Seguidores do perfil:** `{post.owner_profile.followers}`")

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
            st.warning("Nenhum comentário disponível.")
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")
