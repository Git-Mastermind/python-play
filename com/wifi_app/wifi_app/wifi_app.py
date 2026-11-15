import reflex as rx
import requests

# Base URL of your running Flask API backend
FLASK_API_URL = "http://127.0.0.1:5000"


class WifiState(rx.State):
    """Application state for managing Wi-Fi data and API communication."""
    wifis: list[dict] = []
    
    # Form fields for adding new Wi-Fi
    new_name: str = ""
    new_password: str = ""
    
    # Notification state
    toast_message: str = ""
    toast_status: str = ""

    def load_wifis(self):
        """Fetch all Wi-Fi networks from the Flask backend."""
        try:
            res = requests.get(f"{FLASK_API_URL}/get-wifis")
            if res.status_code == 200:
                self.wifis = res.json()
        except Exception:
            self.toast_message = "Failed to connect to Flask API."
            self.toast_status = "error"

    def add_wifi(self):
        """Send a new Wi-Fi entry to Flask."""
        if not self.new_name or not self.new_password:
            self.toast_message = "Please enter both SSID and Password."
            self.toast_status = "warning"
            return

        try:
            res = requests.post(
                f"{FLASK_API_URL}/new-entry",
                params={"name": self.new_name, "password": self.new_password}
            )
            if res.status_code == 201:
                self.toast_message = "Wi-Fi entry created!"
                self.toast_status = "success"
                self.new_name = ""
                self.new_password = ""
                self.load_wifis()
        except Exception:
            self.toast_message = "Error adding network."
            self.toast_status = "error"

    def upvote(self, wifi_id: int):
        """Upvote a Wi-Fi network."""
        try:
            requests.post(f"{FLASK_API_URL}/upvote", params={"id": wifi_id})
            self.load_wifis()
        except Exception:
            pass

    def downvote(self, wifi_id: int):
        """Downvote a Wi-Fi network."""
        try:
            requests.post(f"{FLASK_API_URL}/downvote", params={"id": wifi_id})
            self.load_wifis()
        except Exception:
            pass


def wifi_card(wifi: dict) -> rx.Component:
    """Card element displaying individual Wi-Fi entries."""
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.heading(wifi["name"], size="4"),
                rx.code(wifi["password"], size="3", color_scheme="blue"),
                align_items="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.hstack(
                rx.button(
                    "👍",
                    wifi["upvotes"],
                    on_click=lambda: WifiState.upvote(wifi["id"]),
                    color_scheme="green",
                    variant="soft",
                    cursor="pointer",
                ),
                rx.button(
                    "👎",
                    wifi["downvotes"],
                    on_click=lambda: WifiState.downvote(wifi["id"]),
                    color_scheme="red",
                    variant="soft",
                    cursor="pointer",
                ),
                spacing="2",
            ),
            align="center",
            width="100%",
        ),
        width="100%",
        margin_bottom="3",
        padding="4",
    )


def index() -> rx.Component:
    """Main page UI layout."""
    return rx.container(
        rx.vstack(
            # Header
            rx.vstack(
                rx.heading("📶 Seattle Crowdsourced Wi-Fi", size="8"),
                rx.text(
                    "Community database for local public & shared Wi-Fi passwords across Seattle.",
                    color="gray",
                ),
                align_items="center",
                width="100%",
                padding_y="6",
            ),
            # Form Card
            rx.card(
                rx.vstack(
                    rx.heading("Share a Network", size="4"),
                    rx.hstack(
                        rx.input(
                            placeholder="Network Name (SSID)",
                            value=WifiState.new_name,
                            on_change=WifiState.set_new_name,
                            width="40%",
                        ),
                        rx.input(
                            placeholder="Password",
                            type="password",
                            value=WifiState.new_password,
                            on_change=WifiState.set_new_password,
                            width="40%",
                        ),
                        rx.button(
                            "Add Network",
                            on_click=WifiState.add_wifi,
                            color_scheme="blue",
                            width="20%",
                            cursor="pointer",
                        ),
                        width="100%",
                        spacing="3",
                    ),
                    spacing="3",
                ),
                width="100%",
                margin_bottom="6",
                padding="5",
            ),
            # Directory Heading
            rx.heading("Active Networks", size="5", margin_bottom="3"),
            # Dynamic Network List
            rx.cond(
                WifiState.wifis.length() > 0,
                rx.foreach(WifiState.wifis, wifi_card),
                rx.callout(
                    "No networks added yet. Be the first to share one!",
                    icon="info",
                    color_scheme="blue",
                ),
            ),
            width="100%",
            max_width="800px",
        ),
        on_mount=WifiState.load_wifis,
    )


app = rx.App()
app.add_page(index)