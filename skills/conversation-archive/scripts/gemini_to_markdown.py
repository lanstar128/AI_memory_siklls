#!/usr/bin/env python3
import json
import os
import argparse
from pathlib import Path
from datetime import datetime

def find_latest_session():
    home = Path.home()
    tmp_dir = home / ".gemini" / "tmp"
    # Recursively find session json files
    session_files = list(tmp_dir.glob("**/chats/session-*.json"))
    if not session_files:
        return None
    # Sort by modification time, newest first
    return max(session_files, key=os.path.getmtime)

def format_timestamp(ts_str):
    try:
        # Example: 2026-01-19T02:45:04.074Z -> 2026-01-19 02:45:04
        if 'T' in ts_str:
            dt = datetime.strptime(ts_str.split('.')[0], "%Y-%m-%dT%H:%M:%S")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        pass
    return ts_str

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", help="Conversation title", default="Untitled Conversation")
    args = parser.parse_args()

    session_file = find_latest_session()
    if not session_file:
        print("Error: No session file found in ~/.gemini/tmp/")
        return

    print(f"Processing session: {session_file}")
    
    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading session file: {e}")
        return

    messages = data.get('messages', [])
    if not messages:
        print("Warning: No messages found in session file.")
        return

    # Extract date for filename from the first message
    start_time = messages[0].get('timestamp', datetime.now().isoformat())
    date_str = start_time.split('T')[0] # 2026-01-19
    month_str = date_str[:7] # 2026-01
    
    # Prepare Output Path
    output_dir = Path.home() / ".gemini" / "memory" / "conversations" / month_str
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Sanitize title
    safe_title = "".join([c if c.isalnum() or c in (' ', '-', '_') else '-' for c in args.title]).strip()
    safe_title = safe_title.replace(' ', '-')
    filename = f"{date_str}_{safe_title}.md"
    output_path = output_dir / filename

    # Build Markdown Content
    md_lines = []
    md_lines.append("---")
    md_lines.append(f"title: {args.title}")
    md_lines.append(f"archived: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md_lines.append(f"turns: {len(messages)}")
    md_lines.append("source: gemini-cli-adapter")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append(f"# {args.title}")
    md_lines.append("")

    for msg in messages:
        role = msg.get('type', 'unknown').upper()
        ts = format_timestamp(msg.get('timestamp', ''))
        content = msg.get('content', '')
        
        if role == 'USER':
            md_lines.append(f"### 👤 User Input [{ts}]")
            md_lines.append(content)
            md_lines.append("")
        elif role == 'GEMINI' or role == 'MODEL':
            md_lines.append(f"### 🤖 Model Response [{ts}]")
            md_lines.append(content)
            
            # Handle thoughts (if present)
            if 'thoughts' in msg:
                md_lines.append("")
                md_lines.append("> **Thoughts:**")
                for t in msg['thoughts']:
                    subject = t.get('subject', '')
                    text = t.get('text', '')
                    md_lines.append(f"> - **{subject}**: {text}")
            
            # Handle tool calls (if present in this message object, adjust based on actual structure)
            # Based on grep, toolCalls might be keys in the message
            if 'toolCalls' in msg:
                md_lines.append("")
                md_lines.append("**Tool Calls:**")
                for tc in msg['toolCalls']:
                    # Try to extract name and args, structure might vary
                    tool_name = tc.get('name') or tc.get('function', {}).get('name', 'unknown')
                    tool_args = tc.get('args') or tc.get('function', {}).get('arguments', '{}')
                    md_lines.append(f"- `{tool_name}`: `{tool_args}`")
            
            md_lines.append("")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
        
    print(f"✅ Successfully archived to: {output_path}")
    
    # Print a magic string for the shell script to capture the path
    print(f"__OUTPUT_PATH__:{output_path}")

if __name__ == "__main__":
    main()
