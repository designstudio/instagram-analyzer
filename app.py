import streamlit as st
import instaloader
import pandas as pd
import re
import os

st.set_page_config(page_title="Instagram Post Analyzer", layout="centered")
st.title("📊 Analisador de Post do Instagram")

def extract_shortcode(url):
    m = re.search(r"instagram\.com/p/([A-Za-z0-9_-]+)/?", url)
    return m.group(1) if m else url

post_input = st.text_input("Link ou shortcode:")

if post_input:
    sc = extract_shortcode(post_input)
    try:
        L = instaloader.Instaloader()
        L.login(os.environ["IG_USER"], os.environ["IG_PASS"])
        post = instaloader.Post.from_shortcode(L.context, sc)

        st.success("✅ Dados carregados com sucesso!")
        st.markdown(f"**Autor:** `{post.owner_username}` • ❤️ {post.likes} • 💬 {post.comments} • 👥 {post.owner_profile.followers}")

        comments = [{"Usuário": c.owner.username, "Comentário": c.text, "Data": c.created_at_utc.strftime("%Y-%m-%d %H:%M:%S")}
                    for c in post.get_comments()]
        if comments:
            df = pd.DataFrame(comments)
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Baixar CSV", csv, file_name=f"{sc}_comments.csv", mime="text/csv")
        else:
            st.warning("Sem comentários.")

    except Exception as e:
        st.error(f"❌ Erro: {e}")
