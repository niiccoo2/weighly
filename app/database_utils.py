import datetime
from CTkMessagebox import CTkMessagebox
from datetime import datetime
import requests
import webbrowser
import http.server
import socketserver
import urllib.parse
import json
from supabase import create_client, Client
import threading
from typing import cast
from gotrue.types import CodeExchangeParams, AuthResponse

SUPABASE_URL = "https://oifjrkxhjrtwlrancdho.supabase.co"
SUPABASE_KEY = "sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
session: AuthResponse | None = None

PORT = 5000
REDIRECT_URI = f"http://localhost:{PORT}"

FILENAME="./weighly_backup.csv"

# Write donation data to a file
def save_to_file(filename: str, name: str, weight: float, person_type: str | None = None):
    """
    Saves name, weight, and type to local CSV.
    Returns 0 for success, otherwise returns the error message.
    """
    try:
        clean_name = name.strip().title()
        weight_to_file = weight

        if name != "":
            with open(filename, "a") as hs:
                current_time = datetime.now()
                hs.write(f"{clean_name},{person_type},{weight_to_file},{current_time}\n")
        else:
            return "Name cannot be blank"
        return 0
    except Exception as e:
        return str(e)


def save_to_database(event: int, name: str, weight: float, person_type: str | None = None):
    """
    Saves name, weight, and type to weighly backend.
    Returns 0 for success, otherwise the error message.
    """
    if name != "":
        try:
            url = f"http://127.0.0.1:8000/{event}/add_weight"  # This is for local testing

            payload = {
                "name": name,
                "weight": weight,
                "type": person_type,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            headers = {"Content-Type": "application/json"}

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return 0
        except Exception as e:
            return str(e)
    else:
        return "Name cannot be blank"

def save_weight(event: int, name: str, weight: float, person_type: str | None = None):
    """
    Calls both save to database and file at the same time and gives saved or error message.
    """

    database = "Not attempted"

    file = save_to_file(FILENAME, name, weight, person_type)

    if file == 0: # Only save to db if it saves to file
        database = save_to_database(event, name, weight, person_type)

    if file == 0 and database == 0: # If they both return 0 for no error
        CTkMessagebox(
            title="Saved", message=f"Saved {weight} lbs from {name}!"
        )
    else:
        if file != 0: # Means file is not ok
            CTkMessagebox(
                title="Error", 
                message=f"Error: {str(file)}",
                icon="cancel"
            )
        # if database != 0 and database != "Not attempted": # Means db is not ok, comment to stop all the fuc
        #     CTkMessagebox(
        #         title="Error", 
        #         message=f"Error: {str(database)}",
        #         icon="cancel"
        #     )

def read_running_total(event: int) -> int:
    """
    Reads the running total for an event from database.
    """
    url = f"http://127.0.0.1:8000/{event}/total"

    return 0
    # try:
    #     response = requests.get(url)
    #     response.raise_for_status()

    #     data = response.json()
        
    #     return data

    # except requests.exceptions.RequestException as e:
    #     CTkMessagebox(
    #             title="Error", 
    #             message=f"Error: {e}",
    #             icon="cancel"
    #         )
    #     return 0

def sign_in_supabase():
    """
    Signs in the user using Google OAuth with Supabase by running a temporary
    HTTP server in a separate thread to handle the redirect.
    """
    global session

    # Add explicit type hints to satisfy the static type checker
    auth_code_holder: dict[str, str | None] = {"code": None}
    server_thread: threading.Thread | None = None
    httpd: socketserver.TCPServer | None = None

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            code = query_params.get("code", [None])[0]
            
            if code:
                auth_code_holder["code"] = code

            # Redirect to your website
            redirect_url = "https://weighly.app/python_sign_in_success"  # <-- change this to your site
            self.send_response(302)
            self.send_header("Location", redirect_url)
            self.end_headers()
            
            # Stop the server after handling the request
            if httpd:
                import threading
                threading.Thread(target=httpd.shutdown).start()


    def run_server():
        nonlocal httpd
        with socketserver.TCPServer(("", PORT), Handler) as server:
            httpd = server
            httpd.serve_forever()
        print("Server has been shut down.")

    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    print(f"Server started on http://localhost:{PORT}. Waiting for redirect...")

    data = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {"redirect_to": REDIRECT_URI},
    })
    webbrowser.open(data.url)

    server_thread.join()

    if auth_code_holder["code"]:
        print("Authentication code received. Exchanging for session...")
        try:
            params = cast(CodeExchangeParams, {"auth_code": auth_code_holder["code"]})
            session = cast(AuthResponse, supabase.auth.exchange_code_for_session(params))

            if session and session.user:
                print("Session successfully created!")
                print("User logged in as:", session.user.email)

                # with open("supabase_session.json", "w") as f:
                #     f.write(session.model_dump_json())
                
                return 0 # Success
            else:
                print("Login successful, but failed to retrieve user details.")
                CTkMessagebox(title="Login Warning", message="Could not retrieve user details after login.", icon="warning")

        except Exception as e:
            print(f"Error exchanging code for session: {e}")
            CTkMessagebox(title="Login Error", message=str(e), icon="cancel")

            return str(e) # Return the error message
    else:
        print("Could not get authentication code from redirect.")
        return "Could not get authentication code from redirect."

def get_allowed_events():
    """
    Gets the list of allowed events from the backend.
    """

    print("Checking allowed events for user...")
    if session is None or session.user is None:
        print("No active session. Please sign in first.")
        return []

    response = (
        supabase.rpc("get_allowed_events", { "user_id": session.user.id } )    
        .execute()
    )

    print("Allowed events response:", response)
    return response.data if response.data else []