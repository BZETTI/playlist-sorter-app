"""
Playlist Vibe Builder — Merge Sort Visualiser
CISC 121 Project | Queen's University

Sorts a playlist by energy score or duration using a hand-written
Merge Sort algorithm and shows every comparison step in the UI.
"""

import gradio as gr

# ── Default sample playlist ────────────────────────────────────────────────────
DEFAULT_SONGS = [
    {"title": "Blinding Lights",  "artist": "The Weeknd",     "energy": 80, "duration": 200},
    {"title": "Stay",             "artist": "Justin Bieber",  "energy": 45, "duration": 138},
    {"title": "Levitating",       "artist": "Dua Lipa",       "energy": 72, "duration": 203},
    {"title": "drivers license",  "artist": "Olivia Rodrigo", "energy": 35, "duration": 242},
    {"title": "Good 4 U",         "artist": "Olivia Rodrigo", "energy": 90, "duration": 178},
    {"title": "Peaches",          "artist": "Justin Bieber",  "energy": 55, "duration": 198},
    {"title": "Montero",          "artist": "Lil Nas X",      "energy": 68, "duration": 137},
    {"title": "Save Your Tears",  "artist": "The Weeknd",     "energy": 78, "duration": 215},
]


# ── Merge Sort — implemented from scratch (no sorted() / list.sort()) ──────────

def merge_sort(arr, key, steps):
    """
    Recursively splits the list in half and merges sorted halves.

    Decomposition:
        1. If list has 0 or 1 elements → already sorted (base case).
        2. Split into left and right halves.
        3. Recursively sort each half.
        4. Merge the two sorted halves.

    Parameters
    ----------
    arr   : list[dict]   – songs to sort
    key   : str          – 'energy' or 'duration'
    steps : list         – accumulates step records for visualisation

    Returns
    -------
    A new sorted list; the original is never mutated.
    """
    # Base case — a single-element list is trivially sorted
    if len(arr) <= 1:
        return arr[:]

    # --- Decompose: split into two halves ---
    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid],  key, steps)   # sort left half
    right = merge_sort(arr[mid:],  key, steps)   # sort right half

    # --- Conquer: merge the two sorted halves ---
    return _merge(left, right, key, steps)


def _merge(left, right, key, steps):
    """
    Merges two sorted sub-lists into one sorted list.

    Pattern Recognition:
        We always compare the *front* element of each sub-list.
        The smaller one is moved into the result.
        This comparison repeats until one sub-list is exhausted,
        then the remainder of the other is appended as-is.
    """
    result = []
    i = j  = 0

    while i < len(left) and j < len(right):
        a_val = left[i][key]
        b_val = right[j][key]

        # Record the comparison BEFORE deciding the winner
        steps.append({
            "type":   "compare",
            "a":      left[i],
            "b":      right[j],
            "key":    key,
            "picked": left[i] if a_val <= b_val else right[j],
            "merged": result[:],                # snapshot of result so far
        })

        # Append the smaller value; advance that pointer
        if a_val <= b_val:
            result.append(left[i]);  i += 1
        else:
            result.append(right[j]); j += 1

    # One sub-list is exhausted — append the rest of the other
    result.extend(left[i:])
    result.extend(right[j:])

    # Record the completed merge for this pair of sub-lists
    steps.append({
        "type":   "merge_done",
        "merged": result[:],
    })

    return result


# ── HTML / display helpers ─────────────────────────────────────────────────────

def _duration_str(secs: int) -> str:
    """Converts total seconds to MM:SS string."""
    return f"{secs // 60}:{secs % 60:02d}"


def _energy_bar(e: int) -> str:
    """Returns a 5-block emoji bar representing energy level."""
    filled = e // 20
    return "🟣" * filled + "⚪" * (5 - filled)


HEADER_STYLE = (
    'style="background:#16213e;color:#fff;padding:8px 10px;'
    'text-align:left;font-size:13px;"'
)
CELL_STYLE   = 'style="padding:6px 10px;font-size:13px;"'


def songs_to_html(songs: list, highlight: set = None) -> str:
    """
    Abstraction — renders songs as an HTML table.
    Highlights rows whose titles appear in `highlight` (gold = being compared).
    Internal pointers and recursion depth are hidden from the user.
    """
    highlight = highlight or set()
    rows = ""
    for idx, s in enumerate(songs):
        bg = "#ffe066" if s["title"] in highlight else ("#f4f4f4" if idx % 2 == 0 else "#ffffff")
        rows += (
            f'<tr style="background:{bg};">'
            f'<td {CELL_STYLE}>{idx + 1}</td>'
            f'<td {CELL_STYLE}><b>{s["title"]}</b></td>'
            f'<td {CELL_STYLE}>{s["artist"]}</td>'
            f'<td {CELL_STYLE} style="padding:6px 10px;text-align:center;">'
            f'{s["energy"]}&nbsp;{_energy_bar(s["energy"])}</td>'
            f'<td {CELL_STYLE} style="padding:6px 10px;text-align:center;">'
            f'{_duration_str(s["duration"])}</td>'
            f'</tr>'
        )
    return (
        '<table style="width:100%;border-collapse:collapse;">'
        f'<tr>'
        f'<th {HEADER_STYLE}>#</th>'
        f'<th {HEADER_STYLE}>Title</th>'
        f'<th {HEADER_STYLE}>Artist</th>'
        f'<th {HEADER_STYLE} style="background:#16213e;color:#fff;padding:8px 10px;text-align:center;">Energy</th>'
        f'<th {HEADER_STYLE} style="background:#16213e;color:#fff;padding:8px 10px;text-align:center;">Duration</th>'
        f'</tr>'
        + rows +
        '</table>'
    )


def steps_to_html(steps: list, key: str) -> str:
    """Converts the step log into a collapsible HTML simulation log."""
    if not steps:
        return "<p>No steps recorded.</p>"

    compare_count    = sum(1 for s in steps if s["type"] == "compare")
    merge_done_count = sum(1 for s in steps if s["type"] == "merge_done")

    html = (
        f'<div style="font-size:13px;margin-bottom:8px;">'
        f'<b>Comparisons:</b> {compare_count} &nbsp;|&nbsp; '
        f'<b>Merge completions:</b> {merge_done_count}'
        f'</div>'
        f'<p style="font-size:12px;color:#555;">'
        f'🟡 Gold rows = songs being compared this step. '
        f'Expand a step to see the merge-so-far list.</p>'
    )

    step_num = 0
    for step in steps:
        step_num += 1
        if step["type"] == "compare":
            a, b   = step["a"], step["b"]
            picked = step["picked"]
            html += (
                f'<details style="margin:5px 0;border:1px solid #ddd;'
                f'border-radius:6px;padding:4px 10px;">'
                f'<summary style="cursor:pointer;font-size:13px;">'
                f'<b>Step {step_num}</b> — Compare '
                f'<span style="color:#b5451b;">"{a["title"]}" ({key}={a[key]})</span>'
                f' vs '
                f'<span style="color:#1b6ab5;">"{b["title"]}" ({key}={b[key]})</span>'
                f' &rarr; ✅ <b>"{picked["title"]}"</b> placed next'
                f'</summary>'
                f'<p style="margin:4px 0 4px 12px;font-size:12px;color:#444;">'
                f'Merged so far: {[s["title"] for s in step["merged"]] or "(empty)"}'
                f'</p>'
                f'</details>'
            )
        elif step["type"] == "merge_done":
            titles = [s["title"] for s in step["merged"]]
            html += (
                f'<div style="margin:5px 0;padding:5px 10px;'
                f'background:#e8f5e9;border-left:4px solid #43a047;'
                f'border-radius:4px;font-size:13px;">'
                f'<b>✅ Sub-list merged:</b> {titles}'
                f'</div>'
            )
    return html


# ── Gradio callback functions ──────────────────────────────────────────────────

def add_song_fn(title, artist, energy, dur_min, dur_sec, songs):
    """Validates inputs and appends a new song to the playlist state."""
    title  = (title  or "").strip()
    artist = (artist or "").strip()

    # --- Input validation ---
    if not title:
        return songs, songs_to_html(songs), "⚠️ Song title cannot be empty."
    if not artist:
        return songs, songs_to_html(songs), "⚠️ Artist name cannot be empty."
    try:
        energy  = int(energy)
        dur_min = int(dur_min)
        dur_sec = int(dur_sec)
    except (ValueError, TypeError):
        return songs, songs_to_html(songs), "⚠️ Energy, minutes and seconds must be whole numbers."
    if not (0 <= energy <= 100):
        return songs, songs_to_html(songs), "⚠️ Energy must be 0–100."
    if dur_min < 0 or not (0 <= dur_sec <= 59):
        return songs, songs_to_html(songs), "⚠️ Minutes ≥ 0 and seconds must be 0–59."

    new_song = {
        "title":    title,
        "artist":   artist,
        "energy":   energy,
        "duration": dur_min * 60 + dur_sec,
    }
    updated = songs + [new_song]
    return updated, songs_to_html(updated), f"✅ '{title}' by {artist} added!"


def sort_fn(sort_key, songs):
    """Runs merge sort, collects steps, and returns three HTML panels."""
    if len(songs) < 2:
        msg = "<p>⚠️ Add at least 2 songs before sorting.</p>"
        return songs_to_html(songs), msg, songs_to_html(songs)

    steps        = []
    sorted_songs = merge_sort(songs, sort_key, steps)

    original_html = "<h4>📋 Original order</h4>"  + songs_to_html(songs)
    steps_html    = (
        f"<h4>🔄 Merge Sort simulation — sorting by <b>{sort_key}</b></h4>"
        + steps_to_html(steps, sort_key)
    )
    result_html   = (
        f"<h4>🎵 Sorted by <b>{sort_key}</b> (lowest → highest)</h4>"
        + songs_to_html(sorted_songs)
    )
    return original_html, steps_html, result_html


def reset_fn():
    """Restores the default sample playlist and clears all outputs."""
    return DEFAULT_SONGS[:], songs_to_html(DEFAULT_SONGS), "", "", ""


# ── Gradio UI ──────────────────────────────────────────────────────────────────

with gr.Blocks(title="🎵 Playlist Vibe Builder") as demo:

    # Hidden state — holds the current list of song dicts
    songs_state = gr.State(DEFAULT_SONGS[:])

    # ── Header ─────────────────────────────────────────────────────────────────
    gr.Markdown(
        """
        # 🎵 Playlist Vibe Builder — Merge Sort Visualiser
        Sort your playlist by **energy score** or **duration** and watch
        **Merge Sort** divide, compare, and conquer — step by step.

        > *CISC 121 Project — Queen's University Computing*
        """
    )

    # ── Current playlist display ────────────────────────────────────────────────
    gr.Markdown("## 📋 Current Playlist")
    playlist_display = gr.HTML(value=songs_to_html(DEFAULT_SONGS))

    # ── Add a song ──────────────────────────────────────────────────────────────
    with gr.Accordion("➕ Add a Song to the Playlist", open=False):
        gr.Markdown(
            "Enter the song details below. **Energy** is 0 (mellow) to 100 (intense). "
            "**Duration** is split into minutes and seconds."
        )
        with gr.Row():
            in_title  = gr.Textbox(label="Song Title *",  placeholder="e.g. Cruel Summer")
            in_artist = gr.Textbox(label="Artist *",      placeholder="e.g. Taylor Swift")
        with gr.Row():
            in_energy  = gr.Number(label="Energy (0–100) *",        value=70, minimum=0, maximum=100, precision=0)
            in_dur_min = gr.Number(label="Duration – minutes *",    value=3,  minimum=0, precision=0)
            in_dur_sec = gr.Number(label="Duration – seconds (0–59) *", value=30, minimum=0, maximum=59, precision=0)
        add_btn    = gr.Button("Add Song ➕", variant="secondary")
        add_status = gr.Markdown(value="")

    add_btn.click(
        fn=add_song_fn,
        inputs=[in_title, in_artist, in_energy, in_dur_min, in_dur_sec, songs_state],
        outputs=[songs_state, playlist_display, add_status],
    )

    # ── Sort controls ───────────────────────────────────────────────────────────
    gr.Markdown("## 🔀 Run Merge Sort")
    gr.Markdown(
        "Choose what to sort by, then click **▶ Run Merge Sort**. "
        "Expand any step in the simulation panel to see which two songs were compared."
    )
    with gr.Row():
        sort_key_radio = gr.Radio(
            choices=["energy", "duration"],
            value="energy",
            label="Sort by",
            info="energy = vibe intensity (0–100) | duration = song length",
        )
        with gr.Column(scale=1):
            sort_btn  = gr.Button("▶ Run Merge Sort",  variant="primary")
            reset_btn = gr.Button("🔄 Reset to Default", variant="stop")

    # ── Output panels ───────────────────────────────────────────────────────────
    with gr.Row():
        out_original = gr.HTML(label="Before")
        out_result   = gr.HTML(label="After")

    out_steps = gr.HTML(label="Step-by-step simulation")

    sort_btn.click(
        fn=sort_fn,
        inputs=[sort_key_radio, songs_state],
        outputs=[out_original, out_steps, out_result],
    )

    reset_btn.click(
        fn=reset_fn,
        inputs=[],
        outputs=[songs_state, playlist_display, out_original, out_steps, out_result],
    )

    # ── How-to guide ────────────────────────────────────────────────────────────
    gr.Markdown(
        """
        ---
        ### 📖 How Merge Sort works here
        | Stage | What happens |
        |-------|-------------|
        | **Split** | The playlist is halved repeatedly until each piece has 1 song |
        | **Compare** | Front songs of two sub-lists are compared by the chosen key |
        | **Merge** | The lower-value song is placed into the result; repeat until done |
        | **Done** | All sub-lists are merged back into one fully sorted playlist |

        ### 🎨 Colour guide
        | Colour | Meaning |
        |--------|---------|
        | 🟡 Gold rows | The two songs being compared in that step |
        | ✅ Green bar | A merge sub-operation finished successfully |
        """
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
