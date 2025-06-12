import streamlit as st
import instaloader
import pandas as pd
import re
from io import StringIO

st.set_page_config(page_title="Campanha Instagram", layout="centered")
st.title("📊 Análise de Performance de Campanha no Instagram")

st.markdown("Cole até 10 links de posts públicos abaixo (um por linha):")

def extract_shortcode(url):
    match = re.search(r"instagram\.com/p/([A-Za-z0-9_-]+)/?", url)
    return match.group(1) if match else url.strip()

posts_input = st.text_area("Links dos posts:", height=200)

if posts_input:
    try:
        L = instaloader.Instaloader()
        total_likes = 0
        total_comments = 0
        total_followers = 0
        usernames = set()
        post_data = []

        post_links = posts_input.strip().splitlines()
        for i, url in enumerate(post_links):
            shortcode = extract_shortcode(url)
            post = instaloader.Post.from_shortcode(L.context, shortcode)

            likes = post.likes
            comments = post.comments
            username = post.owner_username
            link = f"https://www.instagram.com/p/{shortcode}/"

            # Captura seguidores apenas do primeiro post
            if i == 0:
                total_followers = post.owner_profile.followers

            total_likes += likes
            total_comments += comments
            usernames.add(username)

            post_data.append({
                "Shortcode": shortcode,
                "Link do Post": link,
                "Curtidas": likes,
                "Comentários": comments,
                "Usuário": username,
                "Seguidores": total_followers
            })

        total_engagement = ((total_likes + total_comments) / total_followers) * 100 if total_followers > 0 else 0

        st.success("✅ Análise concluída!")

        st.markdown(f"**👤 Perfil:** `{', '.join(usernames)}`")
        st.markdown(f"**📸 Total de Posts:** `{len(post_links)}`")
        st.markdown(f"**❤️ Curtidas Totais:** `{total_likes}`")
        st.markdown(f"**💬 Comentários Totais:** `{total_comments}`")
        st.markdown(f"**👥 Seguidores:** `{total_followers}`")

        st.markdown("---")
        st.markdown("### 📈 Engajamento da Campanha")
        st.metric("Engajamento Total", f"{total_engagement:.2f}%")

        if total_engagement >= 5:
            st.success("🔥 Ótimo engajamento! A campanha performou muito bem.")
        elif total_engagement >= 2:
            st.info("👍 Engajamento razoável. Boa visibilidade.")
        else:
            st.warning("📉 Engajamento abaixo do ideal. Reavalie a estratégia de conteúdo.")

        # CSV export
        df = pd.DataFrame(post_data)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        st.markdown("---")
        st.download_button(
            label="⬇️ Baixar CSV com dados da campanha",
            data=csv_data,
            file_name="dados_campanha_instagram.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Erro ao processar os posts: {e}")
