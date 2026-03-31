import streamlit as st
import requests
import re
 
# ============================================================
# Page config
# ============================================================
st.set_page_config(page_title="Just Eat Near Me 🍕", page_icon="🍔", layout="centered")
 
st.title("🍕 Just Eat Near Me")
st.caption("Live data from the Just Eat API")
 
# ============================================================
# Step 1: Postcode input
# ============================================================
st.info("🇬🇧 This app uses the Just Eat UK API — please enter a valid UK postcode (e.g. RG5 4JG, EC4M 7RF).")
postcode = st.text_input("Enter a UK postcode", value="RG5 4JG")
 
fetch = st.button("🔍 Find Restaurants")
 
# ============================================================
# Helper: Validate UK postcode format
# ============================================================
def is_valid_uk_postcode(postcode):
    """Basic UK postcode format check — catches obvious non-UK or empty inputs."""
    # Full postcode (e.g. RG5 4JG) or outward code only (e.g. RG1, EC4M)
    full = r"^[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}$"
    partial = r"^[A-Z]{1,2}\d[A-Z\d]?$"
    clean = postcode.strip().upper()
    return bool(re.match(full, clean) or re.match(partial, clean))
 
# ============================================================
# Step 2: Fetch + parse data
# ============================================================
def fetch_restaurants(postcode):
    """
    Call the Just Eat API for a given UK postcode and return the first 10
    restaurants, each with: name, cuisines, rating (number), and address.
    Raises ValueError if no restaurants are found.
    """
    clean_postcode = postcode.replace(" ", "")
    url = f"https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{clean_postcode}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
 
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
 
    data = response.json()
 
    if "restaurants" not in data or not data["restaurants"]:
        raise ValueError("No restaurants found for this postcode.")
 
    restaurants_raw = data["restaurants"]
 
    restaurants = []
    for restaurant in restaurants_raw[:10]:
        name = restaurant.get("name", "N/A")
 
        cuisines_list = restaurant.get("cuisines", [])
        cuisines = ", ".join([c["name"] for c in cuisines_list]) if cuisines_list else "N/A"
 
        rating_info = restaurant.get("rating", {})
        rating = rating_info.get("starRating", 0)
 
        address_info = restaurant.get("address", {})
        address = (
            f"{address_info.get('firstLine', '')}, "
            f"{address_info.get('city', '')}, "
            f"{address_info.get('postalCode', '')}"
        ).strip(", ")
 
        restaurants.append({
            "name": name,
            "cuisines": cuisines,
            "rating": rating,
            "address": address
        })
 
    return restaurants
 
# ============================================================
# Step 3: Display helpers
# ============================================================
def stars(rating):
    """Convert a numeric rating to a visual star string (e.g. 3.5 → ⭐⭐⭐✨)."""
    full = int(rating)
    half = 1 if rating % 1 != 0 else 0
    return "⭐" * full + ("✨" if half else "")
 
# ============================================================
# Step 4: Fetch and store in session_state
# ============================================================
if fetch:
    if not postcode.strip():
        st.warning("⚠️ Please enter a postcode.")
    elif not is_valid_uk_postcode(postcode):
        st.error("❌ That doesn't look like a valid UK postcode. Please use a format like RG5 4JG or EC4M 7RF.")
    else:
        with st.spinner("Fetching restaurants..."):
            try:
                st.session_state["restaurants"] = fetch_restaurants(postcode)
                st.session_state["postcode"] = postcode
            except ValueError as e:
                st.warning(f"⚠️ {e}")
                st.session_state["restaurants"] = []
            except requests.exceptions.Timeout:
                st.error("⏱️ The Just Eat API took too long to respond. Please try again.")
                st.session_state["restaurants"] = []
            except requests.exceptions.ConnectionError:
                st.error("🌐 Could not connect to the Just Eat API. Check your internet connection.")
                st.session_state["restaurants"] = []
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.session_state["restaurants"] = []
 
# ============================================================
# Step 5: Display results (runs on every rerun from session_state)
# ============================================================
if "restaurants" in st.session_state and st.session_state["restaurants"]:
    restaurants = st.session_state["restaurants"]
    saved_postcode = st.session_state["postcode"]
 
    # --- Sidebar filters ---
    st.sidebar.header("🔍 Filter")
 
    all_cuisines = sorted(set(
        tag.strip()
        for r in restaurants
        for tag in r["cuisines"].split(",")
    ))
    selected_cuisine = st.sidebar.selectbox("Cuisine", ["All"] + all_cuisines)
 
    lowest_rating = float(min(r["rating"] for r in restaurants))
    highest_rating = float(max(r["rating"] for r in restaurants))
    min_rating = st.sidebar.slider("Min rating", lowest_rating, highest_rating, lowest_rating, step=0.5)
 
    # --- Apply filters ---
    filtered = [
        r for r in restaurants
        if (selected_cuisine == "All" or selected_cuisine in r["cuisines"])
        and r["rating"] >= min_rating
    ]
 
    st.markdown(f"### 📍 {len(filtered)} restaurant(s) near `{saved_postcode}`")
    st.divider()
 
    if not filtered:
        st.warning("No restaurants match your filters!")
    else:
        for r in filtered:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"#### {r['name']}")
                    st.markdown(f"🍽️ `{r['cuisines']}`")
                    st.markdown(f"📍 {r['address']}")
                with col2:
                    st.markdown(f"### {stars(r['rating'])}")
                    st.markdown(f"**{r['rating']} / 5**")
                st.divider()