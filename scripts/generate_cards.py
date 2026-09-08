import os
import math
from datetime import datetime, timezone, timedelta
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path

# Static TrueType Fonts
FONT_TITLE = 'fonts/SpaceGrotesk-BoldStatic.ttf'
FONT_REGULAR = 'fonts/SpaceGrotesk-MediumStatic.ttf'
FONT_HEADER = 'fonts/DINAlternate-Bold.ttf'
FONT_BODY_BOLD = 'fonts/Outfit-SemiBold.ttf'
FONT_BODY = 'fonts/Outfit-Medium.ttf'
FONT_CURSIVE = 'fonts/DancingScript.ttf'

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

def get_text_width(text, size, font_path):
    fp = FontProperties(fname=font_path)
    tp = TextPath((0, 0), text, size=size, prop=fp)
    return tp.get_extents().width

def create_card_defs():
    return '''
    <defs>
      <!-- Cohesive Cyber Starlight Palette: Electric Cyan -> Sky Blue -> Lavender -> Neon Violet -->
      <linearGradient id="rainbowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#00f2fe" />
        <stop offset="35%" stop-color="#38bdf8" />
        <stop offset="70%" stop-color="#818cf8" />
        <stop offset="100%" stop-color="#c084fc" />
      </linearGradient>
      <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#00f2fe" />
        <stop offset="35%" stop-color="#38bdf8" />
        <stop offset="70%" stop-color="#818cf8" />
        <stop offset="100%" stop-color="#c084fc" />
      </linearGradient>
      <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#00f2fe" />
        <stop offset="100%" stop-color="#4facfe" />
      </linearGradient>
      <linearGradient id="purpleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#818cf8" />
        <stop offset="100%" stop-color="#c084fc" />
      </linearGradient>
      <linearGradient id="cardBg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0f172a" />
        <stop offset="50%" stop-color="#090d16" />
        <stop offset="100%" stop-color="#070a10" />
      </linearGradient>
      <linearGradient id="cardBorder" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="rgba(0, 242, 254, 0.4)" />
        <stop offset="50%" stop-color="rgba(129, 140, 248, 0.25)" />
        <stop offset="100%" stop-color="rgba(192, 132, 252, 0.4)" />
      </linearGradient>
      <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#00f2fe" />
        <stop offset="50%" stop-color="#818cf8" />
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
    svg.append(f'<ellipse cx="{w/2}" cy="0" rx="180" ry="14" fill="#00f2fe" opacity="0.09" filter="url(#neonGlow)" />')
    
    # Header: Space Grotesk Bold
    svg.append(text_to_svg_path("Nishant Ranjan's GitHub Stats", 24, 38, 18, FONT_TITLE, fill="url(#titleGrad)"))
    
    # Metrics
    items = [
        ("Total Stars Earned:", "1", "#f1c40f"),
        ("Total Commits:", "262", "#00f2fe"),
        ("Total Pull Requests:", "22", "#c084fc"),
        ("Total Issues Closed:", "0", "#38ef7d"),
        ("Contributed to:", "3 Repos", "#f43f5e")
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
    svg.append(text_to_svg_path("Current Streak", cx, 136, 14, FONT_TITLE, anchor="middle", fill="#c084fc"))
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

def generate_repo_card(name, desc_lines, category, tags, forks=0, stars=0):
    w, h = 480, 148
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
    svg.append(create_card_defs())
    svg.append(f'<rect width="{w}" height="{h}" class="card-frame" />')
    
    # Book / Repo Icon
    svg.append('''
      <g transform="translate(24, 18)">
        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" fill="none" stroke="#00f2fe" stroke-width="2" />
        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" fill="none" stroke="#00f2fe" stroke-width="2" />
      </g>
    ''')
    
    # Title in Space Grotesk Bold
    svg.append(text_to_svg_path(name, 56, 36, 17.5, FONT_TITLE, fill="url(#titleGrad)"))
    
    # Category Tag on top-right
    if category:
        cat_w = get_text_width(category, 9.5, FONT_TITLE) + 20
        cat_x = w - 24 - cat_w
        svg.append(f'<rect x="{cat_x}" y="20" width="{cat_w}" height="20" rx="10" fill="rgba(192, 132, 252, 0.08)" stroke="rgba(192, 132, 252, 0.35)" stroke-width="1" />')
        svg.append(text_to_svg_path(category, cat_x + cat_w / 2.0, 34, 9.5, FONT_TITLE, anchor="middle", fill="#c084fc"))
    
    # Description lines in Outfit Medium
    y_text = 64
    for line in desc_lines[:2]:
        svg.append(text_to_svg_path(line, 24, y_text, 12.5, FONT_BODY, fill="#94a3b8"))
        y_text += 18
        
    # Language and Tech Stack Pills on bottom row
    curr_x = 24
    pill_y = 106
    pill_h = 22
    for t_name, col in tags:
        tw = get_text_width(t_name, 11, FONT_BODY_BOLD)
        pw = tw + 22
        svg.append(f'<rect x="{curr_x}" y="{pill_y}" width="{pw:.1f}" height="{pill_h}" rx="6" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.12)" stroke-width="1" />')
        svg.append(f'<circle cx="{curr_x + 9}" cy="{pill_y + 11}" r="3" fill="{col}" filter="url(#softGlow)" />')
        svg.append(text_to_svg_path(t_name, curr_x + 16, pill_y + 15, 11, FONT_BODY_BOLD, fill="#e2e8f0"))
        curr_x += pw + 8
    
    # Forks count if any (Right aligned at bottom)
    if forks > 0:
        stat_x = w - 55
        svg.append(f'''
        <g transform="translate({stat_x}, 109)">
          <circle cx="2" cy="2" r="1.8" fill="none" stroke="#94a3b8" stroke-width="1.2" />
          <circle cx="10" cy="2" r="1.8" fill="none" stroke="#94a3b8" stroke-width="1.2" />
          <circle cx="6" cy="10" r="1.8" fill="none" stroke="#94a3b8" stroke-width="1.2" />
          <path d="M2 4v2a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2V4M6 8v2" fill="none" stroke="#94a3b8" stroke-width="1.2" />
        </g>
        ''')
        svg.append(text_to_svg_path(str(forks), stat_x + 16, 120, 12, FONT_BODY, fill="#94a3b8"))
        
    svg.append('</svg>')
    return '\n'.join(svg)

def generate_header_svg(title, icon_type='code'):
    w, h = 600, 32
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
    svg.append('''
    <defs>
      <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#00f2fe" />
        <stop offset="35%" stop-color="#38bdf8" />
        <stop offset="70%" stop-color="#818cf8" />
        <stop offset="100%" stop-color="#c084fc" />
      </linearGradient>
    </defs>
    ''')
    
    font_size = 14.5
    tw = get_text_width(title, font_size, FONT_HEADER)
    total_w = tw + 28
    start_x = (w - total_w) / 2
    
    # Vector Icons
    icon_svg = ''
    if icon_type == 'user':
        icon_svg = '<circle cx="12" cy="7" r="4" stroke="#00f2fe" stroke-width="2" fill="none" /><path d="M5.5 21a6.5 6.5 0 0 1 13 0" stroke="#00f2fe" stroke-width="2" stroke-linecap="round" fill="none" />'
    elif icon_type == 'terminal':
        icon_svg = '<path d="M4 17l6-6-6-6M12 19h8" stroke="#00f2fe" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none" />'
    elif icon_type == 'folder':
        icon_svg = '<path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z" stroke="#818cf8" stroke-width="2" fill="none" />'
    elif icon_type == 'trophy':
        icon_svg = '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6M18 9h1.5a2.5 2.5 0 0 0 0-5H18M4 22h16M10 14.66V17c0 .55-.45 1-1 1H7M14 14.66V17c0 .55.45 1 1 1h2M18 2H6v7a6 6 0 0 0 12 0V2Z" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none" />'
    elif icon_type == 'award':
        icon_svg = '<circle cx="12" cy="8" r="6" stroke="#c084fc" stroke-width="2" fill="none" /><path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.724.524l-4.268-2.243-4.27 2.243a.5.5 0 0 1-.723-.524l1.515-8.526" stroke="#c084fc" stroke-width="2" fill="none" />'
    elif icon_type == 'cpu':
        icon_svg = '<rect x="4" y="4" width="16" height="16" rx="2" stroke="#38bdf8" stroke-width="2" fill="none" /><rect x="9" y="9" width="6" height="6" stroke="#38bdf8" stroke-width="2" fill="none" /><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3" stroke="#38bdf8" stroke-width="2" fill="none" />'
    elif icon_type == 'stack':
        icon_svg = '<path d="m12 2 10 5-10 5L2 7l10-5ZM2 17l10 5 10-5M2 12l10 5 10-5" stroke="#c084fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none" />'
    elif icon_type == 'music':
        icon_svg = '<path d="M9 18V5l12-2v13M9 18a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm12 0a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" stroke="#818cf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none" />'
    elif icon_type == 'send':
        icon_svg = '<path d="m22 2-7 20-4-9-9-4Z" stroke="#00f2fe" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none" /><path d="M22 2 11 13" stroke="#00f2fe" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none" />'
    else:
        icon_svg = '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3L12 3Z" stroke="#00f2fe" stroke-width="2" fill="none" />'

    svg.append(f'<g transform="translate({start_x}, 5) scale(0.9)">{icon_svg}</g>')
    svg.append(text_to_svg_path(title, start_x + 28, 22, font_size, FONT_HEADER, fill="url(#headerGrad)", extra='stroke="url(#headerGrad)" stroke-width="0.5" stroke-linejoin="round"'))
    svg.append('</svg>')
    return '\n'.join(svg)

def make_cycling_headline_svg(lines, w=680, h=50, font_size=26, dur_per_line=3.5):
    n = len(lines)
    total_dur = n * dur_per_line
    fade_frac = 0.05
    
    svg_groups = []
    for idx, line in enumerate(lines):
        path = text_to_svg_path(line, w/2, h*0.68, font_size, FONT_CURSIVE, anchor='middle', fill='url(#rainbowGrad)', extra='stroke="url(#rainbowGrad)" stroke-width="0.85" stroke-linejoin="round"')
        start_f = idx / n
        fade_in_f = start_f + fade_frac
        hold_f = (idx + 1) / n - fade_frac
        end_f = (idx + 1) / n
        
        pts = []
        if idx == 0:
            pts.append((0.0, 1))
            pts.append((hold_f, 1))
            pts.append((end_f, 0))
            pts.append((1.0 - fade_frac, 0))
            pts.append((1.0, 1))
        else:
            pts.append((0.0, 0))
            pts.append((start_f, 0))
            pts.append((fade_in_f, 1))
            pts.append((hold_f, 1))
            pts.append((end_f, 0))
            if end_f < 1.0:
                pts.append((1.0, 0))
            
        pts = sorted(list(set(pts)), key=lambda x: x[0])
        kt_str = '; '.join(f'{p[0]:.4f}' for p in pts)
        val_str = '; '.join(str(p[1]) for p in pts)
        init_op = "1" if idx == 0 else "0"
        
        svg_groups.append(f'''
        <g opacity="{init_op}">
          <animate attributeName="opacity" dur="{total_dur}s" repeatCount="indefinite"
            values="{val_str}" keyTimes="{kt_str}" />
          {path}
        </g>''')
        
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">
  <defs>
    <linearGradient id="rainbowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2fe" />
      <stop offset="35%" stop-color="#38bdf8" />
      <stop offset="70%" stop-color="#818cf8" />
      <stop offset="100%" stop-color="#c084fc" />
    </linearGradient>
  </defs>
  {''.join(svg_groups)}
</svg>'''

def make_gradient_cursive_svg(text, w, h, font_size):
    path = text_to_svg_path(text, w/2, h*0.68, font_size, FONT_CURSIVE, anchor='middle', fill='url(#rainbowGrad)', extra='stroke="url(#rainbowGrad)" stroke-width="0.85" stroke-linejoin="round"')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">
  <defs>
    <linearGradient id="rainbowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2fe" />
      <stop offset="35%" stop-color="#38bdf8" />
      <stop offset="70%" stop-color="#818cf8" />
      <stop offset="100%" stop-color="#c084fc" />
    </linearGradient>
  </defs>
  {path}
</svg>'''

def generate_hero_banner_svg():
    w, h = 900, 190
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
    svg.append('''
    <defs>
      <linearGradient id="bannerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#00f2fe" />
        <stop offset="35%" stop-color="#38bdf8" />
        <stop offset="70%" stop-color="#818cf8" />
        <stop offset="100%" stop-color="#c084fc" />
      </linearGradient>
      <linearGradient id="bannerBorder" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="rgba(0, 242, 254, 0.4)" />
        <stop offset="50%" stop-color="rgba(129, 140, 248, 0.2)" />
        <stop offset="100%" stop-color="rgba(192, 132, 252, 0.4)" />
      </linearGradient>
      <linearGradient id="bannerBg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0a0e1a" />
        <stop offset="50%" stop-color="#0d1117" />
        <stop offset="100%" stop-color="#120e22" />
      </linearGradient>
      <radialGradient id="cyanOrb" cx="10%" cy="20%" r="50%">
        <stop offset="0%" stop-color="#00f2fe" stop-opacity="0.15" />
        <stop offset="100%" stop-color="#00f2fe" stop-opacity="0" />
      </radialGradient>
      <radialGradient id="purpleOrb" cx="90%" cy="80%" r="50%">
        <stop offset="0%" stop-color="#c084fc" stop-opacity="0.14" />
        <stop offset="100%" stop-color="#c084fc" stop-opacity="0" />
      </radialGradient>
      <linearGradient id="gridGrad" x1="0%" y1="100%" x2="0%" y2="0%">
        <stop offset="0%" stop-color="#818cf8" stop-opacity="0.12" />
        <stop offset="100%" stop-color="#818cf8" stop-opacity="0" />
      </linearGradient>
    </defs>
    ''')
    svg.append(f'<rect width="{w}" height="{h}" rx="16" fill="url(#bannerBg)" stroke="url(#bannerBorder)" stroke-width="1.5" />')
    svg.append(f'<rect width="{w}" height="{h}" rx="16" fill="url(#cyanOrb)" />')
    svg.append(f'<rect width="{w}" height="{h}" rx="16" fill="url(#purpleOrb)" />')
    
    # Perspective grid lines
    for gy in [130, 146, 163, 178]:
        svg.append(f'<line x1="20" y1="{gy}" x2="{w - 20}" y2="{gy}" stroke="url(#gridGrad)" stroke-width="1" />')
    for gx in [120, 240, 360, 480, 600, 720]:
        svg.append(f'<line x1="{gx}" y1="115" x2="{gx}" y2="{h - 10}" stroke="url(#gridGrad)" stroke-width="0.8" />')
        
    # Top-left window controls
    svg.append('''
    <g transform="translate(26, 22)">
      <circle cx="0" cy="0" r="4.5" fill="#ff5f56" />
      <circle cx="15" cy="0" r="4.5" fill="#ffbd2e" />
      <circle cx="30" cy="0" r="4.5" fill="#27c93f" />
    </g>
    ''')
    
    # Top-right live badge
    svg.append(f'''
    <g transform="translate({w - 300}, 12)">
      <rect width="276" height="24" rx="12" fill="rgba(0, 242, 254, 0.06)" stroke="rgba(0, 242, 254, 0.2)" stroke-width="1" />
      <circle cx="14" cy="12" r="3.5" fill="#38ef7d">
        <animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite" />
      </circle>
      <text x="26" y="16" fill="#cbd5e1" font-size="9.5" font-family="monospace" letter-spacing="1">SYSTEM ARCHITECT • CLOUD &amp; AI</text>
    </g>
    ''')
    
    # Main Title
    svg.append(text_to_svg_path("NISHANT RANJAN", 26, 76, 36, FONT_HEADER, fill="url(#bannerGrad)", extra='stroke="url(#bannerGrad)" stroke-width="0.5" stroke-linejoin="round"'))
    # Subtitle
    svg.append(text_to_svg_path("High-Throughput Distributed Engines • Concurrency • Real-Time Speech AI", 26, 106, 13.5, FONT_TITLE, fill="#e2e8f0"))
    # Description
    svg.append(text_to_svg_path("Turning complex distributed protocols and query engines into resilient, zero-friction architectures.", 26, 128, 12, FONT_BODY, fill="#94a3b8"))
    
    # Pills
    pills = [("JAVA", "#b07219"), ("TYPESCRIPT", "#3178c6"), ("PYTHON", "#3776ab"), ("FASTAPI", "#009688"), ("DUCKDB", "#f1c40f"), ("SPRING BOOT", "#6db33f"), ("NEXT.JS", "#00f2fe")]
    px = 26
    for pname, pcol in pills:
        pw = get_text_width(pname, 9.5, FONT_TITLE) + 18
        svg.append(f'<rect x="{px}" y="148" width="{pw}" height="20" rx="4" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.1)" stroke-width="1" />')
        svg.append(f'<circle cx="{px + 7}" cy="158" r="2.5" fill="{pcol}" />')
        svg.append(text_to_svg_path(pname, px + 14, 162, 9.5, FONT_TITLE, fill="#e2e8f0"))
        px += pw + 8
        
    # Decorative architecture node graph on right
    svg.append(f'''
    <g transform="translate({w - 200}, 62)">
      <rect x="0" y="0" width="80" height="26" rx="6" fill="rgba(0,242,254,0.08)" stroke="#00f2fe" stroke-width="1.2" />
      <text x="40" y="17" fill="#00f2fe" font-size="9.5" font-family="monospace" text-anchor="middle" font-weight="bold">TELEMETRY</text>
      <line x1="80" y1="13" x2="108" y2="13" stroke="#818cf8" stroke-width="1.2" stroke-dasharray="2 2" />
      <rect x="108" y="0" width="68" height="26" rx="6" fill="rgba(129,140,248,0.08)" stroke="#818cf8" stroke-width="1.2" />
      <text x="142" y="17" fill="#818cf8" font-size="9.5" font-family="monospace" text-anchor="middle" font-weight="bold">DAG ENGINE</text>
      <path d="M 142 26 L 142 46 L 90 46" stroke="#c084fc" stroke-width="1.2" fill="none" stroke-dasharray="2 2" />
      <rect x="16" y="34" width="74" height="26" rx="6" fill="rgba(192,132,252,0.08)" stroke="#c084fc" stroke-width="1.2" />
      <text x="53" y="51" fill="#c084fc" font-size="9.5" font-family="monospace" text-anchor="middle" font-weight="bold">DUCKDB OLAP</text>
    </g>
    ''')
    
    svg.append('</svg>')
    return '\n'.join(svg)

def generate_world_clocks_svg():
    w, h = 900, 102
    now_utc = datetime.now(timezone.utc)
    ist = now_utc + timedelta(hours=5, minutes=30)
    london = now_utc + timedelta(hours=1)
    
    ist_sec_ang = ist.second * 6
    ist_min_ang = ist.minute * 6 + ist.second * 0.1
    ist_hr_ang = (ist.hour % 12) * 30 + ist.minute * 0.5
    
    lon_sec_ang = london.second * 6
    lon_min_ang = london.minute * 6 + london.second * 0.1
    lon_hr_ang = (london.hour % 12) * 30 + london.minute * 0.5
    
    card_w = (w - 20) / 2
    c2_x = card_w + 20
    
    def render_clock_face(cx, cy, r, hr_ang, min_ang, sec_ang, theme_col, sec_col):
        ticks = []
        for i in range(12):
            ang = math.radians(i * 30)
            x1 = cx + (r - 4) * math.sin(ang)
            y1 = cy - (r - 4) * math.cos(ang)
            x2 = cx + (r - 1.5) * math.sin(ang)
            y2 = cy - (r - 1.5) * math.cos(ang)
            width = 1.6 if i % 3 == 0 else 0.8
            ticks.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{theme_col}" stroke-width="{width}" stroke-linecap="round" opacity="0.6" />')
            
        return f'''
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="#080c14" stroke="{theme_col}" stroke-width="1.8" opacity="0.9" />
        {''.join(ticks)}
        <!-- Hour Hand -->
        <g transform="rotate({hr_ang:.1f} {cx} {cy})">
          <line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r*0.5:.1f}" stroke="#ffffff" stroke-width="2.4" stroke-linecap="round" />
          <animateTransform attributeName="transform" type="rotate" from="{hr_ang:.1f} {cx} {cy}" to="{hr_ang + 360:.1f} {cx} {cy}" dur="43200s" repeatCount="indefinite" />
        </g>
        <!-- Minute Hand -->
        <g transform="rotate({min_ang:.1f} {cx} {cy})">
          <line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r*0.75:.1f}" stroke="{theme_col}" stroke-width="1.8" stroke-linecap="round" />
          <animateTransform attributeName="transform" type="rotate" from="{min_ang:.1f} {cx} {cy}" to="{min_ang + 360:.1f} {cx} {cy}" dur="3600s" repeatCount="indefinite" />
        </g>
        <!-- Second Hand (Continuous sweeping live animation) -->
        <g transform="rotate({sec_ang:.1f} {cx} {cy})">
          <line x1="{cx}" y1="{cy + 5}" x2="{cx}" y2="{cy - r*0.82:.1f}" stroke="{sec_col}" stroke-width="1.2" stroke-linecap="round" />
          <circle cx="{cx}" cy="{cy}" r="2.2" fill="{sec_col}" />
          <animateTransform attributeName="transform" type="rotate" from="{sec_ang:.1f} {cx} {cy}" to="{sec_ang + 360:.1f} {cx} {cy}" dur="60s" repeatCount="indefinite" />
        </g>
        '''
        
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
    svg.append('''
    <defs>
      <linearGradient id="istBg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0c1220" />
        <stop offset="100%" stop-color="#080c14" />
      </linearGradient>
      <linearGradient id="lonBg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#141024" />
        <stop offset="100%" stop-color="#0c0818" />
      </linearGradient>
    </defs>
    ''')
    
    # --- Card 1: India (IST) ---
    svg.append(f'<rect x="0" y="0" width="{card_w}" height="{h}" rx="12" fill="url(#istBg)" stroke="rgba(0, 242, 254, 0.25)" stroke-width="1.2" />')
    svg.append(render_clock_face(48, 51, 30, ist_hr_ang, ist_min_ang, ist_sec_ang, "#00f2fe", "#f43f5e"))
    
    svg.append(text_to_svg_path("NEW DELHI, INDIA", 92, 26, 11, FONT_HEADER, fill="#94a3b8"))
    ist_time_str = ist.strftime('%I:%M %p')
    svg.append(text_to_svg_path(ist_time_str, 92, 52, 21, FONT_TITLE, fill="#ffffff"))
    badge_x = 92 + get_text_width(ist_time_str, 21, FONT_TITLE) + 12
    svg.append(f'<rect x="{badge_x}" y="34" width="38" height="20" rx="4" fill="rgba(0, 242, 254, 0.12)" stroke="rgba(0, 242, 254, 0.3)" stroke-width="1" />')
    svg.append(text_to_svg_path("IST", badge_x + 9, 48, 10, FONT_TITLE, fill="#00f2fe"))
    svg.append(text_to_svg_path("UTC +5:30  •  Primary Base  •  Active Core", 92, 70, 10.5, FONT_BODY, fill="#00f2fe"))
    svg.append(text_to_svg_path("⚡ Click to open second-by-second live HUD ↗", 92, 88, 9.5, FONT_TITLE, fill="#64748b"))
    
    # --- Card 2: London (BST/GMT) ---
    svg.append(f'<rect x="{c2_x}" y="0" width="{card_w}" height="{h}" rx="12" fill="url(#lonBg)" stroke="rgba(192, 132, 252, 0.25)" stroke-width="1.2" />')
    svg.append(render_clock_face(c2_x + 48, 51, 30, lon_hr_ang, lon_min_ang, lon_sec_ang, "#c084fc", "#00f2fe"))
    
    svg.append(text_to_svg_path("LONDON, UNITED KINGDOM", c2_x + 92, 26, 11, FONT_HEADER, fill="#94a3b8"))
    lon_time_str = london.strftime('%I:%M %p')
    svg.append(text_to_svg_path(lon_time_str, c2_x + 92, 52, 21, FONT_TITLE, fill="#ffffff"))
    badge2_x = c2_x + 92 + get_text_width(lon_time_str, 21, FONT_TITLE) + 12
    svg.append(f'<rect x="{badge2_x}" y="34" width="38" height="20" rx="4" fill="rgba(192, 132, 252, 0.12)" stroke="rgba(192, 132, 252, 0.3)" stroke-width="1" />')
    svg.append(text_to_svg_path("BST", badge2_x + 8, 48, 10, FONT_TITLE, fill="#c084fc"))
    svg.append(text_to_svg_path("UTC +1:00  •  Global Base  •  Collaboration", c2_x + 92, 70, 10.5, FONT_BODY, fill="#c084fc"))
    svg.append(text_to_svg_path("⚡ Click to open second-by-second live HUD ↗", c2_x + 92, 88, 9.5, FONT_TITLE, fill="#64748b"))
    
    svg.append('</svg>')
    return '\n'.join(svg)

def generate_divider_svg():
    w, h = 900, 6
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">
  <defs>
    <linearGradient id="glowDivider" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2fe" stop-opacity="0" />
      <stop offset="20%" stop-color="#00f2fe" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#818cf8" stop-opacity="1" />
      <stop offset="80%" stop-color="#c084fc" stop-opacity="0.85" />
      <stop offset="100%" stop-color="#c084fc" stop-opacity="0" />
    </linearGradient>
    <filter id="divGlow" x="-10%" y="-100%" width="120%" height="300%">
      <feGaussianBlur stdDeviation="1.2" result="glow" />
      <feMerge>
        <feMergeNode in="glow" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>
  <rect x="30" y="2" width="{w - 60}" height="2" rx="1" fill="url(#glowDivider)" filter="url(#divGlow)" />
</svg>'''

def generate_divider_gif(folders=['assets', 'dist']):
    from PIL import Image, ImageDraw
    w, h = 900, 8
    line_y = 4
    cols = [
        (0, 242, 254),
        (56, 189, 248),
        (129, 140, 248),
        (192, 132, 252)
    ]
    def get_color_at(t):
        t = max(0.0, min(1.0, t))
        idx = t * 3.0
        i = int(idx)
        if i >= 3:
            return cols[3]
        f = idx - i
        c1, c2 = cols[i], cols[i+1]
        return (
            int(c1[0] + (c2[0] - c1[0]) * f),
            int(c1[1] + (c2[1] - c1[1]) * f),
            int(c1[2] + (c2[2] - c1[2]) * f)
        )
    frames = []
    num_frames = 36
    for frame_idx in range(num_frames):
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        pulse_x = (frame_idx / num_frames) * w
        pulse_radius = 120
        for x in range(w):
            base_c = get_color_at(x / w)
            dist = abs(x - pulse_x)
            if dist < pulse_radius:
                boost = (1.0 - (dist / pulse_radius)) ** 2
                alpha = int(70 + boost * 185)
                r = min(255, int(base_c[0] + boost * (255 - base_c[0]) * 0.8))
                g = min(255, int(base_c[1] + boost * (255 - base_c[1]) * 0.8))
                b = min(255, int(base_c[2] + boost * (255 - base_c[2]) * 0.8))
            else:
                alpha = 70
                r, g, b = base_c
            for dy in range(-1, 2):
                draw.point((x, line_y + dy), fill=(r, g, b, alpha))
        frames.append(im)
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        frames[0].save(
            os.path.join(folder, 'divider.gif'),
            save_all=True,
            append_images=frames[1:],
            duration=45,
            loop=0,
            transparency=0,
            disposal=2
        )

if __name__ == '__main__':
    os.makedirs('assets', exist_ok=True)
    os.makedirs('dist', exist_ok=True)
    
    # 0. Hero Banner, World Clocks, and Glowing Dividers
    banner_svg = generate_hero_banner_svg()
    clocks_svg = generate_world_clocks_svg()
    divider_svg = generate_divider_svg()
    generate_divider_gif(['assets', 'dist'])
    
    # 1. Main Stats, Streak & Languages Cards
    stats_svg = generate_stats_card()
    streak_svg = generate_streak_card()
    langs_svg = generate_languages_card()
    
    # 2. Cycling and Static Cursive Typing SVGs
    headline_lines = [
        'Full-Stack Architect • Building Scalable Systems',
        'AI/ML Explorer • Teaching Machines to Think',
        'Open-Source Builder • Crafting Things That Matter',
        'Turning Complex Problems into Clean Code'
    ]
    typing_headline = make_cycling_headline_svg(headline_lines, 680, 50, 26)
    typing_spotify = make_gradient_cursive_svg("The song that's been playing on my mind recently.", 620, 38, 22)
    typing_footer = make_gradient_cursive_svg("Craft code that thinks, builds that scale, and apps that feel alive.", 680, 44, 24)
    
    # 3. Section Header SVGs
    headers = [
        ('header-about.svg', 'ABOUT ME', 'user'),
        ('header-arsenal.svg', 'CORE TECHNICAL ARSENAL', 'stack'),
        ('header-command-center.svg', 'DEVELOPER COMMAND CENTER', 'terminal'),
        ('header-creations.svg', 'FEATURED ARCHITECTURAL CREATIONS', 'folder'),
        ('header-highlights.svg', 'SYSTEM ARCHITECTURE & DEEP-DIVES', 'cpu'),
        ('header-trophies.svg', 'HALL OF HONORS & TROPHIES', 'trophy'),
        ('header-certifications.svg', 'HONORS & PROFESSIONAL CERTIFICATIONS', 'award'),
        ('header-spotify.svg', 'ON REPEAT IN MY MIND', 'music'),
        ('header-connect.svg', 'CONNECT & COLLABORATE', 'send'),
    ]
    
    for folder in ['assets', 'dist']:
        with open(os.path.join(folder, 'hero-banner.svg'), 'w') as f:
            f.write(banner_svg)
        with open(os.path.join(folder, 'world-clocks.svg'), 'w') as f:
            f.write(clocks_svg)
        with open(os.path.join(folder, 'divider.svg'), 'w') as f:
            f.write(divider_svg)
        with open(os.path.join(folder, 'card-stats.svg'), 'w') as f:
            f.write(stats_svg)
        with open(os.path.join(folder, 'card-streak.svg'), 'w') as f:
            f.write(streak_svg)
        with open(os.path.join(folder, 'card-languages.svg'), 'w') as f:
            f.write(langs_svg)
        with open(os.path.join(folder, 'typing-headline.svg'), 'w') as f:
            f.write(typing_headline)
        with open(os.path.join(folder, 'typing-spotify.svg'), 'w') as f:
            f.write(typing_spotify)
        with open(os.path.join(folder, 'typing-footer.svg'), 'w') as f:
            f.write(typing_footer)
            
        for fname, title, itype in headers:
            with open(os.path.join(folder, fname), 'w') as f:
                f.write(generate_header_svg(title, itype))
            
    repos = [
        (
            "ShadowLedger",
            [
                "Uncertainty-aware value-flow reconstruction & audit engine",
                "designed for high-assurance autonomous financial operations."
            ],
            "FINTECH",
            [("Python", "#3776ab"), ("FastAPI", "#009688"), ("DuckDB", "#f1c40f")],
            0, 0
        ),
        (
            "SPARK-Engine",
            [
                "Speech-Powered Analytics Relational Kit — voice-driven querying",
                "engine for relational databases with real-time audio telemetry."
            ],
            "SPEECH AI",
            [("TypeScript", "#3178c6"), ("Next.js", "#00f2fe"), ("DuckDB", "#f1c40f")],
            2, 0
        ),
        (
            "askDB",
            [
                "Deterministic-probabilistic hybrid NL-to-SQL query parser",
                "translating conversational prompts into validated SQL joins."
            ],
            "NL-TO-SQL",
            [("Python", "#3776ab"), ("FastAPI", "#00f2fe"), ("MySQL", "#4479a1")],
            0, 0
        ),
        (
            "InsightU_v1",
            [
                "Comprehensive academic ecosystem & analytics platform with",
                "predictive student health metrics and collaborative spaces."
            ],
            "EDTECH AI",
            [("TypeScript", "#3178c6"), ("Next.js", "#00f2fe"), ("Supabase", "#3ecf8e")],
            1, 0
        ),
        (
            "easy-q",
            [
                "High-throughput digital queue orchestrator and appointment",
                "scheduler powered by live WebSockets and Spring Security."
            ],
            "SYSTEMS",
            [("Java", "#b07219"), ("Spring Boot", "#6db33f"), ("WebSockets", "#00f2fe")],
            0, 0
        ),
        (
            "Gavel",
            [
                "Model Context Protocol (MCP) AI frontend architect running",
                "deterministic rule engines with transparent confidence scoring."
            ],
            "MCP ENGINE",
            [("TypeScript", "#3178c6"), ("MCP Server", "#c084fc"), ("NitroStack", "#00f2fe")],
            0, 0
        ),
    ]
    
    for idx, (name, desc_lines, category, tags, forks, stars) in enumerate(repos):
        svg_code = generate_repo_card(name, desc_lines, category, tags, forks, stars)
        fname = f'card-repo-{name.lower().replace("-", "").replace("_", "")}.svg'
        for folder in ['assets', 'dist']:
            with open(os.path.join(folder, fname), 'w') as f:
                f.write(svg_code)
                
    print("Regenerated all cards, headers, and golden trophies with multi-color gradient!")
