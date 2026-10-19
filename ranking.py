"""
StudySync -- Find a Study Spot (Ticket 3, Tinker 3B).

TICKET: none of the ranking logic is implemented yet -- every function
below is a stub.
"""

import csv

NOISE_ORDER = {"quiet": 0, "moderate": 1, "loud": 2}


def load_study_spots(csv_path: str) -> list:
    """
    Load study spots from a CSV into a list of dicts, converting
    "distance_miles" to float and "seats_available" to int.
    """
    # TODO: use csv.DictReader to read csv_path into a list of dicts.
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    # TODO: convert row["distance_miles"] to float and row["seats_available"] to int for each row.
    for row in rows:
        row["distance_miles"] = float(row["distance_miles"])
        row["seats_available"] = int(row["seats_available"])
    return rows


def score_study_spot(profile: dict, spot: dict) -> tuple:
    """
    Score one study spot against a student profile.

    profile example: {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}

    Return (score, reasons) where reasons is a list of short strings
    explaining what contributed to the score, e.g. ["quiet enough", "close enough"].
    """

    # Noise, distance, and seats are weighted equally (+-1 each) on purpose:
    # giving any one factor more weight would systematically bury spots that
    # lose on that factor alone (e.g. closest-but-noisier), no matter how well
    # they do elsewhere, which narrows what the user ever sees in the top-k.
    score = 0
    reasons = []

    spot_noise = NOISE_ORDER[spot["noise_level"]]
    max_noise = NOISE_ORDER[profile["max_noise"]]
    if spot_noise <= max_noise:
        score += 1
        reasons.append("quiet enough")
    else:
        score -= 1
        reasons.append("too noisy")

    if spot["distance_miles"] <= profile["max_distance"]:
        score += 1
        reasons.append("close enough")
    else:
        score -= 1
        reasons.append("too far")

    if spot["seats_available"] >= profile["min_seats"]:
        score += 1
        reasons.append("enough seats")
    else:
        score -= 1
        reasons.append("not enough seats")

    return score, reasons


def rank_study_spots(profile: dict, spots: list, k: int = 3) -> list:
    """
    Score every study spot, then return the top k as (spot, score, reasons)
    tuples, sorted by score descending.
    """
    # TODO: score every spot with score_study_spot(), then use
    # sorted(..., key=..., reverse=True)[:k] to keep only the top k.
    scored = [(spot, *score_study_spot(profile, spot)) for spot in spots]
    return sorted(scored, key=lambda result: result[1], reverse=True)[:k]


def format_results(ranked: list) -> None:
    """Print each ranked study spot with its score and reasons, one line each."""
    # TODO: for each (spot, score, reasons) tuple, print a readable line, e.g.:
    # "1. Innovation Commons -- Score: 5.0 -- Because: quiet enough, close enough"
    for rank, (spot, score, reasons) in enumerate(ranked, start=1):
        print(
            f"{rank}. {spot['name']} -- Score: {score:.1f} -- Because: {', '.join(reasons)}"
        )


def render_study_spot_tab():
    import streamlit as st

    st.subheader("Find a Study Spot")
    max_noise = st.selectbox("Max noise level", ["quiet", "moderate", "loud"], index=1)
    max_distance = st.slider("Max distance (miles)", 0.0, 3.0, 1.0)
    min_seats = st.number_input("Minimum seats needed", min_value=1, value=4, step=1)

    if st.button("Find spots"):
        profile = {
            "max_noise": max_noise,
            "max_distance": max_distance,
            "min_seats": min_seats,
        }
        try:
            spots = load_study_spots("data/study_spots.csv")
            ranked = rank_study_spots(profile, spots, k=3)
            for spot, score, reasons in ranked:
                st.write(
                    f"**{spot['name']}** -- Score: {score:.1f} -- Because: {', '.join(reasons)}"
                )
        except NotImplementedError:
            st.warning("🚧 Ranking isn't implemented yet -- that's Tinker 3B's ticket.")


if __name__ == "__main__":
    spots = load_study_spots("data/study_spots.csv")
    profile = {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}
    ranked = rank_study_spots(profile, spots, k=3)
    format_results(ranked)
