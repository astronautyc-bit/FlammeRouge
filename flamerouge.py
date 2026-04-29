import streamlit as st
import random

# --- Configuratie & Constanten ---
st.set_page_config(page_title="Flamme Rouge Automator", page_icon="🚴", layout="centered")

# CSS HACK: Import Oswald font, force ALL-CAPS, eliminate whitespace EN Mobiele Optimalisatie
st.markdown("""
    <style>
        /* Import Oswald from Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;700&display=swap');

        /* Basis lettertype instellingen */
        html, body, [class*="css"], span, div, p, h1, h2, h3, h4, h5, h6, button, input, select, label {
            font-family: 'Oswald', sans-serif !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }

        /* VERGROOT DE STANDAARD TEKST VOOR LAPTOPS/TABLETS */
        p, span, label, button, div[data-baseweb="checkbox"] {
            font-size: 1.25rem !important; 
        }
        h3 { font-size: 2.2rem !important; }

        /* Zorg dat titels en dikgedrukte tekst echt knallen */
        h1, h2, h3, strong, b { font-weight: 700 !important; }

        .block-container {
            padding-top: 3rem !important; 
            padding-bottom: 1rem !important;
            max-width: 600px; 
        }
        div[data-testid="stVerticalBlock"] > div {
            padding-bottom: 0.1rem !important;
        }
        hr {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        h1, h2, h3 { padding-bottom: 0rem !important; }
        
        /* SPECIAL STYLING FOR EXHAUSTION CARD */
        button[kind="primary"] {
            background-color: rgba(255, 75, 75, 0.15) !important; 
            border: 1px solid #ff4b4b !important; 
        }
        button[kind="primary"] p {
            color: #ff4b4b !important; 
            font-weight: 700 !important; 
        }
        button[kind="primary"]:hover {
            background-color: rgba(255, 75, 75, 0.3) !important;
            border-color: #ff4b4b !important;
        }

        /* 📱 MOBIELE OPTIMALISATIE */
        @media (max-width: 600px) {
            p, span, label, button, div[data-baseweb="checkbox"] {
                font-size: 1.0rem !important; 
            }
            h3 { font-size: 1.6rem !important; }
            
            /* DE HORIZONTALE SCROLL-BOOSDOENER IS HIER VERWIJDERD! */
            
            button {
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
            }
            
            /* Maak de gestapelde kolommen op mobiel super strak en compact */
            div[data-testid="column"] {
                padding-bottom: 0rem !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

ROULEUR_CARDS = [3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7]
SPRINTER_CARDS = [2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 9, 9, 9]
EXHAUSTION_CARD = "vermoeidheidskaart (2)" 
ALL_COLORS = ["Blauw", "Rood", "Groen", "Zwart", "Wit", "Roze"]

COLOR_STYLES = {
    "Blauw": "background-color: #007BFF; color: white;",
    "Rood": "background-color: #DC3545; color: white;",
    "Groen": "background-color: #28A745; color: white;",
    "Zwart": "background-color: #212529; color: white; border: 1px solid #495057;",
    "Wit": "background-color: #F8F9FA; color: black; border: 1px solid #DEE2E6;",
    "Roze": "background-color: #FF69B4; color: black;"
}

# --- Klassen ---
class Cyclist:
    def __init__(self, rider_type, is_human=True):
        self.rider_type = rider_type
        self.is_human = is_human
        self.deck = ROULEUR_CARDS.copy() if rider_type == "Rouleur" else SPRINTER_CARDS.copy()
        random.shuffle(self.deck)
        self.played_card = None
        self.drawn_hand = [] 
        self.used_cards = [] 
        self.is_finished = False

    def draw_cards(self):
        if not self.deck:
            self.drawn_hand = []
            return
        draw_count = min(4, len(self.deck))
        hand = [self.deck.pop(0) for _ in range(draw_count)]
        hand.sort(key=lambda x: x if isinstance(x, int) else 2)
        self.drawn_hand = hand

    def play_card(self, card):
        self.played_card = card
        self.drawn_hand.remove(card)

    def undo_play(self):
        if self.played_card is not None and self.played_card != "🏁":
            self.drawn_hand.append(self.played_card)
            self.drawn_hand.sort(key=lambda x: x if isinstance(x, int) else 2)
            self.played_card = None

    def confirm_turn(self):
        if self.drawn_hand:
            self.deck.extend(self.drawn_hand)
            random.shuffle(self.deck)
            self.drawn_hand = []
        if self.played_card is not None and self.played_card != 0 and self.played_card != "🏁":
            self.used_cards.append(self.played_card)

    def play_auto(self):
        if self.is_finished:
            self.played_card = "🏁"
            return self.played_card
            
        if not self.deck:
            self.played_card = 0
        else:
            self.played_card = self.deck.pop(0)
            self.used_cards.append(self.played_card) 
        return self.played_card

    def add_exhaustion(self):
        if not self.is_finished:
            self.deck.append(EXHAUSTION_CARD)
            random.shuffle(self.deck)

    def get_inventory_html(self):
        base_cards = ROULEUR_CARDS.copy() if self.rider_type == "Rouleur" else SPRINTER_CARDS.copy()
        used_temp = self.used_cards.copy()
        
        html = "<div style='line-height: 1.8;'>"
        for card in base_cards:
            if card in used_temp:
                used_temp.remove(card)
                html += f"<span style='text-decoration: line-through; opacity: 0.4; margin-right: 12px;'>{card}</span>"
            else:
                html += f"<span style='font-weight: bold; margin-right: 12px;'>{card}</span>"
                
        ex_in_deck = self.deck.count(EXHAUSTION_CARD)
        ex_used = self.used_cards.count(EXHAUSTION_CARD)
        
        for _ in range(ex_used):
            html += f"<span style='text-decoration: line-through; opacity: 0.4; color: #ff4b4b; margin-right: 12px;'>2</span>"
        for _ in range(ex_in_deck):
            html += f"<span style='font-weight: bold; color: #ff4b4b; margin-right: 12px;'>2</span>"
            
        html += "</div>"
        return html

# --- Sessie Status ---
if 'phase' not in st.session_state:
    st.session_state.phase = 'setup'
    st.session_state.teams = []
    st.session_state.round = 1
    st.session_state.human_queue = [] 
    st.session_state.current_team_idx = None 
    st.session_state.show_hands = False

# --- Hulpfuncties ---
def start_game(num_humans, num_auto, human_names, human_colors):
    available_colors = ALL_COLORS.copy()
    for i in range(num_humans):
        color = human_colors[i]
        if color in available_colors: available_colors.remove(color)
        st.session_state.teams.append({
            "name": human_names[i] if human_names[i] else f"Speler {i+1}",
            "color": color, "is_human": True,
            "Rouleur": Cyclist("Rouleur", True), "Sprinter": Cyclist("Sprinter", True)
        })
    for i in range(num_auto):
        color = available_colors.pop(0)
        st.session_state.teams.append({
            "name": color, "color": color, "is_human": False,
            "Rouleur": Cyclist("Rouleur", False), "Sprinter": Cyclist("Sprinter", False)
        })
    start_round()

def start_round():
    st.session_state.human_queue = []
    for idx, team in enumerate(st.session_state.teams):
        team["Rouleur"].played_card = "🏁" if team["Rouleur"].is_finished else None
        team["Sprinter"].played_card = "🏁" if team["Sprinter"].is_finished else None
        
        if team["is_human"] and (not team["Rouleur"].is_finished or not team["Sprinter"].is_finished):
            st.session_state.human_queue.append(idx)
            
    if st.session_state.human_queue:
        st.session_state.current_team_idx = st.session_state.human_queue.pop(0)
        st.session_state.phase = 'playing'
        st.session_state.show_hands = False
    else:
        process_auto_teams()
        st.session_state.phase = 'summary'

def process_auto_teams():
    for team in st.session_state.teams:
        if not team["is_human"]:
            if not team["Rouleur"].is_finished: team["Rouleur"].play_auto()
            if not team["Sprinter"].is_finished: team["Sprinter"].play_auto()

def next_turn():
    st.session_state.show_hands = False
    if st.session_state.human_queue:
        st.session_state.current_team_idx = st.session_state.human_queue.pop(0)
    else:
        process_auto_teams()
        st.session_state.phase = 'summary'

# --- UI LOGICA ---

# 1. SETUP FASE
if st.session_state.phase == 'setup':
    st.markdown("### 🚴 Flamme Rouge Setup")
    col1, col2 = st.columns(2)
    with col1: num_humans = st.number_input("Menselijke Spelers", 0, 6, 2)
    with col2: num_auto = st.number_input("Automatische Teams", 0, 6 - num_humans, 6 - num_humans)

    human_names, human_colors = [], []
    for i in range(num_humans):
        c1, c2 = st.columns(2)
        with c1: human_names.append(st.text_input(f"Naam {i+1}", key=f"name_{i}"))
        with c2: human_colors.append(st.selectbox(f"Kleur {i+1}", ALL_COLORS, index=i, key=f"color_{i}"))

    if st.button("Start de Race! 🏁", use_container_width=True):
        if len(set(human_colors)) != len(human_colors): st.error("Unieke kleuren vereist!")
        else: start_game(num_humans, num_auto, human_names, human_colors); st.rerun()

# 2. SPEEL FASE
elif st.session_state.phase == 'playing':
    team_idx = st.session_state.current_team_idx
    team = st.session_state.teams[team_idx]

    style = COLOR_STYLES.get(team['color'], "color: white;")
    badge = f'<span style="{style} padding: 4px 12px; border-radius: 6px;">{team["name"]} ({team["color"]})</span>'
    st.markdown(f"### Ronde {st.session_state.round} | Beurt: {badge}", unsafe_allow_html=True)
    st.write("---")

    if not st.session_state.show_hands:
        if st.button("Toon mijn kaarten 👁️", use_container_width=True):
            if not team['Rouleur'].is_finished: team['Rouleur'].draw_cards()
            if not team['Sprinter'].is_finished: team['Sprinter'].draw_cards()
            st.session_state.show_hands = True
            st.rerun()
    else:
        if not team['Rouleur'].is_finished:
            st.markdown("**🚴 Rouleur**")
            if team['Rouleur'].played_card is None or team['Rouleur'].played_card == "🏁":
                if team['Rouleur'].drawn_hand:
                    btn_cols = st.columns(len(team['Rouleur'].drawn_hand))
                    for i, card in enumerate(team['Rouleur'].drawn_hand):
                        b_type = "primary" if card == EXHAUSTION_CARD else "secondary"
                        if btn_cols[i].button(f"**{card}**", key=f"r_{team_idx}_{i}", use_container_width=True, type=b_type):
                            team['Rouleur'].play_card(card)
                            st.rerun()
                else:
                    st.warning("Deck leeg!"); team['Rouleur'].played_card = 0
            else:
                c1, c2 = st.columns([3, 1])
                c1.success(f"**{team['Rouleur'].played_card}**")
                if c2.button("↩️", key=f"undo_r_{team_idx}", use_container_width=True): team['Rouleur'].undo_play(); st.rerun()

        if not team['Sprinter'].is_finished:
            st.markdown("**⚡ Sprinter**")
            if team['Sprinter'].played_card is None or team['Sprinter'].played_card == "🏁":
                if team['Sprinter'].drawn_hand:
                    btn_cols = st.columns(len(team['Sprinter'].drawn_hand))
                    for i, card in enumerate(team['Sprinter'].drawn_hand):
                        b_type = "primary" if card == EXHAUSTION_CARD else "secondary"
                        if btn_cols[i].button(f"**{card}**", key=f"s_{team_idx}_{i}", use_container_width=True, type=b_type):
                            team['Sprinter'].play_card(card)
                            st.rerun()
                else:
                    st.warning("Deck leeg!"); team['Sprinter'].played_card = 0
            else:
                c1, c2 = st.columns([3, 1])
                c1.success(f"**{team['Sprinter'].played_card}**")
                if c2.button("↩️", key=f"undo_s_{team_idx}", use_container_width=True): team['Sprinter'].undo_play(); st.rerun()

        if team['Rouleur'].played_card is not None and team['Sprinter'].played_card is not None:
            st.write("---")
            if st.button("Bevestig keuzes ➡️", use_container_width=True):
                if not team['Rouleur'].is_finished: team['Rouleur'].confirm_turn()
                if not team['Sprinter'].is_finished: team['Sprinter'].confirm_turn()
                next_turn()
                st.rerun()

# 3. OVERZICHT FASE
elif st.session_state.phase == 'summary':
    st.markdown(f"### 📋 Overzicht Ronde {st.session_state.round}")
    for team in st.session_state.teams:
        display_name = f"{team['name']} ({team['color']})" if team['is_human'] else team['color']
        style = COLOR_STYLES.get(team['color'], "background-color: gray; color: white;")
        badge = f'<span style="{style} padding: 4px 12px; border-radius: 6px; font-weight: bold;">{display_name}</span>'
        
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.markdown(badge, unsafe_allow_html=True)
        c2.markdown(f"Rouleur: **{team['Rouleur'].played_card}**")
        c3.markdown(f"Sprinter: **{team['Sprinter'].played_card}**")
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

    st.write("---")
    if st.button("Naar Vermoeidheidsfase ➡️", use_container_width=True):
        st.session_state.phase = 'exhaustion'
        st.rerun()

# 4. VERMOEIDHEIDSFASE
elif st.session_state.phase == 'exhaustion':
    st.markdown("### 🥵 Vermoeidheidsfase")
    st.caption("Wie vangt de wind? Vink de renners aan die een kaart ontvangen.")
    
    selected_exhaustion = []
    for idx, team in enumerate(st.session_state.teams):
        if team['Rouleur'].is_finished and team['Sprinter'].is_finished: continue
        
        display_name = f"{team['name']} ({team['color']})" if team['is_human'] else team['color']
        style = COLOR_STYLES.get(team['color'], "background-color: gray; color: white;")
        badge = f'<span style="{style} padding: 4px 12px; border-radius: 6px; font-weight: bold;">{display_name}</span>'
        
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1: st.markdown(badge, unsafe_allow_html=True)
        with c2: 
            if not team['Rouleur'].is_finished and st.checkbox("Rouleur", key=f"ex_{idx}_rouleur"): selected_exhaustion.append((team, "Rouleur"))
        with c3: 
            if not team['Sprinter'].is_finished and st.checkbox("Sprinter", key=f"ex_{idx}_sprinter"): selected_exhaustion.append((team, "Sprinter"))
        st.markdown("<div style='margin-bottom: 4px;'></div>", unsafe_allow_html=True)

    st.write("---")
    if st.button("Deel uit en ga naar Finishlijn ➡️", type="primary", use_container_width=True):
        for team, r_type in selected_exhaustion: team[r_type].add_exhaustion()
        st.session_state.phase = 'finish'
        st.rerun()

# 5. FINISH FASE
elif st.session_state.phase == 'finish':
    st.markdown("### 🏁 Finishlijn")
    st.caption("Is er iemand de finish gepasseerd? Vink ze hier aan.")
    
    selected_finished = []
    for idx, team in enumerate(st.session_state.teams):
        if team['Rouleur'].is_finished and team['Sprinter'].is_finished: continue
        
        display_name = f"{team['name']} ({team['color']})" if team['is_human'] else team['color']
        style = COLOR_STYLES.get(team['color'], "background-color: gray; color: white;")
        badge = f'<span style="{style} padding: 4px 12px; border-radius: 6px; font-weight: bold;">{display_name}</span>'
        
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1: st.markdown(badge, unsafe_allow_html=True)
        with c2: 
            if not team['Rouleur'].is_finished and st.checkbox("Rouleur", key=f"fin_{idx}_rouleur"): selected_finished.append((team, "Rouleur"))
        with c3: 
            if not team['Sprinter'].is_finished and st.checkbox("Sprinter", key=f"fin_{idx}_sprinter"): selected_finished.append((team, "Sprinter"))
        st.markdown("<div style='margin-bottom: 4px;'></div>", unsafe_allow_html=True)

    st.write("---")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Bevestig & Start Ronde 🔄", type="primary", use_container_width=True):
            for team, r_type in selected_finished: team[r_type].is_finished = True
            st.session_state.round += 1
            start_round()
            st.rerun()
            
    with col_btn2:
        if st.button("Bekijk Deck Inventaris 🗃️", use_container_width=True):
            st.session_state.phase = 'inventory'
            st.rerun()

# 6. INVENTARIS FASE
elif st.session_state.phase == 'inventory':
    st.markdown("### 🗃️ Deck Inventaris")
    st.caption("Doorgestreepte kaarten zijn weggespeeld. Rode kaarten zijn toegevoegde vermoeidheid.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    for team in st.session_state.teams:
        display_name = f"{team['name']} ({team['color']})" if team['is_human'] else team['color']
        style = COLOR_STYLES.get(team['color'], "background-color: gray; color: white;")
        badge = f'<span style="{style} padding: 4px 12px; border-radius: 6px; font-weight: bold;">{display_name}</span>'
        
        st.markdown(badge, unsafe_allow_html=True)
        
        r_title = "**Rouleur** 🏁" if team['Rouleur'].is_finished else "**Rouleur**"
        st.markdown(r_title)
        st.markdown(team['Rouleur'].get_inventory_html(), unsafe_allow_html=True)
        
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
        
        s_title = "**Sprinter** 🏁" if team['Sprinter'].is_finished else "**Sprinter**"
        st.markdown(s_title)
        st.markdown(team['Sprinter'].get_inventory_html(), unsafe_allow_html=True)
        
        st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
        
    st.write("---")
    if st.button("⬅️ Terug", use_container_width=True):
        st.session_state.phase = 'finish'
        st.rerun()
