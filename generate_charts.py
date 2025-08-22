import os, requests, math
import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
from datetime import datetime
from zoneinfo import ZoneInfo
import time

API = os.getenv("API") # link to back-end
if not API:
   raise RuntimeError("Missing API env var. Set API in Github Actions (or locally) before running.")

OUT_DIR = os.path.join("docs", "charts")
os.makedirs(OUT_DIR, exist_ok=True) # creates a folder for docs/charts, ignores if already existing

# customize the palette
COLORS = ["#374151", "#10B981", "#3B82F6"]  # charcoal, teal, blue
# dictonary for reassigning labels
LABEL_PRETTY = {
    "less_than_30_percent": "< 30%",
    "between_30_and_50_percent": "30–50%",
    "greater_than_50_percent": "> 50%",
}

# dictonary for state to abbrev. to find image file path
STATE_CODES = {
    "alabama": "al",
    "alaska": "ak",
    "arizona": "az",
    "arkansas": "ar",
    "california": "ca",
    "colorado": "co",
    "connecticut": "ct",
    "delaware": "de",
    "district of columbia": "dc",
    "florida": "fl",
    "georgia": "ga",
    "hawaii": "hi",
    "idaho": "id",
    "illinois": "il",
    "indiana": "in",
    "iowa": "ia",
    "kansas": "ks",
    "kentucky": "ky",
    "louisiana": "la",
    "maine": "me",
    "maryland": "md",
    "massachusetts": "ma",
    "michigan": "mi",
    "minnesota": "mn",
    "mississippi": "ms",
    "missouri": "mo",
    "montana": "mt",
    "nebraska": "ne",
    "nevada": "nv",
    "new hampshire": "nh",
    "new jersey": "nj",
    "new mexico": "nm",
    "new york": "ny",
    "north carolina": "nc",
    "north dakota": "nd",
    "ohio": "oh",
    "oklahoma": "ok",
    "oregon": "or",
    "pennsylvania": "pa",
    "rhode island": "ri",
    "south carolina": "sc",
    "south dakota": "sd",
    "tennessee": "tn",
    "texas": "tx",
    "utah": "ut",
    "vermont": "vt",
    "virginia": "va",
    "washington": "wa",
    "west virginia": "wv",
    "wisconsin": "wi",
    "wyoming": "wy",
}

# necessary to loop over every state for creating all images
STATES = list(STATE_CODES.keys())
METROS = [1,3,5]


def metroLabel(metro: int) :
    if (metro == 1) :
      return "central city"
    elif (metro == 3) :
      return "suburban area"
    elif (metro == 5) :
        return "rural/small town"
    else : return "error"

def fetch(state: str, metro: int):
    url = f"{API}?state={state}&metro={metro}"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.json()

def to_labels_values(dist: dict):
    # keep a fixed order that matches COLORS
    order = ["less_than_30_percent", "between_30_and_50_percent", "greater_than_50_percent"]
    labels = [LABEL_PRETTY[k] for k in order]
    values = [float(dist[k]) for k in order]

    # normalize if needed (robustness)
    s = sum(values)
    if not math.isclose(s, 1.0, rel_tol=1e-3, abs_tol=1e-3):
        values = [v / s for v in values]
    return labels, values

def render_and_save(data: dict, state_name: str, state_code: str, metro: int):
    region_dist = data["region_stats"]["burden_distribution"]
    metro_dist = data["metro_stats"]["burden_distribution"]

    r_labels, r_vals = to_labels_values(region_dist)
    m_labels, m_vals = to_labels_values(metro_dist)

    fig, axes = plt.subplots(1, 2, figsize=(9, 4), dpi=120)
    explode = [0, 0.06, 0]  # emphasize 30–50%

    # region pie chart
    w0, t0, autotext0 = axes[0].pie(r_vals, labels=r_labels, autopct="%1.1f%%",
                startangle=90, colors=COLORS, explode=explode,
                textprops={"fontsize": 9})
    axes[0].set_title("Region: " + state_code.upper(), fontsize=11)

    # metro pie chart
    w1, t1, autotext1 = axes[1].pie(m_vals, labels=m_labels, autopct="%1.1f%%",
                startangle=90, colors=COLORS, explode=explode,
                textprops={"fontsize": 9})
    axes[1].set_title(f"Metro: {metro}", fontsize=11)

    # setting percentage text to white for <30%
    autotext0[0].set_color("white")  # Region pie, <30%
    autotext1[0].set_color("white")  # Metro pie, <30%


    # shared title + caption
    fig.suptitle(f"Housing Burden Distribution", fontsize=13, y=0.98)
    eastern = ZoneInfo("America/New_York")
    timestamp = datetime.now(eastern).strftime("%Y-%m-%d %H:%M %Z")
    caption = f"{metroLabel(metro)} in {state_name.lower()} · github/jasmingg · Built: {timestamp}"
    fig.text(0.5, 0.02, caption, ha="center", va="bottom", fontsize=9)
    fig.subplots_adjust(top=0.85, bottom=0.14, wspace=0.32)

    base = f"housing_burden_{state_code}_metro{metro}_latest"
    svg_path = os.path.join(OUT_DIR, f"{base}.svg")
    png_path = os.path.join(OUT_DIR, f"{base}.png")

    try:
        fig.savefig(svg_path, format="svg", bbox_inches="tight")
        print(f"✅ Saved {svg_path}")
    except Exception as e:
        print(f"⚠️ SVG failed for {svg_path}: {e}")
        print(f"🖼️ Trying PNG fallback...")
        try:
            fig.savefig(png_path, format="png", bbox_inches="tight", dpi=200)
            print(f"✅ PNG saved: {png_path}")
        except Exception as e2:
            print(f"❌ Failed both SVG and PNG for {base}: {e2}")


    plt.close(fig)


def main():
    count = 0
    for state in STATES:
      for metro in METROS:
        count += 1
        # necessary for avoiding rate-limiting client error from Java 
        if count % 30 == 0:  # every 30 requests
            print("⏳ Waiting to avoid 429...")
            time.sleep(35)  # wait ~35 seconds to stay under 60/min
        try:
          data = fetch(state, metro)
          code = STATE_CODES[state]
          render_and_save(data, state, code, metro)
        except Exception as e:
           print(f"[WARN] Skipping {state} metro {metro}: {e}")

if __name__ == "__main__":
    main()
