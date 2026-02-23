import streamlit as st
import time

# ==========================================
# 1. CONFIGURATION & STATE MANAGEMENT
# ==========================================
st.set_page_config(page_title="ROBIN", layout="wide", page_icon="🐦")

# Initialize routing and state variables
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1
if "submission_type" not in st.session_state:
    st.session_state.submission_type = "resources"
if "lite_mode" not in st.session_state:
    st.session_state.lite_mode = False
if "lang" not in st.session_state:
    st.session_state.lang = "DE"
if "supported_projects" not in st.session_state:
    st.session_state.supported_projects = []

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ==========================================
# 2. TRANSLATION DICTIONARY
# ==========================================
T = {
    "DE": {
        "feed_btn": "💬\n\n**COMMUNITY FEED**\n\nSehen Sie, was Ihre Nachbarn vorschlagen.",
        "dash_btn": "👤\n\n**MEIN DASHBOARD**\n\nVerwalten Sie Ihre Ideen und Ihr Profil.",
        "submit_btn": "💡\n\n**IDEE EINREICHEN**\n\nMelden Sie ein Problem oder eine Idee.",
        "how_btn": "⚙️\n\n**WIE ES FUNKTIONIERT**\n\nSo sorgt der Algorithmus für Fairness.",
        "success_btn": "🌟\n\n**ERFOLGSGESCHICHTEN**\n\nPositive Veränderungen.",
        "admin_btn": "🏢\n\n**STADTVERWALTUNG**\n\n(Nur Personal) Feedback-Schleife.",
        "fin_help": "💰\n\n**FINANZIELLE HILFE**\n\nBeantragen Sie Mikrostipendien.",
        "res_help": "🛠️\n\n**RESSOURCEN & HILFE**\n\nFinden Sie Werkzeuge oder Hilfe.",
        "sub_title": "Welche Art von Unterstützung benötigen Sie?",
        "offline": "📡 **Sie sind offline.** Eingaben werden lokal gespeichert.",
        "next": "Weiter ➔", "back": "⬅ Zurück", "submit_final": "✅ Einreichen",
        "settings": "⚙️ Einstellungen", "lite": "Lite-Modus (Langsames Internet)"
    },
    "EN": {
        "feed_btn": "💬\n\n**COMMUNITY FEED**\n\nSee what neighbors are suggesting.",
        "dash_btn": "👤\n\n**MY DASHBOARD**\n\nManage your ideas and profile.",
        "submit_btn": "💡\n\n**SUBMIT AN IDEA**\n\nReport a problem or share an idea.",
        "how_btn": "⚙️\n\n**HOW IT WORKS**\n\nHow our algorithm ensures fairness.",
        "success_btn": "🌟\n\n**SUCCESS STORIES**\n\nPositive impact in the neighborhood.",
        "admin_btn": "🏢\n\n**CITY ADMIN**\n\n(Staff Only) Close the loop.",
        "fin_help": "💰\n\n**FINANCIAL HELP**\n\nApply for micro-grants or funding.",
        "res_help": "🛠️\n\n**RESOURCES & HELP**\n\nFind tools, volunteers, or space.",
        "sub_title": "What kind of support do you need?",
        "offline": "📡 **You are offline.** Typing is saved to device.",
        "next": "Next ➔", "back": "⬅ Back", "submit_final": "✅ Submit",
        "settings": "⚙️ Settings", "lite": "Lite Mode (Slow Internet)"
    },
    "TR": {
        "feed_btn": "💬\n\n**TOPLULUK AKIŞI**\n\nKomşularınızın neler önerdiğini görün.",
        "dash_btn": "👤\n\n**PANELİM**\n\nFikirlerinizi ve profilinizi yönetin.",
        "submit_btn": "💡\n\n**FİKİR GÖNDER**\n\nBir sorun bildirin veya fikir paylaşın.",
        "how_btn": "⚙️\n\n**NASIL ÇALIŞIR?**\n\nAlgoritmamız adaleti nasıl sağlar?",
        "success_btn": "🌟\n\n**BAŞARI HİKAYELERİ**\n\nMahalledeki olumlu etkiler.",
        "admin_btn": "🏢\n\n**ŞEHİR YÖNETİMİ**\n\n(Sadece Personel) Geri bildirim.",
        "fin_help": "💰\n\n**FİNANSAL YARDIM**\n\nMikro hibeler için başvurun.",
        "res_help": "🛠️\n\n**KAYNAK VE YARDIM**\n\nAraç, gönüllü veya yer bulun.",
        "sub_title": "Ne tür bir desteğe ihtiyacınız var?",
        "offline": "📡 **Çevrimdışısınız.** Yazdıklarınız kaydediliyor.",
        "next": "İleri ➔", "back": "⬅ Geri", "submit_final": "✅ Gönder",
        "settings": "⚙️ Ayarlar", "lite": "Lite Mod (Yavaş İnternet)"
    },
    "GR": {
        "feed_btn": "💬\n\n**ΡΟΗ ΚΟΙΝΟΤΗΤΑΣ**\n\nΔείτε τι προτείνουν οι γείτονες.",
        "dash_btn": "👤\n\n**ΤΟ DASHBOARD ΜΟΥ**\n\nΔιαχειριστείτε τις ιδέες σας.",
        "submit_btn": "💡\n\n**ΥΠΟΒΟΛΗ ΙΔΕΑΣ**\n\nΑναφέρετε ένα πρόβλημα ή ιδέα.",
        "how_btn": "⚙️\n\n**ΠΩΣ ΛΕΙΤΟΥΡΓΕΙ**\n\nΠώς εξασφαλίζεται η δικαιοσύνη.",
        "success_btn": "🌟\n\n**ΙΣΤΟΡΙΕΣ ΕΠΙΤΥΧΙΑΣ**\n\nΘετικός αντίκτυπος στη γειτονιά.",
        "admin_btn": "🏢\n\n**ΔΗΜΟΤΙΚΗ ΑΡΧΗ**\n\n(Μόνο προσωπικό) Feedback.",
        "fin_help": "💰\n\n**ΟΙΚΟΝΟΜΙΚΗ ΒΟΗΘΕΙΑ**\n\nΑίτηση για μικροεπιχορηγήσεις.",
        "res_help": "🛠️\n\n**ΠΟΡΟΙ & ΒΟΗΘΕΙΑ**\n\nΒρείτε εργαλεία ή εθελοντές.",
        "sub_title": "Τι είδους υποστήριξη χρειάζεστε;",
        "offline": "📡 **Είστε εκτός σύνδεσης.** Αποθήκευση στη συσκευή.",
        "next": "Επόμενο ➔", "back": "⬅ Πίσω", "submit_final": "✅ Υποβολή",
        "settings": "⚙️ Ρυθμίσεις", "lite": "Lite Mode (Αργό Ίντερνετ)"
    },
    "RO": {
        "feed_btn": "💬\n\n**FLUX COMUNITATE**\n\nVezi ce sugerează vecinii tăi.",
        "dash_btn": "👤\n\n**DASHBOARD-UL MEU**\n\nGestionează ideile și profilul.",
        "submit_btn": "💡\n\n**TRIMITE O IDEE**\n\nRaportează o problemă sau o idee.",
        "how_btn": "⚙️\n\n**CUM FUNCȚIONEAZĂ**\n\nCum asigură algoritmul echitatea.",
        "success_btn": "🌟\n\n**POVEȘTI DE SUCCES**\n\nImpact pozitiv în cartier.",
        "admin_btn": "🏢\n\n**ADMINISTRAȚIE**\n\n(Doar Personal) Feedback.",
        "fin_help": "💰\n\n**AJUTOR FINANCIAR**\n\nAplică pentru micro-granturi.",
        "res_help": "🛠️\n\n**RESURSE ȘI AJUTOR**\n\nGăsește unelte sau voluntari.",
        "sub_title": "De ce fel de sprijin aveți nevoie?",
        "offline": "📡 **Ești offline.** Datele sunt salvate local.",
        "next": "Înainte ➔", "back": "⬅ Înapoi", "submit_final": "✅ Trimite",
        "settings": "⚙️ Setări", "lite": "Mod Lite (Internet lent)"
    }
}

# ==========================================
# 3. CUSTOM CSS
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    :root {
        --text-mint: #2dd4bf; 
        --text-white: #f8fafc;
    }

    .stApp {
        background: radial-gradient(circle at top left, #1e293b, #0f172a 50%, #020617 100%) !important;
        background-attachment: fixed !important;
        color: var(--text-white);
        font-family: 'Outfit', sans-serif !important;
    }

    .hero-title {
        text-align: center !important;
        font-size: 6.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #fff 0%, #2dd4bf 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 50px !important;
        width: 100% !important;
        display: block !important;
    }

    .page-title {
        text-align: center !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: var(--text-white) !important;
        margin-bottom: 20px !important;
    }

    div.stButton > button[kind="primary"] {
        background: transparent !important;
        border: none !important;
        width: 350px !important; height: 350px !important;
        position: relative !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important; 
        align-items: center !important;
        text-align: center !important;
        transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }

    div.stButton > button[kind="primary"] p:first-of-type {
        position: absolute !important;
        font-size: 250px !important; 
        opacity: 0.15 !important; 
        z-index: 0 !important; 
    }

    div.stButton > button[kind="primary"] strong {
        position: relative !important;
        z-index: 1 !important; 
        font-size: 26px !important; 
        text-shadow: 0px 4px 15px rgba(0,0,0,0.9) !important; 
    }

    div.stButton > button[kind="primary"] p:last-of-type {
        position: relative !important;
        z-index: 1 !important; 
        font-size: 16px !important;
        color: var(--text-mint) !important;
        text-shadow: 0px 2px 10px rgba(0,0,0,0.9) !important; 
    }

    div.stButton > button[kind="primary"]:hover { transform: translateY(-8px) scale(1.05) !important; }

    div.stButton > button[kind="secondary"] {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 50px !important; 
        color: transparent !important;  
        text-shadow: 0 0 0 var(--text-mint) !important; 
        font-size: 30px !important;
    }

    div.stButton > button[kind="tertiary"] {
        background: linear-gradient(135deg, #2dd4bf 0%, #0d9488 100%) !important;
        color: #ffffff !important; 
        border-radius: 12px !important;
        width: 100% !important;
        font-weight: 600 !important;
    }

    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #fff !important;
    }

    footer {visibility: hidden;}
    header {background-color: transparent !important;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. UI ELEMENTS
# ==========================================
lang = st.session_state.lang
txt = T[lang]

with st.sidebar:
    st.markdown(f"<h2 style='text-align: center;'>{txt['settings']}</h2>", unsafe_allow_html=True)
    st.session_state.lite_mode = st.toggle(txt['lite'], value=st.session_state.lite_mode)

col_empty, col_lang = st.columns([8, 1])
with col_lang:
    selected_lang = st.selectbox("Lang", ["DE", "EN", "TR", "GR", "RO"], index=["DE", "EN", "TR", "GR", "RO"].index(lang), label_visibility="collapsed")
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

# ==========================================
# 5. PAGES
# ==========================================
def home_page():
    st.markdown("<div class='hero-title'>ROBIN</div>", unsafe_allow_html=True)
    _, col1, col2, col3, _ = st.columns([0.5, 2.5, 2.5, 2.5, 0.5])
    with col1:
        if st.button(txt['feed_btn'], type="primary"): navigate_to('feed')
        if st.button(txt['dash_btn'], type="primary"): navigate_to('dashboard')
    with col2:
        if st.button(txt['submit_btn'], type="primary"): navigate_to('submit_choice')
        if st.button(txt['how_btn'], type="primary"): navigate_to('how_it_works')
    with col3:
        if st.button(txt['success_btn'], type="primary"): navigate_to('success')
        if st.button(txt['admin_btn'], type="primary"): navigate_to('admin')

def submit_choice_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown(f"<div class='page-title'>{txt['sub_title']}</div><br>", unsafe_allow_html=True)
    _, col1, col2, _ = st.columns([1, 2.5, 2.5, 1])
    with col1:
        if st.button(txt['fin_help'], type="primary"): navigate_to('home') # Simplified for demo
    with col2:
        if st.button(txt['res_help'], type="primary"): navigate_to('home')

# Simplified routing
if st.session_state.page == 'home': home_page()
elif st.session_state.page == 'submit_choice': submit_choice_page()
else:
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown(f"<div class='page-title'>{st.session_state.page.upper()}</div>", unsafe_allow_html=True)
