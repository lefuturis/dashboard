import streamlit as st
from pyodk.client import Client
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
import folium
from streamlit_folium import st_folium
import plotly.express as px





def app():
    def get_marker_color(score):
        if score <= 50.9:
            return "red"
        elif 51 <= score <= 60.9:
            return "orange"
        elif 61 <= score <= 80: 
            return "beige"  # ou "lightblue" ou "cadetblue" selon préférence
        elif 81 <= score <= 100:
            return "green"
        else:
            return "gray"  # au cas où la valeur est hors intervalle

    col1,col2 = st.columns([1.5,4])
    with Client(config_path="config.toml", cache_path="cache.toml",project_id=3) as client:
        epvg_json = client.submissions.get_table(form_id="form_eva_epvg")
        df = pd.json_normalize(data=epvg_json["value"], sep="/")
        df["pourcentage_score"] = (df["total_score"].astype(int) / 1228) * 100
        df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['localisation/coordinates'].tolist(), index=df.index)
        pd.set_option('display.max_columns', None)
    with col1:
        province = st.multiselect(
            "🌐 Sélectionnez la province",
            options=df["province_etablissement"].dropna().unique(),
            default=df["province_etablissement"].dropna().unique()
            )

        ville = st.multiselect(
            "🌏 Sélectionnez la ville",
            options=df["ville_etablissement"].dropna().unique(),
            default=df["ville_etablissement"].dropna().unique()
         )

        forme = st.multiselect(
            "📄 Sélectionnez la forme juridique",
            options=df["forme_juridique"].dropna().unique(),
            default=df["forme_juridique"].dropna().unique()
            )

        # Filtrage du DataFrame
        df_selection = df.query(
            "province_etablissement == @province and ville_etablissement == @ville and forme_juridique == @forme "
        )
         # Create a donut chart
        epvg_inf_50 = int(df_selection[df_selection["pourcentage_score"] <= 50.9].shape[0])
        epvg_51_60 = int(df_selection[df_selection["pourcentage_score"].between(51, 60.9)].shape[0])
        epvg_61_80 = int(df_selection[df_selection["pourcentage_score"].between(61, 80)].shape[0])
        epvg_81_100 = int(df_selection[df_selection["pourcentage_score"].between(81, 100)].shape[0])
        #Données résumées
        donnees = {
            "Tranche de score": [
                "≤ 50%",
                "51% - 60%",
                "61% - 80%",
                "81% - 100%"
            ],
            "Nombre d'EPVG": [
                epvg_inf_50,
                epvg_51_60,
                epvg_61_80,
                epvg_81_100
            ]
        }

        df_donut = pd.DataFrame(donnees)

        # Création du donut chart
        fig = px.pie(
            df_donut,
            values="Nombre d'EPVG",
            names="Tranche de score",
            title="Répartition des EPVG par tranche de score",
            hole=0.4  # ⭕ forme d'anneau
        )

        # Mise en forme
        fig.update_layout(
            width=800,
            height=500,
            font=dict(size=14, color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend_title_text="Tranches"
        )

        # Affichage
        st.plotly_chart(fig, use_container_width=True)
       
    with col2:
       
        with st.expander("AFFICHAGE DES DONNEES"):
            showData=st.multiselect('Filter: ',df_selection.columns)
            st.dataframe(df_selection[showData],use_container_width=True)
                    # Calcul des métriques à partir de df_selection
        total_epvg = int(df_selection.shape[0])
        epvg_inf_50 = int(df_selection[df_selection["pourcentage_score"] <= 50.9].shape[0])
        epvg_51_60 = int(df_selection[df_selection["pourcentage_score"].between(51, 60.9)].shape[0])
        epvg_61_80 = int(df_selection[df_selection["pourcentage_score"].between(61, 80)].shape[0])
        epvg_81_100 = int(df_selection[df_selection["pourcentage_score"].between(81, 100)].shape[0])

            # Affichage dans 5 colonnes
        col1, col2, col3, col4, col5 = st.columns(5, gap='small')

        with col1:
            st.metric(label="💊 Total EPVG", value=total_epvg)

        with col2:
            st.metric(label="🔴 EPVG Score < 50", value=epvg_inf_50)

        with col3:
            st.metric(label="🟡 EPVG Score 51–60", value=epvg_51_60)

        with col4:
            st.metric(label="🟠 EPVG Score 61–80", value=epvg_61_80)

        with col5:
            st.metric(label="🟢 EPVG Score 81–100", value=epvg_81_100)
        style_metric_cards(background_color="#393939",border_left_color="#686664",border_color="#000000",box_shadow="#F71938")
        # Affichage de la carte
        map = folium.Map(location=[-10.5, 26.5], zoom_start=5, scrollWheelZoom=False, tiles='CartoDB positron')
        choropleth = folium.Choropleth(geo_data='cd.json',highlight=True,line_opacity=0.8).add_to(map)
        
        for _, row in df_selection.iterrows():
            if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
                folium.Marker(
                    location=[row['longitude'], row['latitude']],
                    popup=folium.Popup(
                        f"Nom: {row['nom_etablissement']}<br>"
                        f"Score: {row['pourcentage_score']:.2f}%", max_width=300),
                    icon=folium.Icon(color=get_marker_color(row['pourcentage_score']), icon="info-sign")
                ).add_to(map)

        st_folium(map, width=1100, height=500)
