# 🍕 Just Eat Restaurant Finder

A web application that fetches live restaurant data from the Just Eat API and displays the top 10 results for any UK postcode.

---

## How to Run

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/misska7070/JustEat.git
   cd JustEat
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and go to `http://localhost:8501`

Enter any UK postcode (e.g. `RG5 4JG`) and click **Find Restaurants**.

---

## What It Does

- Sends a postcode to the Just Eat enriched restaurant API
- Extracts the following four data points from the first 10 restaurants returned:
  - **Name**
  - **Cuisines**
  - **Rating** (as a number and star display)
  - **Address**
- Displays results in a clean, interactive web interface built with Streamlit

---

## Assumptions

- The API endpoint `https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}` is publicly accessible and does not require authentication
- Postcodes are entered without spaces (e.g. `RG54JG`) as the API does not accept spaces
- A `User-Agent` header is required in the request, as the API returns an empty response without one
- `starRating` under the `rating` object was used as the numeric rating, as it is the most human-readable metric available
- If a restaurant has no rating or cuisines listed, the app defaults to `0` and `N/A` respectively
- Only the first 10 restaurants in the response are displayed, as per the brief

---

## Improvements I Would Make

- **Error handling** — handle invalid postcodes, network failures, and unexpected API response structures more gracefully
- **Loading states** — show a skeleton UI while data is being fetched for a better user experience  
- **Search history** — allow users to revisit previously searched postcodes within the session
- **Sorting and filtering** — let users sort by rating or filter by cuisine type
- **Pagination** — extend beyond 10 results with a "load more" option
- **Unit tests** — add tests for the data extraction logic to ensure robustness against API changes
- **Caching** — cache API responses for the same postcode to reduce redundant network calls using `st.cache_data`
- **Map view** — plot restaurant locations on a map using coordinates available in the API response

---

## Tech Stack

- **Python** — core language
- **Requests** — HTTP calls to the Just Eat API
- **Streamlit** — web interface
