import streamlit as st
from pyodk.client import Client
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards


def app():
    col1,col2 = st.columns([1.5,5])
    with Client(config_path="config.toml", cache_path="cache.toml",project_id=3) as client:
        cs_json = client.submissions.get_table(form_id="form_eva_epvg_tarif")
        dfb = pd.json_normalize(cs_json['value'],sep='-')
        pd.set_option('display.max_columns', None)
        dfb = dfb.set_index('__id')
        repeat_df = client.submissions.get_table(form_id="form_eva_epvg_tarif",table_name="Submissions.info_produit")
        dfr = pd.json_normalize(repeat_df['value'],sep='-')
        join_df = dfr.join(other=dfb, on='__Submissions-id')
        dfp = pd.read_csv("csv_produit.csv", sep=";")
        dfp.rename(columns={"name": "produit"}, inplace=True)
        df = join_df.merge(dfp[['produit', 'label']], on='produit', how='left')
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
            fabricant = st.multiselect(
                "🌏 Sélectionnez le fabricant",
                options=df["fabricant"].dropna().unique(),
                default=[df["fabricant"].dropna().unique()[0]]
            )

            pays = st.multiselect(
                "🌏 Sélectionnez le pays d'origine",
                options=df["pays_origine"].dropna().unique(),
                default=[df["pays_origine"].dropna().unique()[0]]
            )

            


            label = st.selectbox(
                "📄 Sélectionnez le produit",
                options=df["label"].dropna().unique()
                )

            # Filtrage du DataFrame
            df_selection = df.query(
                "province_etablissement == @province and ville_etablissement == @ville and pays_origine == @pays and label == @label and fabricant == @fabricant"
            )
        
    with col2:
        

            prix_max = df_selection['pv'].max()
            prix_min = df_selection['pv'].min()
            prix_moyen = df_selection['pv'].mean()
            prix_ecart_type = df_selection['pv'].std()


                # Affichage dans 4 colonnes
            col1, col2, col3, col4 = st.columns(4, gap='small')

            with col1:
                st.metric(label="💊 Prix max", value=prix_max)

            with col2:
                st.metric(label="💊 Prix min", value=prix_min)

            with col3:
                st.metric(label="💊 Prix moyen", value=prix_moyen)

            with col4:
                st.metric(label="💊 Ecart type", value=prix_ecart_type)
            style_metric_cards(background_color="#393939",border_left_color="#686664",border_color="#000000",box_shadow="#F71938")
            # Affichage de la carte
            with st.expander("AFFICHAGE DES DONNEES"):
                showData=st.multiselect('Filter: ',df_selection.columns,default=['province_etablissement','ville_etablissement','nom_etablissement','pays_origine','fabricant','label','pv'])
                st.dataframe(df_selection[showData],use_container_width=True,hide_index=True)