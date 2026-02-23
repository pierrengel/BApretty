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
# 2. CUSTOM CSS (GIANT EMOJI BUTTONS)
# ==========================================
st.markdown("""
    <style>
    /* Fixed the font import bug by moving it inside the style tag! */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    /* Global Variables */
    :root {
        --app-bg: #1b263b;         
        --text-mint: #2dd4bf; 
        --text-white: #f8fafc;
        --text-muted: #94a3b8;
    }

    /* Base App Styling */
    .stApp {
        background: radial-gradient(circle at top left, #1e293b, #0f172a 50%, #020617 100%) !important;
        background-attachment: fixed !important;
        color: var(--text-white);
        font-family: 'Outfit', sans-serif !important;
    }

    /* Headings */
    h1, h2, h3, h4, p, label, .stMarkdown {
        font-family: 'Outfit', sans-serif !important;
    }
    
    h1 {
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        background: linear-gradient(135deg, #fff 0%, #2dd4bf 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* =========================================
       STYLE 1: GIANT EMOJI BUTTONS (Primary) 
       ========================================= */
    div.stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    div.stButton > button[kind="primary"] {
        /* Remove the box background entirely */
        background: transparent !important;
        border: none !important;
        
        /* STRICT ABSOLUTE SIZING */
        width: 350px !important;
        height: 350px !important;
        min-width: 350px !important;
        max-width: 350px !important;
        min-height: 350px !important;
        max-height: 350px !important;
        
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-sizing: border-box !important;
        
        /* TEXT ALIGNMENT - Centered over the emoji */
        position: relative !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important; 
        align-items: center !important;
        text-align: center !important;
        overflow: hidden !important; 
        
        transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        box-shadow: none !important; /* No more box shadow */
    }

    /* 1. Giant Background Emoji Styling */
    div.stButton > button[kind="primary"] p:first-of-type {
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        font-size: 250px !important; /* Massive Emoji */
        line-height: 1 !important;
        margin: 0 !important;
        opacity: 0.15 !important; /* Semi-transparent */
        z-index: 0 !important; /* Send to back */
        transition: all 0.3s ease !important;
    }

    /* 2. Bold Title Styling */
    div.stButton > button[kind="primary"] strong {
        position: relative !important;
        z-index: 1 !important; /* Bring to front */
        font-size: 28px !important; 
        font-weight: 800 !important;
        display: block !important;  
        margin-bottom: 15px !important; 
        color: var(--text-white) !important;
        line-height: 1.2 !important;
        letter-spacing: 0.5px !important;
        text-shadow: 0px 4px 15px rgba(0,0,0,0.9) !important; /* Makes text pop over the emoji */
    }

    /* 3. Description Text Styling */
    div.stButton > button[kind="primary"] p:last-of-type {
        position: relative !important;
        z-index: 1 !important; /* Bring to front */
        font-size: 18px !important;
        font-weight: 400 !important;
        line-height: 1.5 !important;
        color: var(--text-mint) !important;
        margin: 0 !important;
        text-shadow: 0px 2px 10px rgba(0,0,0,0.9) !important; /* Makes text pop over the emoji */
    }

    /* Premium Hover Effects */
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-8px) scale(1.05) !important;
        background: transparent !important; 
    }
    
    /* Make the emoji glow and grow on hover */
    div.stButton > button[kind="primary"]:hover p:first-of-type {
        opacity: 0.35 !important;
        transform: translate(-50%, -50%) scale(1.1) !important;
        filter: drop-shadow(0px 0px 20px rgba(45, 212, 191, 0.4)) !important;
    }
    
    div.stButton > button[kind="primary"]:hover strong {
        color: var(--text-mint) !important;
    }

    /* =========================================
       STYLE 2: THE BAT BUTTON (Secondary) 
       ========================================= */
    div.stButton > button[kind="secondary"] {
        background: rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 50px !important; 
        color: transparent !important;  
        text-shadow: 0 0 0 var(--text-mint) !important; 
        font-size: 30px !important;
        padding: 10px 25px !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button[kind="secondary"]:hover {
        transform: scale(1.1) rotate(-10deg) !important; 
        background: rgba(45, 212, 191, 0.1) !important; 
        border-color: var(--text-mint) !important;
    }

    /* =========================================
       STYLE 3: ACTION BUTTONS (Tertiary) 
       ========================================= */
    div.stButton > button[kind="tertiary"] {
        background: linear-gradient(135deg, #2dd4bf 0%, #0d9488 100%) !important;
        color: #ffffff !important; 
        border: none !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        width: 100% !important;
        padding: 15px !important;
        margin-top: 20px !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="tertiary"] p { color: #ffffff !important; }
    div.stButton > button[kind="tertiary"]:hover { 
        transform: translateY(-2px) !important;
        filter: brightness(1.1);
    }

    /* =========================================
       STYLE 4: PREMIUM FORM INPUTS
       ========================================= */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #fff !important;
        border-radius: 12px !important;
        padding: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus {
        border-color: var(--text-mint) !important;
    }

    /* Fixed Header */
    footer {visibility: hidden;}
    header {background-color: transparent !important;}
    
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. GLOBAL UI ELEMENTS (Sidebar & Language)
# ==========================================
lang = st.session_state.lang

with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>⚙️ Settings</h2>" if lang == "EN" else "<h2 style='text-align: center;'>⚙️ Einstellungen</h2>", unsafe_allow_html=True)
    lbl_lite = "Lite Mode (Slow Internet)" if lang == "EN" else "Lite-Modus (Langsames Internet)"
    st.session_state.lite_mode = st.toggle(lbl_lite, value=st.session_state.lite_mode)

col_empty, col_lang = st.columns([9, 1])
with col_lang:
    selected_lang = st.selectbox("Language", ["DE", "EN"], index=0 if lang == "DE" else 1, label_visibility="collapsed")
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

mock_ideas = [
    {"id": 1, "title": "Mehr Bänke im Nordpark" if lang == "DE" else "More benches in Nordpark", "desc": "Senioren brauchen mehr Sitzgelegenheiten." if lang == "DE" else "Seniors need more places to rest.", "sector": "Sektor 4", "tag": "Infrastruktur" if lang == "DE" else "Infrastructure"},
    {"id": 2, "title": "Straßenlaternen reparieren" if lang == "DE" else "Fix streetlights", "desc": "Nach 17 Uhr wird es dunkel." if lang == "DE" else "It gets dangerously dark.", "sector": "Sektor 2", "tag": "Sicherheit" if lang == "DE" else "Safety"}
]

# ==========================================
# 4. DIALOGS (Modals)
# ==========================================
dlg_title = "Warum unterstützen Sie das?" if lang == "DE" else "Why do you support this?"
@st.dialog(dlg_title)
def support_dialog(project_id, project_title):
    st.write("Grund auswählen:" if lang == "DE" else "Select your primary reason:")
    opts = ["Erhöht die Sicherheit", "Spart Geld", "Fördert die Gemeinschaft", "Sonstiges"] if lang == "DE" else ["Improves Safety", "Saves Money", "Builds Community", "Other"]
    reason = st.radio("Grund", opts, label_visibility="collapsed")
    
    if st.button("Bestätigen" if lang == "DE" else "Confirm Support", type="tertiary"):
        st.session_state.supported_projects.append(project_id)
        st.toast("Stimme gezählt!" if lang == "DE" else "Voice added!", icon="✅")
        time.sleep(1)
        st.rerun()

# ==========================================
# 5. PAGE ROUTING FUNCTIONS
# ==========================================

def home_page():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 5.5rem; margin-bottom: 50px;'>ROBIN</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        lbl_feed = "💬\n\n**COMMUNITY FEED**\n\nSehen Sie, was Ihre Nachbarn vorschlagen." if lang == "DE" else "💬\n\n**COMMUNITY FEED**\n\nSee what neighbors are suggesting."
        if st.button(lbl_feed, type="primary"): navigate_to('feed')
            
        lbl_dash = "👤\n\n**MEIN DASHBOARD**\n\nVerwalten Sie Ihre Ideen und Ihr Profil." if lang == "DE" else "👤\n\n**MY DASHBOARD**\n\nManage your ideas and profile."
        if st.button(lbl_dash, type="primary"): navigate_to('dashboard')

    with col2:
        lbl_submit = "💡\n\n**IDEE EINREICHEN**\n\nMelden Sie ein Problem oder eine Idee." if lang == "DE" else "💡\n\n**SUBMIT AN IDEA**\n\nReport a problem or share an idea."
        if st.button(lbl_submit, type="primary"): navigate_to('submit_choice')
            
        lbl_how = "⚙️\n\n**WIE ES FUNKTIONIERT**\n\nSo sorgt der Algorithmus für Fairness." if lang == "DE" else "⚙️\n\n**HOW IT WORKS**\n\nHow our algorithm ensures fairness."
        if st.button(lbl_how, type="primary"): navigate_to('how_it_works')
        
    with col3:
        lbl_success = "🌟\n\n**ERFOLGSGESCHICHTEN**\n\nPositive Veränderungen in der Nachbarschaft." if lang == "DE" else "🌟\n\n**SUCCESS STORIES**\n\nPositive impact in the neighborhood."
        if st.button(lbl_success, type="primary"): navigate_to('success')

        lbl_admin = "🏢\n\n**STADTVERWALTUNG**\n\n(Nur Personal) Feedback-Schleife schließen." if lang == "DE" else "🏢\n\n**CITY ADMIN**\n\n(Staff Only) Close the feedback loop."
        if st.button(lbl_admin, type="primary"): navigate_to('admin')


def submit_choice_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown("---")
    
    title = "Welche Art von Unterstützung benötigen Sie?" if lang == "DE" else "What kind of support do you need?"
    st.markdown(f"<h1 style='text-align: center;'>{title}</h1><br><br>", unsafe_allow_html=True)
    
    _, col1, col2, _ = st.columns([1, 2, 2, 1])
    
    with col1:
        lbl_fin = "💰\n\n**FINANZIELLE HILFE**\n\nBeantragen Sie Mikrostipendien oder Gemeindefinanzierung." if lang == "DE" else "💰\n\n**FINANCIAL HELP**\n\nApply for micro-grants or community funding."
        if st.button(lbl_fin, type="primary"):
            st.session_state.submission_type = "financial"
            st.session_state.wizard_step = 1
            navigate_to('submit')
            
    with col2:
        lbl_res = "🛠️\n\n**RESSOURCEN & HILFE**\n\nFinden Sie Werkzeuge, Freiwillige oder Platz für Ihr Projekt." if lang == "DE" else "🛠️\n\n**RESOURCES & HELP**\n\nFind tools, volunteers, or space for your project."
        if st.button(lbl_res, type="primary"):
            st.session_state.submission_type = "resources"
            st.session_state.wizard_step = 1
            navigate_to('submit')


def submit_page():
    if st.button("🦇", type="secondary"): navigate_to('submit_choice')
    
    st.markdown("---")
    st.warning("📡 **Sie sind offline.** Ihre Eingaben werden auf dem Gerät gespeichert." if lang == "DE" else "📡 **You are offline.** Your typing is automatically saved to your device.", icon="⚠️")
    
    st.markdown(f"<h1 style='text-align: center;'>{'IDEE EINREICHEN' if lang == 'DE' else 'SUBMIT AN IDEA'}</h1>", unsafe_allow_html=True)
    st.progress(st.session_state.wizard_step / 3.0)
    st.markdown("<br>", unsafe_allow_html=True)
    
    _, center, _ = st.columns([1, 2, 1])
    
    with center:
        with st.container(border=True): 
            if st.session_state.wizard_step == 1:
                st.subheader("1. Was ist das Problem oder die Idee?" if lang == "DE" else "1. What is the problem or idea?")
                
                assisted_mode = st.toggle("Assistenz-Modus aktivieren" if lang == "DE" else "Enable Assisted Mode", value=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                if not assisted_mode:
                    p_text = "Z.B. Der Bürgersteig auf der Hauptstraße ist kaputt..." if lang == "DE" else "E.g., The sidewalk on Main St. is broken..."
                    st.text_area("Beschreibung", placeholder=p_text, label_visibility="collapsed", key="ta_desc")
                    st.write("**Oder sprechen Sie eine Nachricht ein:**" if lang == "DE" else "**Or, record a voice message:**")
                    st.audio_input("Sprachaufnahme" if lang == "DE" else "Record your voice", label_visibility="collapsed")
                else:
                    if st.session_state.submission_type == "financial":
                        st.markdown("#### Geschätztes benötigtes Budget:" if lang == "DE" else "#### Estimated Budget Needed:")
                        b_opts = ["Bis zu 50€", "50€ - 200€", "200€ - 500€", "Mehr als 500€"] if lang == "DE" else ["Up to 50€", "50€ - 200€", "200€ - 500€", "Over 500€"]
                        st.selectbox("Budget", b_opts, label_visibility="collapsed", key="fin_budget")
                        
                        st.markdown("#### Art der Finanzierung:" if lang == "DE" else "#### Type of Funding:")
                        f_opts = ["Mikrozuschuss", "Spenden", "Stadtbudget"] if lang == "DE" else ["Micro-grant", "Donations", "City Budget"]
                        st.pills("Finanzierungstyp", f_opts, label_visibility="collapsed", key="fin_type")
                        
                        st.markdown("#### Projektphase:" if lang == "DE" else "#### Project Phase:")
                        p_opts = ["Nur eine Idee", "In Planung", "Startklar"] if lang == "DE" else ["Just an idea", "Planning", "Ready to start"]
                        st.pills("Phase", p_opts, label_visibility="collapsed", key="fin_phase")
    
                    else:
                        st.markdown("#### Um welche Art von Projekt handelt es sich?" if lang == "DE" else "#### What kind of project is it?")
                        t_opts = ["Schnelle Lösung", "Große Idee", "Sonstiges"] if lang == "DE" else ["Quick fix", "Big idea", "Other"]
                        st.pills("Typ", t_opts, label_visibility="collapsed", key="res_type")
                        
                        st.markdown("#### Welche Ressourcen benötigen Sie?" if lang == "DE" else "#### What resources do you need?")
                        r_opts = ["Hammer", "Arbeitsplatz", "Bohrmaschine", "3D-Drucker", "Farbe", "Holz", "Metall", "Lötkolben", "Laptop"] if lang == "DE" else ["Hammer", "Workspace", "Drill", "3D Printer", "Paint", "Wood", "Metal", "Soldering Iron", "Laptop"]
                        st.multiselect("Ressourcen", r_opts, label_visibility="collapsed", key="res_items")
                        
                        st.markdown("#### Möchten Sie sich persönlich treffen?" if lang == "DE" else "#### Do you want to meet face to face?")
                        st.pills("Treffen", ["Ja", "Nein"] if lang == "DE" else ["Yes", "No"], label_visibility="collapsed", key="res_meet")
                
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                if c1.button("Weiter ➔" if lang == "DE" else "Next ➔", type="tertiary"):
                    st.session_state.wizard_step = 2
                    st.rerun()
                if c2.button("💾 Entwurf speichern" if lang == "DE" else "💾 Save Draft", type="tertiary"):
                    st.toast("Entwurf lokal gespeichert!" if lang == "DE" else "Draft saved locally!", icon="💾")
    
            elif st.session_state.wizard_step == 2:
                st.subheader("2. Wo befindet sich das?" if lang == "DE" else "2. Where is this located?")
                st.text_input("Ort", placeholder="Z.B. Ecke 5. Straße und Elm" if lang == "DE" else "E.g., Corner of 5th and Elm", label_visibility="collapsed")
                
                if not st.session_state.lite_mode:
                    st.caption("*(Interaktive Karte würde hier laden, im Lite-Modus deaktiviert)*" if lang == "DE" else "*(Interactive map disabled in Lite Mode)*")
                    
                c1, c2, c3 = st.columns(3)
                if c1.button("⬅ Zurück" if lang == "DE" else "⬅ Back", type="tertiary"):
                    st.session_state.wizard_step = 1
                    st.rerun()
                if c2.button("Weiter ➔" if lang == "DE" else "Next ➔", type="tertiary"):
                    st.session_state.wizard_step = 3
                    st.rerun()
                if c3.button("💾 Entwurf" if lang == "DE" else "💾 Draft", type="tertiary"):
                    st.toast("Gespeichert!" if lang == "DE" else "Saved!", icon="💾")
    
            elif st.session_state.wizard_step == 3:
                st.subheader("3. Überprüfen & Einreichen" if lang == "DE" else "3. Review & Submit")
                st.info("Ihre Idee sieht gut aus. Bereit, sie mit der Community zu teilen?" if lang == "DE" else "Idea looks great. Ready to share?")
                
                c1, c2 = st.columns(2)
                if c1.button("⬅ Zurück" if lang == "DE" else "⬅ Back", type="tertiary"):
                    st.session_state.wizard_step = 2
                    st.rerun()
                if c2.button("✅ Einreichen" if lang == "DE" else "✅ Submit", type="tertiary"):
                    st.toast("Idee eingereicht! Sie werden bei Neuigkeiten benachrichtigt." if lang == "DE" else "Idea Submitted! You'll be notified.", icon="🎉")
                    st.session_state.wizard_step = 1
                    time.sleep(2)
                    navigate_to('home')


def feed_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown(f"<h1 style='text-align: center; font-size: 3rem;'>{'COMMUNITY-FEED' if lang == 'DE' else 'COMMUNITY FEED'}</h1>", unsafe_allow_html=True)
    st.info("📣 **Mikro-Erfolge:** Tom hat seine Leiter mit Anna geteilt." if lang == "DE" else "📣 **Micro-Wins:** Tom shared his ladder with Anna.", icon="✨")
    
    for idea in mock_ideas:
        with st.container(border=True):
            st.markdown(f"### {idea['title']}")
            st.write(idea['desc'])
            if idea['id'] in st.session_state.supported_projects:
                st.button("✅ Unterstützt" if lang == "DE" else "✅ Supported", disabled=True, key=f"btn_disabled_{idea['id']}")
            else:
                if st.button("🤝 Idee unterstützen" if lang == "DE" else "🤝 Support this Idea", key=f"btn_support_{idea['id']}", type="tertiary"):
                    support_dialog(idea['id'], idea['title'])

def dashboard_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown(f"<h1 style='text-align: center;'>{'MEIN DASHBOARD' if lang == 'DE' else 'MY DASHBOARD'}</h1>", unsafe_allow_html=True)
    st.write("Profil und Privatsphäre Einstellungen" if lang == "DE" else "Profile and Privacy settings")

def admin_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown(f"<h1 style='text-align: center;'>{'STADTVERWALTUNG' if lang == 'DE' else 'CITY ADMIN'}</h1>", unsafe_allow_html=True)

def how_it_works_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown(f"<h1 style='text-align: center;'>{'WIE ES FUNKTIONIERT' if lang == 'DE' else 'HOW IT WORKS'}</h1>", unsafe_allow_html=True)

def success_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown(f"<h1 style='text-align: center;'>{'ERFOLGSGESCHICHTEN' if lang == 'DE' else 'SUCCESS STORIES'}</h1>", unsafe_allow_html=True)

# ==========================================
# 6. MAIN CONTROLLER
# ==========================================
if st.session_state.page == 'home': home_page()
elif st.session_state.page == 'submit_choice': submit_choice_page()
elif st.session_state.page == 'feed': feed_page()
elif st.session_state.page == 'submit': submit_page()
elif st.session_state.page == 'dashboard': dashboard_page()
elif st.session_state.page == 'admin': admin_page()
elif st.session_state.page == 'how_it_works': how_it_works_page()
elif st.session_state.page == 'success': success_page()
