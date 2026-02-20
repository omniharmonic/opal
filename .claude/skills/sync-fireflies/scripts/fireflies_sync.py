#!/usr/bin/env python3
"""
Fireflies.ai -> OPAL Sync
=========================
Pulls meeting transcripts and AI summaries from the Fireflies.ai GraphQL API
and saves them as formatted markdown files.

Uses only Python standard library - no pip installs needed.

Usage:
    # Pull last 7 days of meetings
    python3 fireflies_sync.py --api-key YOUR_KEY --output-dir _inbox/transcripts/fireflies --days 7

    # List meetings without saving (dry run)
    python3 fireflies_sync.py --api-key YOUR_KEY --list-only --days 30

    # Pull a specific meeting
    python3 fireflies_sync.py --api-key YOUR_KEY --output-dir DIR --meeting-id abc123

Security:
    - API key is only sent to api.fireflies.ai over HTTPS
    - Only query operations - nothing in your Fireflies account is modified
    - Data goes straight from Fireflies to local files, nowhere else
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
# Fireflies GraphQL API client
# ---------------------------------------------------------------------------

GRAPHQL_URL = "https://api.fireflies.ai/graphql"


def graphql_query(query: str, variables: dict, api_key: str) -> dict:
    """
    Execute a GraphQL query against the Fireflies API.

    Args:
        query: GraphQL query string
        variables: Query variables dict
        api_key: Fireflies API key

    Returns:
        Parsed JSON response data
    """
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")

    req = Request(GRAPHQL_URL, data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")

    try:
        with urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if "errors" in result:
                for err in result["errors"]:
                    print(f"GraphQL Error: {err.get('message', err)}", file=sys.stderr)
                if not result.get("data"):
                    sys.exit(1)
            return result.get("data", {})
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Error: Fireflies API returned {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Error: Could not reach Fireflies API: {e.reason}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# GraphQL Queries
# ---------------------------------------------------------------------------

LIST_TRANSCRIPTS_QUERY = """
query Transcripts($limit: Int, $skip: Int, $fromDate: DateTime) {
  transcripts(limit: $limit, skip: $skip, fromDate: $fromDate) {
    id
    title
    date
    duration
    speakers {
      id
      name
    }
    meeting_attendance {
      name
    }
  }
}
"""

GET_TRANSCRIPT_QUERY = """
query Transcript($id: String!) {
  transcript(id: $id) {
    id
    title
    date
    duration
    speakers {
      id
      name
    }
    sentences {
      speaker_name
      text
      start_time
      end_time
    }
    summary {
      keywords
      action_items
      outline
      overview
    }
    meeting_attendance {
      name
      join_time
      leave_time
    }
    host_email
    organizer_email
    transcript_url
    audio_url
  }
}
"""


def list_meetings(api_key: str, from_date: str = None, limit: int = 50) -> list:
    """
    Fetch all meetings, handling pagination automatically.

    Args:
        api_key: Fireflies API key
        from_date: ISO timestamp - only return meetings after this date
        limit: Max results per page (API max is 50)

    Returns:
        List of meeting dicts
    """
    all_meetings = []
    skip = 0

    while True:
        variables = {"limit": min(limit, 50), "skip": skip}
        if from_date:
            variables["fromDate"] = from_date

        data = graphql_query(LIST_TRANSCRIPTS_QUERY, variables, api_key)
        meetings = data.get("transcripts", [])

        if not meetings:
            break

        all_meetings.extend(meetings)

        # If we got fewer than requested, we've reached the end
        if len(meetings) < variables["limit"]:
            break

        skip += len(meetings)

        # Respect rate limits
        time.sleep(0.5)

    return all_meetings


def get_transcript(api_key: str, meeting_id: str) -> dict:
    """
    Fetch full transcript details for a single meeting.

    Args:
        api_key: Fireflies API key
        meeting_id: The meeting ID

    Returns:
        Full transcript dict with sentences, summary, etc.
    """
    data = graphql_query(GET_TRANSCRIPT_QUERY, {"id": meeting_id}, api_key)
    return data.get("transcript", {})


# ---------------------------------------------------------------------------
# Markdown formatting
# ---------------------------------------------------------------------------

def sanitize_filename(name: str) -> str:
    """Remove characters that are unsafe for filenames."""
    cleaned = re.sub(r'[\\/:*?"<>|]', "-", name)
    cleaned = re.sub(r"-{2,}", "-", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    return cleaned.strip(" -.")[:50]


def format_timestamp(seconds) -> str:
    """Convert seconds to human-readable timestamp like 1:23:45 or 0:45."""
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


def format_duration(seconds) -> str:
    """Format duration as Xh Ym or just Ym."""
    if not seconds:
        return "Unknown"
    try:
        minutes = int(float(seconds)) // 60
    except (ValueError, TypeError):
        return "Unknown"

    if minutes >= 60:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h {mins}m"
    return f"{minutes}m"


def parse_meeting_datetime(meeting: dict) -> datetime:
    """Extract datetime from meeting's date field."""
    date_str = meeting.get("date")
    if date_str:
        try:
            if date_str.endswith("Z"):
                date_str = date_str[:-1] + "+00:00"
            return datetime.fromisoformat(date_str)
        except ValueError:
            pass
    return datetime.now(timezone.utc)


def format_meeting_markdown(meeting: dict, transcript_data: dict) -> str:
    """
    Build the full markdown content for a meeting note.

    Structure:
        - YAML frontmatter
        - Summary section
        - Action Items
        - Transcript (speaker-labeled, timestamped)
    """
    dt = parse_meeting_datetime(meeting)
    title = meeting.get("title") or "Untitled Meeting"
    meeting_id = meeting.get("id", "")
    duration = meeting.get("duration")

    # Get attendees
    attendees = []
    for att in transcript_data.get("meeting_attendance") or []:
        name = att.get("name")
        if name:
            attendees.append(name)

    # Get host/organizer
    host = transcript_data.get("host_email") or transcript_data.get("organizer_email") or ""

    # URLs
    transcript_url = transcript_data.get("transcript_url") or ""
    audio_url = transcript_data.get("audio_url") or ""

    # --- Frontmatter ---
    fm_lines = [
        "---",
        "source: fireflies",
        f'source_id: "{meeting_id}"',
        f'title: "{title}"',
        f"date: {dt.strftime('%Y-%m-%d')}",
        f"synced_at: {datetime.now(timezone.utc).isoformat()}",
    ]

    if duration:
        try:
            fm_lines.append(f"duration_minutes: {int(float(duration)) // 60}")
        except (ValueError, TypeError):
            pass

    fm_lines.append("type: transcript")

    if host:
        fm_lines.append(f'host: "{host}"')

    if attendees:
        fm_lines.append("attendees:")
        for att in attendees:
            fm_lines.append(f'  - "{att}"')

    if transcript_url:
        fm_lines.append(f'fireflies_url: "{transcript_url}"')
    if audio_url:
        fm_lines.append(f'audio_url: "{audio_url}"')

    fm_lines.append("---")

    sections = ["\n".join(fm_lines)]

    # --- Header ---
    header_lines = [f"\n# {title}\n"]
    header_lines.append(f"**Source:** Fireflies.ai")
    header_lines.append(f"**Date:** {dt.strftime('%B %d, %Y at %I:%M %p')}")
    header_lines.append(f"**Duration:** {format_duration(duration)}")
    if host:
        header_lines.append(f"**Host:** {host}")
    if attendees:
        header_lines.append(f"**Attendees:** {', '.join(attendees)}")

    sections.append("\n".join(header_lines))

    # --- Summary ---
    summary = transcript_data.get("summary") or {}

    sections.append("\n---\n\n## Summary")

    overview = summary.get("overview")
    if overview:
        sections.append(f"\n{overview}")
    else:
        sections.append("\n*Summary not available.*")

    # Outline
    outline = summary.get("outline")
    if outline:
        sections.append(f"\n### Outline\n\n{outline}")

    # Keywords
    keywords = summary.get("keywords")
    if keywords:
        if isinstance(keywords, list):
            keywords = ", ".join(keywords)
        sections.append(f"\n### Keywords\n\n{keywords}")

    # --- Action Items ---
    action_items = summary.get("action_items") or []
    if action_items:
        items_md = "\n".join(f"- [ ] {item}" for item in action_items)
        sections.append(f"\n## Action Items\n\n{items_md}")

    # --- Transcript ---
    sections.append("\n---\n\n## Transcript")

    sentences = transcript_data.get("sentences") or []
    if sentences:
        transcript_lines = []
        for sent in sentences:
            speaker = sent.get("speaker_name") or "Unknown"
            text = (sent.get("text") or "").strip()
            start_time = sent.get("start_time")
            ts_str = format_timestamp(start_time)

            if ts_str:
                transcript_lines.append(f"\n**{speaker}** ({ts_str})")
            else:
                transcript_lines.append(f"\n**{speaker}**")
            transcript_lines.append(text)

        sections.append("\n".join(transcript_lines))
    else:
        sections.append("\n*Transcript not available.*")

    return "\n".join(sections) + "\n"


# ---------------------------------------------------------------------------
# File operations
# ---------------------------------------------------------------------------

def existing_meeting_ids(output_dir: str) -> set:
    """
    Scan existing markdown files for source_id in frontmatter.
    Returns set of meeting IDs already synced.
    """
    ids = set()
    if not os.path.isdir(output_dir):
        return ids

    for root, _, files in os.walk(output_dir):
        for fname in files:
            if not fname.endswith(".md"):
                continue
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
                        if in_frontmatter and line.startswith("source_id:"):
                            mid = line.split(":", 1)[1].strip().strip('"').strip("'")
                            if mid:
                                ids.add(mid)
                            break
            except (IOError, UnicodeDecodeError):
                continue

    return ids


def save_meeting(markdown: str, meeting: dict, output_dir: str, date_folders: bool = False) -> str:
    """Save meeting markdown to output directory."""
    dt = parse_meeting_datetime(meeting)
    title = meeting.get("title") or "Untitled Meeting"
    safe_title = sanitize_filename(title)
    filename = f"{dt.strftime('%Y-%m-%d')}_{safe_title}.md"

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
        description="Pull Fireflies.ai meeting transcripts as markdown.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Pull last 7 days
  python3 fireflies_sync.py --api-key KEY --output-dir _inbox/transcripts/fireflies --days 7

  # Dry run - list meetings only
  python3 fireflies_sync.py --api-key KEY --list-only --days 30

  # Pull one specific meeting
  python3 fireflies_sync.py --api-key KEY --output-dir DIR --meeting-id abc123
        """,
    )

    parser.add_argument(
        "--api-key",
        default=os.environ.get("FIREFLIES_API_KEY"),
        help="Fireflies API key (or set FIREFLIES_API_KEY env variable)",
    )
    parser.add_argument(
        "--output-dir",
        help="Path to folder where markdown files will be saved",
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
        help="Pull a specific meeting by its ID",
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="Just list meetings - don't save anything",
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
        print("Use --api-key YOUR_KEY or set the FIREFLIES_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    if not args.list_only and not args.output_dir:
        print("Error: --output-dir is required when saving files.", file=sys.stderr)
        sys.exit(1)

    # --- Determine date filter ---
    if args.since:
        from_date = args.since
        if "T" not in from_date:
            from_date += "T00:00:00Z"
    else:
        cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
        from_date = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")

    # --- Fetch meetings ---
    print(f"Fetching meetings since {from_date}...")
    meetings = list_meetings(args.api_key, from_date=from_date)

    if not meetings:
        print("No meetings found in that time range.")
        return

    print(f"Found {len(meetings)} meeting(s).\n")

    # --- If specific meeting requested, filter ---
    if args.meeting_id:
        meetings = [m for m in meetings if m.get("id") == args.meeting_id]
        if not meetings:
            print(f"No meeting found with ID: {args.meeting_id}")
            return

    # --- List-only mode ---
    if args.list_only:
        print(f"{'Date':<14} {'Title':<50} {'ID'}")
        print("-" * 90)
        for m in meetings:
            dt = parse_meeting_datetime(m)
            title = (m.get("title") or "Untitled")[:48]
            mid = m.get("id", "")[:20]
            print(f"{dt.strftime('%Y-%m-%d'):<14} {title:<50} {mid}")
        return

    # --- Check for duplicates ---
    existing = set()
    if not args.overwrite:
        existing = existing_meeting_ids(args.output_dir)

    # --- Process each meeting ---
    saved = 0
    skipped = 0

    for i, meeting in enumerate(meetings):
        meeting_id = meeting.get("id", "")
        title = meeting.get("title") or "Untitled"

        # Skip duplicates
        if meeting_id in existing and not args.overwrite:
            print(f"  Skipping (already exists): {title}")
            skipped += 1
            continue

        print(f"  [{i + 1}/{len(meetings)}] Processing: {title}...")

        # Fetch full transcript
        transcript_data = get_transcript(args.api_key, meeting_id)
        time.sleep(0.5)  # Pace API calls

        if not transcript_data:
            print(f"    Warning: Could not fetch transcript for {title}")
            continue

        # Format and save
        markdown = format_meeting_markdown(meeting, transcript_data)
        filepath = save_meeting(markdown, meeting, args.output_dir, args.date_folders)

        print(f"    Saved: {filepath}")
        saved += 1

    print(f"\nDone! Saved {saved} meeting(s), skipped {skipped} duplicate(s).")


if __name__ == "__main__":
    main()
