from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import os
import pickle
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'label_lords_secret_key'  # For session management

# ==========================
# === Global Game State & Data ===
# ==========================

class GameState:
    def __init__(self):
        self.label_name = ""
        self.ceo_name = ""
        self.label_country = ""
        self.label_city = ""
        self.money = 5000
        self.week = 1
        self.starting_year = 2000
        self.sample_genres = ["Pop", "Hip Hop", "Rock", "Electronic", "Indie"]
        self.sample_names = ["Nova Flame", "Echo Drift", "Luna Vibe", "Shadow Pulse"]
        self.unsigned_artists = [self.generate_artist(name) for name in self.sample_names]
        self.signed_artists = []

    def generate_artist(self, name):
        """Generate a random unsigned artist profile."""
        return {
            "name": name,
            "genre": random.choice(self.sample_genres),
            "talent": random.randint(60, 100),
            "popularity": random.randint(10, 50),
            "signing_cost": random.choice([0, 1000, 2000, 3000]),
            "releases": [],
            "last_promoted_week": 0
        }

game_state = GameState()

# Create save folder if needed
if not os.path.exists('saves'):
    os.makedirs('saves')

# ==========================
# === Save / Load System ===
# ==========================

def save_game(slot, label=""):
    """Save the current game state to a slot."""
    save_data = {
        'game_state': game_state,
        'label': label or f"Slot {slot}",
        'timestamp': datetime.now().isoformat()
    }
    with open(f'saves/slot_{slot}.pkl', 'wb') as f:
        pickle.dump(save_data, f)


def load_game(slot):
    """Load game state from a save slot."""
    global game_state
    file_path = f'saves/slot_{slot}.pkl'
    if not os.path.exists(file_path):
        return False
    try:
        with open(file_path, 'rb') as f:
            save_data = pickle.load(f)
        loaded_state = save_data.get('game_state')
        if not isinstance(loaded_state, GameState):
            return False
        migrate_save_data(loaded_state)
        game_state = loaded_state
        return True
    except Exception:
        return False


def delete_save(slot):
    """Delete a save slot file."""
    file_path = f'saves/slot_{slot}.pkl'
    if os.path.exists(file_path):
        os.remove(file_path)


def get_save_slots():
    """Return current save slot metadata for the UI."""
    slots = {}
    for i in range(1, 4):
        file_path = f'saves/slot_{i}.pkl'
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    save_data = pickle.load(f)
                label = save_data.get('label', f'Slot {i}')
                timestamp_str = save_data.get('timestamp', '')
                formatted_time = 'Unknown'
                if timestamp_str:
                    try:
                        formatted_time = datetime.fromisoformat(timestamp_str).strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        formatted_time = timestamp_str

                saved_state = save_data.get('game_state')
                game_date = 'Unknown'
                if isinstance(saved_state, GameState):
                    game_date = get_current_date(getattr(saved_state, 'week', 1), getattr(saved_state, 'starting_year', 2000))

                slots[i] = {
                    'exists': True,
                    'label': label,
                    'timestamp': formatted_time,
                    'game_date': game_date
                }
            except Exception:
                slots[i] = {
                    'exists': True,
                    'label': f'Slot {i}',
                    'timestamp': 'Unknown',
                    'game_date': 'Unknown'
                }
        else:
            slots[i] = {
                'exists': False,
                'label': '',
                'timestamp': '',
                'game_date': ''
            }
    return slots


def migrate_save_data(state):
    """Ensure loaded saves have required fields for newer versions."""
    if not state:
        return

    if not hasattr(state, 'label_name'):
        state.label_name = ''
    if not hasattr(state, 'ceo_name'):
        state.ceo_name = ''
    if not hasattr(state, 'label_country'):
        state.label_country = ''
    if not hasattr(state, 'label_city'):
        state.label_city = ''
    if not hasattr(state, 'money'):
        state.money = 5000
    if not hasattr(state, 'week'):
        state.week = 1
    if not hasattr(state, 'starting_year'):
        state.starting_year = 2000
    if not hasattr(state, 'unsigned_artists'):
        state.unsigned_artists = []
    if not hasattr(state, 'signed_artists'):
        state.signed_artists = []

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
    return any(r.get("week") == game_state.week for r in artist.get("releases", []))

# ==========================
# === Game Mechanics ===
# ==========================

def promote_artist(artist):
    """Spend money to increase artist popularity."""
    cost = 500
    if artist["last_promoted_week"] == game_state.week:
        return f"{artist['name']} has already been promoted this week."
    if game_state.money < cost:
        return "You don't have enough money to promote this artist."
    increase = random.randint(5, 15)
    artist["popularity"] = min(100, artist["popularity"] + increase)
    artist["last_promoted_week"] = game_state.week
    game_state.money -= cost
    return f"You promoted {artist['name']}! Popularity increased by {increase}. Remaining balance: ${game_state.money}"

def release_single(artist):
    """Spend money to release a new single for the artist."""
    cost = 500
    if game_state.money < cost:
        return "You don't have enough money to release a single."
    if has_released_this_week(artist):
        return f"{artist['name']} has already released something this week."
    title = generate_release_name()
    artist["releases"].append({"type": "Single", "name": title, "week": game_state.week, "year": get_current_date(game_state.week, game_state.starting_year).split(', ')[1]})
    game_state.money -= cost
    return f"{artist['name']} released a single titled '{title}'. Cost: ${cost}. Remaining funds: ${game_state.money}"

def release_album(artist):
    """Spend money to release a new album for the artist."""
    cost = 1500
    if game_state.money < cost:
        return "You don't have enough money to release an album."
    if has_released_this_week(artist):
        return f"{artist['name']} has already released something this week."
    title = generate_release_name()
    artist["releases"].append({"type": "Album", "name": title, "week": game_state.week, "year": get_current_date(game_state.week, game_state.starting_year).split(', ')[1]})
    game_state.money -= cost
    return f"{artist['name']} released an album titled '{title}'. Cost: ${cost}. Remaining funds: ${game_state.money}"

def finish_week():
    """End the week, calculate revenue based on releases with depreciation, and advance time."""
    summary = f"--- Week {game_state.week} Summary ---\n"
    weekly_revenue = 0
    for artist in game_state.signed_artists:
        artist_revenue = 0
        active_singles = 0
        active_albums = 0
        for release in artist.get("releases", []):
            release_week = release.get("week", 0)
            age = game_state.week - release_week
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
            summary += f"{artist['name']} earned ${artist_revenue} from {active_singles} single(s) and {active_albums} album(s) (Popularity: {artist['popularity']}).\n"
    game_state.money += weekly_revenue
    summary += f"\nTotal weekly revenue: ${weekly_revenue}"
    game_state.week += 1
    return summary

# ==========================
# === Flask Routes ===
# ==========================

@app.route('/', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        game_state.ceo_name = request.form['ceo_name']
        game_state.label_name = request.form['label_name']
        game_state.starting_year = int(request.form['starting_year'])
        game_state.label_country = request.form['country']
        game_state.label_city = request.form['city']
        return redirect(url_for('menu'))
    return render_template('setup.html')

@app.route('/menu')
def menu():
    save_slots = get_save_slots()
    return render_template('menu.html', game_state=game_state, get_current_date=get_current_date, save_slots=save_slots)

@app.route('/save_game/<int:slot>', methods=['POST'])
def save_game_route(slot):
    if 1 <= slot <= 3:
        label = request.form.get('label', f'Slot {slot}')
        save_game(slot, label)
        flash(f'Saved to slot {slot}.')
    return redirect(request.referrer or url_for('menu'))

@app.route('/load_game/<int:slot>')
def load_game_route(slot):
    if 1 <= slot <= 3 and load_game(slot):
        flash(f'Loaded slot {slot}.')
        return redirect(url_for('menu'))
    flash(f'Unable to load slot {slot}.')
    return redirect(request.referrer or url_for('menu'))

@app.route('/delete_game/<int:slot>')
def delete_game_route(slot):
    if 1 <= slot <= 3:
        delete_save(slot)
        flash(f'Deleted slot {slot}.')
    return redirect(request.referrer or url_for('menu'))

@app.route('/unsigned')
def unsigned():
    return render_template('unsigned.html', game_state=game_state, get_current_date=get_current_date)

@app.route('/sign_artist/<int:idx>', methods=['POST'])
def sign_artist(idx):
    artist = game_state.unsigned_artists[idx]
    if game_state.money >= artist['signing_cost']:
        game_state.signed_artists.append(artist)
        game_state.unsigned_artists.pop(idx)
        game_state.money -= artist['signing_cost']
        flash(f"You signed {artist['name']}! Remaining funds: ${game_state.money}")
    else:
        flash("Not enough funds to sign this artist.")
    return redirect(url_for('unsigned'))

@app.route('/signed')
def signed():
    return render_template('signed.html', game_state=game_state, get_current_date=get_current_date)

@app.route('/manage_artist/<int:idx>')
def manage_artist(idx):
    artist = game_state.signed_artists[idx]
    return render_template('manage_artist.html', artist=artist, idx=idx, game_state=game_state, get_current_date=get_current_date)

@app.route('/promote_artist/<int:idx>', methods=['POST'])
def promote_artist_route(idx):
    artist = game_state.signed_artists[idx]
    message = promote_artist(artist)
    flash(message)
    return redirect(url_for('manage_artist', idx=idx))

@app.route('/release_single/<int:idx>', methods=['POST'])
def release_single_route(idx):
    artist = game_state.signed_artists[idx]
    message = release_single(artist)
    flash(message)
    return redirect(url_for('manage_artist', idx=idx))

@app.route('/release_album/<int:idx>', methods=['POST'])
def release_album_route(idx):
    artist = game_state.signed_artists[idx]
    message = release_album(artist)
    flash(message)
    return redirect(url_for('manage_artist', idx=idx))

@app.route('/finish_week', methods=['POST'])
def finish_week_route():
    summary = finish_week()
    flash(summary)
    return redirect(url_for('menu'))

if __name__ == "__main__":
    app.run(debug=True)
