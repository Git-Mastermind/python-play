import streamlit as st
import requests
import os
import difflib

# Uses Streamlit secrets when deployed (see .streamlit/secrets.toml),
# falls back to your local Flask server for local development.
try:
    API_BASE = st.secrets["API_BASE"]
except (FileNotFoundError, KeyError):
    API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:5000")

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
.wifi-id-badge {
    display: inline-block;
    background-color: #eef2ff;
    color: #4338ca !important;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 3px 10px;
    border-radius: 20px;
    margin-top: 8px;
    margin-right: 8px;
    border: 1px solid #c7d2fe;
}
.wifi-downvotes {
    color: #9ca3af !important;
    font-size: 0.82rem;
}
.notice-box {
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    border-left: 4px solid #9ca3af;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 10px 0;
    color: #374151 !important;
    font-size: 0.95rem;
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

tab_browse, tab_add, tab_search = st.tabs(
    ["🌐 Browse", "➕ Add", "🔍 Search"]
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
        # Some APIs return {"error": "..."} or {"message": "..."} when there's
        # no match. That's a normal empty result, not a real failure.
        if "error" in payload or "message" in payload:
            return [], None
        return [payload], None

    # API returned a proper list
    if isinstance(payload, list):
        # Filter out anything that isn't a dict, just in case
        cleaned = [item for item in payload if isinstance(item, dict)]
        return cleaned, None

    # API returned something unexpected (a raw string, number, etc.)
    return [], f"Unexpected response format: {payload!r}"


def suggest_similar_names(searched_name, all_wifis, limit=3):
    """Find close-spelling matches from the full wifi list, for a 'did you mean' hint."""
    all_names = list({wifi.get("name", "") for wifi in all_wifis if wifi.get("name")})
    return difflib.get_close_matches(searched_name, all_names, n=limit, cutoff=0.5)


def friendly_notice(message):
    """A calm, non-alarming way to show problems instead of Streamlit's red error box."""
    st.markdown(f"""
    <div class="notice-box">🙁 &nbsp;{message}</div>
    """, unsafe_allow_html=True)


def downvote_wifi(wifi_id):
    """Send a downvote and show a status-appropriate message. Returns True on success."""
    _, error, status = fetch_json("POST", f"{API_BASE}/downvote", params={"id": wifi_id})
    if error:
        friendly_notice("We couldn't submit your downvote right now. Please check your connection and try again.")
        return False
    elif is_server_side_issue(status):
        friendly_notice("Something went wrong on our end submitting your downvote. Please try again shortly.")
        return False
    elif is_client_side_issue(status):
        st.warning("That downvote couldn't be submitted — the wifi may no longer exist.")
        return False
    else:
        return True


def render_wifi_card(item):
    name = item.get("name", "Unknown")
    password = item.get("password", "—")
    wifi_id = item.get("id", "—")
    downvotes = item.get("downvotes", 0)

    col1, col2 = st.columns([5, 1])

    with col1:
        st.markdown(f"""
        <div class="wifi-card">
            <div class="wifi-name">{name}</div>
            <div class="wifi-pass">{password}</div>
            <div>
                <span class="wifi-id-badge">ID: {wifi_id}</span>
                <span class="wifi-downvotes">👎 {downvotes} downvotes</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("👎", key=f"downvote_{wifi_id}", help="Downvote this wifi", use_container_width=True):
            if downvote_wifi(wifi_id):
                st.rerun()


def fetch_json(method, url, **kwargs):
    """
    Make a request and safely parse JSON.
    Returns (data, network_error, status_code).

    network_error is only set when the request never got a response at all
    (server down, timeout, DNS failure, etc). Any HTTP status code that DID
    come back — including 400, 404, 422 — is returned as-is in status_code,
    since different APIs use different codes for "no match" or "bad input",
    and none of those mean the request itself failed.
    """
    try:
        response = requests.request(method, url, timeout=5, **kwargs)
    except requests.exceptions.RequestException:
        return None, "network_error", None

    try:
        data = response.json()
    except ValueError:
        data = None

    return data, None, response.status_code


def is_client_side_issue(status):
    """
    True for any 4xx status — these mean 'no match' or 'bad input',
    not a real server/network failure. Covers 400, 404, 422, etc. at once,
    since APIs aren't consistent about which one they use for 'not found'.
    """
    return status is not None and 400 <= status < 500


def is_server_side_issue(status):
    """True for 5xx — an actual problem on the server, worth a generic apology message."""
    return status is not None and status >= 500


# ---------- Browse ----------
with tab_browse:
    payload, error, status = fetch_json("GET", f"{API_BASE}/get-wifis")

    if error:
        friendly_notice("We couldn't load the wifi list right now. Please check your connection and try again.")
    elif is_server_side_issue(status):
        friendly_notice("Something went wrong on our end loading the wifi list. Please try again shortly.")
    else:
        wifis, list_error = normalize_wifi_list(payload)
        if list_error:
            friendly_notice("Something went wrong loading the wifi list. Please try again shortly. (API closed?)")
        elif not wifis:
            st.info("No wifis added yet. Be the first!")
        else:
            for wifi in wifis:
                render_wifi_card(wifi)

    st.caption("Just submitted a wifi? Reload the page to see it here.")

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
            _, error, status = fetch_json(
                "POST", f"{API_BASE}/new-entry",
                params={"name": name, "password": password},
            )
            if error:
                friendly_notice("We couldn't add your wifi right now. Please check your connection and try again.")
            elif is_server_side_issue(status):
                friendly_notice("Something went wrong on our end adding your wifi. Please try again shortly.")
            elif is_client_side_issue(status):
                st.warning("That entry couldn't be added — it may already exist, or the name/password format wasn't accepted.")
            else:
                st.success(f"✅ '{name}' was added!")

# ---------- Search ----------
with tab_search:
    name = st.text_input("Search by name")
    if name:
        payload, error, status = fetch_json("GET", f"{API_BASE}/search", params={"name": name})

        no_match = False

        if error:
            friendly_notice("We couldn't complete your search right now. Please check your connection and try again.")
        elif is_server_side_issue(status):
            friendly_notice("Something went wrong on our end searching. Please try again shortly.")
        elif is_client_side_issue(status):
            # Any 4xx here (400, 404, 422...) means "no match" or "bad input" — not a real failure.
            no_match = True
        else:
            wifis, list_error = normalize_wifi_list(payload)
            if list_error:
                friendly_notice("Something went wrong with that search. Please try again shortly.")
            elif not wifis:
                no_match = True
            else:
                for wifi in wifis:
                    render_wifi_card(wifi)

        if no_match:
            all_payload, all_error, all_status = fetch_json("GET", f"{API_BASE}/get-wifis")
            all_wifis = []
            if not all_error and not is_client_side_issue(all_status) and not is_server_side_issue(all_status):
                all_wifis, _ = normalize_wifi_list(all_payload)

            suggestions = suggest_similar_names(name, all_wifis)

            if suggestions:
                suggestion_text = ", ".join(f"**{s}**" for s in suggestions)
                st.warning(f"No wifi found named '{name}'. Did you mean: {suggestion_text}?")
            else:
                st.info(f"No wifi found named '{name}'. Double check the spelling, or browse all networks instead.")
