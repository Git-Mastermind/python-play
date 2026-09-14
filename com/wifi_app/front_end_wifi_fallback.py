import streamlit as st
import requests

API_BASE = "http://127.0.0.1:5000"

st.set_page_config(page_title="OpenWifi", page_icon="📶", layout="centered")

# ---------- Styling ----------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    max-width: 780px;
}
.hero {
    text-align: center;
    padding: 1.2rem 0 1.8rem 0;
}
.hero h1 {
    font-size: 2.4rem;
    margin-bottom: 0.2rem;
}
.hero p {
    color: #6b7280;
    font-size: 1.05rem;
}
.wifi-card {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.wifi-name {
    font-size: 1.2rem;
    font-weight: 700;
    color: #111827 !important;
}
.wifi-pass {
    font-family: "Courier New", monospace;
    background-color: #f3f4f6;
    color: #111827 !important;
    padding: 4px 10px;
    border-radius: 8px;
    display: inline-block;
    margin-top: 6px;
    font-size: 0.95rem;
}
.wifi-meta {
    color: #6b7280 !important;
    font-size: 0.82rem;
    margin-top: 8px;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown("""
<div class="hero">
    <h1>📶 OpenWifi</h1>
    <p>Free, community-shared wifi for restaurants, gyms, cafes &amp; more.</p>
</div>
""", unsafe_allow_html=True)

tab_browse, tab_add, tab_search, tab_downvote = st.tabs(
    ["🌐 Browse", "➕ Add", "🔍 Search", "👎 Downvote"]
)


# ---------- Helpers ----------
def normalize_wifi_list(payload):
    """
    Make sure we always end up with a list of dicts, no matter what
    shape the API happens to send back. Returns (list_of_wifis, error_message).
    """
    if payload is None:
        return [], None

    # API returned a single wifi object instead of a list
    if isinstance(payload, dict):
        # Some APIs return {"error": "..."} or {"message": "..."} on no match
        if "error" in payload or "message" in payload:
            return [], payload.get("error") or payload.get("message")
        return [payload], None

    # API returned a proper list
    if isinstance(payload, list):
        # Filter out anything that isn't a dict, just in case
        cleaned = [item for item in payload if isinstance(item, dict)]
        return cleaned, None

    # API returned something unexpected (a raw string, number, etc.)
    return [], f"Unexpected response format: {payload!r}"


def render_wifi_card(item):
    name = item.get("name", "Unknown")
    password = item.get("password", "—")
    wifi_id = item.get("id", "—")
    downvotes = item.get("downvotes", 0)

    st.markdown(f"""
    <div class="wifi-card">
        <div class="wifi-name">{name}</div>
        <div class="wifi-pass">{password}</div>
        <div class="wifi-meta">ID: {wifi_id} &nbsp;•&nbsp; 👎 {downvotes} downvotes</div>
    </div>
    """, unsafe_allow_html=True)


def fetch_json(method, url, **kwargs):
    """Make a request and safely parse JSON, returning (data, error_message)."""
    try:
        response = requests.request(method, url, timeout=5, **kwargs)
        response.raise_for_status()
        try:
            return response.json(), None
        except ValueError:
            return None, "The server didn't return valid JSON."
    except requests.exceptions.RequestException as e:
        return None, f"Couldn't reach the server: {e}"


# ---------- Browse ----------
with tab_browse:
    payload, error = fetch_json("GET", f"{API_BASE}/get-wifis")

    if error:
        st.error(error)
    else:
        wifis, list_error = normalize_wifi_list(payload)
        if list_error:
            st.error(list_error)
        elif not wifis:
            st.info("No wifis added yet. Be the first!")
        else:
            for wifi in wifis:
                render_wifi_card(wifi)

# ---------- Add ----------
with tab_add:
    with st.form("add_wifi_form"):
        name = st.text_input("Wifi name (SSID)")
        password = st.text_input("Wifi password")
        submitted = st.form_submit_button("Add wifi", use_container_width=True)

    if submitted:
        if not name or not password:
            st.warning("Please fill in both fields.")
        else:
            _, error = fetch_json(
                "POST", f"{API_BASE}/new-entry",
                params={"name": name, "password": password},
            )
            if error:
                st.error(error)
            else:
                st.success(f"✅ '{name}' was added!")

# ---------- Search ----------
with tab_search:
    name = st.text_input("Search by name")
    if name:
        payload, error = fetch_json("GET", f"{API_BASE}/search", params={"name": name})

        if error:
            st.error(error)
        else:
            wifis, list_error = normalize_wifi_list(payload)
            if list_error:
                st.error(list_error)
            elif not wifis:
                st.info("No matches found.")
            else:
                for wifi in wifis:
                    render_wifi_card(wifi)

# ---------- Downvote ----------
with tab_downvote:
    with st.form("downvote_form"):
        wifi_id = st.text_input("Wifi ID")
        submitted = st.form_submit_button("Downvote", use_container_width=True)

    if submitted:
        if not wifi_id:
            st.warning("Please enter an ID.")
        else:
            _, error = fetch_json("POST", f"{API_BASE}/downvote", params={"id": wifi_id})
            if error:
                st.error(error)
            else:
                st.success("✅ Downvoted!")
