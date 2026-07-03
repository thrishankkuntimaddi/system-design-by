import os
import json
import re
import html

# Source directory containing notebooks
SOURCE_DIR = "/Users/thrishankkuntimaddi/Documents/antigravity/system design/Data-Structures-and-Algorithms-Advanced-main"
# Target output HTML file
TARGET_HTML = "/Users/thrishankkuntimaddi/Documents/antigravity/system design/subjects/dsa_advanced/index.html"

# Map of topics in order
TOPICS = [
    {"id": "bit_magic", "title": "Bit Magic", "icon": "ti-cpu"},
    {"id": "list", "title": "List", "icon": "ti-list-numbers"},
    {"id": "recursion", "title": "Recursion", "icon": "ti-refresh"},
    {"id": "searching", "title": "Searching", "icon": "ti-search"},
    {"id": "matrix", "title": "Matrix", "icon": "ti-grid-dots"},
    {"id": "sorting", "title": "Sorting", "icon": "ti-arrows-sort"},
    {"id": "hashing", "title": "Hashing", "icon": "ti-hash"},
    {"id": "string", "title": "String", "icon": "ti-letters-case"},
    {"id": "linked_list", "title": "LinkedList", "icon": "ti-link"},
    {"id": "stack", "title": "Stack", "icon": "ti-layers-difference"},
    {"id": "infix_postfix", "title": "Infix, Postfix, Prefix", "icon": "ti-brackets"},
    {"id": "queue_deque", "title": "Queue & Deque", "icon": "ti-arrows-double-ne-sw"},
    {"id": "trees", "title": "Tree Data Structure", "icon": "ti-git-branch"},
    {"id": "bst", "title": "Binary Search Tree", "icon": "ti-binary-tree"},
    {"id": "heap", "title": "Heap", "icon": "ti-binary-tree-2"},
    {"id": "graph", "title": "Graph Data Structure", "icon": "ti-git-commit"},
    {"id": "greedy", "title": "Greedy Algorithms", "icon": "ti-award"},
    {"id": "backtracking", "title": "Backtracking", "icon": "ti-history"},
    {"id": "dp", "title": "Dynamic Programming", "icon": "ti-border-all"},
    {"id": "trie", "title": "Trie Data Structure", "icon": "ti-hierarchy-2"},
    {"id": "disjoint_set", "title": "Disjoint Set", "icon": "ti-intersection"},
    {"id": "segment_tree", "title": "Segment Tree", "icon": "ti-chart-bar"},
    {"id": "binary_indexed_tree", "title": "Binary Indexed Tree", "icon": "ti-binary-tree-2"}
]

# Topic Summaries for the Grid View Cards
SUMMARIES = {
    "bit_magic": "Bitwise operations, binary representations, kth set bit, counting set bits, and lookup tables.",
    "list": "Advanced array operations: left rotations, trapping rain water, stock buy & sell, and max difference.",
    "recursion": "Recursive problems: Rope Cutting, Tower of Hanoi, subset generation, and subset sum solver.",
    "searching": "Searching in infinite sorted arrays, sorted rotated arrays, finding peaks, and two-pointer scenarios.",
    "matrix": "Multi-dimensional arrays, snake pattern printing, matrix boundary traversal, and transposes.",
    "sorting": "Advanced sorting: General purpose sort algorithms, hybrid algorithms, tail-call optimizations, and Kth smallest.",
    "hashing": "Intersection and union of unsorted arrays, subarray sum problems, checking for palindrome permutations.",
    "string": "Pattern searching algorithms: Rabin-Karp rolling hash, improved hash algorithms, and string matching.",
    "linked_list": "Floyd's cycle detection, loop removal, reverse in K-groups, and advanced list configurations.",
    "stack": "Multiple stacks in single arrays, stock span problem, previous greater element, and custom stacks.",
    "infix_postfix": "Infix to postfix/prefix conversions, associativity guidelines, and postfix evaluation.",
    "queue_deque": "Reversing queues, circular lists, generating numbers with given digits, and double ended queues.",
    "trees": "Level order traversals line-by-line, balanced trees check, vertical traversals, and bottom view graphs.",
    "bst": "Floor/Ceiling on left side, Kth smallest element, swapped nodes recovery, and pair sum.",
    "heap": "Median of a stream, sorting k-sorted arrays, k closest elements, and merging K sorted arrays.",
    "graph": "Adjacency matrix/list representations, BFS/DFS, cycle detection, topological sorting (Kahn's), Prim's, and Dijkstra's.",
    "greedy": "Greedy strategy, Fractional Knapsack, Activity Selection, and Job Sequencing optimizations.",
    "backtracking": "Rat in a maze, N-Queens problem, Sudoku solver, and exhaustive state searches.",
    "dp": "Memoization & Tabulation, Longest Common Subsequence, 0-1 Knapsack, optimal strategy, and egg dropping.",
    "trie": "Retrieval trees, inserting/searching keys, deleting keys, and counting distinct rows in binary matrices.",
    "disjoint_set": "Union-find data structure, union by rank, path compression, and dynamic connectivity.",
    "segment_tree": "Interval trees, range sum query, range updates, and segment construction.",
    "binary_indexed_tree": "Fenwick trees, prefix sums, updates, and space-efficient range queries."
}

def clean_markdown(text):
    # Convert notebook markdown lines to HTML
    lines = text.split('\n')
    html_lines = []
    in_list = False
    in_example = False
    example_buffer = []

    for line in lines:
        stripped = line.strip()
        
        # Check for example/input/output boxes
        is_example_indicator = (
            stripped.startswith("Input") or 
            stripped.startswith("I/P") or 
            stripped.startswith("Output") or 
            stripped.startswith("O/P") or 
            stripped.startswith("Explanation")
        )
        
        if is_example_indicator:
            if not in_example:
                in_example = True
            example_buffer.append(line)
            continue
        elif in_example and stripped == "":
            example_buffer.append(line)
            continue
        elif in_example and not is_example_indicator:
            html_lines.append(format_example_box(example_buffer))
            example_buffer = []
            in_example = False
            
        # Standard headings
        if stripped.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            h_text = stripped[2:].strip()
            html_lines.append(f'<h3 class="h">{h_text}</h3>')
        elif stripped.startswith("## ") or stripped.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            h_text = stripped.lstrip('#').strip()
            html_lines.append(f'<h4 class="h4">{h_text}</h4>')
        # Lists
        elif stripped.startswith("* ") or stripped.startswith("- "):
            if not in_list:
                html_lines.append('<ul class="plain">')
                in_list = True
            item_text = stripped[2:].strip()
            item_text = parse_inline_elements(item_text)
            html_lines.append(f'<li>{item_text}</li>')
        else:
            if in_list and stripped != "":
                html_lines.append("</ul>")
                in_list = False
            
            if stripped != "":
                text_parsed = parse_inline_elements(line)
                html_lines.append(f'<p>{text_parsed}</p>')
            else:
                html_lines.append("")

    if in_list:
        html_lines.append("</ul>")
    if in_example:
        html_lines.append(format_example_box(example_buffer))

    return '\n'.join(html_lines)

def format_example_box(lines):
    content = "<br>".join([parse_inline_elements(line.strip()) for line in lines if line.strip() != ""])
    content = content.replace("Input  :", "<strong>Input:</strong>")
    content = content.replace("Input :", "<strong>Input:</strong>")
    content = content.replace("I/P :", "<strong>Input:</strong>")
    content = content.replace("I/P  :", "<strong>Input:</strong>")
    content = content.replace("Output :", "<strong>Output:</strong>")
    content = content.replace("Output  :", "<strong>Output:</strong>")
    content = content.replace("O/P :", "<strong>Output:</strong>")
    content = content.replace("O/P  :", "<strong>Output:</strong>")
    content = content.replace("Explanation :", "<strong>Explanation:</strong>")
    content = content.replace("Explanation  :", "<strong>Explanation:</strong>")
    
    return f"""<div class="example">
  <div class="label"><i class="ti ti-terminal-2"></i> Case Example</div>
  <p>{content}</p>
</div>"""

def parse_inline_elements(text):
    text = html.escape(text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\`(.*?)\`', r'<code class="inline-code">\1</code>', text)
    return text

def parse_code_cell(cell):
    code_lines = cell.get("source", [])
    code_text = "".join(code_lines)
    
    time_match = re.search(r'#\s*Time\s*(?:complexity)?\s*:\s*([^\n\r]+)', code_text, re.IGNORECASE)
    space_match = re.search(r'#\s*Space\s*(?:complexity)?\s*:\s*([^\n\r]+)', code_text, re.IGNORECASE)
    
    time_complexity = time_match.group(1).strip() if time_match else None
    space_complexity = space_match.group(1).strip() if space_match else None
    
    clean_code = code_text
    if time_match:
        clean_code = re.sub(r'#\s*Time\s*(?:complexity)?\s*:\s*[^\n\r]+\n?', '', clean_code, flags=re.IGNORECASE)
    if space_match:
        clean_code = re.sub(r'#\s*Space\s*(?:complexity)?\s*:\s*[^\n\r]+\n?', '', clean_code, flags=re.IGNORECASE)
    
    clean_code = clean_code.strip()
    escaped_code = html.escape(clean_code)
    
    badges_html = ""
    if time_complexity or space_complexity:
        badges_html = '<div class="complexity-badges">'
        if time_complexity:
            badges_html += f'<span class="badge-time" title="Time Complexity"><i class="ti ti-clock"></i> {time_complexity}</span>'
        if space_complexity:
            badges_html += f'<span class="badge-space" title="Space Complexity"><i class="ti ti-database"></i> {space_complexity}</span>'
        badges_html += '</div>'
        
    return f"""<div class="code-block-container">
  <div class="code-block-header">
    <span class="code-lang">Python Implementation</span>
    {badges_html}
  </div>
  <pre><code>{escaped_code}</code></pre>
</div>"""

def parse_notebook_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return f"<p class='danger'>Error loading notebook: {e}</p>"
        
    sections_html = []
    first_h1_skipped = False
    for cell in data.get("cells", []):
        cell_type = cell.get("cell_type")
        if cell_type == "markdown":
            source = "".join(cell.get("source", []))
            if "colab-badge.svg" in source:
                continue
            
            # Skip the very first H1 title in the notebook to avoid duplicate section headings
            if not first_h1_skipped:
                lines = source.split('\n')
                new_lines = []
                for line in lines:
                    if line.strip().startswith("# ") and not first_h1_skipped:
                        first_h1_skipped = True
                        continue
                    new_lines.append(line)
                source = '\n'.join(new_lines)
                
            sections_html.append(clean_markdown(source))
        elif cell_type == "code":
            sections_html.append(parse_code_cell(cell))
            
    return "\n".join(sections_html)

def compile_dsa_html():
    sections_code = []
    
    for t in TOPICS:
        tid = t["id"]
        title = t["title"]
        print(f"Compiling advanced content for: {title}...")
        
        # Open section tag
        section_html = f'<section id="p-{tid}">\n'
        
        if tid == "graph":
            # Graph merges 16.1, 16.2, 16.3
            section_html += f'<h2 class="pagetitle">{title}</h2>'
            section_html += '<p class="lead">Graphs represent pairwise relationships between objects using vertices and connecting edges. This topic merges Representations, BFS/DFS cycles, Topological sorting, Prim\'s MST, and Dijkstra\'s shortest path algorithms.</p>'
            for sub in ["16.1 - Graph Data Structure.ipynb", "16.2 - Graph Data Structure.ipynb", "16.3 - Graph Data Structure.ipynb"]:
                path = os.path.join(SOURCE_DIR, sub)
                section_html += f'<div class="graph-part" style="margin-top: 32px; border-top: 1px dashed var(--border); padding-top: 24px;">'
                section_html += parse_notebook_file(path)
                section_html += '</div>'
        elif tid == "dp":
            # DP merges 19.1, 19.2
            section_html += f'<h2 class="pagetitle">{title}</h2>'
            section_html += '<p class="lead">Dynamic Programming solves problems by combining solutions to overlapping subproblems, using Memoization (Top-down) or Tabulation (Bottom-up).</p>'
            for sub in ["19.1 - Dynamic Programming.ipynb", "19.2 - Dynamic Programming.ipynb"]:
                path = os.path.join(SOURCE_DIR, sub)
                section_html += f'<div class="dp-part" style="margin-top: 32px; border-top: 1px dashed var(--border); padding-top: 24px;">'
                section_html += parse_notebook_file(path)
                section_html += '</div>'
        else:
            # Match notebooks by prefix number
            matched_file = None
            for filename in os.listdir(SOURCE_DIR):
                if filename.endswith(".ipynb"):
                    prefix_match = re.match(r'^(\d+)\s*-', filename)
                    if prefix_match:
                        num = int(prefix_match.group(1))
                        if tid == "bit_magic" and num == 1: matched_file = filename
                        elif tid == "list" and num == 2: matched_file = filename
                        elif tid == "recursion" and num == 3: matched_file = filename
                        elif tid == "searching" and num == 4: matched_file = filename
                        elif tid == "matrix" and num == 5: matched_file = filename
                        elif tid == "sorting" and num == 6: matched_file = filename
                        elif tid == "hashing" and num == 7: matched_file = filename
                        elif tid == "string" and num == 8: matched_file = filename
                        elif tid == "linked_list" and num == 9: matched_file = filename
                        elif tid == "stack" and num == 10: matched_file = filename
                        elif tid == "infix_postfix" and num == 11: matched_file = filename
                        elif tid == "queue_deque" and num == 12: matched_file = filename
                        elif tid == "trees" and num == 13: matched_file = filename
                        elif tid == "bst" and num == 14: matched_file = filename
                        elif tid == "heap" and num == 15: matched_file = filename
                        elif tid == "greedy" and num == 17: matched_file = filename
                        elif tid == "backtracking" and num == 18: matched_file = filename
                        elif tid == "trie" and num == 20: matched_file = filename
                        elif tid == "disjoint_set" and num == 21: matched_file = filename
                        elif tid == "segment_tree" and num == 22: matched_file = filename
                        elif tid == "binary_indexed_tree" and num == 23: matched_file = filename
            
            if matched_file:
                path = os.path.join(SOURCE_DIR, matched_file)
                section_html += f'<h2 class="pagetitle">{title}</h2>'
                section_html += parse_notebook_file(path)
            else:
                section_html += f'<h2 class="pagetitle">{title}</h2><p class="danger">Notebook content missing.</p>'
        
        section_html += '\n</section>'
        sections_code.append(section_html)
        
    return "\n\n".join(sections_code)

def generate_full_html():
    sections_content = compile_dsa_html()
    
    # Generate sidebar links
    sidebar_links = []
    for t in TOPICS:
        sidebar_links.append(f"""
      <div class="navlink" id="sn-{t['id']}" onclick="go('{t['id']}')">
        <i class="ti {t['icon']}"></i>
        <span>{t['title']}</span>
      </div>""")
    sidebar_links_str = "\n".join(sidebar_links)
    
    # Generate grid items
    grid_items = []
    for i, t in enumerate(TOPICS, start=1):
        num_str = f"{i:02d}"
        summary = SUMMARIES.get(t['id'], "")
        grid_items.append(f"""
      <div class="grid-card" onclick="go('{t['id']}')">
        <div class="card-num">{num_str}</div>
        <div class="card-icon-wrap"><i class="ti {t['icon']}"></i></div>
        <div class="card-title-wrap">
          <div class="card-tag">TOPIC {num_str}</div>
          <h4 class="card-heading">{t['title']}</h4>
        </div>
        <p class="card-summary">{summary}</p>
        <div class="card-action">
          <span>Explore Chapter</span>
          <i class="ti ti-arrow-right"></i>
        </div>
      </div>""")
    grid_items_str = "\n".join(grid_items)

    # Order array for JS navigation
    order_array = ['intro'] + [t['id'] for t in TOPICS]
    order_array_str = json.dumps(order_array)
    
    # Labels object for JS navigation
    labels_dict = {'intro': 'Overview'}
    for t in TOPICS:
        labels_dict[t['id']] = t['title']
    labels_dict_str = json.dumps(labels_dict)

    # Read layout template and replace placeholders
    template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>DSA Advanced — Notes</title>
  <link rel="manifest" href="../../manifest.json">
  <link rel="icon" type="image/svg+xml" href="../../favicon.svg">
  <link rel="apple-touch-icon" href="../../favicon.svg">
  <meta name="theme-color" content="#0f1117">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="DSA Advanced">
  <meta name="description" content="Structured notes on Advanced Data Structures & Algorithms. Covers Trees, Graphs, Greedy algorithms, Backtracking, DP, Trie, Segment trees.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #0a0d14;
      --bg2: #111520;
      --bg3: #161d2e;
      --bg4: #1d263b;
      --border: #1f2d48;
      --border2: #2d3f64;
      --text: #edf0f7;
      --text2: #8a96b0;
      --text3: #5a6480;
      --accent: #f472b6; /* Pink Theme for DSA Advanced */
      --cyan: #22d3ee;
      --green: #34d399;
      --red: #ef4444;
      --radius: 12px;
      --radius-sm: 8px;
      --mono: 'JetBrains Mono', monospace;
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    html { scroll-behavior: smooth; }
    ::selection { background: var(--accent); color: #000; }

    body {
      font-family: var(--font-sans);
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      font-size: 15px;
      overflow-x: hidden;
    }

    /* ── App Shell Layout ────────────────────────────────────── */
    .app-shell {
      display: flex;
      min-height: 100vh;
      width: 100%;
    }

    /* Split-Pane Views toggle states */
    .app-shell.view-grid .sidebar {
      display: none !important;
    }
    .app-shell.view-grid .main-content {
      width: 100%;
      padding: 0;
    }
    .app-shell.view-grid .split-view {
      display: none !important;
    }
    .app-shell.view-grid .grid-view {
      display: block !important;
    }

    .app-shell.view-content .grid-view {
      display: none !important;
    }
    .app-shell.view-content .split-view {
      display: flex !important;
      width: 100%;
    }

    /* ── Grid View Styling (Dashboard Mode) ──────────────────── */
    .grid-view {
      display: block;
      max-width: 1100px;
      margin: 0 auto;
      padding: 48px 24px 80px;
    }

    .grid-header {
      text-align: center;
      margin-bottom: 48px;
    }
    
    .grid-back-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--text3);
      text-decoration: none;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .08em;
      margin-bottom: 24px;
      transition: color .15s;
    }
    .grid-back-btn:hover { color: var(--accent); }

    .grid-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(244, 114, 182, 0.1);
      border: 1px solid rgba(244, 114, 182, 0.25);
      border-radius: 20px;
      padding: 6px 16px;
      font-size: 11px;
      color: var(--accent);
      font-weight: 700;
      letter-spacing: .05em;
      text-transform: uppercase;
      margin-bottom: 16px;
    }

    .grid-header h1 {
      font-size: 32px;
      font-weight: 800;
      color: var(--text);
      letter-spacing: -.02em;
      margin-bottom: 12px;
    }

    .grid-header p {
      font-size: 15px;
      color: var(--text2);
      max-width: 580px;
      margin: 0 auto 32px;
      line-height: 1.65;
    }

    .grid-stats-bar {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 32px;
      background: var(--bg2);
      border: 1px solid var(--border);
      border-radius: 40px;
      padding: 12px 32px;
      margin: 0 auto;
    }
    .stat-item {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 600;
      color: var(--text2);
    }
    .stat-item i {
      font-size: 16px;
      color: var(--accent);
    }

    .topics-grid-container {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }

    .grid-card {
      background: var(--bg2);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      height: 100%;
      min-height: 220px;
      transition: transform .2s, border-color .2s, box-shadow .2s;
    }
    .grid-card:hover {
      transform: translateY(-3px);
      border-color: var(--accent);
      box-shadow: 0 8px 30px rgba(0,0,0,.3);
    }

    .card-num {
      position: absolute;
      top: 24px;
      right: 24px;
      font-family: var(--mono);
      font-size: 18px;
      font-weight: 800;
      color: var(--text3);
      opacity: 0.15;
    }

    .card-icon-wrap {
      width: 44px;
      height: 44px;
      border-radius: 10px;
      background: rgba(244, 114, 182, 0.1);
      border: 1px solid rgba(244, 114, 182, 0.2);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      color: var(--accent);
      margin-bottom: 20px;
      transition: transform .2s;
    }
    .grid-card:hover .card-icon-wrap {
      transform: scale(1.05);
    }

    .card-title-wrap {
      margin-bottom: 12px;
    }
    .card-tag {
      font-family: var(--mono);
      font-size: 9px;
      font-weight: 700;
      letter-spacing: .08em;
      color: var(--accent);
      margin-bottom: 4px;
    }
    .card-heading {
      font-size: 16px;
      font-weight: 700;
      color: var(--text);
      letter-spacing: -.01em;
    }
    .card-summary {
      font-size: 12.5px;
      color: var(--text2);
      line-height: 1.6;
      margin-bottom: 24px;
      flex-grow: 1;
    }

    .card-action {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: .04em;
      text-transform: uppercase;
      color: var(--text3);
      border-top: 1px solid var(--border);
      padding-top: 14px;
      margin-top: auto;
      transition: color .15s;
    }
    .grid-card:hover .card-action {
      color: var(--accent);
    }
    .card-action i {
      font-size: 14px;
      transition: transform .15s;
    }
    .grid-card:hover .card-action i {
      transform: translateX(4px);
    }

    /* ── Sidebar (Split Content Mode) ───────────────────────── */
    .sidebar {
      width: 260px;
      flex-shrink: 0;
      background: var(--bg2);
      border-right: 1px solid var(--border);
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
      padding-bottom: 40px;
    }

    .sidebar-header {
      padding: 16px 20px 12px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 8px;
    }
    
    .grid-dashboard-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 700;
      color: var(--text3);
      text-decoration: none;
      letter-spacing: .06em;
      text-transform: uppercase;
      padding: 6px 0;
      margin-bottom: 12px;
      transition: color .15s;
      cursor: pointer;
    }
    .grid-dashboard-btn:hover { color: var(--accent); }
    .grid-dashboard-btn i { font-size: 14px; }

    .sidebar-header h1 {
      font-size: 13px;
      font-weight: 800;
      color: var(--accent);
      letter-spacing: .12em;
      text-transform: uppercase;
    }
    .sidebar-header p {
      font-size: 11px;
      color: var(--text3);
      margin-top: 3px;
    }

    .search-wrap {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border);
      position: relative;
    }
    .search-input {
      width: 100%;
      background: var(--bg3);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 7px 12px 7px 34px;
      font-size: 13px;
      color: var(--text);
      outline: none;
      transition: border-color .15s;
    }
    .search-input:focus {
      border-color: var(--accent);
    }
    .search-icon {
      position: absolute;
      left: 26px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text3);
      font-size: 14px;
    }

    .nav-section {
      padding: 8px 12px 4px 20px;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: .1em;
      text-transform: uppercase;
      color: var(--text3);
    }

    .navlink {
      display: flex;
      align-items: center;
      gap: 9px;
      padding: 7px 12px 7px 20px;
      cursor: pointer;
      font-size: 13px;
      color: var(--text2);
      border-left: 2px solid transparent;
      transition: all .15s;
      border-radius: 0 6px 6px 0;
      margin-right: 8px;
    }
    .navlink i {
      font-size: 15px;
      width: 17px;
      flex-shrink: 0;
      color: var(--text3);
      transition: color .15s;
    }
    .navlink:hover { background: var(--bg3); color: var(--text); border-left-color: var(--border2); }
    .navlink:hover i { color: var(--text); }
    .navlink.active { background: var(--bg3); color: var(--accent); border-left-color: var(--accent); font-weight: 500; }
    .navlink.active i { color: var(--accent); }

    /* ── Split View Main Content Area ───────────────────────── */
    .main {
      flex: 1;
      overflow-y: auto;
      padding: 0;
    }

    .content {
      max-width: 900px;
      margin: 0 auto;
      padding: 36px 40px 100px;
    }

    /* Mobile Title Header */
    .mobile-header-bar {
      display: none;
      align-items: center;
      justify-content: space-between;
      padding: 14px 18px;
      background: var(--bg2);
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 50;
    }
    .mobile-logo-text {
      font-size: 13px;
      font-weight: 800;
      letter-spacing: .08em;
      text-transform: uppercase;
      color: var(--accent);
    }
    .mobile-nav-title {
      font-size: 13px;
      font-weight: 600;
      color: var(--text);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 180px;
    }
    .mobile-nav-btn {
      background: none;
      border: none;
      color: var(--text);
      font-size: 20px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .sidebar-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.6);
      z-index: 90;
      opacity: 0;
      transition: opacity .25s ease;
    }
    .sidebar-overlay.active {
      display: block;
      opacity: 1;
    }

    /* ── Content Styling ────────────────────────────────────── */
    section { display: none; animation: fadein .35s ease; }
    section.active { display: block; }
    @keyframes fadein {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .eyebrow {
      font-family: var(--mono);
      font-size: 11px;
      letter-spacing: .16em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .eyebrow::before { content: ''; width: 22px; height: 1px; background: var(--accent); }

    h2.pagetitle {
      font-size: 28px;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--text);
      margin-bottom: 8px;
    }
    
    .subtitle, .lead {
      color: var(--text2);
      font-size: 14.5px;
      max-width: 720px;
      margin-bottom: 28px;
      line-height: 1.65;
    }
    .lead { font-size: 15px; color: var(--text); margin-bottom: 24px; }

    h3.h {
      font-size: 18px;
      font-weight: 700;
      margin: 36px 0 14px;
      padding-top: 18px;
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 10px;
      color: var(--text);
    }
    h3.h:first-of-type { border-top: none; padding-top: 0; margin-top: 0; }
    h4.h4 { font-size: 14.5px; font-weight: 700; margin: 24px 0 10px; color: var(--text); }
    
    p { color: var(--text2); font-size: 14.2px; margin-bottom: 14px; line-height: 1.65; }
    p strong { color: var(--text); font-weight: 600; }

    ul.plain, ol.plain { margin: 12px 0 18px; padding-left: 0; list-style: none; }
    ul.plain li, ol.plain li {
      padding-left: 18px; position: relative; margin-bottom: 8px; font-size: 14px; color: var(--text2);
      line-height: 1.6;
    }
    ul.plain li::before { content: '—'; position: absolute; left: 0; color: var(--accent); }
    
    ol.plain { counter-reset: item; }
    ol.plain li { counter-increment: item; }
    ol.plain li::before {
      content: counter(item) '.'; position: absolute; left: 0; color: var(--accent);
      font-family: var(--mono); font-size: 12px; font-weight: 600;
    }

    /* ── Custom Component boxes ──────────────────────────────── */
    .def {
      background: var(--bg2);
      border: 1px solid var(--border);
      border-left: 3px solid var(--accent);
      border-radius: 6px;
      padding: 14px 16px;
      margin: 18px 0;
    }
    .def .label {
      font-family: var(--mono);
      font-size: 10px;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 6px;
      font-weight: 600;
    }
    .def p { margin: 0; color: var(--text); font-size: 13.5px; }

    .example {
      background: rgba(244, 114, 182, 0.03);
      border: 1px solid rgba(244, 114, 182, 0.15);
      border-left: 3px solid var(--accent);
      border-radius: 6px;
      padding: 14px 16px;
      margin: 18px 0;
    }
    .example .label {
      font-family: var(--mono);
      font-size: 10px;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 6px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .example p { margin: 0; font-size: 13.5px; color: var(--text2); line-height: 1.6; }

    code, .mono { font-family: var(--mono); font-size: 12.5px; }
    .inline-code {
      background: var(--bg3);
      padding: 2px 6px;
      border-radius: 4px;
      font-family: var(--mono);
      font-size: 12px;
      color: var(--accent);
    }

    /* ── Complexity Code Blocks ──────────────────────────────── */
    .code-block-container {
      margin: 18px 0;
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
      background: #06080e;
    }
    .code-block-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: var(--bg2);
      padding: 8px 14px;
      border-bottom: 1px solid var(--border);
    }
    .code-lang {
      font-family: var(--mono);
      font-size: 11px;
      font-weight: 600;
      color: var(--text3);
      text-transform: uppercase;
      letter-spacing: .05em;
    }
    .complexity-badges {
      display: flex;
      gap: 8px;
    }
    .badge-time, .badge-space {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-family: var(--mono);
      font-size: 10.5px;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 4px;
    }
    .badge-time {
      background: rgba(244, 114, 182, 0.1);
      color: var(--accent);
      border: 1px solid rgba(244, 114, 182, 0.2);
    }
    .badge-space {
      background: rgba(34, 211, 238, 0.1);
      color: var(--cyan);
      border: 1px solid rgba(34, 211, 238, 0.2);
    }
    .code-block-container pre {
      margin: 0;
      border: none;
      border-radius: 0;
      background: transparent;
      padding: 14px 16px;
      overflow-x: auto;
      font-family: var(--mono);
      font-size: 12.5px;
      color: #bbf7e6;
      line-height: 1.7;
    }

    /* ── Components & Tables ─────────────────────────────────── */
    table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 13.5px; }
    th {
      text-align: left;
      font-family: var(--mono);
      font-size: 10.5px;
      letter-spacing: .08em;
      text-transform: uppercase;
      color: var(--text3);
      padding: 8px 11px;
      border-bottom: 1px solid var(--border);
    }
    td { padding: 10px 11px; border-bottom: 1px solid var(--border); color: var(--text2); }
    tr:last-child td { border-bottom: none; }
    td strong, td .mono { color: var(--text); }
    
    .table-wrapper {
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      margin: 16px 0;
      border-radius: 8px;
      border: 1px solid var(--border);
    }

    .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 16px 0; }
    .grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 16px 0; }
    @media (max-width: 900px) {
      .grid2, .grid3 { grid-template-columns: 1fr; }
    }

    .proscons { border: 1px solid var(--border); border-radius: 8px; overflow: hidden; margin-top: 10px; }
    .proscons .pc-head {
      padding: 8px 12px;
      font-family: var(--mono);
      font-size: 11px;
      letter-spacing: .15em;
      text-transform: uppercase;
      font-weight: 700;
    }
    .pc-pro .pc-head { background: rgba(52, 211, 153, .08); color: var(--green); }
    .pc-con .pc-head { background: rgba(239, 68, 68, .08); color: var(--red); }
    .proscons ul { list-style: none; padding: 10px 12px; }
    .proscons li { padding-left: 16px; position: relative; font-size: 13px; color: var(--text2); margin-bottom: 6px; }
    .pc-pro li::before { content: '+'; position: absolute; left: 0; color: var(--green); font-weight: 700; }
    .pc-con li::before { content: '–'; position: absolute; left: 0; color: var(--red); font-weight: 700; }

    /* Topic Next/Prev Nav Bar */
    .topic-nav-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-top: 48px;
      padding-top: 24px;
      border-top: 1px solid var(--border);
    }
    .topic-nav-btn {
      display: flex;
      align-items: center;
      gap: 10px;
      background: var(--bg2);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 16px;
      cursor: pointer;
      color: var(--text2);
      transition: all .15s;
      flex: 1;
      max-width: 240px;
      outline: none;
    }
    .topic-nav-btn:hover {
      border-color: var(--accent);
      color: var(--text);
      background: var(--bg3);
    }
    .topic-nav-btn i {
      font-size: 16px;
    }
    .topic-nav-label {
      display: flex;
      flex-direction: column;
      text-align: left;
      font-size: 11px;
    }
    .topic-nav-hint {
      color: var(--text3);
      font-size: 9px;
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: .05em;
    }
    .topic-nav-name {
      font-weight: 600;
      font-size: 13px;
      margin-top: 2px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 170px;
    }

    /* ── Scrollbar Styling ───────────────────────────────────── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

    /* ── Responsive Styling ──────────────────────────────────── */
    @media (max-width: 960px) {
      .topics-grid-container { grid-template-columns: repeat(2, 1fr); }
    }

    @media (max-width: 760px) {
      .app-shell.view-content .sidebar {
        position: fixed;
        left: 0; top: 0; bottom: 0;
        z-index: 100;
        width: 260px;
        transform: translateX(-100%);
        transition: transform .25s cubic-bezier(0.4, 0, 0.2, 1);
        display: block !important;
      }
      .app-shell.view-content .sidebar.open {
        transform: translateX(0);
      }
      .mobile-header-bar {
        display: flex;
      }
      .content {
        padding: 24px 20px 80px;
      }
      .topics-grid-container { grid-template-columns: 1fr; gap: 12px; }
      .grid-view { padding: 32px 16px 64px; }
      .grid-header h1 { font-size: 26px; }
      .grid-stats-bar { display: flex; flex-direction: column; gap: 10px; border-radius: 16px; padding: 12px 24px; }
      .grid-back-btn { margin-bottom: 16px; }
    }
  </style>
</head>

<body>
  <div class="app-shell view-grid" id="appShell">
    
    <!-- GRID VIEW (DASHBOARD) -->
    <div class="grid-view">
      <div class="grid-header">
        <a href="../../index.html" class="grid-back-btn"><i class="ti ti-arrow-left"></i> Home</a>
        <br>
        <div class="grid-badge"><i class="ti ti-topology-star-ring"></i> Live Subject</div>
        <h1>Data Structures & Algorithms Advanced</h1>
        <p>A step-by-step masterclass covering advanced recursion, graph theory, dynamic programming, and complex range search trees.</p>
        
        <div class="grid-stats-bar">
          <div class="stat-item"><i class="ti ti-folders"></i> 23 Chapters</div>
          <div class="stat-item"><i class="ti ti-braces"></i> Python Implementations</div>
          <div class="stat-item"><i class="ti ti-clock"></i> Complexity Focus</div>
        </div>
      </div>
      
      <div class="topics-grid-container">
        __GRID_ITEMS__
      </div>
    </div>
    
    <!-- CONTENT VIEW (SPLIT PANE) -->
    <div class="split-view" style="display:none; width: 100%;">
      <!-- Sidebar Navigation -->
      <aside class="sidebar" id="sidebar">
        <div class="sidebar-header">
          <div class="grid-dashboard-btn" onclick="go('intro')"><i class="ti ti-layout-grid"></i> Overview Grid</div>
          <h1>DSA — Advanced</h1>
          <p>23 Core Topics</p>
        </div>
        
        <div class="search-wrap">
          <i class="ti ti-search search-icon"></i>
          <input type="text" class="search-input" id="searchInput" placeholder="Search topics..." oninput="filterNav(this.value)">
        </div>
        
        <nav style="padding-top: 8px;">
          <div class="nav-section">Topics Checklist</div>
          __SIDEBAR_LINKS__
        </nav>
      </aside>
      
      <!-- Overlay for mobile sidebar -->
      <div class="sidebar-overlay" id="sidebarOverlay"></div>
      
      <!-- Main Content Container -->
      <main class="main" id="mainContent">
        <!-- Mobile Topbar header -->
        <header class="mobile-header-bar">
          <button class="mobile-nav-btn" id="hamburgerBtn" aria-label="Menu" aria-expanded="false">
            <i class="ti ti-menu-2" id="hamburgerIcon"></i>
          </button>
          <div class="mobile-nav-title" id="mobileNavTitle">Overview</div>
          <div class="mobile-logo-text" onclick="go('intro')">DSA</div>
        </header>
        
        <div class="content" id="contentArea">
          __SECTIONS_CONTENT__
        </div>
      </main>
    </div>
    
  </div>

  <script>
    const ORDER = __ORDER_ARRAY__;
    const LABELS = __LABELS_DICT__;

    function go(id) {
      const shell = document.getElementById('appShell');
      
      if (id === 'intro') {
        shell.className = 'app-shell view-grid';
        document.querySelector('.split-view').style.display = 'none';
        
        try { 
          localStorage.setItem('dsaa_topic', 'intro'); 
          localStorage.setItem('dsaa_topic_time', Date.now()); 
        } catch(e) {}
        
        window.scrollTo(0, 0);
        return;
      }
      
      shell.className = 'app-shell view-content';
      document.querySelector('.split-view').style.display = 'flex';
      
      document.querySelectorAll('section').forEach(s => s.classList.remove('active'));
      document.querySelectorAll('.sidebar .navlink').forEach(n => n.classList.remove('active'));

      const targetSection = document.getElementById('p-' + id);
      if (targetSection) targetSection.classList.add('active');

      const navItem = document.getElementById('sn-' + id);
      if (navItem) {
        navItem.classList.add('active');
        navItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }

      document.getElementById('mainContent').scrollTop = 0;
      window.scrollTo(0, 0);

      const label = LABELS[id];
      const mobileTitle = document.getElementById('mobileNavTitle');
      if (mobileTitle) mobileTitle.textContent = label;

      try { 
        localStorage.setItem('dsaa_topic', id); 
        localStorage.setItem('dsaa_topic_time', Date.now()); 
      } catch(e) {}

      closeSidebar();

      const idx = ORDER.indexOf(id);
      
      const prevId = idx > 1 ? ORDER[idx - 1] : 'intro';
      const prevBtn = targetSection ? targetSection.querySelector('.topic-nav-btn.prev') : null;
      if (prevBtn) {
        prevBtn.style.visibility = 'visible';
        prevBtn.querySelector('.topic-nav-hint').textContent = prevId === 'intro' ? 'Dashboard' : 'Previous';
        prevBtn.querySelector('.topic-nav-name').textContent = LABELS[prevId];
        prevBtn.onclick = () => go(prevId);
      }

      const nextId = idx < ORDER.length - 1 ? ORDER[idx + 1] : 'intro';
      const nextBtn = targetSection ? targetSection.querySelector('.topic-nav-btn.next') : null;
      if (nextBtn) {
        const isLast = idx === ORDER.length - 1;
        nextBtn.querySelector('.topic-nav-hint').textContent = isLast ? 'Back to start' : 'Next';
        nextBtn.querySelector('.topic-nav-name').textContent = LABELS[nextId];
        nextBtn.onclick = () => go(nextId);
      }
    }

    function openSidebar() {
      document.getElementById('sidebar').classList.add('open');
      document.getElementById('sidebarOverlay').classList.add('active');
      document.getElementById('hamburgerBtn').setAttribute('aria-expanded', 'true');
      document.getElementById('hamburgerIcon').className = 'ti ti-x';
      document.body.style.overflow = 'hidden';
    }

    function closeSidebar() {
      document.getElementById('sidebar').classList.remove('open');
      document.getElementById('sidebarOverlay').classList.remove('active');
      document.getElementById('hamburgerBtn').setAttribute('aria-expanded', 'false');
      document.getElementById('hamburgerIcon').className = 'ti ti-menu-2';
      document.body.style.overflow = '';
    }

    function toggleNav() {
      document.getElementById('sidebar').classList.contains('open') ? closeSidebar() : openSidebar();
    }

    function filterNav(q) {
      q = q.toLowerCase();
      document.querySelectorAll('.sidebar .navlink').forEach(n => {
        const match = !q || n.textContent.toLowerCase().includes(q);
        n.style.display = match ? 'flex' : 'none';
      });
      
      document.querySelectorAll('.sidebar .nav-section').forEach(sec => {
        let el = sec.nextElementSibling;
        let hasVisibleSibling = false;
        while (el && !el.classList.contains('nav-section')) {
          if (el.classList.contains('navlink') && el.style.display !== 'none') {
            hasVisibleSibling = true;
            break;
          }
          el = el.nextElementSibling;
        }
        sec.style.display = (q && !hasVisibleSibling) ? 'none' : 'block';
      });
    }

    document.addEventListener('DOMContentLoaded', () => {
      const btn = document.getElementById('hamburgerBtn');
      if (btn) {
        btn.addEventListener('click', e => { e.stopPropagation(); toggleNav(); });
        btn.addEventListener('touchend', e => { e.preventDefault(); e.stopPropagation(); toggleNav(); }, { passive: false });
      }

      const overlay = document.getElementById('sidebarOverlay');
      if (overlay) {
        overlay.addEventListener('click', closeSidebar);
        overlay.addEventListener('touchend', e => { e.preventDefault(); closeSidebar(); }, { passive: false });
      }

      const navBarHTML = `
        <div class="topic-nav-bar">
          <button class="topic-nav-btn prev" type="button" aria-label="Previous topic">
            <i class="ti ti-arrow-left"></i>
            <span class="topic-nav-label">
              <span class="topic-nav-hint">Previous</span>
              <span class="topic-nav-name">—</span>
            </span>
          </button>
          <button class="topic-nav-btn next" type="button" aria-label="Next topic">
            <span class="topic-nav-label" style="text-align:right">
              <span class="topic-nav-hint">Next</span>
              <span class="topic-nav-name">—</span>
            </span>
            <i class="ti ti-arrow-right"></i>
          </button>
        </div>`;
      document.querySelectorAll('section').forEach(sec => sec.insertAdjacentHTML('beforeend', navBarHTML));

      document.querySelectorAll('table').forEach(table => {
        const wrapper = document.createElement('div');
        wrapper.className = 'table-wrapper';
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
      });

      let startId = 'intro';
      try {
        const saved = localStorage.getItem('dsaa_topic');
        if (saved && ORDER.includes(saved)) startId = saved;
      } catch(e) {}
      go(startId);
    });

    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeSidebar(); });
  </script>
</body>
</html>"""

    full_html = template.replace("__GRID_ITEMS__", grid_items_str)
    full_html = full_html.replace("__SIDEBAR_LINKS__", sidebar_links_str)
    full_html = full_html.replace("__SECTIONS_CONTENT__", sections_content)
    full_html = full_html.replace("__ORDER_ARRAY__", order_array_str)
    full_html = full_html.replace("__LABELS_DICT__", labels_dict_str)
    
    return full_html

if __name__ == "__main__":
    print("Compiling all DSA Advanced data structures notes...")
    html_output = generate_full_html()
    
    os.makedirs(os.path.dirname(TARGET_HTML), exist_ok=True)
    with open(TARGET_HTML, 'w', encoding='utf-8') as f:
        f.write(html_output)
        
    print(f"Successfully generated target HTML at: {TARGET_HTML}")
