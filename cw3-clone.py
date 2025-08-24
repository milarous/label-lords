import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import readchar
import random
import os

# ==========================
# === Global Game State & Data ===
# ==========================

label_name = ""
ceo_name = ""
label_country = ""
label_city = ""

money = 5000
week = 1
starting_year = 2000

# Predefined sample data
sample_genres = ["Pop", "Hip Hop", "Rock", "Electronic", "Indie"]
sample_names = ["Nova Flame", "Echo Drift", "Luna Vibe", "Shadow Pulse"]

# ==========================
# === Utility Functions ===
# ==========================

def get_current_date(week, starting_year):
    """Return formatted date string based on week and year."""
    year = starting_year + (week - 1) // 52
    week_number = ((week - 1) % 52) + 1
    return f"Week {week_number}, {year}"

def generate_release_name():
    """Create a random release title from adjectives and nouns."""
    adjectives = ["Burning", "Lonely", "Shattered", "Golden", "Falling", "Electric", "Silent", "Midnight"]
    nouns = ["Dreams", "Skies", "Hearts", "Echoes", "Truth", "Storm", "Fire", "Voices"]
    return f"{random.choice(adjectives)} {random.choice(nouns)}"

def count_releases(artist, release_type):
    """Count how many releases of a given type the artist has."""
    return sum(1 for r in artist.get("releases", []) if r["type"] == release_type)

def has_released_this_week(artist):
    """Determines if the artist has released a record in the current week"""
    return any(r.get("week") == week for r in artist.get("releases", []))

# ==========================
# === Artist Initialisation ===
# ==========================

def generate_artist(name):
    """Generate a random unsigned artist profile."""
    return {
        "name": name,
        "genre": random.choice(sample_genres),
        "talent": random.randint(60, 100),
        "popularity": random.randint(10, 50),
        "signing_cost": random.choice([0, 1000, 2000, 3000]),
        "releases": [],
        "last_promoted_week": 0
    }

# Initial artist pools
unsigned_artists = [generate_artist(name) for name in sample_names]
signed_artists = []

# ==========================
# === Setup & Main Menu ===
# ==========================

def setup_game():
    """Prompt user to name their label and choose starting year."""
    global label_name, starting_year
    label_name = input("Welcome! What would you like to name your record label? ").strip()
    print(f"\nGreat! Welcome to {label_name} Records.\n")
    starting_year = int(input("Enter the starting year (e.g. 2000): "))

def setup_game_gui():
    """Show a Tkinter form to collect startup info."""
    def on_ok():
        global ceo_name, label_name, starting_year, label_country, label_city
        ceo_name = ceo_var.get()
        label_name = label_var.get()
        starting_year = int(year_var.get())
        label_country = country_var.get()
        label_city = city_var.get()
        root.destroy()  # Close the form

    def on_exit():
        root.destroy()
        exit()

    root = tk.Tk()
    root.title("Label Lords Setup")

    # Add welcome message at the top
    tk.Label(
        root,
        text="Welcome to Label Lords - A Chart Wars 3 Clone!",
        font=("Arial", 14, "bold"),
        justify="center",
        padx=10,
        pady=8
    ).grid(row=0, column=0, columnspan=2, sticky="n", pady=(15, 0))

    tk.Label(
        root,
        text="Please enter the following information to get started:",
        font=("Arial", 11),
        justify="center",
        padx=10,
        pady=4
    ).grid(row=1, column=0, columnspan=2, sticky="n")

    # Add some vertical space after the welcome message
    row_offset = 2

    tk.Label(root, text="CEO Name:").grid(row=row_offset+0, column=0, sticky="e", padx=10, pady=5)
    ceo_var = tk.StringVar()
    tk.Entry(root, textvariable=ceo_var, width=30).grid(row=row_offset+0, column=1, padx=10, pady=5)

    tk.Label(root, text="Record Label Name:").grid(row=row_offset+1, column=0, sticky="e", padx=10, pady=5)
    label_var = tk.StringVar()
    tk.Entry(root, textvariable=label_var, width=30).grid(row=row_offset+1, column=1, padx=10, pady=5)

    tk.Label(root, text="Starting Year:").grid(row=row_offset+2, column=0, sticky="e", padx=10, pady=5)
    year_var = tk.StringVar(value="2000")
    tk.Entry(root, textvariable=year_var, width=30).grid(row=row_offset+2, column=1, padx=10, pady=5)

    tk.Label(root, text="Country:").grid(row=row_offset+3, column=0, sticky="e", padx=10, pady=5)
    country_var = tk.StringVar(value="Australia")
    ttk.Combobox(root, textvariable=country_var, values=["Australia"], state="readonly", width=28)\
        .grid(row=row_offset+3, column=1, padx=10, pady=5)

    tk.Label(root, text="City:").grid(row=row_offset+4, column=0, sticky="e", padx=10, pady=5)
    city_var = tk.StringVar(value="Adelaide")
    ttk.Combobox(root, textvariable=city_var, values=["Adelaide"], state="readonly", width=28)\
        .grid(row=row_offset+4, column=1, padx=10, pady=5)

    # Add more space before the buttons
    tk.Button(root, text="EXIT", command=on_exit, width=12).grid(row=row_offset+5, column=0, pady=15)
    tk.Button(root, text="OK", command=on_ok, width=12).grid(row=row_offset+5, column=1, pady=15)

    root.mainloop()

def show_main_menu():
    """Display current status and main menu options with arrow key navigation."""
    global money
    menu_options = [
        "View Unsigned Artists",
        "Manage Signed Artists",
        "Finish Week",
        "Exit"
    ]
    selected = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n=== {label_name} Records ===")
        print(f"--- {get_current_date(week, starting_year)} ---")
        print(f"Funds: ${money}\n")
        print("Use ↑ ↓ to navigate. Press Enter to select:\n")

        for i, option in enumerate(menu_options):
            prefix = "> " if i == selected else "  "
            print(f"{prefix}{option}")

        key = readchar.readkey()

        if key == readchar.key.UP:
            selected = (selected - 1) % len(menu_options)
        elif key == readchar.key.DOWN:
            selected = (selected + 1) % len(menu_options)
        elif key == readchar.key.ENTER:
            if selected == 0:
                view_unsigned_artists()
            elif selected == 1:
                manage_signed_artists()
            elif selected == 2:
                finish_week()
            elif selected == 3:
                print("Thanks for playing!")
                exit()
        elif key == 'q':  # optional: quit with 'q'
            exit()

def show_main_menu_gui():
    """Display the main menu as a Tkinter window."""
    def on_view_unsigned():
        root.destroy()
        view_unsigned_artists_gui()
        show_main_menu_gui()

    def on_manage_signed():
        root.destroy()
        manage_signed_artists_gui()
        show_main_menu_gui()

    def on_finish_week():
        root.destroy()
        finish_week_gui()
        show_main_menu_gui()

    def on_exit():
        root.destroy()
        print("Thanks for playing!")
        exit()

    root = tk.Tk()
    root.title(f"{label_name} Records - Main Menu")

    tk.Label(root, text=f"{label_name} Records", font=("Arial", 16, "bold")).pack(pady=(15, 5))
    tk.Label(root, text=f"{get_current_date(week, starting_year)}", font=("Arial", 12)).pack()
    tk.Label(root, text=f"Funds: ${money}", font=("Arial", 12)).pack(pady=(0, 15))

    tk.Button(root, text="View Unsigned Artists", width=28, command=on_view_unsigned).pack(pady=4)
    tk.Button(root, text="Manage Signed Artists", width=28, command=on_manage_signed).pack(pady=4)
    tk.Button(root, text="Finish Week", width=28, command=on_finish_week).pack(pady=4)
    tk.Button(root, text="Exit", width=28, command=on_exit).pack(pady=(15, 10))

    root.mainloop()

# ==========================
# === Artist Management Menu ===
# ==========================

def view_artist_profile(artist):
    """Display key stats and release history for a given artist."""
    print(f"\nName: {artist['name']}")
    print(f"Genre: {artist['genre']}")
    print(f"Talent: {artist['talent']}")
    print(f"Popularity: {artist['popularity']}")
    print(f"Signing Cost: ${artist['signing_cost']}")

    releases = artist.get("releases", [])
    if not releases:
        print("No releases yet.")
        return
    
    # Sort releases by release week (oldest first)
    sorted_releases = sorted(releases, key=lambda r: (r.get("year", 0), r.get("week", 0)))
    singles = [r for r in sorted_releases if r["type"] == "Single"]
    albums = [r for r in sorted_releases if r["type"] == "Album"]

    if singles:
        print(f"\nSingles ({len(singles)}):")
        for s in singles:
            print(f"  - {s['name']} (Week {s.get('week','?')}, {s.get('year','?')})")
    else:
        print("\nNo singles released yet.")

    if albums:
        print(f"\nAlbums ({len(albums)}):")
        for a in albums:
            print(f"  - {a['name']} (Week {a.get('week','?')}, {a.get('year','?')})")
    else:
        print("No albums released yet.")

def view_artist_profile_gui(artist):
    """Show artist profile in a popup window."""
    releases = artist.get("releases", [])
    singles = [r for r in releases if r["type"] == "Single"]
    albums = [r for r in releases if r["type"] == "Album"]
    profile = (
        f"Name: {artist['name']}\n"
        f"Genre: {artist['genre']}\n"
        f"Talent: {artist['talent']}\n"
        f"Popularity: {artist['popularity']}\n"
        f"Signing Cost: ${artist['signing_cost']}\n"
        f"\nSingles ({len(singles)}):\n" +
        ("\n".join(f"  - {s['name']} (Week {s.get('week','?')}, {s.get('year','?')})" for s in singles) if singles else "  None") +
        f"\n\nAlbums ({len(albums)}):\n" +
        ("\n".join(f"  - {a['name']} (Week {a.get('week','?')}, {a.get('year','?')})" for a in albums) if albums else "  None")
    )
    top = tk.Toplevel()
    top.title(f"{artist['name']} Profile")
    tk.Label(top, text=profile, justify="left", font=("Arial", 11)).pack(padx=15, pady=10)
    tk.Button(top, text="Close", command=top.destroy).pack(pady=6)

def view_unsigned_artists():
    """View, inspect, and sign unsigned artists using arrow key navigation."""
    global money
    selected = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- Unsigned Artists ---")
        if not unsigned_artists:
            print("No unsigned artists left!")
            input("Press Enter to return to the main menu.")
            return

        menu_options = [f"{artist['name']} ({artist['genre']})" for artist in unsigned_artists]
        menu_options.append("Back to Main Menu")

        for i, option in enumerate(menu_options):
            prefix = "> " if i == selected else "  "
            print(f"{prefix}{option}")          

        key = readchar.readkey()

        if key == readchar.key.UP:
            selected = (selected - 1) % len(menu_options)
        elif key == readchar.key.DOWN:
            selected = (selected + 1) % len(menu_options)
        elif key == readchar.key.ENTER:
            if selected == len(menu_options) - 1:  # Back to Main Menu
                return
            else:
                artist = unsigned_artists[selected]
                view_artist_profile(artist)
                print(f"\nSign {artist['name']} for ${artist['signing_cost']}? (y/n)")
                confirm = readchar.readkey().lower()
                if confirm == "y":
                    if money >= artist['signing_cost']:
                        signed_artists.append(artist)
                        unsigned_artists.pop(selected)
                        money -= artist['signing_cost']
                        print(f"\nYou signed {artist['name']}!")
                        print(f"Remaining funds: ${money}")
                        input("Press Enter to continue.")
                        selected = min(selected, len(unsigned_artists))
                    else:
                        print("Not enough funds.")
                        input("Press Enter to continue.")
                else:
                    print("Artist not signed.")
                    input("Press Enter to continue.")

def view_unsigned_artists_gui():
    """GUI for viewing, inspecting, and signing unsigned artists."""
    def refresh():
        for widget in root.winfo_children():
            widget.destroy()
        tk.Label(root, text="Unsigned Artists", font=("Arial", 14, "bold")).pack(pady=10)
        if not unsigned_artists:
            tk.Label(root, text="No unsigned artists left!").pack(pady=10)
            tk.Button(root, text="Back to Main Menu", command=lambda: [root.destroy(), show_main_menu_gui()]).pack(pady=10)
            return
        for idx, artist in enumerate(unsigned_artists):
            btn = tk.Button(root, text=f"{artist['name']} ({artist['genre']})", width=32,
                            command=lambda i=idx: show_artist_profile(i))
            btn.pack(pady=2)
        tk.Button(root, text="Back to Main Menu", command=lambda: [root.destroy(), show_main_menu_gui()]).pack(pady=10)

    def show_artist_profile(idx):
        artist = unsigned_artists[idx]
        profile = (
            f"Name: {artist['name']}\n"
            f"Genre: {artist['genre']}\n"
            f"Talent: {artist['talent']}\n"
            f"Popularity: {artist['popularity']}\n"
            f"Signing Cost: ${artist['signing_cost']}\n"
        )
        top = tk.Toplevel(root)
        top.title(f"{artist['name']} Profile")
        tk.Label(top, text=profile, justify="left", font=("Arial", 11)).pack(padx=15, pady=10)
        def sign_artist():
            global money
            if money >= artist['signing_cost']:
                signed_artists.append(artist)
                unsigned_artists.pop(idx)
                money -= artist['signing_cost']
                tk.messagebox.showinfo("Signed!", f"You signed {artist['name']}!\nRemaining funds: ${money}")
                top.destroy()
                refresh()
            else:
                tk.messagebox.showwarning("Insufficient Funds", "Not enough funds to sign this artist.")
        tk.Button(top, text=f"Sign for ${artist['signing_cost']}", command=sign_artist).pack(pady=4)
        tk.Button(top, text="Close", command=top.destroy).pack(pady=4)

    root = tk.Tk()
    root.title("Unsigned Artists")
    refresh()
    root.mainloop()

def manage_signed_artists():
    """View and manage signed artists using arrow key navigation."""
    global money
    selected = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n--- {label_name} Records: Signed Artists (Funds: ${money}) ---")
        if not signed_artists:
            print("You haven't signed any artists yet.")
            input("Press Enter to return to the main menu.")
            return

        menu_options = [f"{artist['name']} ({artist['genre']})" for artist in signed_artists]
        menu_options.append("Back to Main Menu")

        for i, option in enumerate(menu_options):
            prefix = "> " if i == selected else "  "
            print(f"{prefix}{option}")

        key = readchar.readkey()

        if key == readchar.key.UP:
            selected = (selected - 1) % len(menu_options)
        elif key == readchar.key.DOWN:
            selected = (selected + 1) % len(menu_options)
        elif key == readchar.key.ENTER:
            if selected == len(menu_options) - 1:
                return
            else:
                artist = signed_artists[selected]
                result = manage_artist_menu(artist)
                if result == "main":
                    return  # Exit the whole menu to main
                
def manage_signed_artists_gui():
    """GUI for viewing and managing signed artists."""
    def refresh():
        for widget in root.winfo_children():
            widget.destroy()
        tk.Label(root, text=f"{label_name} Records: Signed Artists", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(root, text=f"Funds: ${money}", font=("Arial", 11)).pack()
        if not signed_artists:
            tk.Label(root, text="You haven't signed any artists yet.").pack(pady=10)
            tk.Button(root, text="Back to Main Menu", command=lambda: [root.destroy(), show_main_menu_gui()]).pack(pady=10)
            return
        for idx, artist in enumerate(signed_artists):
            btn = tk.Button(root, text=f"{artist['name']} ({artist['genre']})", width=32,
                            command=lambda i=idx: manage_artist_gui(i))
            btn.pack(pady=2)
        tk.Button(root, text="Back to Main Menu", command=lambda: [root.destroy(), show_main_menu_gui()]).pack(pady=10)

    def manage_artist_gui(idx):
        artist = signed_artists[idx]
        top = tk.Toplevel(root)
        top.title(f"Manage {artist['name']}")
        tk.Label(top, text=f"--- Managing {artist['name']} ---", font=("Arial", 12, "bold")).pack(pady=8)
        tk.Button(top, text="View Profile", width=28, command=lambda: view_artist_profile_gui(artist)).pack(pady=2)
        tk.Button(top, text="Promote Artist ($500)", width=28, command=lambda: promote_artist_gui(artist, parent=top)).pack(pady=2)
        tk.Button(top, text="Release Single ($500)", width=28, command=lambda: release_single_gui(artist, parent=top)).pack(pady=2)
        tk.Button(top, text="Release Album ($1500)", width=28, command=lambda: release_album_gui(artist, parent=top)).pack(pady=2)
        tk.Button(top, text="Close", width=28, command=top.destroy).pack(pady=(10, 4))

    root = tk.Tk()
    root.title("Signed Artists")
    refresh()
    root.mainloop()

def manage_artist_menu(artist):
    """Submenu for managing a signed artist using arrow key navigation."""
    menu_options = [
        "View Profile",
        "Promote Artist ($500)",
        "Release Single ($500)",
        "Release Album ($1500)",
        "Back to Signed Artists",
        "Return to Main Menu"
    ]
    selected = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n--- Managing {artist['name']} ---")
        for i, option in enumerate(menu_options):
            prefix = "> " if i == selected else "  "
            print(f"{prefix}{option}")

        key = readchar.readkey()

        if key == readchar.key.UP:
            selected = (selected - 1) % len(menu_options)
        elif key == readchar.key.DOWN:
            selected = (selected + 1) % len(menu_options)
        elif key == readchar.key.ENTER:
            if selected == 0:
                view_artist_profile(artist)
                input("Press Enter to continue.")
            elif selected == 1:
                promote_artist(artist)
                input("Press Enter to continue.")
            elif selected == 2:
                release_single(artist)
                input("Press Enter to continue.")
            elif selected == 3:
                release_album(artist)
                input("Press Enter to continue.")
            elif selected == 4:
                return "back"  # Go back to artist list
            elif selected == 5:
                return "main"  # Go all the way back to main menu

# ==========================
# === Game Mechanics ===
# ==========================

def promote_artist(artist):
    """Spend money to increase artist popularity."""
    global money, week
    cost = 500

    if artist["last_promoted_week"] == week:
        print(f"{artist['name']} has already been promoted this week.")
        return

    if money < cost:
        print("You don’t have enough money to promote this artist.")
        return

    increase = random.randint(5, 15)
    artist["popularity"] = min(100, artist["popularity"] + increase)
    artist["last_promoted_week"] = week
    money -= cost
    print(f"You promoted {artist['name']}! Popularity increased by {increase}.")
    print(f"Remaining balance: ${money}")

def promote_artist_gui(artist, parent=None):
    """Promote artist with GUI feedback."""
    global money, week
    cost = 500
    if artist["last_promoted_week"] == week:
        messagebox.showinfo("Promotion", f"{artist['name']} has already been promoted this week.", parent=parent)
        return
    if money < cost:
        messagebox.showwarning("Promotion", "You don’t have enough money to promote this artist.", parent=parent)
        return
    increase = random.randint(5, 15)
    artist["popularity"] = min(100, artist["popularity"] + increase)
    artist["last_promoted_week"] = week
    money -= cost
    messagebox.showinfo("Promotion", f"You promoted {artist['name']}! Popularity increased by {increase}.\nRemaining balance: ${money}", parent=parent)

def release_single(artist):
    """Spend money to release a new single for the artist."""
    global money
    cost = 500

    if money < cost:
        print("You don’t have enough money to release a single.")
        return

    if has_released_this_week(artist):
        print(f"{artist['name']} has already released something this week.")
        return

    title = generate_release_name()
    artist["releases"].append({"type": "Single", "name": title, "week": week, "year": get_current_date(week, starting_year).split(', ')[1]})
    money -= cost
    print(f"{artist['name']} released a single titled '{title}'. Cost: ${cost}. Remaining funds: ${money}")

def release_single_gui(artist, parent=None):
    """Release single with GUI feedback."""
    global money
    cost = 500
    if money < cost:
        messagebox.showwarning("Release Single", "You don’t have enough money to release a single.", parent=parent)
        return
    if has_released_this_week(artist):
        messagebox.showinfo("Release Single", f"{artist['name']} has already released something this week.", parent=parent)
        return
    title = generate_release_name()
    artist["releases"].append({"type": "Single", "name": title, "week": week, "year": get_current_date(week, starting_year).split(', ')[1]})
    money -= cost
    messagebox.showinfo("Release Single", f"{artist['name']} released a single titled '{title}'.\nCost: ${cost}. Remaining funds: ${money}", parent=parent)

def release_album(artist):
    """Spend money to release a new album for the artist."""
    global money
    cost = 1500

    if money < cost:
        print("You don’t have enough money to release an album.")
        return

    if has_released_this_week(artist):
        print(f"{artist['name']} has already released something this week.")
        return

    title = generate_release_name()
    artist["releases"].append({"type": "Album", "name": title, "week": week, "year": get_current_date(week, starting_year).split(', ')[1]})
    money -= cost
    print(f"{artist['name']} released an album titled '{title}'. Cost: ${cost}. Remaining funds: ${money}")

def release_album_gui(artist, parent=None):
    """Release album with GUI feedback."""
    global money
    cost = 1500
    if money < cost:
        messagebox.showwarning("Release Album", "You don’t have enough money to release an album.", parent=parent)
        return
    if has_released_this_week(artist):
        messagebox.showinfo("Release Album", f"{artist['name']} has already released something this week.", parent=parent)
        return
    title = generate_release_name()
    artist["releases"].append({"type": "Album", "name": title, "week": week, "year": get_current_date(week, starting_year).split(', ')[1]})
    money -= cost
    messagebox.showinfo("Release Album", f"{artist['name']} released an album titled '{title}'.\nCost: ${cost}. Remaining funds: ${money}", parent=parent)

def finish_week():
    """End the week, calculate revenue based on releases with depreciation, and advance time."""
    global week, money
    print(f"\n--- Week {week} Summary ---")
    weekly_revenue = 0

    for artist in signed_artists:
        artist_revenue = 0
        active_singles = 0
        active_albums = 0

        for release in artist.get("releases", []):
            release_week = release.get("week", 0)
            age = week - release_week
            popularity_multiplier = artist["popularity"] / 100

            if release["type"] == "Single":
                if 0 <= age < 5:
                    # Depreciation: 100%, 80%, 60%, 40%, 20%
                    depreciation = 1.0 - 0.2 * age
                    base_income = 200
                    income = int(base_income * depreciation * popularity_multiplier)
                    artist_revenue += income
                    active_singles += 1
            elif release["type"] == "Album":
                if 0 <= age < 10:
                    # Depreciation: 100%, 90%, ..., 10%
                    depreciation = 1.0 - 0.1 * age
                    base_income = 500
                    income = int(base_income * depreciation * popularity_multiplier)
                    artist_revenue += income
                    active_albums += 1

        weekly_revenue += artist_revenue

        if artist_revenue > 0:
            print(f"{artist['name']} earned ${artist_revenue} from {active_singles} single(s) and {active_albums} album(s) "
                  f"(Popularity: {artist['popularity']}).")

    money += weekly_revenue
    print(f"\nTotal weekly revenue: ${weekly_revenue}")
    week += 1
    input("Press Enter to continue to the next week.")

def finish_week_gui():
    """End the week, calculate revenue with depreciation, and show summary in a GUI dialog."""
    global week, money
    summary = f"--- Week {week} Summary ---\n"
    weekly_revenue = 0

    for artist in signed_artists:
        artist_revenue = 0
        active_singles = 0
        active_albums = 0

        for release in artist.get("releases", []):
            release_week = release.get("week", 0)
            age = week - release_week
            popularity_multiplier = artist["popularity"] / 100

            if release["type"] == "Single":
                if 0 <= age < 5:
                    depreciation = 1.0 - 0.2 * age
                    base_income = 200
                    income = int(base_income * depreciation * popularity_multiplier)
                    artist_revenue += income
                    active_singles += 1
            elif release["type"] == "Album":
                if 0 <= age < 10:
                    depreciation = 1.0 - 0.1 * age
                    base_income = 500
                    income = int(base_income * depreciation * popularity_multiplier)
                    artist_revenue += income
                    active_albums += 1

        weekly_revenue += artist_revenue

        if artist_revenue > 0:
            summary += (f"{artist['name']} earned ${artist_revenue} from {active_singles} single(s) and {active_albums} album(s) "
                        f"(Popularity: {artist['popularity']}).\n")

    money += weekly_revenue
    summary += f"\nTotal weekly revenue: ${weekly_revenue}\n"
    week += 1
    messagebox.showinfo("Week Summary", summary)

# ==========================
# === Main Game Loop ===
# ==========================

if __name__ == "__main__":
    setup_game_gui()
    show_main_menu_gui()