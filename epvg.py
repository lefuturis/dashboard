import streamlit as st
from pyodk.client import Client
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
from PIL import Image
from io import BytesIO
import requests
from datetime import datetime, timezone
from dateutil import parser
import numpy as np
import plotly.express as px

ODK_DOMAIN = "https://odk.arccsu.gouv.cd"
EMAIL = "support@arccsu.gouv.cd"
PASSWORD = "@rc-csu10?Odk"

# Authentifier et obtenir le token
def get_odk_headers():
    if (
        "odk_token" in st.session_state and
        "odk_token_expiry" in st.session_state
    ):
        expiry = parser.isoparse(st.session_state["odk_token_expiry"])  # convertit ISO 8601 → datetime aware
        if datetime.now(timezone.utc) < expiry:
            return {"Authorization": f"Bearer {st.session_state['odk_token']}"}

    # Authentification si aucun token valide
    response = requests.post(
        f"{ODK_DOMAIN}/v1/sessions",
        json={"email": EMAIL, "password": PASSWORD}
    )

    if response.status_code == 200:
        data = response.json()
        st.session_state["odk_token"] = data["token"]
        st.session_state["odk_token_expiry"] = data["expiresAt"]
        return {"Authorization": f"Bearer {data['token']}"}
    else:
        st.error(f"Erreur d'authentification : {response.status_code}")
        return None

def build_image_url(instance_id, image_filename, form_id, project_id):
    base_url = "https://odk.arccsu.gouv.cd"
    return f"{base_url}/v1/projects/{project_id}/forms/{form_id}/submissions/{instance_id}/attachments/{image_filename}"

def app():
    col1,col2 = st.columns([1.5,4])
    with Client(config_path="config.toml", cache_path="cache.toml",project_id=3) as client:
        epvg_json = client.submissions.get_table(form_id="form_eva_epvg")
        df = pd.json_normalize(data=epvg_json["value"], sep="/")
        df.columns = [col.split("/")[-1] for col in df.columns]
        df["pourcentage_score"] = (df["total_score"].astype(float) / 1230) * 100
        df["Organisation et gestion"] = (df["score_organisation_et_gestion"].astype(float) / 20) * 100
        df["Gestion de la qualité"] = (df["score_gestion_de_la_qualite"].astype(float) / 96) * 100
        df["Gestion du risque qualité"] = (df["score_gestion_du_risque_qualite"].astype(float) / 15) * 100
        df["Revue de la direction"] = (df["score_revue_de_la_direction"].astype(float) / 25) * 100
        df["Réclamations"] = (df["score_reclamations"].astype(float) / 30) * 100
        df["Produits retournés"] = (df["score_produits_retournes"].astype(float) / 40) * 100
        df["Rappels"] = (df["score_rappels"].astype(float) / 45) * 100
        df["Auto-inspections"] = (df["score_auto_inspections"].astype(float) / 20) * 100
        df["Audits / inspections antérieures"] = (df["score_audits_inspections_anterieures"].astype(float) / 20) * 100
        df["Locaux"] = (df["score_locaux"].astype(float) / 504) * 100
        df["Contrôle de rotation du stock"] = (df["score_controle_rotation_stock"].astype(float) / 25) * 100
        df["Équipements"] = (df["score_equipements"].astype(float) / 25) * 100
        df["Qualification et validation"] = (df["score_qualification_et_validation"].astype(float) / 25) * 100
        df["Personnels"] = (df["score_personnels"].astype(float) / 115) * 100
        df["Documentation"] = (df["score_documentation"].astype(float) / 75) * 100
        df["Activités et opérations"] = (df["score_activites_et_operations"].astype(float) / 110) * 100
        df["Activités externalisées"] = (df["score_activites_externalisees"].astype(float) / 15) * 100
        df["Produits de qualité inférieure et falsifiés"] = (df["score_produits_qualite_inferieure_et_falsifies"].astype(float) / 25) * 100


        pd.set_option('display.max_columns', None)
    with col1:
        # 1. Sélection unique de la province
        province = st.selectbox(
            "🌐 Sélectionnez la province",
            options=sorted(df["province_etablissement"].dropna().unique())
        )

        # 2. Filtrer le DataFrame pour n’afficher que les villes de la province sélectionnée
        villes_disponibles = df[df["province_etablissement"] == province]["ville_etablissement"].dropna().unique()
        ville = st.selectbox(
            "🌏 Sélectionnez la ville",
            options=sorted(villes_disponibles)
        )

        # 3. Filtrer le DataFrame pour les établissements dans la province et la ville sélectionnées
        etabs_disponibles = df[(df["province_etablissement"] == province) & (df["ville_etablissement"] == ville)]["nom_etablissement"].dropna().unique()
        etablissement = st.selectbox(
            "🏥 Sélectionnez l’établissement",
            options=sorted(etabs_disponibles)
        )
        # Filtrage du DataFrame
        df_selection = df.query(
            "province_etablissement == @province and ville_etablissement == @ville and nom_etablissement == @etablissement")
        global_avg = np.average(df["pourcentage_score"])
        current_avg = np.average(df_selection["pourcentage_score"])
        delta = current_avg - global_avg
        st.subheader("Score global de l’établissement")
        st.metric(
            label=f"Score de {etablissement} (%)",
            value=f"{current_avg:,.2f}%",
            delta=f"{delta:+.2f}%",
            help="Comparé à la moyenne",
            delta_color="normal"  # normal si le sous-groupe est au-dessus
        )
        style_metric_cards(background_color="#393939",border_left_color="#686664",border_color="#000000",box_shadow="#F71938")
        with st.expander("⬇ COMMENTAIRES SUR LE RESRÉSULTAT ⬇",expanded=True):
                st.write(f'''
                - :orange[**Organisation et gestion**]: {df_selection["commentaire_organisation_et_gestion"].values[0]}
                - :orange[**Gestion de la qualité**]: {df_selection["commentaire_gestion_de_la_qualite"].values[0]}
                - :orange[**Gestion du risque qualité**]: {df_selection["commentaire_gestion_du_risque_qualite"].values[0]}
                - :orange[**Revue de la direction**]: {df_selection["commentaire_revue_de_la_direction"].values[0]}
                - :orange[**Réclamations**]: {df_selection["commentaire_reclamations"].values[0]}
                - :orange[**Produits retournés**]: {df_selection["commentaire_produits_retournes"].values[0]}
                - :orange[**Rappels**]: {df_selection["commentaire_rappels"].values[0]}
                - :orange[**Auto-inspections**]: {df_selection["commentaire_auto_inspections"].values[0]}
                - :orange[**Audits / inspections antérieures**]: {df_selection["commentaire_inspections_anterieures"].values[0]}
                - :orange[**Locaux**]: {df_selection["commentaire_locaux"].values[0]}
                - :orange[**Contrôle de rotation du stock**]: {df_selection["commentaire_controle_rotation_stock"].values[0]}
                - :orange[**Équipements**]: {df_selection["commentaire_equipements"].values[0]}
                - :orange[**Qualification et validation**]: {df_selection["commentaire_qualification_et_validation"].values[0]}
                - :orange[**Personnels**]: {df_selection["commentaire_personnels"].values[0]}
                - :orange[**Documentation**]: {df_selection["commentaire_documentation"].values[0]}
                - :orange[**Activités et opérations**]: {df_selection["commentaire_activites_et_operations"].values[0]}
                - :orange[**Activités externalisées**]: {df_selection["commentaire_activites_externalisees"].values[0]}
                - :orange[**Produits de qualité inférieure et falsifiés**]: {df_selection["commentaire_produits_qualite_inferieure_et_falsifies"].values[0]}
                ''')


    with col2:
        def afficher_image_encadree(colonne, titre, filename):
            image_url = build_image_url(
                instance_id=df_selection["__id"].values[0],
                image_filename=filename,
                form_id="form_eva_epvg",
                project_id=3
            )
            headers = get_odk_headers()
            response = requests.get(image_url, headers=headers)

            with colonne:
                st.markdown(f"""
                    <div style="border:1px solid #ccc; padding:10px; border-radius:10px; margin-bottom:10px;">
                        <p style="text-align:center; font-weight:bold;">{titre}</p>
                """, unsafe_allow_html=True)

                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    st.image(image, width=300)
                else:
                    st.error(f"Erreur d'accès à l'image : {response.status_code}")

                st.markdown("</div>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        # Affichage des 4 photos avec encadrement
        afficher_image_encadree(col1, "Photo de face", df_selection["photo_face"].values[0])
        afficher_image_encadree(col2, "Zone de réception", df_selection["photo_zs_reception"].values[0])
        afficher_image_encadree(col3, "Zone de préparation", df_selection["photo_zs_preparation"].values[0])
        afficher_image_encadree(col4, "Zone de quarantaine", df_selection["photo_zs_quarantaine"].values[0])

                # Sélection manuelle des colonnes lisibles (créées précédemment)
        # Colonnes avec les scores en pourcentage (précédemment créées)
        colonnes_scores_pourcentages = [
            "Organisation et gestion",
            "Gestion de la qualité",
            "Gestion du risque qualité",
            "Revue de la direction",
            "Réclamations",
            "Produits retournés",
            "Rappels",
            "Auto-inspections",
            "Audits / inspections antérieures",
            "Locaux",
            "Contrôle de rotation du stock",
            "Équipements",
            "Qualification et validation",
            "Personnels",
            "Documentation",
            "Activités et opérations",
            "Activités externalisées",
            "Produits de qualité inférieure et falsifiés"
        ]

        # Extraire les pourcentages pour le premier établissement
        data_scores = df_selection[colonnes_scores_pourcentages].iloc[0]

        # Convertir en DataFrame
        dist = pd.DataFrame({
            "Critère": data_scores.index,
            "Pourcentage obtenu": data_scores.values
        })

        # Trier du plus grand au plus petit
        dist = dist.sort_values(by="Pourcentage obtenu", ascending=False)

        # Formater les pourcentages avec une décimale pour affichage
        dist["Pourcentage"] = dist["Pourcentage obtenu"].map(lambda x: f"{x:.1f}")

        # Créer le graphique
        fig = px.bar(
            dist,
            x="Critère",
            y="Pourcentage obtenu",
            text="Pourcentage",
            title="Pourcentage obtenu par critère",
            orientation="v"
        )
            # Mise en forme du graphique
        fig.update_traces(
            textposition="outside",
            textfont=dict(
                color="white",
                size=12,
                family="Arial",
            )
        )
        # Mise en forme du graphique
        fig.update_layout(
            height=600,
            xaxis_title="Critères",
            yaxis_title="Pourcentage (%)",
            
            # ✅ Mise en forme du titre de l'axe X
            xaxis_title_font=dict(
                size=16,
                color="black",
                family="Arial Black"  # police grasse
            ),
            
            # ✅ Mise en forme du titre de l'axe Y
            yaxis_title_font=dict(
                size=14,
                color="black",
                family="Arial"
            ),
            
            # ✅ Mise en forme générale
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="black", size=13, family="Arial"),
            
            xaxis=dict(showgrid=True, gridcolor='#cecdcd', tickangle=45),
            yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
            margin=dict(l=40, r=30, t=80, b=120)
        )


        # Afficher dans Streamlit
        st.plotly_chart(fig, use_container_width=True)
