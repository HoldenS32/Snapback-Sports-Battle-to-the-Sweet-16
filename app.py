import streamlit as st
import pandas as pd
import random
import os
import altair as alt

st.set_page_config(
    page_title="Snapback Sports March Madness: Battle to the Sweet 16",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# TEAM COLORS (accent only)
# -----------------------------
TEAM_COLORS = {
    "Duke": "#003087",
    "Kansas": "#0051BA",
    "UConn": "#000E2F",
    "Houston": "#C8102E",
    "Gonzaga": "#041E42",
    "Arizona": "#CC0033",
    "North Carolina": "#7BAFD4",
    "Kentucky": "#0033A0",
    "Purdue": "#CFB991",
    "Michigan State": "#18453B",
}

# -----------------------------
# KEY PLAYER INSIGHTS (example)
# -----------------------------
PLAYER_NOTES = {
    "Duke": {
        "star": "Star Guard (All‑American caliber)",
        "note": "High‑usage creator; late‑game shot maker that boosts upset resistance.",
    },
    "Kansas": {
        "star": "Versatile Wing",
        "note": "Switchable defender who can guard 1–4; path may hinge on foul trouble.",
    },
    "UConn": {
        "star": "Dominant Big",
        "note": "Elite rim protector and rebounder; tough matchup for undersized opponents.",
    },
    "Houston": {
        "star": "Two‑way Guard",
        "note": "Drives the offense and sets tone defensively; key vs high‑tempo teams.",
    },
    "Gonzaga": {
        "star": "Stretch Big",
        "note": "Floor‑spacing big who pulls shot‑blockers away from the rim.",
    },
    "North Carolina": {
        "star": "Scoring Wing",
        "note": "Reliable 3‑level scorer; gives UNC a bailout option late in clock.",
    },
    "Purdue": {
        "star": "Interior Anchor",
        "note": "Post‑centric offense; matchup vs teams without size is a major advantage.",
    },
    "Kentucky": {
        "star": "Freshman Guard",
        "note": "High‑variance shooter; can swing games with hot or cold spells.",
    },
}

# -----------------------------
# TEAMS (from your bracket)
# -----------------------------
FIELD_2026 = [
    # East Region
    {"name": "Duke", "region": "East", "seed": 1},
    {"name": "Siena", "region": "East", "seed": 16},
    {"name": "Ohio State", "region": "East", "seed": 8},
    {"name": "TCU", "region": "East", "seed": 9},
    {"name": "St. John’s", "region": "East", "seed": 5},
    {"name": "Northern Iowa", "region": "East", "seed": 12},
    {"name": "Kansas", "region": "East", "seed": 4},
    {"name": "Cal Baptist", "region": "East", "seed": 13},
    {"name": "Louisville", "region": "East", "seed": 6},
    {"name": "South Florida", "region": "East", "seed": 11},
    {"name": "Michigan State", "region": "East", "seed": 3},
    {"name": "North Dakota State", "region": "East", "seed": 14},
    {"name": "UCLA", "region": "East", "seed": 7},
    {"name": "UCF", "region": "East", "seed": 10},
    {"name": "UConn", "region": "East", "seed": 2},
    {"name": "Furman", "region": "East", "seed": 15},

    # West Region
    {"name": "Arizona", "region": "West", "seed": 1},
    {"name": "Long Island", "region": "West", "seed": 16},
    {"name": "Villanova", "region": "West", "seed": 8},
    {"name": "Utah State", "region": "West", "seed": 9},
    {"name": "Wisconsin", "region": "West", "seed": 5},
    {"name": "High Point", "region": "West", "seed": 12},
    {"name": "Arkansas", "region": "West", "seed": 4},
    {"name": "Hawaii", "region": "West", "seed": 13},
    {"name": "BYU", "region": "West", "seed": 6},
    {"name": "Texas/NC State winner", "region": "West", "seed": 11},
    {"name": "Gonzaga", "region": "West", "seed": 3},
    {"name": "Kennesaw State", "region": "West", "seed": 14},
    {"name": "Miami (FL)", "region": "West", "seed": 7},
    {"name": "Missouri", "region": "West", "seed": 10},
    {"name": "Purdue", "region": "West", "seed": 2},
    {"name": "Queens (N.C.)", "region": "West", "seed": 15},

    # South Region
    {"name": "Florida", "region": "South", "seed": 1},
    {"name": "Prairie View A&M/Lehigh winner", "region": "South", "seed": 16},
    {"name": "Clemson", "region": "South", "seed": 8},
    {"name": "Iowa", "region": "South", "seed": 9},
    {"name": "Vanderbilt", "region": "South", "seed": 5},
    {"name": "McNeese", "region": "South", "seed": 12},
    {"name": "Nebraska", "region": "South", "seed": 4},
    {"name": "Troy", "region": "South", "seed": 13},
    {"name": "Tennessee", "region": "South", "seed": 6},
    {"name": "Miami (Ohio)/SMU winner", "region": "South", "seed": 11},
    {"name": "North Carolina", "region": "South", "seed": 3},
    {"name": "VCU", "region": "South", "seed": 14},
    {"name": "Illinois", "region": "South", "seed": 7},
    {"name": "Penn", "region": "South", "seed": 10},
    {"name": "Saint Mary’s", "region": "South", "seed": 2},
    {"name": "Texas A&M", "region": "South", "seed": 15},

    # Midwest Region
    {"name": "Michigan", "region": "Midwest", "seed": 1},
    {"name": "UMBC/Howard winner", "region": "Midwest", "seed": 16},
    {"name": "Georgia", "region": "Midwest", "seed": 8},
    {"name": "Saint Louis", "region": "Midwest", "seed": 9},
    {"name": "Texas Tech", "region": "Midwest", "seed": 5},
    {"name": "Akron", "region": "Midwest", "seed": 12},
    {"name": "Alabama", "region": "Midwest", "seed": 4},
    {"name": "Hofstra", "region": "Midwest", "seed": 13},
    {"name": "Tennessee State", "region": "Midwest", "seed": 6},
    {"name": "Wright State", "region": "Midwest", "seed": 11},
    {"name": "Kentucky", "region": "Midwest", "seed": 3},
    {"name": "Santa Clara", "region": "Midwest", "seed": 14},
    {"name": "Iowa State", "region": "Midwest", "seed": 7},
    {"name": "Virginia", "region": "Midwest", "seed": 10},
    {"name": "Houston", "region": "Midwest", "seed": 2},
    {"name": "Idaho", "region": "Midwest", "seed": 15},
]

# -----------------------------
# ROUND OF 64 MATCHUPS
# -----------------------------
GAMES_2026 = [
    # East
    ("East", "E1", "Duke", "Siena"),
    ("East", "E2", "Ohio State", "TCU"),
    ("East", "E3", "St. John’s", "Northern Iowa"),
    ("East", "E4", "Kansas", "Cal Baptist"),
    ("East", "E5", "Louisville", "South Florida"),
    ("East", "E6", "Michigan State", "North Dakota State"),
    ("East", "E7", "UCLA", "UCF"),
    ("East", "E8", "UConn", "Furman"),

    # West
    ("West", "W1", "Arizona", "Long Island"),
    ("West", "W2", "Villanova", "Utah State"),
    ("West", "W3", "Wisconsin", "High Point"),
    ("West", "W4", "Arkansas", "Hawaii"),
    ("West", "W5", "BYU", "Texas/NC State winner"),
    ("West", "W6", "Gonzaga", "Kennesaw State"),
    ("West", "W7", "Miami (FL)", "Missouri"),
    ("West", "W8", "Purdue", "Queens (N.C.)"),

    # South
    ("South", "S1", "Florida", "Prairie View A&M/Lehigh winner"),
    ("South", "S2", "Clemson", "Iowa"),
    ("South", "S3", "Vanderbilt", "McNeese"),
    ("South", "S4", "Nebraska", "Troy"),
    ("South", "S5", "Tennessee", "Miami (Ohio)/SMU winner"),
    ("South", "S6", "North Carolina", "VCU"),
    ("South", "S7", "Illinois", "Penn"),
    ("South", "S8", "Saint Mary’s", "Texas A&M"),

    # Midwest
    ("Midwest", "M1", "Michigan", "UMBC/Howard winner"),
    ("Midwest", "M2", "Georgia", "Saint Louis"),
    ("Midwest", "M3", "Texas Tech", "Akron"),
    ("Midwest", "M4", "Alabama", "Hofstra"),
    ("Midwest", "M5", "Tennessee State", "Wright State"),
    ("Midwest", "M6", "Kentucky", "Santa Clara"),
    ("Midwest", "M7", "Iowa State", "Virginia"),
    ("Midwest", "M8", "Houston", "Idaho"),
]

BRACKETS = {
    "East":    ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"],
    "West":    ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"],
    "South":   ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"],
    "Midwest": ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"],
}

# -----------------------------
# MODEL PROFILES (AI flavors)
# -----------------------------
MODEL_PROFILES = {
    "Balanced (default)": {},
    "Chalky AI": {"boost_top4": 1.08, "cut_10plus": 0.90},
    "Upset‑hunting AI": {"boost_5to12": 1.15, "cut_1to3": 0.90},
}

# -----------------------------
# HELPERS
# -----------------------------
def find_team_game(team_name: str, region: str):
    for reg, gid, t1, t2 in GAMES_2026:
        if reg == region and (t1 == team_name or t2 == team_name):
            return reg, gid, t1, t2
    return None

def build_round_of32_opponent(region: str, game_id: str):
    order = BRACKETS[region]
    idx = order.index(game_id)
    if idx % 2 == 0:
        paired_game_id = order[idx + 1]
    else:
        paired_game_id = order[idx - 1]

    for reg, gid, t1, t2 in GAMES_2026:
        if reg == region and gid == paired_game_id:
            return t1, t2
    return None, None

def favored_status(seed_self: int, seed_opp_low: int, seed_opp_high: int):
    avg_opp_seed = (seed_opp_low + seed_opp_high) / 2
    if seed_self < avg_opp_seed:
        return "Likely favored"
    if seed_self > avg_opp_seed:
        return "Likely underdog"
    return "Toss-up"

def upset_risk(seed_self: int, seed_opp: int):
    gap = seed_opp - seed_self
    if seed_self <= 4 and seed_opp in (10, 11, 12):
        return "High"
    if gap <= 2:
        return "Medium"
    if gap > 4:
        return "Low"
    return "Medium"

def path_difficulty(seed_self: int, seed_opp_r64: int, seed_opp32_1: int, seed_opp32_2: int):
    avg32 = (seed_opp32_1 + seed_opp32_2) / 2
    raw = (17 - seed_opp_r64) + 1.5 * (17 - avg32)
    return raw

def default_probs_for_seed(seed: int):
    if seed == 1:
        return 90, 75
    if seed == 2:
        return 85, 70
    if seed == 3:
        return 80, 65
    if seed == 4:
        return 78, 62
    if seed in (5, 6):
        return 70, 55
    if seed in (7, 8):
        return 65, 50
    if seed in (9, 10):
        return 60, 45
    return 55, 40

def apply_model_profile(seed: int, p64: int, p32: int, profile: dict):
    mult = 1.0
    if seed <= 3 and "cut_1to3" in profile:
        mult = profile["cut_1to3"]
    if seed <= 4 and "boost_top4" in profile:
        mult = profile["boost_top4"]
    if 5 <= seed <= 12 and "boost_5to12" in profile:
        mult = profile["boost_5to12"]
    if seed >= 10 and "cut_10plus" in profile:
        mult = profile["cut_10plus"]
    p64_adj = min(int(p64 * mult), 98)
    p32_adj = min(int(p32 * mult), 95)
    return p64_adj, p32_adj

def estimated_public_pick_rate(seed: int) -> float:
    base = {
        1: 0.85, 2: 0.75, 3: 0.65, 4: 0.60,
        5: 0.45, 6: 0.40, 7: 0.30, 8: 0.25,
        9: 0.20, 10: 0.18, 11: 0.15,
        12: 0.12, 13: 0.08, 14: 0.05, 15: 0.03, 16: 0.01,
    }
    return base.get(seed, 0.20)

def describe_pod(seed, p64, p32, prob_two_game):
    if prob_two_game >= 0.50:
        return "Heavy favorite to survive the weekend."
    if prob_two_game >= 0.30:
        return "Solid but vulnerable Sweet‑16 candidate."
    if prob_two_game >= 0.15:
        return "Classic live underdog with real Cinderella upside."
    return "Long‑shot to reach the Sweet 16; better as upset fodder."

def build_region_summary(region: str, seed_range=None):
    rows = []
    for t in FIELD_2026:
        if t["region"] != region:
            continue
        if seed_range is not None:
            min_s, max_s = seed_range
            if not (min_s <= t["seed"] <= max_s):
                continue

        name = t["name"]
        seed = t["seed"]
        game = find_team_game(name, region)
        if not game:
            continue
        _, gid, t1, t2 = game
        opp = t2 if t1 == name else t1
        seed_opp = next(x["seed"] for x in FIELD_2026 if x["name"] == opp)
        status_r64 = favored_status(seed, seed_opp, seed_opp)
        risk = upset_risk(seed, seed_opp)

        r32_1, r32_2 = build_round_of32_opponent(region, gid)
        if r32_1 and r32_2:
            r32_pair = f"{r32_1} / {r32_2}"
            s1 = next(x["seed"] for x in FIELD_2026 if x["name"] == r32_1)
            s2 = next(x["seed"] for x in FIELD_2026 if x["name"] == r32_2)
            status_r32 = favored_status(seed, s1, s2)
            pdiff = path_difficulty(seed, seed_opp, s1, s2)
        else:
            r32_pair = "-"
            status_r32 = "-"
            pdiff = None

        rows.append(
            {
                "Team": name,
                "Seed": seed,
                "R64 Opponent": opp,
                "R64 Opp Seed": seed_opp,
                "R64 Status": status_r64,
                "Upset Risk": risk,
                "R32 Opp Pair": r32_pair,
                "R32 Status": status_r32,
                "Path Difficulty Score": pdiff,
            }
        )

    df = pd.DataFrame(rows).sort_values(["Seed", "Team"])
    if not df.empty and df["Path Difficulty Score"].notna().any():
        q = df["Path Difficulty Score"].quantile([0.33, 0.66])
        def label_pd(x):
            if pd.isna(x):
                return "-"
            if x <= q[0.33]:
                return "Easy"
            if x <= q[0.66]:
                return "Medium"
            return "Hard"
        df["Path Label"] = df["Path Difficulty Score"].apply(label_pd)
    else:
        df["Path Label"] = "-"
    return df

def style_upset_risk(df: pd.DataFrame):
    def color_cell(val):
        if val == "High":
            return "background-color: #ffcccc"
        if val == "Medium":
            return "background-color: #ffe4b3"
        if val == "Low":
            return "background-color: #d6f5d6"
        return ""
    def color_pd(val):
        if val == "Easy":
            return "background-color: #d6f5d6"
        if val == "Medium":
            return "background-color: #ffe4b3"
        if val == "Hard":
            return "background-color: #ffcccc"
        return ""
    styled = df.style.applymap(color_cell, subset=["Upset Risk"])
    if "Path Label" in df.columns:
        styled = styled.applymap(color_pd, subset=["Path Label"])
    return styled

# -----------------------------
# APP
# -----------------------------
def main():
    st.markdown(
        """
        <h1 style='text-align:center;'>
        Snapback Sports March Madness: Battle to the Sweet 16 🏀
        </h1>
        <p style='text-align:center;color:#777;'>
        Built for the Snapback AI Interns prompt — focus on two‑game paths, not just single upsets or full‑bracket champs.
        </p>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("What this tool does", expanded=False):
        st.markdown(
            "- Looks at Round of 64 + Round of 32 as a two‑game pod.\n"
            "- Lets you plug in win probabilities from any model or odds source.\n"
            "- Highlights upset risk, path difficulty, and leverage vs the field."
        )

    tab_team, tab_region, tab_compare = st.tabs(
        ["Team Explorer", "Region Overview", "Compare & Simulate"]
    )

    regions = ["All", "East", "West", "South", "Midwest"]

    # ------------- TEAM EXPLORER -------------
    with tab_team:
        st.subheader("How to use this view")
        st.caption(
            "Filter by region and seed, pick a team, then explore its 4‑team pod, "
            "win probabilities, and Sweet‑16 odds."
        )

        st.sidebar.header("Team Explorer filters")
        region_filter = st.sidebar.selectbox("Region", regions, index=0, key="detail_region")
        min_seed, max_seed = st.sidebar.slider(
            "Seed range", min_value=1, max_value=16, value=(1, 16), key="detail_seed_range"
        )
        model_profile_name = st.sidebar.selectbox(
            "AI model profile", list(MODEL_PROFILES.keys()), index=0
        )
        model_profile = MODEL_PROFILES[model_profile_name]

        filtered = []
        for t in FIELD_2026:
            if region_filter != "All" and t["region"] != region_filter:
                continue
            if not (min_seed <= t["seed"] <= max_seed):
                continue
            filtered.append(t)

        if not filtered:
            st.error("No teams match the current filters.")
            return

        labels = [f"{t['name']} ({t['region']} {t['seed']})" for t in filtered]
        name_to_team = {labels[i]: filtered[i] for i in range(len(filtered))}

        selected_label = st.selectbox("Choose a team", labels, index=0)
        team = name_to_team[selected_label]

        region = team["region"]
        name = team["name"]
        seed = team["seed"]

        game = find_team_game(name, region)
        if game is None:
            st.error("Could not find this team's Round of 64 game in the data.")
            return

        reg, gid, t1, t2 = game
        opp1 = t2 if t1 == name else t1

        accent_color = TEAM_COLORS.get(name, "#1f77b4")
        col_logo, col_title = st.columns([1, 3], gap="medium")
        with col_logo:
            if name == "Texas/NC State winner":
                for school in ["Texas", "NC State"]:
                    logo_path = os.path.join("logos", f"{school}.png")
                    if os.path.exists(logo_path):
                        st.image(logo_path, width=60, caption=school)
            elif name == "Prairie View A&M/Lehigh winner":
                for school in ["Prairie View A&M", "Lehigh"]:
                    logo_path = os.path.join("logos", f"{school}.png")
                    if os.path.exists(logo_path):
                        st.image(logo_path, width=60, caption=school)
            elif name == "UMBC/Howard winner":
                for school in ["UMBC", "Howard"]:
                    logo_path = os.path.join("logos", f"{school}.png")
                    if os.path.exists(logo_path):
                        st.image(logo_path, width=60, caption=school)
            elif name == "Miami (Ohio)/SMU winner":
                for school in ["Miami (Ohio)", "SMU"]:
                    logo_path = os.path.join("logos", f"{school}.png")
                    if os.path.exists(logo_path):
                        st.image(logo_path, width=60, caption=school)
            else:
                logo_path = os.path.join("logos", f"{name}.png")
                if os.path.exists(logo_path):
                    st.image(logo_path, width=80)

        with col_title:
            st.markdown(
                f"<div style='padding:10px;border-radius:8px;background-color:{accent_color}20;'>"
                f"<strong>{name}</strong> – {region} Region, {seed}-seed"
                f"</div>",
                unsafe_allow_html=True,
            )
        st.caption(f"Model profile: {model_profile_name}")

        col_left, col_right = st.columns([2, 1], gap="large")

        # LEFT: pod, path, probabilities, simulation
        with col_left:
            with st.container(border=True):
                st.subheader("Interactive 4‑team pod")

                opp32_t1, opp32_t2 = build_round_of32_opponent(region, gid)
                if opp32_t1 and opp32_t2:
                    def seed_of(n):
                        return next(t["seed"] for t in FIELD_2026 if t["name"] == n)
                    s1 = seed_of(t1)
                    s2 = seed_of(t2)
                    s3 = seed_of(opp32_t1)
                    s4 = seed_of(opp32_t2)

                    st.caption("Fill out the mini‑bracket for this pod.")

                    col_g1, col_g2 = st.columns(2)

                    with col_g1:
                        st.markdown("**Game 1**")
                        winner_g1_label = st.radio(
                            "Winner of Game 1",
                            [f"{t1} ({s1})", f"{t2} ({s2})"],
                            key=f"pod_g1_{name}",
                        )

                    with col_g2:
                        st.markdown("**Game 2**")
                        winner_g2_label = st.radio(
                            "Winner of Game 2",
                            [f"{opp32_t1} ({s3})", f"{opp32_t2} ({s4})"],
                            key=f"pod_g2_{name}",
                        )

                    winner_g1 = winner_g1_label.split(" (")[0]
                    winner_g2 = winner_g2_label.split(" (")[0]

                    st.markdown("**Pod winner (advances to Sweet 16):**")
                    pod_winner = st.radio(
                        "Who do you advance from this pod?",
                        [winner_g1, winner_g2],
                        key=f"pod_winner_{name}",
                    )

                    st.markdown(
                        f"""
                        <div style="padding:10px;border-radius:6px;background-color:#F5F5F8;">
                        <strong>Pod winners selected:</strong><br>
                        Game 1: {winner_g1_label}<br>
                        Game 2: {winner_g2_label}<br><br>
                        <strong>Sweet 16 from this pod:</strong> {pod_winner}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown("#### Pod selections context")
                    for sel in {winner_g1, winner_g2, pod_winner}:
                        sel_team = next(t for t in FIELD_2026 if t["name"] == sel)
                        sel_seed = sel_team["seed"]
                        sel_region = sel_team["region"]
                        sel_game = find_team_game(sel, sel_region)
                        if not sel_game:
                            continue
                        _, sel_gid, st1_, st2_ = sel_game
                        sel_opp = st2_ if st1_ == sel else st1_
                        sel_opp_seed = next(t["seed"] for t in FIELD_2026 if t["name"] == sel_opp)
                        sel_status = favored_status(sel_seed, sel_opp_seed, sel_opp_seed)
                        sel_risk = upset_risk(sel_seed, sel_opp_seed)

                        st.markdown(
                            f"**{sel} ({sel_region} {sel_seed})** – vs {sel_opp} (seed {sel_opp_seed}), "
                            f"{sel_status}, upset risk: {sel_risk}"
                        )
                else:
                    st.info("Pod data unavailable for this matchup.")

            st.divider()

            with st.container(border=True):
                st.subheader("Win probabilities & Sweet‑16 odds")
                st.caption(
                    "Set these using your own beliefs, betting lines, or an external model."
                )

                col1, col2 = st.columns(2)
                base_p64, base_p32 = default_probs_for_seed(seed)
                base_p64, base_p32 = apply_model_profile(seed, base_p64, base_p32, model_profile)

                with col1:
                    p64 = st.slider(
                        "Chance to win Round of 64 (%)",
                        min_value=0,
                        max_value=100,
                        value=base_p64,
                        key=f"p64_{name}",
                    )
                with col2:
                    p32 = st.slider(
                        "Chance to win Round of 32 (%)",
                        min_value=0,
                        max_value=100,
                        value=base_p32,
                        key=f"p32_{name}",
                    )

                prob_two_game = (p64 / 100) * (p32 / 100)
                st.markdown(
                    f"""
                    <div style="padding:10px;border-radius:6px;background-color:#F5F5F8;">
                    <strong>Estimated Sweet‑16 chance:</strong> {prob_two_game*100:.1f}% 
                    <span style="color:#777;">(= {p64}% × {p32}%)</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                summary_sentence = describe_pod(seed, p64, p32, prob_two_game)
                st.markdown(
                    f"<p style='color:#555;font-style:italic;margin-top:6px;'>{summary_sentence}</p>",
                    unsafe_allow_html=True,
                )

                with st.expander("Simulate this team’s first two rounds"):
                    st.caption(
                        "Random simulations using the probabilities above."
                    )
                    num_sims = st.number_input(
                        "Number of simulations",
                        min_value=100,
                        max_value=20000,
                        value=1000,
                        step=100,
                        key=f"sims_{name}",
                    )
                    if st.button("Run simulation", key=f"run_sim_{name}"):
                        wins_both = 0
                        for _ in range(int(num_sims)):
                            r64_win = random.random() < (p64 / 100)
                            if not r64_win:
                                continue
                            r32_win = random.random() < (p32 / 100)
                            if r32_win:
                                wins_both += 1
                        est = wins_both / num_sims * 100
                        st.write(
                            f"In {int(num_sims)} simulations, {name} reached the Sweet 16 "
                            f"{wins_both} times."
                        )
                        st.write(f"Simulated Sweet 16 rate: **{est:.1f}%**")

        # RIGHT: key player + notes
        with col_right:
            with st.container(border=True):
                st.subheader("Key player insight")
                note = PLAYER_NOTES.get(name)
                if note:
                    st.markdown(
                        f"**Star:** {note['star']}\n\n"
                        f"**Why it matters:** {note['note']}"
                    )
                else:
                    st.write(
                        "No specific player insight added yet. Add star usage, "
                        "matchup advantages, or injury concerns here."
                    )

            st.divider()
            with st.container(border=True):
                st.subheader("Notes & scouting report")
                notes_key = f"notes_{name}"
                if notes_key not in st.session_state:
                    st.session_state[notes_key] = ""
                _notes = st.text_area(
                    f"Notes for {selected_label}",
                    key=notes_key,
                    value=st.session_state[notes_key],
                    placeholder="Matchup thoughts, injuries, betting angles, etc.",
                    height=150,
                )

    # ------------- REGION OVERVIEW -------------
    with tab_region:
        st.subheader("Region overview")
        st.caption(
            "Scan an entire region’s Round‑of‑64 opponents, upset risk, and path difficulty at once."
        )

        region_sum = st.selectbox(
            "Region", ["East", "West", "South", "Midwest"], index=0, key="sum_region"
        )
        seed_min, seed_max = st.slider(
            "Seed range (summary)",
            min_value=1,
            max_value=16,
            value=(1, 16),
            key="sum_seed_range",
        )
        df_sum = build_region_summary(region_sum, (seed_min, seed_max))
        if df_sum.empty:
            st.info("No teams in this region/seed range.")
        else:
            st.dataframe(style_upset_risk(df_sum), use_container_width=True)

    # ------------- COMPARE & SIMULATE -------------
    with tab_compare:
        st.subheader("Compare teams within a region")
        st.caption(
            "Pick multiple teams from the same region to compare their first two games, "
            "upset risk, path difficulty, and two‑game advancement probability."
        )

        region_comp = st.selectbox(
            "Region", ["East", "West", "South", "Midwest"], index=0, key="comp_region"
        )

        region_teams = [
            f"{t['name']} (Seed {t['seed']})"
            for t in FIELD_2026
            if t["region"] == region_comp
        ]
        selected_multi = st.multiselect(
            "Teams to compare (same region)",
            region_teams,
            max_selections=6,
        )

        if selected_multi:
            rows = []
            for label in selected_multi:
                name_part = label.split(" (Seed")[0]
                team = next(
                    t
                    for t in FIELD_2026
                    if t["name"] == name_part and t["region"] == region_comp
                )
                name = team["name"]
                seed = team["seed"]

                game = find_team_game(name, region_comp)
                if not game:
                    continue
                _, gid, t1, t2 = game
                opp = t2 if t1 == name else t1
                seed_opp = next(
                    x["seed"] for x in FIELD_2026 if x["name"] == opp
                )
                status_r64 = favored_status(seed, seed_opp, seed_opp)
                risk = upset_risk(seed, seed_opp)

                r32_1, r32_2 = build_round_of32_opponent(region_comp, gid)
                if r32_1 and r32_2:
                    r32_pair = f"{r32_1} / {r32_2}"
                    s1 = next(
                        x["seed"] for x in FIELD_2026 if x["name"] == r32_1
                    )
                    s2 = next(
                        x["seed"] for x in FIELD_2026 if x["name"] == r32_2
                    )
                    pdiff = path_difficulty(seed, seed_opp, s1, s2)
                else:
                    r32_pair = "-"
                    pdiff = None

                p64_def, p32_def = default_probs_for_seed(seed)
                p64_def, p32_def = apply_model_profile(
                    seed, p64_def, p32_def, MODEL_PROFILES["Balanced (default)"]
                )
                prob = (p64_def / 100) * (p32_def / 100)
                public_pick = estimated_public_pick_rate(seed)
                leverage = prob - public_pick

                rows.append(
                    {
                        "Team": name,
                        "Seed": seed,
                        "R64 Opponent": opp,
                        "R64 Opp Seed": seed_opp,
                        "R64 Status": status_r64,
                        "Upset Risk": risk,
                        "R32 Opp Pair": r32_pair,
                        "Path Difficulty Score": pdiff,
                        "Default P(2-game) %": prob * 100,
                        "Est. Field Pick %": public_pick * 100,
                        "Leverage (pts)": leverage * 100,
                    }
                )

            df_comp = pd.DataFrame(rows).sort_values(["Seed", "Team"])
            df_disp = df_comp.copy()
            df_disp["Default P(2-game) %"] = df_disp["Default P(2-game) %"].map(lambda x: f"{x:.1f}")
            df_disp["Est. Field Pick %"] = df_disp["Est. Field Pick %"].map(lambda x: f"{x:.1f}")
            df_disp["Leverage (pts)"] = df_disp["Leverage (pts)"].map(lambda x: f"{x:.1f}")
            st.dataframe(df_disp, use_container_width=True)

            st.markdown("#### Default two‑game odds (Balanced model)")
            chart_df = df_comp[["Team", "Seed", "Default P(2-game) %"]].copy()
            chart = (
                alt.Chart(chart_df)
                .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
                .encode(
                    x=alt.X("Team:N", sort="-y"),
                    y=alt.Y("Default P(2-game) %:Q", title="2‑game probability (%)"),
                    color=alt.Color("Seed:O", legend=alt.Legend(title="Seed")),
                    tooltip=["Team", "Seed", "Default P(2-game) %"],
                )
                .properties(height=300)
            )
            st.altair_chart(chart, use_container_width=True)

            st.markdown("#### Leverage vs estimated public picks")
            lev_df = df_comp[["Team", "Leverage (pts)"]].copy()
            lev_chart = (
                alt.Chart(lev_df)
                .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
                .encode(
                    x=alt.X("Team:N", sort="-y"),
                    y=alt.Y("Leverage (pts):Q", title="Edge (prob − field pick, pts)"),
                    tooltip=["Team", "Leverage (pts)"],
                )
                .properties(height=250)
            )
            st.altair_chart(lev_chart, use_container_width=True)

            if len(df_comp) == 2:
                t1, t2 = df_comp.iloc[0], df_comp.iloc[1]
                p1 = t1["Default P(2-game) %"]
                p2 = t2["Default P(2-game) %"]
                if abs(p1 - p2) < 2:
                    st.info(
                        f"Based on default probabilities and path difficulty, "
                        f"{t1['Team']} and {t2['Team']} are essentially even "
                        f"for reaching the Sweet 16."
                    )
                else:
                    better = t1 if p1 > p2 else t2
                    worse = t2 if p1 > p2 else t1
                    st.success(
                        f"Based on default probabilities and path difficulty, "
                        f"**{better['Team']}** has a clearer path to the Sweet 16 "
                        f"than {worse['Team']}."
                    )
        else:
            st.info("Select 1–6 teams from this region to compare.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"App crashed with error: {e}")