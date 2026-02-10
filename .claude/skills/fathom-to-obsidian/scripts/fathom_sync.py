#!/usr/bin/env python3
"""
Fathom -> Obsidian Sync
======================
Pulls meeting transcripts and AI summaries from the Fathom API
and saves them as formatted markdown files in an Obsidian vault.

Uses only Python standard library — no pip installs needed.

Usage:
    # Pull last 7 days of meetings
    python3 fathom_sync.py --api-key YOUR_KEY --output-dir /path/to/vault/Meetings --days 7

    # List meetings without saving (dry run)
    python3 fathom_sync.py --api-key YOUR_KEY --list-only --days 30

    # Pull a specific meeting
    python3 fathom_sync.py --api-key YOUR_KEY --output-dir /path/to/vault/Meetings --meeting-id rec_abc123

Security:
    - API key is only sent to api.fathom.ai over HTTPS
    - Only GET requests — nothing in your Fathom account is modified
    - Data goes straight from Fathom to local files, nowhere else
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ---------------------------------------------------------------------------
# Fathom API client
# ---------------------------------------------------------------------------

BASE_URL = "https://api.fathom.ai/external/v1"


def fathom_get(endpoint: str, api_key: str, params: dict = None) -> dict:
    """
    Make a GET request to the Fathom API.

    Args:
        endpoint: API path (e.g., "/meetings")
        api_key: Your Fathom API key
        params: Optional query parameters

    Returns:
        Parsed JSON response as a dict
    """
    url = f"{BASE_URL}{endpoint}"

    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
        if query:
            url = f"{url}?{query}"

    req = Request(url)
    req.add_header("X-Api-Key", api_key)
    req.add_header("Accept", "application/json")

    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Error: Fathom API returned {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Error: Could not reach Fathom API: {e.reason}", file=sys.stderr)
        sys.exit(1)


def list_meetings(api_key: str, created_after: str = None) -> list:
    """
    Fetch all meetings, handling pagination automatically.

    Args:
        api_key: Your Fathom API key
        created_after: ISO timestamp — only return meetings after this date

    Returns:
        List of meeting dicts
    """
    all_meetings = []
    cursor = None

    while True:
        params = {}
        if created_after:
            params["created_after"] = created_after
        if cursor:
            params["cursor"] = cursor

        data = fathom_get("/meetings", api_key, params)

        meetings = data.get("items", data.get("meetings", data.get("data", [])))
        if isinstance(meetings, list):
            all_meetings.extend(meetings)
        else:
            # If the response shape is unexpected, try to adapt
            all_meetings.append(meetings)

        # Handle pagination
        cursor = data.get("next_cursor") or data.get("cursor")
        if not cursor:
            break

        # Respect rate limits (60 calls/min)
        time.sleep(1)

    return all_meetings


def get_recording_id(meeting: dict) -> str:
    """Extract the recording ID from a meeting object."""
    # The API may nest this differently depending on version
    # Try direct recording_id first (current API), then nested recording.id
    rid = meeting.get("recording_id")
    if rid:
        return str(rid)
    rec = meeting.get("recording", {})
    return str(rec.get("id") or meeting.get("id", ""))


def get_summary(api_key: str, recording_id: str) -> dict:
    """
    Fetch the AI-generated summary for a recording.

    Returns:
        Summary dict with markdown content, or empty dict if unavailable
    """
    try:
        return fathom_get(f"/recordings/{recording_id}/summary", api_key)
    except SystemExit:
        # Summary might not be ready yet — not fatal
        return {}


def get_transcript(api_key: str, recording_id: str) -> list:
    """
    Fetch the full transcript for a recording.

    Returns:
        List of transcript segment dicts with speaker, text, timestamp
    """
    try:
        data = fathom_get(f"/recordings/{recording_id}/transcript", api_key)
        return data.get("transcript", data.get("items", data.get("segments", [])))
    except SystemExit:
        return []


# ---------------------------------------------------------------------------
# Markdown formatting
# ---------------------------------------------------------------------------

def sanitize_filename(name: str) -> str:
    """Remove characters that are unsafe for filenames."""
    # Replace slashes, colons, pipes, etc. with dashes
    cleaned = re.sub(r'[\\/:*?"<>|]', "-", name)
    # Collapse multiple dashes/spaces
    cleaned = re.sub(r"-{2,}", "-", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    return cleaned.strip(" -.")


def format_timestamp(seconds) -> str:
    """Convert seconds to a human-readable timestamp like 1:23:45 or 0:45."""
    if seconds is None:
        return ""
    try:
        seconds = int(float(seconds))
    except (ValueError, TypeError):
        return str(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def parse_meeting_datetime(meeting: dict) -> datetime:
    """Extract a datetime from the meeting's timestamp fields."""
    for field in ["scheduled_at", "created_at", "recorded_at"]:
        val = meeting.get(field)
        if val:
            try:
                # Handle ISO format with or without timezone
                if val.endswith("Z"):
                    val = val[:-1] + "+00:00"
                return datetime.fromisoformat(val)
            except ValueError:
                continue
    return datetime.now(timezone.utc)


def format_meeting_markdown(meeting: dict, summary_data: dict, transcript_segments: list) -> str:
    """
    Build the full markdown content for a meeting note.

    Structure:
        - YAML frontmatter (title, date, attendees, etc.)
        - ## Summary (AI-generated)
        - ## Action Items (extracted from summary if available)
        - ## Transcript (speaker-labeled, timestamped)
    """
    dt = parse_meeting_datetime(meeting)
    title = meeting.get("title") or meeting.get("meeting_title") or "Untitled Meeting"
    recording_id = get_recording_id(meeting)
    fathom_url = meeting.get("share_url") or meeting.get("url") or ""

    # --- Attendees ---
    invitees = meeting.get("calendar_invitees", [])
    attendee_lines = []
    for inv in invitees:
        name = inv.get("name", "Unknown")
        email = inv.get("email", "")
        if email:
            attendee_lines.append(f"  - {name} ({email})")
        else:
            attendee_lines.append(f"  - {name}")

    # --- Duration ---
    duration_str = ""
    rec = meeting.get("recording", {})
    duration_sec = rec.get("duration") or meeting.get("duration")
    if duration_sec:
        try:
            duration_str = str(int(float(duration_sec)) // 60)
        except (ValueError, TypeError):
            duration_str = ""

    # --- Frontmatter ---
    time_str = dt.strftime("%-I:%M %p")
    fm_lines = [
        "---",
        f'title: "{title}"',
        f"date: {dt.strftime('%Y-%m-%d')}",
        f'time: "{time_str}"',
    ]
    if duration_str:
        fm_lines.append(f"duration_minutes: {duration_str}")
    if attendee_lines:
        fm_lines.append("attendees:")
        fm_lines.extend(attendee_lines)
    fm_lines.append("source: fathom")
    if recording_id:
        fm_lines.append(f'recording_id: "{recording_id}"')
    if fathom_url:
        fm_lines.append(f'fathom_url: "{fathom_url}"')
    fm_lines.append("---")

    sections = ["\n".join(fm_lines)]

    # --- Summary ---
    summary_md = summary_data.get("summary") or summary_data.get("markdown") or summary_data.get("content", "")
    # Handle case where summary is a nested dict
    if isinstance(summary_md, dict):
        summary_md = summary_md.get("markdown_formatted") or summary_md.get("text") or summary_md.get("content") or summary_md.get("markdown") or ""
    if summary_md and isinstance(summary_md, str):
        sections.append(f"\n## Summary\n\n{summary_md.strip()}")
    else:
        sections.append("\n## Summary\n\n*Summary not yet available. Re-run sync to check again.*")

    # --- Action Items (if present in summary) ---
    action_items = summary_data.get("action_items", [])
    if action_items:
        items_md = "\n".join(f"- [ ] {item}" for item in action_items)
        sections.append(f"\n## Action Items\n\n{items_md}")

    # --- Transcript ---
    sections.append("\n---\n\n## Transcript")

    if transcript_segments:
        transcript_lines = []
        for seg in transcript_segments:
            # Handle speaker as string or dict
            speaker = seg.get("speaker_display_name") or seg.get("speaker") or "Unknown"
            if isinstance(speaker, dict):
                speaker = speaker.get("display_name") or speaker.get("name") or "Unknown"
            text = seg.get("text", "")
            if isinstance(text, dict):
                text = text.get("text") or text.get("content") or ""
            text = text.strip() if isinstance(text, str) else str(text)
            ts = seg.get("timestamp") or seg.get("start_time") or seg.get("start")
            ts_str = format_timestamp(ts)

            if ts_str:
                transcript_lines.append(f"\n**{speaker}** ({ts_str})")
            else:
                transcript_lines.append(f"\n**{speaker}**")
            transcript_lines.append(text)

        sections.append("\n".join(transcript_lines))
    else:
        sections.append("\n*Transcript not yet available.*")

    return "\n".join(sections) + "\n"


# ---------------------------------------------------------------------------
# File operations
# ---------------------------------------------------------------------------

def existing_recording_ids(output_dir: str) -> set:
    """
    Scan existing markdown files in output_dir for recording_id in frontmatter.
    Returns a set of recording IDs that have already been saved.
    """
    ids = set()
    if not os.path.isdir(output_dir):
        return ids

    for fname in os.listdir(output_dir):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(output_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                in_frontmatter = False
                for line in f:
                    line = line.strip()
                    if line == "---":
                        if not in_frontmatter:
                            in_frontmatter = True
                            continue
                        else:
                            break  # End of frontmatter
                    if in_frontmatter and line.startswith("recording_id:"):
                        rid = line.split(":", 1)[1].strip().strip('"').strip("'")
                        if rid:
                            ids.add(rid)
                        break
        except (IOError, UnicodeDecodeError):
            continue

    # Also scan subdirectories (for date-folder mode)
    for root, dirs, files in os.walk(output_dir):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            if root == output_dir:
                continue  # Already scanned above
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    in_frontmatter = False
                    for line in f:
                        line = line.strip()
                        if line == "---":
                            if not in_frontmatter:
                                in_frontmatter = True
                                continue
                            else:
                                break
                        if in_frontmatter and line.startswith("recording_id:"):
                            rid = line.split(":", 1)[1].strip().strip('"').strip("'")
                            if rid:
                                ids.add(rid)
                            break
            except (IOError, UnicodeDecodeError):
                continue

    return ids


def save_meeting(markdown: str, meeting: dict, output_dir: str, date_folders: bool = False):
    """Save a meeting's markdown to the output directory."""
    dt = parse_meeting_datetime(meeting)
    title = meeting.get("title") or meeting.get("meeting_title") or "Untitled Meeting"
    safe_title = sanitize_filename(title)
    filename = f"{dt.strftime('%Y-%m-%d')} - {safe_title}.md"

    if date_folders:
        folder = os.path.join(output_dir, dt.strftime("%Y"), dt.strftime("%m"))
    else:
        folder = output_dir

    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown)

    return filepath


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Pull Fathom meeting transcripts into Obsidian as markdown.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Pull last 7 days
  python3 fathom_sync.py --api-key KEY --output-dir ~/Vault/Meetings --days 7

  # Dry run — list meetings only
  python3 fathom_sync.py --api-key KEY --list-only --days 30

  # Pull one specific meeting
  python3 fathom_sync.py --api-key KEY --output-dir ~/Vault/Meetings --meeting-id rec_abc
        """,
    )

    parser.add_argument(
        "--api-key",
        default=os.environ.get("FATHOM_API_KEY"),
        help="Fathom API key (or set FATHOM_API_KEY env variable)",
    )
    parser.add_argument(
        "--output-dir",
        help="Path to the folder where markdown files will be saved",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Pull meetings from the last N days (default: 7)",
    )
    parser.add_argument(
        "--since",
        help="Pull meetings after this date (ISO format, e.g., 2026-02-01)",
    )
    parser.add_argument(
        "--meeting-id",
        help="Pull a specific meeting by its recording ID",
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="Just list meetings — don't save anything",
    )
    parser.add_argument(
        "--date-folders",
        action="store_true",
        help="Organize files into YYYY/MM subfolders",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files for the same meeting",
    )

    args = parser.parse_args()

    # --- Validate inputs ---
    if not args.api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Use --api-key YOUR_KEY or set the FATHOM_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    if not args.list_only and not args.output_dir:
        print("Error: --output-dir is required when saving files.", file=sys.stderr)
        sys.exit(1)

    # --- Determine date filter ---
    if args.since:
        created_after = args.since
        if "T" not in created_after:
            created_after += "T00:00:00Z"
    else:
        cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
        created_after = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")

    # --- Fetch meetings ---
    print(f"Fetching meetings since {created_after}...")
    meetings = list_meetings(args.api_key, created_after=created_after)

    if not meetings:
        print("No meetings found in that time range.")
        return

    print(f"Found {len(meetings)} meeting(s).\n")

    # --- If specific meeting requested, filter ---
    if args.meeting_id:
        meetings = [m for m in meetings if get_recording_id(m) == args.meeting_id]
        if not meetings:
            print(f"No meeting found with recording ID: {args.meeting_id}")
            return

    # --- List-only mode ---
    if args.list_only:
        print(f"{'Date':<14} {'Title':<50} {'Recording ID'}")
        print("-" * 90)
        for m in meetings:
            dt = parse_meeting_datetime(m)
            title = (m.get("title") or m.get("meeting_title") or "Untitled")[:48]
            rid = get_recording_id(m)
            print(f"{dt.strftime('%Y-%m-%d'):<14} {title:<50} {rid}")
        return

    # --- Check for duplicates ---
    existing = set()
    if not args.overwrite:
        existing = existing_recording_ids(args.output_dir)

    # --- Process each meeting ---
    saved = 0
    skipped = 0

    for i, meeting in enumerate(meetings):
        recording_id = get_recording_id(meeting)
        title = meeting.get("title") or meeting.get("meeting_title") or "Untitled"

        # Skip duplicates
        if recording_id in existing and not args.overwrite:
            print(f"  Skipping (already exists): {title}")
            skipped += 1
            continue

        print(f"  [{i + 1}/{len(meetings)}] Processing: {title}...")

        # Fetch summary and transcript
        summary_data = get_summary(args.api_key, recording_id)
        time.sleep(0.5)  # Pace API calls

        transcript = get_transcript(args.api_key, recording_id)
        time.sleep(0.5)

        # Format and save
        markdown = format_meeting_markdown(meeting, summary_data, transcript)
        filepath = save_meeting(markdown, meeting, args.output_dir, args.date_folders)

        print(f"    Saved: {filepath}")
        saved += 1

    print(f"\nDone! Saved {saved} meeting(s), skipped {skipped} duplicate(s).")


if __name__ == "__main__":
    main()
