import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json

# Configuration de la page
st.set_page_config(
    page_title="Scraper Salons & Appels d'Offres Maroc",
    page_icon="🇲🇦",
    layout="wide"
)

# Titre principal
st.title("🇲🇦 Scraper des Salons et Appels d'Offres au Maroc")
st.markdown("---")

# Fonction de scraping générique
def scrape_website(url, headers=None):
    """Fonction générique pour scraper un site web"""
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        st.error(f"Erreur lors du scraping de {url}: {str(e)}")
        return None

# Configuration des sources à scraper
SALONS_SOURCES = {
    "SIEL (Salon International de l'Édition et du Livre)": {
        "url": "https://www.salondulivrecasablanca.ma",
        "type": "Salon du Livre"
    },
    "SIAM (Salon International de l'Agriculture)": {
        "url": "https://www.salon-agriculture.ma",
        "type": "Salon de l'Agriculture"
    },
    "Salon du Cheval": {
        "url": "https://www.salonduchevalelmansour.ma",
        "type": "Salon du Cheval"
    },
    "SMIT (Salon Marocain de l'Innovation Touristique)": {
        "url": "http://www.smit.ma",
        "type": "Salon du Tourisme"
    }
}

APPELS_OFFRES_SOURCES = {
    "Portail Marocain des Marchés Publics": "http://www.marchespublics.gov.ma",
    "Trésorerie Générale du Royaume": "https://www.tgr.gov.ma"
}

# Sidebar pour la navigation
st.sidebar.header("Navigation")
mode = st.sidebar.radio(
    "Choisir le type de recherche:",
    ["🎪 Salons Marocains", "📋 Appels d'Offres Publics", "⚙️ Configuration"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Note:** Cette application nécessite :
- Les URLs exactes des sites officiels
- La structure HTML de chaque site
- Des autorisations pour le scraping
""")

# Section Salons
if mode == "🎪 Salons Marocains":
    st.header("🎪 Recherche dans les Salons Marocains")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        salon_type = st.selectbox(
            "Type de salon:",
            ["Tous", "Salon du Livre", "Salon de l'Agriculture", 
             "Salon du Cheval", "Salon du Tourisme", "Salon de la Pêche"]
        )
    
    with col2:
        annee = st.selectbox("Année:", [2025, 2024, 2023])
    
    if st.button("🔍 Rechercher les Salons", type="primary"):
        with st.spinner("Recherche en cours..."):
            
            # Données d'exemple (à remplacer par du scraping réel)
            data_salons = {
                "Nom du Salon": [
                    "SIEL 2025 - Salon du Livre",
                    "SIAM 2025 - Salon de l'Agriculture",
                    "Salon du Cheval 2025"
                ],
                "Type": ["Livre", "Agriculture", "Équestre"],
                "Dates": ["6-16 Février 2025", "24-29 Avril 2025", "Octobre 2025"],
                "Lieu": ["Casablanca", "Meknès", "El Jadida"],
                "Responsable": [
                    "Direction des Affaires Culturelles",
                    "Ministère de l'Agriculture",
                    "Association du Salon du Cheval"
                ],
                "Téléphone": ["+212 5XX XX XX XX", "+212 5XX XX XX XX", "+212 5XX XX XX XX"],
                "Email": ["contact@siel.ma", "contact@siam.ma", "contact@saloncheval.ma"],
                "Site Web": [
                    "www.salondulivrecasablanca.ma",
                    "www.salon-agriculture.ma",
                    "www.salonduchevalelmansour.ma"
                ]
            }
            
            df_salons = pd.DataFrame(data_salons)
            
            st.success(f"✅ {len(df_salons)} salons trouvés")
            
            # Affichage des résultats
            for idx, row in df_salons.iterrows():
                with st.expander(f"📌 {row['Nom du Salon']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"**Type:** {row['Type']}")
                        st.markdown(f"**Dates:** {row['Dates']}")
                        st.markdown(f"**Lieu:** {row['Lieu']}")
                    
                    with col2:
                        st.markdown(f"**Responsable:**")
                        st.markdown(row['Responsable'])
                        st.markdown(f"**Téléphone:** {row['Téléphone']}")
                    
                    with col3:
                        st.markdown(f"**Email:** {row['Email']}")
                        st.markdown(f"**Site Web:** {row['Site Web']}")
            
            # Export des données
            st.download_button(
                label="📥 Télécharger les données (CSV)",
                data=df_salons.to_csv(index=False).encode('utf-8'),
                file_name=f"salons_marocains_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

# Section Appels d'Offres
elif mode == "📋 Appels d'Offres Publics":
    st.header("📋 Appels d'Offres - Services Informatiques")
    
    col1, col2 = st.columns(2)
    
    with col1:
        secteur = st.selectbox(
            "Secteur:",
            ["Tous", "Informatique", "Services IT", "Infrastructure", "Développement"]
        )
    
    with col2:
        budget_min = st.number_input("Budget minimum (MAD):", min_value=0, value=0, step=10000)
    
    if st.button("🔍 Rechercher les Appels d'Offres", type="primary"):
        with st.spinner("Recherche en cours..."):
            
            # Données d'exemple
            data_ao = {
                "Référence": ["AO/2025/001", "AO/2025/002", "AO/2025/003"],
                "Organisme": [
                    "Ministère de l'Éducation Nationale",
                    "Direction Générale des Impôts",
                    "Agence de Développement Digital"
                ],
                "Objet": [
                    "Développement d'une plateforme éducative digitale",
                    "Infrastructure réseau et cybersécurité",
                    "Système de gestion documentaire"
                ],
                "Budget (MAD)": ["2 500 000", "1 800 000", "3 200 000"],
                "Date Limite": ["15/12/2025", "20/12/2025", "30/12/2025"],
                "Contact": [
                    "M. Ahmed Bennani",
                    "Mme Fatima Alaoui",
                    "M. Youssef Tazi"
                ],
                "Téléphone": ["+212 537 XX XX XX", "+212 537 XX XX XX", "+212 537 XX XX XX"],
                "Email": ["marches@men.gov.ma", "ao@dgi.gov.ma", "contact@add.gov.ma"]
            }
            
            df_ao = pd.DataFrame(data_ao)
            
            st.success(f"✅ {len(df_ao)} appels d'offres trouvés")
            
            # Affichage avec mise en forme
            for idx, row in df_ao.iterrows():
                with st.expander(f"📄 {row['Référence']} - {row['Organisme']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Objet:**")
                        st.info(row['Objet'])
                        st.markdown(f"**Budget:** {row['Budget (MAD)']} MAD")
                        st.markdown(f"**Date limite:** {row['Date Limite']}")
                    
                    with col2:
                        st.markdown(f"**Personne à contacter:**")
                        st.markdown(f"👤 {row['Contact']}")
                        st.markdown(f"📞 {row['Téléphone']}")
                        st.markdown(f"📧 {row['Email']}")
                    
                    # Calcul du temps restant
                    st.warning(f"⏰ Temps restant pour soumissionner")
            
            # Export
            st.download_button(
                label="📥 Télécharger les données (CSV)",
                data=df_ao.to_csv(index=False).encode('utf-8'),
                file_name=f"appels_offres_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

# Section Configuration
else:
    st.header("⚙️ Configuration du Scraper")
    
    st.info("""
    ### 🔧 Comment utiliser cette application
    
    Cette application nécessite une configuration pour chaque site web à scraper.
    """)
    
    tab1, tab2 = st.tabs(["Sites des Salons", "Sites d'Appels d'Offres"])
    
    with tab1:
        st.subheader("Sites officiels des Salons")
        
        for salon, info in SALONS_SOURCES.items():
            with st.expander(salon):
                st.markdown(f"**URL:** {info['url']}")
                st.markdown(f"**Type:** {info['type']}")
                
                if st.button(f"Tester {salon}", key=f"test_{salon}"):
                    soup = scrape_website(info['url'])
                    if soup:
                        st.success("✅ Site accessible")
                    else:
                        st.error("❌ Site non accessible")
        
        st.markdown("---")
        st.markdown("**Ajouter un nouveau salon:**")
        new_salon = st.text_input("Nom du salon:")
        new_url = st.text_input("URL du site:")
        if st.button("Ajouter"):
            st.success(f"Salon '{new_salon}' ajouté!")
    
    with tab2:
        st.subheader("Sites d'Appels d'Offres")
        
        for source, url in APPELS_OFFRES_SOURCES.items():
            with st.expander(source):
                st.markdown(f"**URL:** {url}")
                
                if st.button(f"Tester {source}", key=f"test_ao_{source}"):
                    soup = scrape_website(url)
                    if soup:
                        st.success("✅ Site accessible")
                    else:
                        st.error("❌ Site non accessible")
    
    st.markdown("---")
    st.warning("""
    ### ⚠️ Notes importantes:
    
    1. **Légalité:** Assurez-vous d'avoir le droit de scraper ces sites
    2. **Robots.txt:** Vérifiez les fichiers robots.txt de chaque site
    3. **Rate Limiting:** Utilisez des délais entre les requêtes
    4. **Données personnelles:** Respectez le RGPD et les lois marocaines
    5. **APIs officielles:** Privilégiez les APIs quand elles existent
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🇲🇦 Scraper des Salons et Appels d'Offres Maroc | Développé avec Streamlit</p>
    <p><small>Pour un scraping efficace, configurez les sélecteurs CSS pour chaque site</small></p>
</div>
""", unsafe_allow_html=True)