import streamlit as st
import pandas as pd
import os
import re
from PIL import Image

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Fashion Stylist",
    page_icon="👗",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #fff7fb, #f5f1ff);
}

.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.result-card {
    background: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 7px 25px rgba(0,0,0,0.10);
    margin-top: 25px;
}

.result-title {
    color: #8e3a66;
    font-size: 30px;
    font-weight: 800;
}

.tip {
    background: #fff4fa;
    padding: 18px;
    border-radius: 12px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">👗 AI Fashion Stylist</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Discover the best fashion style for your unique appearance.'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# DATASET PATH
# ============================================================

CSV_PATH = r"C:\Users\ASUS\OneDrive\Desktop\AI-fashion trend\recommendations (1).csv"

# ============================================================
# LOAD DATASET
# ============================================================

if not os.path.exists(CSV_PATH):

    st.error("❌ Dataset file not found.")

    st.info(
        "Please check the CSV_PATH in the code."
    )

    st.stop()

try:

    df = pd.read_csv(CSV_PATH)

except Exception as e:

    st.error("❌ Could not load the dataset.")

    st.error(str(e))

    st.stop()

# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

def clean_column_name(name):

    name = str(name).strip().lower()

    name = name.replace(" ", "_")
    name = name.replace("-", "_")

    name = re.sub(
        r"[^a-z0-9_]",
        "",
        name
    )

    return name


df.columns = [
    clean_column_name(column)
    for column in df.columns
]

df = df.dropna(how="all")

# ============================================================
# FIND REQUIRED COLUMNS
# ============================================================

def find_column(names):

    for name in names:

        name = clean_column_name(name)

        if name in df.columns:
            return name

    return None


hair_col = find_column([
    "hair_color",
    "hair_colour",
    "hair"
])

eye_col = find_column([
    "eye_color",
    "eye_colour",
    "eye"
])

skin_col = find_column([
    "skin_tone",
    "skin_color",
    "skin_colour",
    "skin"
])

undertone_col = find_column([
    "under_tone",
    "undertone",
    "skin_undertone",
    "skin_under_tone"
])

# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

missing = []

if hair_col is None:
    missing.append("Hair Color")

if eye_col is None:
    missing.append("Eye Color")

if skin_col is None:
    missing.append("Skin Tone")

if undertone_col is None:
    missing.append("Under Tone")

if missing:

    st.error(
        "❌ The following columns were not found in the dataset:"
    )

    for item in missing:
        st.write("• " + item)

    st.stop()

# ============================================================
# GET UNIQUE VALUES
# ============================================================

def get_options(column):

    values = (
        df[column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    values = values[
        values != ""
    ]

    return sorted(
        values.unique().tolist()
    )


hair_options = get_options(hair_col)
eye_options = get_options(eye_col)
skin_options = get_options(skin_col)
undertone_options = get_options(undertone_col)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("👤 Your Appearance")

# ============================================================
# IMAGE UPLOAD
# ============================================================

uploaded_image = st.sidebar.file_uploader(
    "📷 Upload Your Photo",
    type=["jpg", "jpeg", "png", "webp"]
)

# ============================================================
# SHOW IMAGE
# ============================================================

if uploaded_image is not None:

    try:

        image = Image.open(uploaded_image)

        st.subheader("📷 Your Photo")

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:

            st.image(
                image,
                caption="Uploaded Photo",
                use_container_width=True
            )

    except Exception:

        st.error(
            "❌ Invalid image file."
        )

# ============================================================
# HAIR COLOR
# ============================================================

hair_color = st.sidebar.selectbox(
    "💇 Hair Color",
    hair_options
)

# ============================================================
# EYE COLOR
# ============================================================

eye_color = st.sidebar.selectbox(
    "👁️ Eye Color",
    eye_options
)

# ============================================================
# SKIN TONE
# ============================================================

skin_tone = st.sidebar.selectbox(
    "🌈 Skin Tone",
    skin_options
)

# ============================================================
# UNDERTONE GUIDE
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader("✨ How to Find Your Undertone")

st.sidebar.write(
    "Not sure about your undertone? "
    "Use the simple tests below."
)

with st.sidebar.expander("🩸 Vein Test"):

    st.write(
        "**Look at the veins on your wrist in natural daylight.**"
    )

    st.write(
        "🟢 Green-looking veins → Usually Warm"
    )

    st.write(
        "🔵 Blue/Purple veins → Usually Cool"
    )

    st.write(
        "🟢🔵 Difficult to tell / mixture → Usually Neutral"
    )

with st.sidebar.expander("💍 Jewelry Test"):

    st.write(
        "**Compare gold and silver jewelry against your skin.**"
    )

    st.write(
        "🥇 Gold looks better → Usually Warm"
    )

    st.write(
        "🥈 Silver looks better → Usually Cool"
    )

    st.write(
        "🥇🥈 Both look good → Usually Neutral"
    )

with st.sidebar.expander("☀️ Sun Test"):

    st.write(
        "Think about how your skin usually reacts to sunlight."
    )

    st.write(
        "☀️ Tans easily → Often Warm/Neutral"
    )

    st.write(
        "🔴 Burns easily → Often Cool"
    )

    st.caption(
        "These are general indicators, not a medical or scientific diagnosis."
    )

# ============================================================
# UNDERTONE SELECTION
# ============================================================

undertone_choice = st.sidebar.selectbox(
    "✨ Under Tone",
    undertone_options
)

# ============================================================
# PROFILE
# ============================================================

st.subheader("✨ Your Style Profile")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        f"""
        <div class="card">
        <b>💇 Hair Color</b><br>
        {hair_color}
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        f"""
        <div class="card">
        <b>👁️ Eye Color</b><br>
        {eye_color}
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        f"""
        <div class="card">
        <b>🌈 Skin Tone</b><br>
        {skin_tone}
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:

    st.markdown(
        f"""
        <div class="card">
        <b>✨ Under Tone</b><br>
        {undertone_choice}
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# RECOMMENDATION BUTTON
# ============================================================

st.markdown("")

generate = st.button(
    "✨ Generate My Fashion Recommendation",
    use_container_width=True
)

# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

if generate:

    # --------------------------------------------------------
    # Normalize inputs
    # --------------------------------------------------------

    hair_input = hair_color.strip().lower()
    eye_input = eye_color.strip().lower()
    skin_input = skin_tone.strip().lower()
    undertone_input = undertone_choice.strip().lower()

    # --------------------------------------------------------
    # Normalize dataset
    # --------------------------------------------------------

    hair_values = (
        df[hair_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    eye_values = (
        df[eye_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    skin_values = (
        df[skin_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    undertone_values = (
        df[undertone_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # --------------------------------------------------------
    # MATCH SCORE
    # --------------------------------------------------------

    score = (
        (hair_values == hair_input).astype(int)
        +
        (eye_values == eye_input).astype(int)
        +
        (skin_values == skin_input).astype(int)
        +
        (undertone_values == undertone_input).astype(int)
    )

    best_score = score.max()

    # ========================================================
    # NO MATCH
    # ========================================================

    if best_score == 0:

        st.warning(
            "⚠️ No matching style was found in the recommendation database."
        )

        st.info(
            "Try another combination of Hair Color, Eye Color, "
            "Skin Tone, and Under Tone."
        )

    # ========================================================
    # MATCH FOUND
    # ========================================================

    else:

        matching_rows = df.loc[
            score == best_score
        ]

        # Select best matching recommendation
        recommendation = matching_rows.iloc[0]

        # ----------------------------------------------------
        # Hide input columns
        # ----------------------------------------------------

        input_columns = {
            hair_col,
            eye_col,
            skin_col,
            undertone_col
        }

        recommendation_columns = [
            column
            for column in df.columns
            if column not in input_columns
        ]

        # ====================================================
        # DISPLAY RESULT
        # ====================================================

        st.markdown(
            """
            <div class="result-card">

            <div class="result-title">
            👗 Your Personalized Fashion Style
            </div>

            <p>
            Your appearance profile has been matched with
            the most suitable style recommendation.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # Recommendation information
        # ----------------------------------------------------

        found = False

        for column in recommendation_columns:

            value = recommendation[column]

            if pd.isna(value):
                continue

            value = str(value).strip()

            if value == "":
                continue

            if value.lower() == "nan":
                continue

            label = (
                column
                .replace("_", " ")
                .title()
            )

            st.markdown(
                f"""
                <div class="card">
                <h3>✨ {label}</h3>
                <p>{value}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            found = True

        # ----------------------------------------------------
        # No recommendation information
        # ----------------------------------------------------

        if not found:

            st.warning(
                "A matching profile was found, but the dataset "
                "does not contain styling information for it."
            )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "👗 AI Fashion Stylist | Personalized recommendations"
)