import os
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path

# Static TrueType Fonts
FONT_TITLE = 'fonts/SpaceGrotesk-BoldStatic.ttf'
FONT_REGULAR = 'fonts/SpaceGrotesk-MediumStatic.ttf'
FONT_BODY_BOLD = 'fonts/Outfit-SemiBold.ttf'
FONT_BODY = 'fonts/Outfit-Medium.ttf'

def text_to_svg_path(text, x, y, size, font_path, anchor='start', fill='#ffffff', opacity=1.0, extra=''):
    """Converts a text string into an SVG <path> element with vector glyphs."""
    if not text:
        return ''
    fp = FontProperties(fname=font_path)
    tp = TextPath((0, 0), text, size=size, prop=fp)
    bbox = tp.get_extents()
    
    if anchor == 'middle':
        dx = x - (bbox.xmin + bbox.xmax) / 2.0
    elif anchor == 'end':
        dx = x - bbox.xmax
    else: # start
        dx = x - bbox.xmin
        
    dy = y
    d = []
    i = 0
    v = tp.vertices
    c = tp.codes
    while i < len(c):
        code = c[i]
        if code == Path.MOVETO:
            d.append(f"M {dx + v[i][0]:.2f} {dy - v[i][1]:.2f}")
            i += 1
        elif code == Path.LINETO:
            d.append(f"L {dx + v[i][0]:.2f} {dy - v[i][1]:.2f}")
            i += 1
        elif code == Path.CURVE3:
            d.append(f"Q {dx + v[i][0]:.2f} {dy - v[i][1]:.2f} {dx + v[i+1][0]:.2f} {dy - v[i+1][1]:.2f}")
            i += 2
        elif code == Path.CURVE4:
            d.append(f"C {dx + v[i][0]:.2f} {dy - v[i][1]:.2f} {dx + v[i+1][0]:.2f} {dy - v[i+1][1]:.2f} {dx + v[i+2][0]:.2f} {dy - v[i+2][1]:.2f}")
            i += 3
        elif code == Path.CLOSEPOLY:
            d.append("Z")
            i += 1
        else:
            i += 1
            
    op_attr = f' opacity="{opacity}"' if opacity < 1.0 else ''
    return f'<path d="{" ".join(d)}" fill="{fill}"{op_attr} {extra}/>'

def create_card_defs():
    return '''
    <defs>
      <!-- Gradient Palettes: Cyber Aurora (Crisp Vibrant Cyan -> Emerald) -->
      <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#00f2fe" />
        <stop offset="100%" stop-color="#38ef7d" />
      </linearGradient>
      <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#00f2fe" />
        <stop offset="100%" stop-color="#4facfe" />
      </linearGradient>
      <linearGradient id="purpleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#c084fc" />
        <stop offset="100%" stop-color="#a855f7" />
      </linearGradient>
      <linearGradient id="cardBg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0f172a" />
        <stop offset="50%" stop-color="#090d16" />
        <stop offset="100%" stop-color="#070a10" />
      </linearGradient>
      <linearGradient id="cardBorder" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="rgba(0, 242, 254, 0.45)" />
        <stop offset="50%" stop-color="rgba(56, 239, 125, 0.3)" />
        <stop offset="100%" stop-color="rgba(192, 132, 252, 0.4)" />
      </linearGradient>
      <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#00f2fe" />
        <stop offset="60%" stop-color="#38ef7d" />
        <stop offset="100%" stop-color="#c084fc" />
      </linearGradient>
      
      <!-- Subtle Glow Filter -->
      <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="3.5" result="blur" />
        <feComposite in="SourceGraphic" in2="blur" operator="over" />
      </filter>
      <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="2" result="blur" />
        <feComposite in="SourceGraphic" in2="blur" operator="over" />
      </filter>

      <style>
        .card-frame { fill: url(#cardBg); stroke: url(#cardBorder); stroke-width: 1.5px; rx: 18px; ry: 18px; }
      </style>
    </defs>
    '''

def generate_stats_card():
    w, h = 480, 205
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
    svg.append(create_card_defs())
    svg.append(f'<rect width="{w}" height="{h}" class="card-frame" />')
    
    # Top Accent ambient glow
    svg.append(f'<ellipse cx="{w/2}" cy="0" rx="160" ry="12" fill="#00f2fe" opacity="0.08" filter="url(#neonGlow)" />')
    
    # Header: Space Grotesk Bold
    svg.append(text_to_svg_path("Nishant Ranjan's GitHub Stats", 24, 38, 18, FONT_TITLE, fill="url(#titleGrad)"))
    
    # Metrics
    items = [
        ("Total Stars Earned:", "1", "#f1c40f"),
        ("Total Commits:", "262", "#00f2fe"),
        ("Total Pull Requests:", "22", "#c084fc"),
        ("Total Issues Closed:", "0", "#38ef7d"),
        ("Contributed to:", "3 Repos", "#38ef7d")
    ]
    
    start_y = 68
    for idx, (label, val, icon_col) in enumerate(items):
        y = start_y + (idx * 26)
        svg.append(f'<circle cx="32" cy="{y - 4}" r="4" fill="{icon_col}" filter="url(#softGlow)" />')
        svg.append(text_to_svg_path(label, 44, y, 13.5, FONT_BODY, fill="#94a3b8"))
        svg.append(text_to_svg_path(val, 215, y, 15, FONT_TITLE, fill="#ffffff"))
        
    # Grade Circle (Right Side)
    cx, cy, r = 378, 100, 44
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="rgba(255,255,255,0.06)" stroke-width="6.5" fill="none" />')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="url(#ringGrad)" stroke-width="6.5" stroke-linecap="round" stroke-dasharray="276" stroke-dashoffset="30" fill="none" filter="url(#neonGlow)" />')
    svg.append(text_to_svg_path("A+", cx, cy + 10, 29, FONT_TITLE, anchor="middle", fill="url(#titleGrad)"))
    svg.append(text_to_svg_path("SUPER ARCHITECT", cx, cy + 62, 10, FONT_TITLE, anchor="middle", fill="#00f2fe"))

    svg.append('</svg>')
    return '\n'.join(svg)

def generate_streak_card():
    w, h = 480, 205
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
    svg.append(create_card_defs())
    svg.append(f'<rect width="{w}" height="{h}" class="card-frame" />')
    
    col_w = w / 3
    
    # Col 1: Total Contributions
    c1_x = col_w * 0.5
    svg.append(text_to_svg_path("319", c1_x, 85, 34, FONT_TITLE, anchor="middle", fill="#ffffff"))
    svg.append(text_to_svg_path("Total Contributions", c1_x, 114, 13.5, FONT_TITLE, anchor="middle", fill="#00f2fe"))
    svg.append(text_to_svg_path("Sep 14, 2024 - Present", c1_x, 134, 12, FONT_BODY, anchor="middle", fill="#64748b"))
    
    # Divider 1
    svg.append(f'<line x1="{col_w}" y1="45" x2="{col_w}" y2="160" stroke="rgba(255,255,255,0.08)" stroke-width="1.5" />')
    
    # Col 2: Current Streak
    cx, cy = col_w * 1.5, 78
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="35" stroke="rgba(255,255,255,0.06)" stroke-width="5.5" fill="none" />')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="35" stroke="url(#ringGrad)" stroke-width="5.5" stroke-dasharray="220" stroke-dashoffset="45" stroke-linecap="round" fill="none" filter="url(#neonGlow)" />')
    svg.append(text_to_svg_path("1", cx, cy + 9, 27, FONT_TITLE, anchor="middle", fill="#ffffff"))
    svg.append(text_to_svg_path("Current Streak", cx, 136, 14, FONT_TITLE, anchor="middle", fill="#00f2fe"))
    svg.append(text_to_svg_path("DAILY ACTIVE", cx, 154, 10.5, FONT_TITLE, anchor="middle", fill="#38ef7d"))
    
    # Divider 2
    svg.append(f'<line x1="{col_w * 2}" y1="45" x2="{col_w * 2}" y2="160" stroke="rgba(255,255,255,0.08)" stroke-width="1.5" />')
    
    # Col 3: Longest Streak
    c3_x = col_w * 2.5
    svg.append(text_to_svg_path("3", c3_x, 85, 34, FONT_TITLE, anchor="middle", fill="#ffffff"))
    svg.append(text_to_svg_path("Longest Streak", c3_x, 114, 13.5, FONT_TITLE, anchor="middle", fill="#00f2fe"))
    svg.append(text_to_svg_path("Peak Consistency", c3_x, 134, 12, FONT_BODY, anchor="middle", fill="#64748b"))
    
    svg.append('</svg>')
    return '\n'.join(svg)

def generate_languages_card():
    w, h = 540, 225
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
    svg.append(create_card_defs())
    svg.append(f'<rect width="{w}" height="{h}" class="card-frame" />')
    
    # Header
    svg.append(text_to_svg_path("Most Used Languages", 24, 38, 19, FONT_TITLE, fill="url(#titleGrad)"))
    
    langs = [
        ("TypeScript", 62.28, "#3178c6"),
        ("Python", 11.51, "#3776ab"),
        ("HTML", 9.01, "#e34c26"),
        ("Java", 7.68, "#b07219"),
        ("JavaScript", 5.64, "#f1e05a"),
        ("CSS", 3.62, "#563d7c"),
        ("Shell", 0.22, "#89e051"),
        ("Makefile", 0.04, "#427819")
    ]
    
    bar_x = 24
    bar_y = 56
    bar_w = w - 48
    bar_h = 10
    
    # Progress Bar Background
    svg.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="5" fill="rgba(255,255,255,0.06)" />')
    
    curr_x = bar_x
    for name, pct, col in langs:
        seg_w = (pct / 100) * bar_w
        if seg_w < 2: seg_w = 2
        svg.append(f'<rect x="{curr_x:.1f}" y="{bar_y}" width="{seg_w:.1f}" height="{bar_h}" fill="{col}" rx="1" />')
        curr_x += seg_w
        
    svg.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="5" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="1" />')
    
    # 2 Column Legend
    col1_x = 34
    col2_x = 290
    start_y = 96
    row_h = 28
    
    for i, (name, pct, col) in enumerate(langs):
        is_col2 = (i >= 4)
        lx = col2_x if is_col2 else col1_x
        ly = start_y + ((i % 4) * row_h)
        
        svg.append(f'<circle cx="{lx}" cy="{ly - 4}" r="5" fill="{col}" filter="url(#softGlow)" />')
        svg.append(text_to_svg_path(name, lx + 16, ly, 14, FONT_TITLE, fill="#ffffff"))
        svg.append(text_to_svg_path(f"{pct:.2f}%", lx + 155, ly, 13, FONT_BODY, fill="#94a3b8"))
        
    svg.append('</svg>')
    return '\n'.join(svg)

def generate_repo_card(name, desc, lang, lang_col, forks=0, stars=0):
    w, h = 480, 125
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
    svg.append(create_card_defs())
    svg.append(f'<rect width="{w}" height="{h}" class="card-frame" />')
    
    # Book / Repo Icon
    svg.append('''
      <g transform="translate(24, 20)">
        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" fill="none" stroke="#00f2fe" stroke-width="2" />
        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" fill="none" stroke="#00f2fe" stroke-width="2" />
      </g>
    ''')
    
    # Title in Space Grotesk Bold
    svg.append(text_to_svg_path(name, 56, 38, 17.5, FONT_TITLE, fill="url(#titleGrad)"))
    
    # Description lines in Outfit Medium
    d = desc if desc else "High-performance software engine & architectural component."
    if len(d) > 65:
        d1 = d[:65]
        d2 = d[65:128] + ('...' if len(d) > 128 else '')
        svg.append(text_to_svg_path(d1, 24, 66, 13, FONT_BODY, fill="#94a3b8"))
        svg.append(text_to_svg_path(d2, 24, 84, 13, FONT_BODY, fill="#94a3b8"))
    else:
        svg.append(text_to_svg_path(d, 24, 70, 13, FONT_BODY, fill="#94a3b8"))
        
    # Language dot + tag
    svg.append(f'<circle cx="28" cy="104" r="4.5" fill="{lang_col}" filter="url(#softGlow)" />')
    svg.append(text_to_svg_path(lang, 38, 108, 12.5, FONT_BODY_BOLD, fill="#cbd5e1"))
    
    # Forks count if any
    stat_x = 135
    if forks > 0:
        svg.append(f'''
        <g transform="translate({stat_x}, 97)">
          <circle cx="2" cy="2" r="1.8" fill="none" stroke="#94a3b8" stroke-width="1.2" />
          <circle cx="10" cy="2" r="1.8" fill="none" stroke="#94a3b8" stroke-width="1.2" />
          <circle cx="6" cy="10" r="1.8" fill="none" stroke="#94a3b8" stroke-width="1.2" />
          <path d="M2 4v2a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2V4M6 8v2" fill="none" stroke="#94a3b8" stroke-width="1.2" />
        </g>
        ''')
        svg.append(text_to_svg_path(str(forks), stat_x + 16, 108, 12, FONT_BODY, fill="#94a3b8"))
        stat_x += 40
        
    svg.append('</svg>')
    return '\n'.join(svg)

if __name__ == '__main__':
    os.makedirs('assets', exist_ok=True)
    os.makedirs('dist', exist_ok=True)
    
    # 1. Main Stats Card
    stats_svg = generate_stats_card()
    streak_svg = generate_streak_card()
    langs_svg = generate_languages_card()
    
    for folder in ['assets', 'dist']:
        with open(os.path.join(folder, 'card-stats.svg'), 'w') as f:
            f.write(stats_svg)
        with open(os.path.join(folder, 'card-streak.svg'), 'w') as f:
            f.write(streak_svg)
        with open(os.path.join(folder, 'card-languages.svg'), 'w') as f:
            f.write(langs_svg)
            
    repos = [
        ("ShadowLedger", "Uncertainty-aware value-flow reconstruction for finance operations", "Python", "#3776ab", 0, 0),
        ("SPARK-Engine", "Speech Powered Analytics Relational Kit - Voice-Enabled Data Analytics Companion.", "TypeScript", "#3178c6", 2, 0),
        ("askDB", "Natural language interface & query parser for relational databases", "Python", "#3776ab", 0, 0),
        ("InsightU_v1", "Comprehensive academic intelligence and student performance analytics engine.", "TypeScript", "#3178c6", 1, 0),
        ("easy-q", "High-throughput digital queue and appointment orchestrator.", "Java", "#b07219", 0, 0),
        ("Gavel", "Decentralized legal tech verification and consensus protocol.", "TypeScript", "#3178c6", 0, 0),
    ]
    
    for idx, (name, desc, lang, col, forks, stars) in enumerate(repos):
        svg_code = generate_repo_card(name, desc, lang, col, forks, stars)
        fname = f'card-repo-{name.lower().replace("-", "").replace("_", "")}.svg'
        for folder in ['assets', 'dist']:
            with open(os.path.join(folder, fname), 'w') as f:
                f.write(svg_code)
                
    print("Regenerated all cards with SpaceGrotesk Bold and Outfit typography!")
