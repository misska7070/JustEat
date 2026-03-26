import streamlit as st
import requests
 
# ============================================================
# Page config
# ============================================================
st.set_page_config(page_title="Just Eat Near Me 🍕", page_icon="🍔", layout="centered")
 
st.title("🍕 Just Eat Near Me")
st.caption("Live data from the Just Eat API")
 
# ============================================================
# Step 1: Postcode input
# ============================================================
postcode = st.text_input("Enter a UK postcode", value="RG54JG").replace(" ", "")
 
fetch = st.button("🔍 Find Restaurants")
 
# ============================================================
# Step 2: Fetch + parse data (your original pipeline)
# ============================================================
def fetch_restaurants(postcode):
    url = f"https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
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
# Step 3: Display results
# ============================================================
def stars(rating):
    full = int(rating)
    half = 1 if rating % 1 != 0 else 0
    return "⭐" * full + ("✨" if half else "")
 
if fetch:
    with st.spinner("Fetching restaurants..."):
        try:
            restaurants = fetch_restaurants(postcode)
 
            # --- Sidebar filters ---
            st.sidebar.header("🔍 Filter")
 
            all_cuisines = sorted(set(
                tag.strip()
                for r in restaurants
                for tag in r["cuisines"].split(",")
            ))
            selected_cuisine = st.sidebar.selectbox("Cuisine", ["All"] + all_cuisines)
            min_rating = st.sidebar.slider("Min rating", 1.0, 5.0, 1.0, step=0.5)
 
            # --- Filter ---
            filtered = [
                r for r in restaurants
                if (selected_cuisine == "All" or selected_cuisine in r["cuisines"])
                and r["rating"] >= min_rating
            ]
 
            st.markdown(f"### 📍 {len(filtered)} restaurant(s) near `{postcode}`")
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
 
        except Exception as e:
            st.error(f"Something went wrong: {e}")
 