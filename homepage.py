import streamlit as st
from streamlit_option_menu import option_menu
import liste_prix, accueil, data, epvg
import streamlit_authenticator as stauth
import yaml 
from yaml.loader import SafeLoader

st.set_page_config(page_title="ARC CSU ANALYTICS",page_icon="🌍", layout="wide")
with open('credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['key'],
    config['cookie']['name'],
    config['cookie']['expiry_days'],
)

authenticator.login(location="main")
if st.session_state.get("authentication_status"):
    # Configuration de la page
    
    st.header("EVALUATION DES ETABLISSEMENTS PHARMACEUTIQUES DE VENTE EN GROS (EPVG)")
    theme_plotly = None 
    # load Style css
    with open('style.css')as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

    class MultiApp:

        def __init__(self):
            self.apps = []

        def add_app(self, title, func):
            self.apps.append({
                "title": title,
                "function": func
            })

        def run(self):
            with st.sidebar:
                st.sidebar.image("images/logo_arccsu.png", width=200)
                app = option_menu(
                    menu_title="ANALYTICS",
                    options=["Accueil", "Évaluation", "Données", "Tarifs"],
                    icons=["house", "hospital", "file-medical", "patch-question"],
                    menu_icon="bar-chart",
                    default_index=0,
                )
                st.subheader("version 1.0")
                authenticator.logout("Se déconnecter","sidebar")

            # Appels des modules en fonction de la sélection
            if app == "Accueil":
                accueil.app()
            elif app == "Évaluation":
                epvg.app()
            elif app == "Données":
                data.app()
            elif app == "Tarifs":
                liste_prix.app()


    # ✅ Instanciation et exécution
    app_instance = MultiApp()
    app_instance.run()
elif st.session_state.get("authentication_status") is False:
    st.error("Nom d’utilisateur ou mot de passe incorrect.")
elif st.session_state.get("authentication_status") is None:
    st.warning("Veuillez entrer vos identifiants.")