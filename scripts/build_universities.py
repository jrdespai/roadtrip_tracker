#!/usr/bin/env python3
"""Generate universities.json from NCAA D1 schools + curated regional supplements."""

import csv
import json
import re
import unicodedata
import urllib.request
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
D1_URL = "https://raw.githubusercontent.com/Lowgy/d1-atlas/main/app/data/colleges.ts"
CSV_URL = "https://raw.githubusercontent.com/zicodeng/us-colleges/master/data/us-colleges.csv"

STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "District of Columbia": "DC", "D.C.": "DC", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME",
    "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
    "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
}

# Short D1 nicknames -> search tokens for CSV name scoring
D1_ALIASES = {
    "Air Force": ["air force academy"],
    "Army": ["military academy"],
    "Navy": ["naval academy"],
    "Alabama A&M": ["alabama a", "m university"],
    "American": ["american university"],
    "Arkansas-Pine Bluff": ["arkansas at pine bluff"],
    "Cal Poly": ["cal polytechnic", "san luis obispo"],
    "CSU Bakersfield": ["bakersfield"],
    "CSU Fullerton": ["fullerton"],
    "CSU Northridge": ["northridge"],
    "Florida A&M": ["agricultural and mechanical"],
    "Fresno State": ["fresno"],
    "Georgia Tech": ["georgia institute of technology"],
    "George Washington": ["george washington university"],
    "Georgetown": ["georgetown university"],
    "Grand Canyon": ["grand canyon university"],
    "Hawaii": ["hawaii at manoa"],
    "Howard": ["howard university"],
    "IUPUI": ["indianapolis"],
    "IU Indy": ["indianapolis"],
    "Jacksonville": ["jacksonville university"],
    "Kansas City": ["missouri-kansas city"],
    "LIU": ["long island university"],
    "LMU": ["loyola marymount"],
    "Louisiana-Monroe": ["louisiana at monroe"],
    "Loyola (IL)": ["loyola university chicago"],
    "Loyola (MD)": ["loyola university maryland"],
    "LSU": ["louisiana state"],
    "Miami (FL)": ["university of miami"],
    "Miami (OH)": ["miami university"],
    "NC A&T": ["north carolina a"],
    "NC Central": ["north carolina central"],
    "NJIT": ["new jersey institute"],
    "North Carolina": ["north carolina at chapel hill"],
    "Notre Dame": ["notre dame"],
    "Ohio State": ["ohio state university"],
    "Ole Miss": ["mississippi"],
    "Penn State": ["pennsylvania state university"],
    "Queens": ["queens university of charlotte"],
    "Sacramento State": ["sacramento"],
    "Saint Francis (PA)": ["saint francis university"],
    "Saint Louis": ["saint louis university"],
    "Saint Mary's": ["saint mary"],
    "Saint Peter's": ["saint peter"],
    "San Diego": ["san diego state"],
    "San Francisco": ["san francisco"],
    "Seattle": ["seattle university"],
    "SIU Edwardsville": ["edwardsville"],
    "SMU": ["southern methodist"],
    "Southern": ["southern university"],
    "Southern Miss": ["southern mississippi"],
    "St. Bonaventure": ["st bonaventure"],
    "St. Thomas": ["st thomas"],
    "TCU": ["texas christian"],
    "Texas A&M": ["texas a", "m university", "college station"],
    "Texas A&M Commerce": ["texas a", "m university", "commerce"],
    "Texas A&M-Corpus Christi": ["corpus christi"],
    "The Citadel": ["citadel military"],
    "UAB": ["alabama at birmingham"],
    "UC Davis": ["california-davis"],
    "UC Irvine": ["california-irvine"],
    "UC Riverside": ["california-riverside"],
    "UC San Diego": ["california-san diego"],
    "UC Santa Barbara": ["california-santa barbara"],
    "UCF": ["central florida"],
    "UCLA": ["california-los angeles"],
    "UConn": ["connecticut"],
    "UIC": ["illinois chicago"],
    "UMass": ["massachusetts-amherst"],
    "UMass Lowell": ["massachusetts-lowell"],
    "UNC Asheville": ["north carolina at asheville"],
    "UNC Greensboro": ["north carolina at greensboro"],
    "UNC Wilmington": ["north carolina wilmington"],
    "UNLV": ["nevada-las vegas"],
    "USC": ["southern california"],
    "USC Upstate": ["south carolina-upstate"],
    "UT Arlington": ["texas at arlington"],
    "UT Martin": ["tennessee-martin"],
    "UTEP": ["texas at el paso"],
    "UTRGV": ["rio grande valley"],
    "UT Rio Grande Valley": ["rio grande valley"],
    "UTSA": ["texas at san antonio"],
    "Utah Tech": ["dixie state", "utah tech"],
    "VCU": ["virginia commonwealth"],
    "William & Mary": ["william", "mary"],
    "Green Bay": ["wisconsin-green bay"],
    "Milwaukee": ["wisconsin-milwaukee"],
    "Binghamton": ["binghamton"],
    "Buffalo": ["buffalo"],
    "Incarnate Word": ["incarnate word"],
    "Little Rock": ["arkansas at little rock"],
    "Central Arkansas": ["central arkansas"],
    "North Alabama": ["north alabama"],
    "North Florida": ["north florida"],
    "North Texas": ["north texas"],
    "South Alabama": ["south alabama"],
    "South Florida": ["south florida"],
    "West Georgia": ["west georgia"],
    "Charleston": ["charleston"],
    "Charlotte": ["north carolina at charlotte"],
    "Chattanooga": ["tennessee-chattanooga"],
    "Houston Christian": ["houston christian"],
    "Long Island": ["long island university"],
    "Loyola Marymount": ["loyola marymount"],
    "New Orleans": ["new orleans"],
    "Omaha": ["nebraska at omaha"],
    "Portland": ["portland state"],
    "Prairie View A&M": ["prairie view"],
    "Queens (NC)": ["queens university of charlotte"],
    "St. Francis (PA)": ["saint francis university"],
    "St. John's": ["st john"],
    "Princeton": ["princeton university"],
    "Texas": ["texas at austin"],
    "Penn": ["university of pennsylvania"],
    "Virginia": ["university of virginia"],
    "Washington": ["university of washington"],
    "California": ["university of california-berkeley", "berkeley"],
    "Colorado": ["university of colorado boulder", "colorado boulder"],
    "Oregon": ["university of oregon"],
    "Utah": ["university of utah"],
    "Nebraska": ["university of nebraska-lincoln", "nebraska lincoln"],
    "Minnesota": ["university of minnesota-twin cities", "minnesota twin"],
    "Missouri": ["university of missouri-columbia", "missouri columbia"],
    "Illinois": ["university of illinois urbana", "illinois urbana"],
    "Iowa": ["university of iowa"],
    "Kansas": ["university of kansas"],
    "Maryland": ["university of maryland-college park", "maryland college park"],
    "Massachusetts": ["university of massachusetts"],
    "New Mexico": ["university of new mexico"],
    "New Hampshire": ["university of new hampshire"],
    "Maine": ["university of maine"],
    "Delaware": ["university of delaware"],
    "Connecticut": ["university of connecticut"],
    "Vermont": ["university of vermont"],
    "Rhode Island": ["university of rhode island"],
    "Montana": ["university of montana"],
    "Idaho": ["university of idaho"],
    "Nevada": ["university of nevada"],
    "Wyoming": ["university of wyoming"],
    "Alabama": ["university of alabama"],
    "Auburn": ["auburn university"],
    "Florida": ["university of florida"],
    "Florida State": ["florida state university"],
    "Georgia": ["university of georgia"],
    "Michigan": ["university of michigan"],
    "Wisconsin": ["university of wisconsin-madison"],
    "Indiana": ["indiana university-bloomington"],
    "Kentucky": ["university of kentucky"],
    "Tennessee": ["university of tennessee"],
    "Ohio": ["ohio state university"],
    "Oklahoma": ["university of oklahoma"],
    "Arkansas": ["university of arkansas"],
    "Arizona": ["university of arizona"],
    "Louisiana": ["louisiana state"],
    "Mississippi": ["university of mississippi"],
    "South Carolina": ["university of south carolina-columbia"],
    "North Dakota": ["university of north dakota"],
    "South Dakota": ["university of south dakota"],
    "West Virginia": ["west virginia university"],
    "Virginia Tech": ["virginia polytechnic", "virginia tech"],
}

MANUAL = {
    "Grand Canyon University": {"city": "Phoenix", "state": "AZ", "lat": 33.5133, "lng": -112.1299},
    "University of Texas Rio Grande Valley": {"city": "Edinburg", "state": "TX", "lat": 26.3064, "lng": -98.1742},
}

# D1 short names that need hardcoded official entries (missing or ambiguous in CSV)
D1_OVERRIDES = {
    "Grand Canyon": {
        "name": "Grand Canyon University",
        "city": "Phoenix",
        "state": "AZ",
        "lat": 33.5133,
        "lng": -112.1299,
    },
    "UTRGV": {
        "name": "University of Texas Rio Grande Valley",
        "city": "Edinburg",
        "state": "TX",
        "lat": 26.3064,
        "lng": -98.1742,
    },
    "UT Rio Grande Valley": {
        "name": "University of Texas Rio Grande Valley",
        "city": "Edinburg",
        "state": "TX",
        "lat": 26.3064,
        "lng": -98.1742,
    },
}

# Prominent non-D1 / regional four-year institutions (exact official names)
SUPPLEMENTAL = [
    "University of Alaska Anchorage",
    "University of Alaska Fairbanks",
    "University of Alaska Southeast",
    "Alaska Pacific University",
    "Massachusetts Institute of Technology",
    "Williams College",
    "Amherst College",
    "Swarthmore College",
    "Pomona College",
    "Wellesley College",
    "Middlebury College",
    "Bowdoin College",
    "Carleton College",
    "Davidson College",
    "Colby College",
    "Bates College",
    "Hamilton College",
    "Vassar College",
    "Grinnell College",
    "Macalester College",
    "Oberlin College",
    "Reed College",
    "Whitman College",
    "Harvey Mudd College",
    "Washington and Lee University",
    "Bucknell University",
    "Lafayette College",
    "Lehigh University",
    "Creighton University",
    "Drake University",
    "Bradley University",
    "Butler University",
    "DePaul University",
    "Marquette University",
    "University of the Pacific",
    "University of San Diego",
    "Pepperdine University",
    "Chapman University",
    "University of Puget Sound",
    "Whitworth University",
    "Seattle Pacific University",
    "Pacific Lutheran University",
    "Willamette University",
    "Trinity University",
    "Southwestern University",
    "Austin College",
    "Rice University",
    "Emory University",
    "Tulane University of Louisiana",
    "University of Denver",
    "Colorado College",
    "University of New England",
    "Quinnipiac University",
    "Fairfield University",
    "University of Scranton",
    "Duquesne University",
    "Drexel University",
    "Elon University",
    "High Point University",
    "James Madison University",
    "University of Richmond",
    "Allegheny College",
    "Dickinson College",
    "Franklin & Marshall College",
    "Gettysburg College",
    "Haverford College",
    "Bryn Mawr College",
    "Rochester Institute of Technology",
    "Rensselaer Polytechnic Institute",
    "Skidmore College",
    "St Lawrence University",
    "Ithaca College",
    "University of Dayton",
    "Case Western Reserve University",
    "John Carroll University",
    "College of Wooster",
    "Kenyon College",
    "Denison University",
    "Ohio Wesleyan University",
    "University of Evansville",
    "Valparaiso University",
    "University of Indianapolis",
    "Ball State University",
    "Indiana State University",
    "University of Southern Indiana",
    "University of Wisconsin-Eau Claire",
    "University of Wisconsin-La Crosse",
    "University of Nebraska at Kearney",
    "University of Nebraska at Omaha",
    "University of Central Missouri",
    "University of Missouri-Kansas City",
    "University of Louisiana at Lafayette",
    "Florida Gulf Coast University",
    "Florida Atlantic University",
    "Florida International University",
    "Rollins College",
    "Flagler College-St Augustine",
    "Georgia Southern University",
    "Kennesaw State University",
    "Mercer University",
    "Spelman College",
    "Morehouse College",
    "Coastal Carolina University",
    "Furman University",
    "Presbyterian College",
    "Belmont University",
    "Lipscomb University",
    "Rhodes College",
    "Sewanee-The University of the South",
    "Boise State University",
    "Idaho State University",
    "Montana Tech of the University of Montana",
    "Norwich University",
    "Champlain College",
    "Keene State College",
    "Plymouth State University",
    "Providence College",
    "Bryant University",
    "Towson University",
    "Salisbury University",
    "Christopher Newport University",
    "Old Dominion University",
    "Radford University",
    "Longwood University",
    "University of Mary Washington",
    "Hampton University",
    "Liberty University",
    "St Olaf College",
    "Gustavus Adolphus College",
    "Concordia College at Moorhead",
    "Carthage College",
    "Lawrence University",
    "Beloit College",
    "Ripon College",
    "University of Wisconsin-Whitewater",
    "University of Wisconsin-Stevens Point",
    "Oakland University",
    "Grand Valley State University",
    "Hope College",
    "Kalamazoo College",
    "Calvin University",
    "Hillsdale College",
    "Centre College",
    "Transylvania University",
    "California Institute of Technology",
    "University of California-Merced",
    "University of California-Santa Cruz",
    "Sonoma State University",
    "Azusa Pacific University",
    "Biola University",
    "Point Loma Nazarene University",
    "Western Washington University",
    "Central Washington University",
    "Eastern Washington University",
    "Linfield University",
    "Pacific University",
    "Southern Oregon University",
    "Eastern Oregon University",
    "Oregon Institute of Technology",
]


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def slugify(name: str) -> str:
    text = normalize(name)
    text = re.sub(r"\b(the|of|at|in|and|a|an)\b", " ", text)
    return re.sub(r"\s+", "-", text.strip())[:80]


def csv_state(row_state: str, target: str) -> bool:
    if row_state == target:
        return True
    return target == "DC" and row_state == "NA"


def normalize_state(row_state: str) -> str:
    return "DC" if row_state == "NA" else row_state


def city_match(a: str, b: str) -> bool:
    na, nb = normalize(a), normalize(b)
    return na == nb or na in nb or nb in na


def search_tokens(short_name: str) -> list[str]:
    if short_name in D1_ALIASES:
        return D1_ALIASES[short_name]
    return [normalize(short_name)]


def score_row(name: str, tokens: list[str]) -> int:
    name_n = normalize(name)
    if any(term in name_n for term in ("seminary", "theological", "rabbinical", "bible college")):
        return -100
    score = 0
    for token in tokens:
        if token in name_n:
            score += len(token.split()) + 2
    for word in tokens[0].split():
        if len(word) > 2 and word in name_n:
            score += 1
    if name_n.startswith(tokens[0]) or tokens[0] in name_n:
        score += 4
    return score


def find_csv_by_name(name: str) -> Optional[dict]:
    name_n = normalize(name)
    for row in csv_rows:
        if normalize(row["name"]) == name_n:
            return row
    for row in csv_rows:
        if name_n in normalize(row["name"]):
            return row
    return None


def find_csv_for_d1(short_name: str, city: str, state: str) -> Optional[dict]:
    tokens = search_tokens(short_name)
    candidates = [
        row for row in csv_rows
        if csv_state(row["state_abbreviation"], state) and city_match(row["city"], city)
    ]
    if not candidates:
        candidates = [row for row in csv_rows if csv_state(row["state_abbreviation"], state)]

    best = None
    best_score = 0
    for row in candidates:
        score = score_row(row["name"], tokens)
        if city_match(row["city"], city):
            score += 3
        if score > best_score:
            best_score = score
            best = row
    return best if best_score >= 4 else None


def make_entry(name: str, city: str, state: str, lat: float, lng: float) -> dict:
    return {
        "id": f"uni-{slugify(name)}",
        "name": name,
        "type": "university",
        "city": city,
        "state": state,
        "lat": round(float(lat), 6),
        "lng": round(float(lng), 6),
    }


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "roadtrip-tracker/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def parse_d1(content: str) -> list[dict]:
    pattern = (
        r"\{\s*id:\s*\d+,\s*name:\s*'([^']+)',\s*location:\s*\{\s*"
        r"city:\s*'([^']+)',\s*state:\s*'([^']+)',\s*"
        r"lat:\s*([\d.-]+),\s*lng:\s*([\d.-]+),"
    )
    schools = []
    for match in re.finditer(pattern, content):
        name, city, state, lat, lng = match.groups()
        schools.append({
            "short_name": name,
            "city": city.strip(),
            "state": STATE_ABBR.get(state, state),
            "lat": float(lat),
            "lng": float(lng),
        })
    return schools


def main() -> None:
    global csv_rows
    d1_content = fetch(D1_URL)
    csv_text = fetch(CSV_URL)
    csv_rows = list(csv.DictReader(csv_text.splitlines()))

    universities: dict[tuple[str, str], dict] = {}

    def add(entry: dict) -> None:
        key = (normalize(entry["name"]), entry["state"])
        if key not in universities:
            universities[key] = entry

    for school in parse_d1(d1_content):
        if school["short_name"] in D1_OVERRIDES:
            override = D1_OVERRIDES[school["short_name"]]
            add(make_entry(
                override["name"], override["city"], override["state"],
                override["lat"], override["lng"],
            ))
            continue

        row = find_csv_for_d1(school["short_name"], school["city"], school["state"])
        if row:
            add(make_entry(
                row["name"], row["city"], normalize_state(row["state_abbreviation"]),
                row["latitude"], row["longitude"],
            ))
            continue

        official = D1_ALIASES.get(school["short_name"], [school["short_name"]])
        if isinstance(official, list):
            manual_name = None
        else:
            manual_name = official

        for manual_key, manual_data in MANUAL.items():
            if any(token in normalize(manual_key) for token in search_tokens(school["short_name"])):
                add(make_entry(manual_key, manual_data["city"], manual_data["state"], manual_data["lat"], manual_data["lng"]))
                break
        else:
            fallback_name = f"{school['short_name']} University"
            add(make_entry(
                fallback_name, school["city"], school["state"], school["lat"], school["lng"],
            ))

    for name in SUPPLEMENTAL:
        row = find_csv_by_name(name)
        if row:
            add(make_entry(
                row["name"], row["city"], normalize_state(row["state_abbreviation"]),
                row["latitude"], row["longitude"],
            ))

    result = sorted(universities.values(), key=lambda item: (item["state"], item["name"]))
    output = ROOT / "universities.json"
    with output.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, separators=(",", ":"))

    print(f"Wrote {len(result)} universities to {output}")


if __name__ == "__main__":
    main()
