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

def get_text_width(text, size, font_path):
    fp = FontProperties(fname=font_path)
    tp = TextPath((0, 0), text, size=size, prop=fp)
    return tp.get_extents().width

def create_card_defs():
    return '''
    <defs>
      <!-- Multi-Color Gradient Palette: Cyber Aurora (Cyan -> Emerald -> Purple -> Coral) -->
      <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#00f2fe" />
        <stop offset="32%" stop-color="#38ef7d" />
        <stop offset="68%" stop-color="#c084fc" />
        <stop offset="100%" stop-color="#f43f5e" />
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
        <stop offset="33%" stop-color="rgba(56, 239, 125, 0.35)" />
        <stop offset="66%" stop-color="rgba(192, 132, 252, 0.35)" />
        <stop offset="100%" stop-color="rgba(244, 63, 94, 0.45)" />
      </linearGradient>
      <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#00f2fe" />
        <stop offset="33%" stop-color="#38ef7d" />
        <stop offset="66%" stop-color="#c084fc" />
        <stop offset="100%" stop-color="#f43f5e" />
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

def make_trophy_icon(cx, cy, scale=1.0):
    return f'''
    <g transform="translate({cx},{cy}) scale({scale})">
      <ellipse cx="0" cy="42" rx="28" ry="5" fill="#f59e0b" opacity="0.25" filter="url(#goldGlow)" />
      
      <!-- Laurel Leaves -->
      <path d="M-28,12 C-34,-4 -28,-22 -14,-30 C-20,-18 -22,-2 -18,14 Z" fill="url(#goldShine)" opacity="0.75" />
      <path d="M28,12 C34,-4 28,-22 14,-30 C20,-18 22,-2 18,14 Z" fill="url(#goldShine)" opacity="0.75" />
      
      <!-- Handles -->
      <path d="M-18,-18 C-36,-18 -36,8 -16,12 L-14,8 C-28,5 -28,-14 -16,-14 Z" fill="url(#goldDark)" />
      <path d="M18,-18 C36,-18 36,8 16,12 L14,8 C28,5 28,-14 16,-14 Z" fill="url(#goldDark)" />
      
      <!-- Cup Body -->
      <path d="M-18,-26 L18,-26 C16,-6 14,16 0,22 C-14,16 -16,-6 -18,-26 Z" fill="url(#goldCup)" filter="url(#specular3D)" />
      <!-- Rim -->
      <ellipse cx="0" cy="-26" rx="19" ry="4.5" fill="url(#goldHighlight)" />
      <ellipse cx="0" cy="-26" rx="16" ry="3" fill="url(#goldDark)" />
      
      <!-- Stem -->
      <path d="M-4,21 L4,21 L3,32 L-3,32 Z" fill="url(#goldDark)" />
      <ellipse cx="0" cy="32" rx="7" ry="2.5" fill="url(#goldHighlight)" />
      
      <!-- Pedestal -->
      <path d="M-16,33 L16,33 L20,40 L-20,40 Z" fill="url(#goldBase)" />
      <rect x="-22" y="40" width="44" height="4" rx="1.5" fill="url(#goldHighlight)" />
      
      <!-- Star on Cup -->
      <polygon points="0,-8 2.5,-1 9,-1 3.5,3 5.5,10 0,6 -5.5,10 -3.5,3 -9,-1 -2.5,-1" fill="#ffffff" opacity="0.9" filter="url(#softGlow)" />
    </g>
    '''

def generate_golden_trophies_card():
    w, h = 980, 220
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">']
    svg.append('''
    <defs>
      <linearGradient id="trophyCardBg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0f172a" />
        <stop offset="50%" stop-color="#0b0f19" />
        <stop offset="100%" stop-color="#070a10" />
      </linearGradient>
      <linearGradient id="goldBorder" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="rgba(253, 224, 71, 0.45)" />
        <stop offset="50%" stop-color="rgba(234, 179, 8, 0.25)" />
        <stop offset="100%" stop-color="rgba(161, 98, 7, 0.4)" />
      </linearGradient>
      
      <linearGradient id="goldCup" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#fef08a" />
        <stop offset="20%" stop-color="#fde047" />
        <stop offset="50%" stop-color="#ffffff" />
        <stop offset="70%" stop-color="#eab308" />
        <stop offset="100%" stop-color="#a16207" />
      </linearGradient>
      <linearGradient id="goldHighlight" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#ffffff" />
        <stop offset="40%" stop-color="#fde047" />
        <stop offset="100%" stop-color="#ca8a04" />
      </linearGradient>
      <linearGradient id="goldDark" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#eab308" />
        <stop offset="100%" stop-color="#713f12" />
      </linearGradient>
      <linearGradient id="goldShine" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#fef9c3" />
        <stop offset="50%" stop-color="#eab308" />
        <stop offset="100%" stop-color="#854d0e" />
      </linearGradient>
      <linearGradient id="goldBase" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#854d0e" />
        <stop offset="30%" stop-color="#eab308" />
        <stop offset="60%" stop-color="#fde047" />
        <stop offset="100%" stop-color="#713f12" />
      </linearGradient>

      <filter id="goldGlow" x="-30%" y="-30%" width="160%" height="160%">
        <feGaussianBlur stdDeviation="5" result="blur" />
        <feComposite in="SourceGraphic" in2="blur" operator="over" />
      </filter>
      <filter id="specular3D">
        <feDropShadow dx="0" dy="4" stdDeviation="3" flood-color="#000000" flood-opacity="0.6" />
      </filter>
      <filter id="softGlow">
        <feGaussianBlur stdDeviation="2" result="blur" />
        <feComposite in="SourceGraphic" in2="blur" operator="over" />
      </filter>

      <style>
        .gold-card { fill: url(#trophyCardBg); stroke: url(#goldBorder); stroke-width: 1.5px; rx: 18px; }
      </style>
    </defs>
    ''')
    svg.append(f'<rect width="{w}" height="{h}" class="gold-card" />')

    col_w = w / 4
    trophies = [
        ("1ST PLACE", "TechKnow 2025", "National Project Expo", "Top Honors Nationwide"),
        ("TOP 2% NATIONALLY", "NPTEL Java Elite", "Ministry of Education, GoI", "Elite + Silver Honor"),
        ("3RD PLACE", "DAYZERO Hackathon", "National 36-Hr Build", "Intelligent AI Terminal"),
        ("2ND PLACE", "Reuse & Remodel", "National Engineering Expo", "Sustainable Tech Award")
    ]

    for idx, (rank, title, subtitle, extra) in enumerate(trophies):
        cx = (idx + 0.5) * col_w
        svg.append(make_trophy_icon(cx, 68, scale=1.15))
        
        rw = 132
        svg.append(f'<rect x="{cx - rw/2}" y="128" width="{rw}" height="20" rx="10" fill="rgba(234, 179, 8, 0.12)" stroke="rgba(253, 224, 71, 0.35)" stroke-width="1" />')
        svg.append(text_to_svg_path(rank, cx, 142, 10, FONT_TITLE, anchor='middle', fill='#fde047'))
        svg.append(text_to_svg_path(title, cx, 168, 14, FONT_TITLE, anchor='middle', fill='#ffffff'))
        svg.append(text_to_svg_path(subtitle, cx, 186, 11, FONT_BODY, anchor='middle', fill='#94a3b8'))
        svg.append(text_to_svg_path(extra, cx, 202, 10, FONT_BODY, anchor='middle', fill='#eab308'))
        
        if idx < 3:
            div_x = (idx + 1) * col_w
            svg.append(f'<line x1="{div_x}" y1="30" x2="{div_x}" y2="{h - 30}" stroke="rgba(255,255,255,0.06)" stroke-width="1.5" />')

    svg.append('</svg>')
    return '\n'.join(svg)

def generate_header_svg(title, icon_type='code'):
    w, h = 600, 36
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
    svg.append('''
    <defs>
      <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#00f2fe" />
        <stop offset="33%" stop-color="#38ef7d" />
        <stop offset="66%" stop-color="#c084fc" />
        <stop offset="100%" stop-color="#f43f5e" />
      </linearGradient>
      <filter id="glow">
        <feGaussianBlur stdDeviation="2.5" result="blur" />
        <feComposite in="SourceGraphic" in2="blur" operator="over" />
      </filter>
    </defs>
    ''')
    
    # Calculate title width for centering with icon
    tw = get_text_width(title, 18, FONT_TITLE)
    total_w = tw + 32 # 32px for icon + gap
    start_x = (w - total_w) / 2
    
    # Vector Icons
    icon_svg = ''
    if icon_type == 'terminal': # Command Center
        icon_svg = f'<path d="M4 17l6-6-6-6M12 19h8" stroke="#00f2fe" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none" />'
    elif icon_type == 'folder': # Creations
        icon_svg = f'<path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z" stroke="#f43f5e" stroke-width="2" fill="none" />'
    elif icon_type == 'trophy': # Trophies
        icon_svg = f'<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6M18 9h1.5a2.5 2.5 0 0 0 0-5H18M4 22h16M10 14.66V17c0 .55-.45 1-1 1H7M14 14.66V17c0 .55.45 1 1 1h2M18 2H6v7a6 6 0 0 0 12 0V2Z" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none" />'
    elif icon_type == 'award': # Certifications
        icon_svg = f'<circle cx="12" cy="8" r="6" stroke="#c084fc" stroke-width="2" fill="none" /><path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.724.524l-4.268-2.243-4.27 2.243a.5.5 0 0 1-.723-.524l1.515-8.526" stroke="#c084fc" stroke-width="2" fill="none" />'
    elif icon_type == 'cpu': # Highlights / Architecture
        icon_svg = f'<rect x="4" y="4" width="16" height="16" rx="2" stroke="#38ef7d" stroke-width="2" fill="none" /><rect x="9" y="9" width="6" height="6" stroke="#38ef7d" stroke-width="2" fill="none" /><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3" stroke="#38ef7d" stroke-width="2" fill="none" />'
    elif icon_type == 'stack': # Arsenal
        icon_svg = f'<path d="m12 2 10 5-10 5L2 7l10-5ZM2 17l10 5 10-5M2 12l10 5 10-5" stroke="#c084fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none" />'
    else: # Default sparkles
        icon_svg = f'<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3L12 3Z" stroke="#00f2fe" stroke-width="2" fill="none" />'

    svg.append(f'<g transform="translate({start_x}, 6)">{icon_svg}</g>')
    svg.append(text_to_svg_path(title, start_x + 32, 24, 18, FONT_TITLE, fill="url(#headerGrad)"))
    svg.append('</svg>')
    return '\n'.join(svg)

if __name__ == '__main__':
    os.makedirs('assets', exist_ok=True)
    os.makedirs('dist', exist_ok=True)
    
    # 1. Main Stats, Streak & Languages Cards
    stats_svg = generate_stats_card()
    streak_svg = generate_streak_card()
    langs_svg = generate_languages_card()
    trophies_svg = generate_golden_trophies_card()
    
    # 2. Section Header SVGs
    headers = [
        ('header-command-center.svg', 'DEVELOPER COMMAND CENTER', 'terminal'),
        ('header-creations.svg', 'FEATURED ARCHITECTURAL CREATIONS', 'folder'),
        ('header-trophies.svg', 'HALL OF HONORS & TROPHIES', 'trophy'),
        ('header-certifications.svg', 'HONORS & PROFESSIONAL CERTIFICATIONS', 'award'),
        ('header-arsenal.svg', 'CORE TECHNICAL ARSENAL', 'stack'),
        ('header-highlights.svg', 'SYSTEM ARCHITECTURE & DEEP-DIVES', 'cpu'),
    ]
    
    for folder in ['assets', 'dist']:
        with open(os.path.join(folder, 'card-stats.svg'), 'w') as f:
            f.write(stats_svg)
        with open(os.path.join(folder, 'card-streak.svg'), 'w') as f:
            f.write(streak_svg)
        with open(os.path.join(folder, 'card-languages.svg'), 'w') as f:
            f.write(langs_svg)
        with open(os.path.join(folder, 'card-golden-trophies.svg'), 'w') as f:
            f.write(trophies_svg)
            
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
