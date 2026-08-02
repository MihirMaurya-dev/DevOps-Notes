import os
import re

def process_file(filepath):
    print(f"Processing {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into frontmatter and body
    parts = content.split('---')
    frontmatter = parts[1]
    body = '---'.join(parts[2:])

    # Extract Title and intro
    header_match = re.search(r'(# .*?)\n## ', body, re.DOTALL)
    if header_match:
        intro = header_match.group(1).strip()
        body = body[len(header_match.group(1)):]
    else:
        intro = ""

    sections_raw = re.split(r'\n## ', '\n' + body)
    
    # Identify and categorize sections
    sections = {}
    for s in sections_raw[1:]:
        lines = s.strip().split('\n')
        s_title = lines[0].strip()
        s_content = '\n'.join(lines[1:]).strip()
        
        # Extract questions
        q_splits = re.split(r'\n### (?:Q?\d+:?|(?=\d+\.)|(?=\bScenario:))', '\n' + s_content)
        questions = []
        for q in q_splits[1:]:
            q_clean = q.strip()
            if q_clean.startswith('Scenario:'):
                questions.append(q_clean)
            elif q_clean.startswith('Q'):
                # Try to clean up 'Q12: ' etc
                q_clean = re.sub(r'^Q\d+:?\s*', '', q_clean)
                questions.append(q_clean)
            else:
                # Might be like '1. What is...'
                q_clean = re.sub(r'^\d+\.\s*', '', q_clean)
                questions.append(q_clean)
        
        sections[s_title] = questions
        
    print(f"Found sections: {list(sections.keys())}")
    
    return frontmatter, intro, sections

if __name__ == "__main__":
    print("Script started")
