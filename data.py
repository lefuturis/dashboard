import streamlit as st
from pyodk.client import Client
import pandas as pd
from streamlit_slickgrid import (
    slickgrid,
    Formatters,
    Filters,
    FieldType,
    OperatorType,
    ExportServices,
    StreamlitSlickGridFormatters,
    StreamlitSlickGridSorters,
)
def app():
       with Client(config_path="config.toml", cache_path="cache.toml",project_id=3) as client:
        epvg_json = client.submissions.get_table(form_id="form_eva_epvg")
        df = pd.json_normalize(data=epvg_json["value"], sep="/")
        df.columns = [col.split("/")[-1] for col in df.columns]
        df["pourcentage_score"] = (df["total_score"].astype(float) / 1228) * 100
        df["Organisation et gestion"] = (df["score_organisation_et_gestion"].astype(float) / 18) * 100
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
        colonnes_pourcentages = [
                "__id",
                "province_etablissement",
                "ville_etablissement",
                "forme_juridique",
                "nom_etablissement",
                "pourcentage_score",
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
        # Création du DataFrame contenant uniquement ces colonnes
        df_pourcentages = df[colonnes_pourcentages]
        red = "#ff4b4b"
        orange = "#ffa421"
        yellow = "#ffe312"
        green = "#21c354"
        teal = "#00c0f2"
        blue = "#1c83e1"
        violet = "#803df5"
        white = "#fafafa"
        gray = "#808495"
        black = "#262730"

        columns = [
            {
                "id": "province_etablissement",
                "name": "Province Etablissement",
                "field": "province_etablissement",
                "sortable": True,
                "minWidth": 150,
                "type": FieldType.string,
                "filterable": True
            },
            {
                "id": "ville_etablissement",
                "name": "Ville Etablissement",
                "field": "ville_etablissement",
                "sortable": True,
                "minWidth": 150,
                "type": FieldType.string,
                "filterable": True
            },
            {
                "id": "forme_juridique",
                "name": "Forme Juridique",
                "field": "forme_juridique",
                "sortable": True,
                "minWidth": 150,
                "type": FieldType.string,
                "filterable": True
            },
            {
                "id": "nom_etablissement",
                "name": "Nom Etablissement",
                "field": "nom_etablissement",
                "sortable": True,
                "minWidth": 150,
                "type": FieldType.string,
                "filterable": True
            },

            # Champs numériques formatés
            {
                "id": "pourcentage_score",
                "name": "Score total",
                "field": "pourcentage_score",
                "sortable": True,
                "minWidth": 150,
                "type": FieldType.number,
                "filterable": True,
                "formatter": StreamlitSlickGridFormatters.barFormatter,
                "params": {
                    "colors": [
                        [50.9, "white", "red"],
                        [60.9, "black", "yellow"],
                        [80.0, "black", "orange"],
                        [100.0, "white", "green"]
                    ],
                    "minDecimal": 0,
                    "maxDecimal": 2,
                    "numberSuffix": "%"
                }
            },
            {
                "id": "Organisation et gestion",
                "name": "Organisation et gestion",
                "field": "Organisation et gestion",
                "sortable": True,
                "minWidth": 150,
                "type": FieldType.number,
                "filterable": True,
                "formatter": StreamlitSlickGridFormatters.barFormatter,
                "params": {
                    "colors": [
                        [50.9, "white", "red"],
                        [60.9, "black", "yellow"],
                        [80.0, "black", "orange"],
                        [100.0, "white", "green"]
                    ],
                    "minDecimal": 0,
                    "maxDecimal": 2,
                    "numberSuffix": "%"
                }
            },
            {
                "id": "Gestion de la qualité",
                "name": "Gestion de la qualité",
                "field": "Gestion de la qualité",
                "sortable": True,
                "minWidth": 150,
                "type": FieldType.number,
                "filterable": True,
                "formatter": StreamlitSlickGridFormatters.barFormatter,
                "params": {
                    "colors": [
                        [50.9, "white", "red"],
                        [60.9, "black", "yellow"],
                        [80.0, "black", "orange"],
                        [100.0, "white", "green"]
                    ],
                    "minDecimal": 0,
                    "maxDecimal": 2,
                    "numberSuffix": "%"
                }
            },
            {
            "id": "Gestion du risque qualité",
            "name": "Gestion du risque qualité",
            "field": "Gestion du risque qualité",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Revue de la direction",
            "name": "Revue de la direction",
            "field": "Revue de la direction",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Réclamations",
            "name": "Réclamations",
            "field": "Réclamations",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Produits retournés",
            "name": "Produits retournés",
            "field": "Produits retournés",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Rappels",
            "name": "Rappels",
            "field": "Rappels",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Auto-inspections",
            "name": "Auto-inspections",
            "field": "Auto-inspections",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Audits / inspections antérieures",
            "name": "Audits / inspections antérieures",
            "field": "Audits / inspections antérieures",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Locaux",
            "name": "Locaux",
            "field": "Locaux",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Contrôle de rotation du stock",
            "name": "Contrôle de rotation du stock",
            "field": "Contrôle de rotation du stock",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Équipements",
            "name": "Équipements",
            "field": "Équipements",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Qualification et validation",
            "name": "Qualification et validation",
            "field": "Qualification et validation",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Personnels",
            "name": "Personnels",
            "field": "Personnels",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Documentation",
            "name": "Documentation",
            "field": "Documentation",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Activités et opérations",
            "name": "Activités et opérations",
            "field": "Activités et opérations",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Activités externalisées",
            "name": "Activités externalisées",
            "field": "Activités externalisées",
            "sortable": True,
            "minWidth": 150,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Produits de qualité inférieure et falsifiés",
            "name": "Produits de qualité inférieure et falsifiés",
            "field": "Produits de qualité inférieure et falsifiés",
            "sortable": True,
            "minWidth": 200,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        },
        {
            "id": "Produits de qualité inférieure et falsifiés",
            "name": "Produits de qualité inférieure et falsifiés",
            "field": "Produits de qualité inférieure et falsifiés",
            "sortable": True,
            "minWidth": 200,
            "type": FieldType.number,
            "filterable": True,
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [[50.9, "white", "red"], [60.9, "black", "yellow"], [80.0, "black", "orange"], [100.0, "white", "green"]],
                "minDecimal": 0, "maxDecimal": 2, "numberSuffix": "%"
            }
        }
        ]
        options = {
            
            "enableFiltering": True,
            
            "enableTextExport": True,
            "enableExcelExport": True,
            "excelExportOptions": {"sanitizeDataExport": True},
            "textExportOptions": {"sanitizeDataExport": True},
            "externalResources": [
                ExportServices.ExcelExportService,
                ExportServices.TextExportService,
            ],
            "autoResize": {
                "minHeight": 500,
            },
            "enableTreeData": True,
            "multiColumnSort": False,
            "treeDataOptions": {
                "columnId": "title",
                "indentMarginLeft": 15,
                "initiallyCollapsed": True,
                "parentPropName": "__parent",
                "levelPropName": "__depth",
            },
        }
        df_pourcentages.rename(columns={"__id": "id"}, inplace=True)
        out = slickgrid(df_pourcentages.to_dict(orient="records"), columns, options)
