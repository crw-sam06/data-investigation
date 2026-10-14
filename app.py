import streamlit as st
import pandas as pd
import pydeck as pdk
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DATA INVESTIGATION",
    page_icon="🕵️",
    layout="wide"
)


# ============================================================
# CHEMIN DU PROJET
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

@st.cache_data
def charger_donnees():

    deplacements = pd.read_csv(
        DATA_DIR / "deplacements.csv"
    )

    communications = pd.read_csv(
        DATA_DIR / "communications.csv"
    )

    cameras = pd.read_csv(
        DATA_DIR / "cameras.csv"
    )

    transactions = pd.read_csv(
        DATA_DIR / "transactions.csv"
    )

    temoignages = pd.read_csv(
        DATA_DIR / "temoignages.csv"
    )

    lieux = pd.read_csv(
        DATA_DIR / "lieux.csv"
    )

    return (
        deplacements,
        communications,
        cameras,
        transactions,
        temoignages,
        lieux
    )


(
    deplacements,
    communications,
    cameras,
    transactions,
    temoignages,
    lieux
) = charger_donnees()


# ============================================================
# NOMS DES SUSPECTS
# ============================================================

noms_suspects = {
    "S01": "Alice Martin",
    "S02": "Karim Benali",
    "S03": "Élodie Garnier",
    "S04": "Lucas Morel",
    "S05": "Sophie Laurent",
    "S06": "Marc Dubois"
}


profils_suspects = {
    "S01": "Associée",
    "S02": "Ancien associé",
    "S03": "Ex-partenaire",
    "S04": "Frère",
    "S05": "Employée",
    "S06": "Ami"
}


declarations_suspects = {
    "S01": "Je suis restée chez moi toute la soirée.",
    "S02": "J'étais au restaurant jusqu'à 23 h.",
    "S03": "Je suis passée près de chez lui mais je ne suis pas montée.",
    "S04": "Je suis allé courir vers 22 h.",
    "S05": "Je travaillais dans mon bureau jusqu'à 23 h.",
    "S06": "Je n'ai pas quitté mon domicile."
}


# ============================================================
# SESSION
# ============================================================

if "enquete_commencee" not in st.session_state:
    st.session_state.enquete_commencee = False

if "mission1_validee" not in st.session_state:
    st.session_state.mission1_validee = False

if "mission2_validee" not in st.session_state:
    st.session_state.mission2_validee = False

if "mission3_validee" not in st.session_state:
    st.session_state.mission3_validee = False

if "mission4_validee" not in st.session_state:
    st.session_state.mission4_validee = False

if "mission5_validee" not in st.session_state:
    st.session_state.mission5_validee = False


# ============================================================
# TITRE
# ============================================================

st.title("🕵️ DATA INVESTIGATION")

st.subheader("L'affaire du 17 octobre")

st.write(
    "Une enquête fictive basée sur les Sciences des Données."
)


# ============================================================
# PAGE D'ACCUEIL
# ============================================================

if not st.session_state.enquete_commencee:

    st.markdown("---")

    st.header("📁 DOSSIER D'ENQUÊTE")

    st.write(
        """
        Paris, 17 octobre 2026.

        À 23h47, Thomas Morel, directeur d'une société de conseil,
        est retrouvé mort dans son appartement.

        Les enquêteurs disposent de plusieurs sources de données :
        déplacements, communications, caméras, transactions et témoignages.
        """
    )

    st.warning(
        "⚠️ Votre objectif n'est pas de trouver un coupable grâce à un seul indice. "
        "Vous devez croiser les données et reconstruire la soirée."
    )

    st.markdown("---")

    st.header("👥 Les suspects")

    for suspect_id in noms_suspects:

        with st.expander(
            f"{suspect_id} — {noms_suspects[suspect_id]}"
        ):

            st.write(
                f"**Profil :** {profils_suspects[suspect_id]}"
            )

            st.write(
                f"**Déclaration :** "
                f"{declarations_suspects[suspect_id]}"
            )

    st.markdown("---")

    if st.button(
        "🚨 COMMENCER L'ENQUÊTE",
        type="primary",
        use_container_width=True
    ):

        st.session_state.enquete_commencee = True

        st.rerun()

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🕵️ Enquête")

st.sidebar.write("Progression")

st.sidebar.write("🕐 Mission 1 — Quand ?")
st.sidebar.write("🗺️ Mission 2 — Où étaient-ils ?")
st.sidebar.write("🔎 Mission 3 — Qui dit vrai ?")
st.sidebar.write("⏱️ Mission 4 — Reconstituez la soirée")
st.sidebar.write("🎯 Mission 5 — Votre conclusion")
st.sidebar.write("🎬 Révélation finale")


# ============================================================
# MISSION 1
# ============================================================

st.header("🕐 Mission 1 — Quand ?")

st.write(
    """
    La première étape consiste à déterminer la période pendant laquelle
    les événements importants ont probablement eu lieu.
    """
)

st.info(
    "Les données indiquent une fenêtre critique comprise entre 22h35 et 22h55."
)

st.subheader("❓ Quelle est la fenêtre temporelle étudiée ?")

choix_m1 = st.radio(
    "Sélectionnez votre réponse :",
    [
        "21h00 – 22h00",
        "22h35 – 22h55",
        "23h00 – 23h30",
        "23h30 – 00h00"
    ],
    key="mission1"
)

if st.button(
    "Valider la Mission 1",
    key="btn_m1"
):

    if choix_m1 == "22h35 – 22h55":

        st.success(
            "✅ Bonne réponse ! La fenêtre critique est 22h35 – 22h55."
        )

        st.session_state.mission1_validee = True

    else:

        st.error(
            "❌ Ce n'est pas la bonne période. Analysez les événements critiques."
        )


# ============================================================
# MISSION 2
# ============================================================

if st.session_state.mission1_validee:

    st.divider()

    st.header("🗺️ Mission 2 — Où étaient-ils ?")

    st.write(
        """
        Les déplacements permettent de suivre les suspects
        pendant la période critique.
        """
    )

    suspect_selectionne = st.selectbox(
        "Choisissez un suspect :",
        list(noms_suspects.keys()),
        format_func=lambda x: noms_suspects[x],
        key="mission2_suspect"
    )

    nom_suspect = noms_suspects[suspect_selectionne]

    trajets = deplacements[
        deplacements["suspect"] == suspect_selectionne
    ].copy()

    trajets = trajets.sort_values("heure")

    st.subheader(
        f"📍 Déplacements de {nom_suspect}"
    )

    if len(trajets) > 0:

        for _, ligne in trajets.iterrows():

            st.write(
                f"📍 À {ligne['heure']}, "
                f"{nom_suspect} se trouve à **{ligne['lieu']}**."
            )

        st.markdown("---")

        st.subheader("🛣️ Trajet")

        points = []

        for _, ligne in trajets.iterrows():

            points.append(
                [
                    ligne["longitude"],
                    ligne["latitude"]
                ]
            )

        if len(points) >= 2:

            path_data = pd.DataFrame(
                {
                    "path": [points]
                }
            )

            scatter_data = pd.DataFrame(
                {
                    "longitude": [
                        p[0] for p in points
                    ],
                    "latitude": [
                        p[1] for p in points
                    ]
                }
            )

            # ================================================
            # DÉPART = VERT
            # ================================================

            depart_data = scatter_data.iloc[[0]].copy()

            # ================================================
            # ÉTAPES INTERMÉDIAIRES = BLEU
            # ================================================

            if len(scatter_data) > 2:

                intermediaires_data = scatter_data.iloc[1:-1].copy()

            else:

                intermediaires_data = scatter_data.iloc[0:0].copy()

            # ================================================
            # ARRIVÉE = ROUGE
            # ================================================

            arrivee_data = scatter_data.iloc[[-1]].copy()

            # ================================================
            # COULEURS DE LA CARTE
            # ================================================

            layers = [

                # --------------------------------------------
                # TRAJET = NOIR
                # --------------------------------------------

                pdk.Layer(
                    "PathLayer",
                    data=path_data,
                    get_path="path",
                    get_width=7,
                    get_color=[0, 0, 0, 220],
                    pickable=True
                ),

                # --------------------------------------------
                # DÉPART = VERT
                # --------------------------------------------

                pdk.Layer(
                    "ScatterplotLayer",
                    data=depart_data,
                    get_position=[
                        "longitude",
                        "latitude"
                    ],
                    get_radius=140,
                    get_fill_color=[
                        0,
                        180,
                        0,
                        255
                    ],
                    pickable=True
                ),

                # --------------------------------------------
                # ÉTAPES = BLEU
                # --------------------------------------------

                pdk.Layer(
                    "ScatterplotLayer",
                    data=intermediaires_data,
                    get_position=[
                        "longitude",
                        "latitude"
                    ],
                    get_radius=110,
                    get_fill_color=[
                        0,
                        100,
                        255,
                        255
                    ],
                    pickable=True
                ),

                # --------------------------------------------
                # ARRIVÉE = ROUGE
                # --------------------------------------------

                pdk.Layer(
                    "ScatterplotLayer",
                    data=arrivee_data,
                    get_position=[
                        "longitude",
                        "latitude"
                    ],
                    get_radius=150,
                    get_fill_color=[
                        220,
                        0,
                        0,
                        255
                    ],
                    pickable=True
                )
            ]

            # ================================================
            # POSITION DE LA CARTE
            # ================================================

            view_state = pdk.ViewState(
                latitude=scatter_data["latitude"].mean(),
                longitude=scatter_data["longitude"].mean(),
                zoom=13
            )

            # ================================================
            # AFFICHAGE DE LA CARTE
            # ================================================

            st.pydeck_chart(
                pdk.Deck(
                    layers=layers,
                    initial_view_state=view_state,
                    map_style=(
                        "https://basemaps.cartocdn.com/"
                        "gl/positron-gl-style/style.json"
                    )
                )
            )

            # ================================================
            # LÉGENDE
            # ================================================

            st.markdown(
                """
                🟢 **Départ**

                🔵 **Étapes intermédiaires**

                🔴 **Arrivée**

                ⚫ **Trajet**
                """
            )

        st.markdown("---")

        st.subheader("📋 Données du trajet")

        tableau = trajets[
            [
                "heure",
                "lieu",
                "type_transport"
            ]
        ].copy()

        tableau.columns = [
            "Heure",
            "Lieu",
            "Transport"
        ]

        st.dataframe(
            tableau,
            use_container_width=True,
            hide_index=True
        )

    if st.button(
        "Valider la Mission 2",
        key="btn_m2"
    ):

        st.success(
            "✅ Mission 2 validée ! Vous avez commencé à reconstruire les déplacements."
        )

        st.session_state.mission2_validee = True


# ============================================================
# MISSION 3
# ============================================================

if st.session_state.mission2_validee:

    st.divider()

    st.header("🔎 Mission 3 — Qui dit vrai ?")

    st.write(
        """
        Maintenant, comparez les déclarations avec les données disponibles.

        Une déclaration peut être compatible, incertaine ou incompatible
        avec les observations.
        """
    )

    suspect_m3 = st.selectbox(
        "Choisissez un suspect à analyser :",
        list(noms_suspects.keys()),
        format_func=lambda x: noms_suspects[x],
        key="mission3_suspect"
    )

    nom_m3 = noms_suspects[suspect_m3]

    st.subheader(
        f"🗣️ Déclaration de {nom_m3}"
    )

    st.info(
        declarations_suspects[suspect_m3]
    )

    # --------------------------------------------------------
    # DÉPLACEMENTS
    # --------------------------------------------------------

    st.subheader("📍 Déplacements")

    dep_suspect = deplacements[
        deplacements["suspect"] == suspect_m3
    ].copy()

    if len(dep_suspect) > 0:

        for _, ligne in dep_suspect.iterrows():

            st.write(
                f"📍 À {ligne['heure']}, "
                f"{nom_m3} se trouve à **{ligne['lieu']}**."
            )

    else:

        st.write(
            "Aucun déplacement enregistré."
        )

    # --------------------------------------------------------
    # COMMUNICATIONS
    # --------------------------------------------------------

    st.subheader("📞 Communications")

    communications_suspect = communications[
        (
            communications["emetteur"]
            .str.contains(
                nom_m3,
                case=False,
                na=False
            )
        )
        |
        (
            communications["destinataire"]
            .str.contains(
                nom_m3,
                case=False,
                na=False
            )
        )
    ]

    if len(communications_suspect) > 0:

        for _, ligne in communications_suspect.iterrows():

            st.write(
                f"📞 À {ligne['heure']}, "
                f"{ligne['emetteur']} communique avec "
                f"{ligne['destinataire']}."
            )

    else:

        st.write(
            "Aucune communication enregistrée."
        )

    # --------------------------------------------------------
    # TRANSACTIONS
    # --------------------------------------------------------

    st.subheader("💳 Transactions")

    carte_suspect = "CARD_" + suspect_m3

    transactions_suspect = transactions[
        transactions["carte"] == carte_suspect
    ]

    if len(transactions_suspect) > 0:

        for _, ligne in transactions_suspect.iterrows():

            st.write(
                f"💳 À {ligne['heure']}, "
                f"une transaction de **{ligne['montant']} €** "
                f"est enregistrée à **{ligne['lieu']}**."
            )

    else:

        st.write(
            "Aucune transaction enregistrée."
        )

    # --------------------------------------------------------
    # CAMÉRAS
    # --------------------------------------------------------

    st.subheader("📹 Caméras")

    cameras_suspect = cameras[
        cameras["objet"].str.contains(
            nom_m3,
            case=False,
            na=False
        )
    ].copy()

    if len(cameras_suspect) > 0:

        for _, ligne in cameras_suspect.iterrows():

            st.write(
                f"📹 À {ligne['heure']}, "
                f"{ligne['objet']} est filmé : "
                f"{ligne['direction']}."
            )

    else:

        st.write(
            "Aucune caméra n'identifie directement ce suspect."
        )

    # --------------------------------------------------------
    # ANALYSE
    # --------------------------------------------------------

    st.subheader("🧠 Analyse")

    if suspect_m3 == "S02":

        st.warning(
            "Karim Benali affirme être resté au restaurant jusqu'à 23h. "
            "Pourtant, les données indiquent un déplacement au Centre "
            "pendant la période critique."
        )

    elif suspect_m3 == "S03":

        st.warning(
            "Élodie Garnier affirme ne pas être montée chez Thomas. "
            "Les données montrent toutefois une présence au Centre "
            "pendant la période critique."
        )

    elif suspect_m3 == "S04":

        st.warning(
            "Lucas Morel affirme être allé courir. "
            "Un déplacement au Centre apparaît à 22h50."
        )

    elif suspect_m3 == "S05":

        st.info(
            "Les données disponibles indiquent principalement "
            "une présence au Bureau B1."
        )

    elif suspect_m3 == "S06":

        st.warning(
            "Marc Dubois affirme ne pas avoir quitté son domicile. "
            "Une présence au Centre apparaît plus tard dans les données."
        )

    else:

        st.info(
            "Les données disponibles ne permettent pas de relever "
            "une contradiction majeure."
        )

    # --------------------------------------------------------
    # VERDICT
    # --------------------------------------------------------

    st.subheader("❓ Quel est votre verdict ?")

    verdict = st.radio(
        "Pour ce suspect :",
        [
            "Compatible avec les données",
            "Incompatible avec les données",
            "Les données sont insuffisantes"
        ],
        key="verdict_m3"
    )

    if st.button(
        "Valider la Mission 3",
        key="btn_m3"
    ):

        st.success(
            "✅ Analyse enregistrée."
        )

        st.session_state.mission3_validee = True


# ============================================================
# MISSION 4
# ============================================================

if st.session_state.mission3_validee:

    st.divider()

    st.header("⏱️ Mission 4 — Reconstituez la soirée")

    st.write(
        """
        Vous disposez maintenant de plusieurs sources.

        Replacez les événements importants sur une même chronologie.
        """
    )

    st.subheader("📅 Chronologie")

    evenements = [

        (
            "22h32",
            "📍 Karim Benali est au Restaurant R1."
        ),

        (
            "22h39",
            "📍 Karim Benali se déplace au Centre."
        ),

        (
            "22h41",
            "📞 Élodie Garnier communique avec Thomas Morel."
        ),

        (
            "22h43",
            "📞 Karim Benali communique avec le Restaurant R1."
        ),

        (
            "22h44",
            "📹 Une personne avec une veste sombre est filmée."
        ),

        (
            "22h45",
            "📹 Une personne inconnue est filmée en direction de l'appartement."
        ),

        (
            "22h46",
            "📍 Karim Benali est de nouveau au Centre."
        ),

        (
            "22h47",
            "📞 Thomas Morel communique avec un numéro inconnu."
        ),

        (
            "22h47",
            "📍 Élodie Garnier est au Centre."
        ),

        (
            "22h49",
            "💳 Une transaction de 7,50 € est effectuée au Restaurant R1."
        ),

        (
            "22h50",
            "📍 Lucas Morel apparaît au Centre."
        ),

        (
            "22h51",
            "📞 Sophie Laurent communique avec Thomas Morel."
        ),

        (
            "22h52",
            "📍 Karim Benali revient au Restaurant R1."
        )
    ]

    for heure, description in evenements:

        st.write(
            f"**{heure}** — {description}"
        )

    # --------------------------------------------------------
    # ÉVÉNEMENTS CLÉS
    # --------------------------------------------------------

    st.subheader("⭐ Quelques événements clés")

    st.markdown(
        """
        **22h39** — Karim Benali est au Centre.

        **22h41** — Élodie Garnier communique avec Thomas Morel.

        **22h49** — Une transaction est enregistrée au Restaurant R1.
        """
    )

    st.warning(
        "Plusieurs événements sont proches dans le temps. "
        "Il faut déterminer lesquels sont réellement importants "
        "pour reconstruire le scénario."
    )

    st.subheader("❓ Quelle période est au cœur de l'enquête ?")

    periode = st.radio(
        "Votre réponse :",
        [
            "21h00 – 22h00",
            "22h35 – 22h55",
            "23h00 – 23h30"
        ],
        key="periode_m4"
    )

    if st.button(
        "Valider la Mission 4",
        key="btn_m4"
    ):

        if periode == "22h35 – 22h55":

            st.success(
                "✅ Bonne réponse ! Vous avez reconstitué la période critique."
            )

            st.session_state.mission4_validee = True

        else:

            st.error(
                "❌ Regardez les horaires des événements importants."
            )


# ============================================================
# MISSION 5
# ============================================================

if st.session_state.mission4_validee:

    st.divider()

    st.header("🎯 Mission 5 — Votre conclusion")

    st.write(
        """
        C'est à vous de construire votre scénario.

        Vous devez utiliser plusieurs éléments de données
        pour justifier votre conclusion.
        """
    )

    suspect_final = st.selectbox(
        "Quel suspect souhaitez-vous retenir dans votre scénario ?",
        list(noms_suspects.keys()),
        format_func=lambda x: noms_suspects[x],
        key="suspect_final"
    )

    nom_final = noms_suspects[suspect_final]

    st.subheader(
        f"🕵️ {nom_final}"
    )

    presence = st.radio(
        "Selon vous, sa présence dans la zone critique est-elle :",
        [
            "Oui",
            "Incertaine",
            "Non"
        ],
        key="presence_final"
    )

    st.subheader(
        "🔎 Sélectionnez les éléments qui justifient votre conclusion"
    )

    preuves = st.multiselect(
        "Choisissez au moins 3 éléments :",
        [
            "Déplacement au Centre",
            "Communication avec Thomas Morel",
            "Transaction bancaire",
            "Observation par caméra",
            "Contradiction avec le témoignage",
            "Présence dans un autre lieu",
            "Chronologie des événements"
        ],
        key="preuves_final"
    )

    st.subheader("📝 Votre conclusion")

    conclusion = st.text_area(
        "Expliquez votre scénario :",
        placeholder=(
            "Expliquez ce que vous pensez être arrivé "
            "et utilisez les données pour justifier votre réponse."
        ),
        height=180,
        key="conclusion_finale"
    )

    if st.button(
        "🔐 Valider ma conclusion",
        key="btn_m5",
        type="primary"
    ):

        if len(preuves) < 3:

            st.error(
                "❌ Sélectionnez au moins 3 éléments de données."
            )

        elif conclusion.strip() == "":

            st.error(
                "❌ Écrivez une conclusion avant de valider."
            )

        else:

            st.success(
                "✅ Votre scénario a été enregistré."
            )

            st.session_state.mission5_validee = True


# ============================================================
# RÉVÉLATION FINALE
# ============================================================

if st.session_state.mission5_validee:

    st.divider()

    st.header("🎬 Révélation finale")

    st.write(
        """
        Vous avez terminé l'enquête.

        Mais comment avons-nous réussi à construire cette enquête
        à partir de données ?
        """
    )

    st.info(
        "L'objectif du projet n'était pas de trouver un coupable "
        "grâce à un seul indice, mais de croiser plusieurs sources "
        "de données afin de reconstruire un scénario cohérent."
    )

    # --------------------------------------------------------
    # SCÉNARIO
    # --------------------------------------------------------

    st.subheader("🕵️ Le scénario reconstitué")

    st.write(
        """
        Pendant la période critique, plusieurs événements se
        chevauchent : déplacements, communications, transactions
        et observations.

        Leur comparaison permet de mettre en évidence des
        contradictions entre certaines déclarations et les
        données observées.
        """
    )

    st.warning(
        "⚠️ Les données permettent de reconstruire un scénario cohérent, "
        "mais ne constituent pas à elles seules une preuve judiciaire."
    )

    # --------------------------------------------------------
    # DONNÉES
    # --------------------------------------------------------

    st.subheader("📂 1. Les données")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "👥 Suspects",
            "6"
        )

    with col2:

        st.metric(
            "📍 Lieux",
            "5"
        )

    with col3:

        st.metric(
            "📊 Sources",
            "7"
        )

    st.write(
        """
        L'enquête repose sur plusieurs tables de données :

        - suspects
        - lieux
        - déplacements
        - communications
        - caméras
        - transactions
        - témoignages
        """
    )

    # --------------------------------------------------------
    # NETTOYAGE
    # --------------------------------------------------------

    st.subheader("🧹 2. Nettoyage des données")

    st.write(
        """
        Avant d'analyser les données, nous devons nous assurer
        qu'elles sont correctement structurées.
        """
    )

    st.markdown(
        """
        ✅ Vérification des fichiers CSV

        ✅ Vérification des colonnes

        ✅ Vérification des identifiants

        ✅ Vérification des horaires

        ✅ Préparation des données pour l'analyse
        """
    )

    # --------------------------------------------------------
    # PYTHON
    # --------------------------------------------------------

    st.subheader("🐍 3. Python et Pandas")

    st.write(
        """
        Python permet de charger, filtrer et analyser les données.
        """
    )

    st.code(
        '''import pandas as pd

deplacements = pd.read_csv(
    "deplacements.csv"
)

evenements = deplacements[
    deplacements["heure"] >= "22:35"
]

print(evenements)
''',
        language="python"
    )

    st.success(
        "Python permet d'automatiser le traitement des données."
    )

    # --------------------------------------------------------
    # POSTGRESQL
    # --------------------------------------------------------

    st.subheader("🗄️ 4. PostgreSQL et SQL")

    st.write(
        """
        Les données sont stockées dans une base PostgreSQL.
        SQL permet ensuite de croiser différentes tables.
        """
    )

    st.code(
        '''SELECT
    d.suspect,
    d.heure,
    d.lieu,
    t.heure AS heure_transaction,
    t.montant
FROM deplacements d
JOIN transactions t
    ON d.suspect = REPLACE(t.carte, 'CARD_', '')
    AND d.lieu = t.lieu
WHERE d.heure BETWEEN '22:35' AND '22:55';
''',
        language="sql"
    )

    st.success(
        "SQL permet de rechercher des relations entre plusieurs sources."
    )

    # --------------------------------------------------------
    # STATISTIQUES
    # --------------------------------------------------------

    st.subheader("📊 5. Statistiques")

    st.write(
        """
        Les statistiques permettent d'étudier les horaires,
        les écarts entre événements et les périodes importantes.
        """
    )

    st.markdown(
        """
        **Exemple :**

        Karim Benali apparaît au Restaurant R1 à **22h52**.

        Une transaction est enregistrée au même endroit à **22h49**.

        ➡️ Écart entre les deux événements : **3 minutes**.
        """
    )

    # --------------------------------------------------------
    # VISUALISATION
    # --------------------------------------------------------

    st.subheader("📈 6. Visualisation")

    st.write(
        """
        Les données peuvent être représentées sous différentes
        formes pour faciliter leur compréhension.
        """
    )

    st.markdown(
        """
        📍 Carte des déplacements

        ⏱️ Chronologie des événements

        📊 Analyse des horaires

        🔎 Comparaison des sources
        """
    )

    # --------------------------------------------------------
    # CARTOGRAPHIE
    # --------------------------------------------------------

    st.subheader("🗺️ 7. Analyse géographique")

    st.write(
        """
        Chaque déplacement contient des coordonnées géographiques.

        Nous pouvons donc représenter le trajet d'un suspect
        directement sur une carte.
        """
    )

    st.info(
        "La cartographie permet de transformer une suite de coordonnées "
        "en trajet compréhensible."
    )

    # --------------------------------------------------------
    # CROISEMENT
    # --------------------------------------------------------

    st.subheader("🔗 8. Croisement des données")

    st.markdown(
        """
        **Déplacement**

        +

        **Communication**

        +

        **Transaction**

        +

        **Caméra**

        +

        **Témoignage**

        ↓

        **Scénario reconstitué**
        """
    )

    st.warning(
        "Une donnée isolée n'est pas automatiquement une preuve. "
        "C'est le croisement des sources qui permet de faire émerger "
        "un scénario."
    )

    # --------------------------------------------------------
    # COMPÉTENCES BUT SD
    # --------------------------------------------------------

    st.subheader(
        "🎓 9. Les compétences du BUT Sciences des Données"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            ### 🧹 Préparation des données

            Nettoyer et structurer des données brutes.

            ### 🗄️ Bases de données

            Stocker et organiser les informations avec PostgreSQL.

            ### 🔎 SQL

            Filtrer, rechercher et croiser plusieurs tables.

            ### 🐍 Programmation

            Utiliser Python et Pandas pour automatiser les analyses.
            """
        )

    with col2:

        st.markdown(
            """
            ### 📊 Statistiques

            Analyser les horaires, les écarts et les événements.

            ### 📈 Datavisualisation

            Transformer les données en informations compréhensibles.

            ### 🗺️ Données géographiques

            Représenter et analyser les déplacements.

            ### 💬 Communication

            Présenter les résultats d'une analyse.
            """
        )

    # --------------------------------------------------------
    # ARCHITECTURE
    # --------------------------------------------------------

    st.subheader(
        "🏗️ 10. Comment l'application fonctionne ?"
    )

    st.markdown(
        """
        👤 **Joueur**

        ↓

        🌐 **Application Streamlit**

        ↓

        🐍 **Python / Pandas**

        ↓

        🗄️ **PostgreSQL**

        ↓

        📊 **Analyse des données**

        ↓

        📈 **Visualisations**

        ↓

        🕵️ **Enquête**
        """
    )

    # --------------------------------------------------------
    # CONCLUSION
    # --------------------------------------------------------

    st.divider()

    st.header("🎯 DATA INVESTIGATION")

    st.write(
        """
        Derrière une enquête fictive se cache un véritable projet
        de Sciences des Données.
        """
    )

    st.markdown(
        """
        **Données brutes**

        ↓

        **Nettoyage**

        ↓

        **Base de données**

        ↓

        **SQL**

        ↓

        **Python**

        ↓

        **Statistiques**

        ↓

        **Visualisations**

        ↓

        **Interprétation**

        ↓

        **Conclusion**
        """
    )

    st.success(
        """
        🧠 DATA INVESTIGATION montre comment les compétences du
        BUT Sciences des Données permettent de transformer des
        données brutes en informations utiles.
        """
    )

    st.balloons()
