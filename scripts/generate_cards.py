import os

def create_card_defs():
    return '''
    <defs>
      <!-- Gradient Palettes: Cyber Aurora (Cyan -> Emerald -> Purple) -->
      <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#00f2fe" />
        <stop offset="60%" stop-color="#38ef7d" />
        <stop offset="100%" stop-color="#a855f7" />
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
        <stop offset="0%" stop-color="rgba(0, 242, 254, 0.4)" />
        <stop offset="50%" stop-color="rgba(56, 239, 125, 0.25)" />
        <stop offset="100%" stop-color="rgba(168, 85, 247, 0.35)" />
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
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700;800&amp;family=Outfit:wght@400;500;600;700&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap');
        .card-frame { fill: url(#cardBg); stroke: url(#cardBorder); stroke-width: 1.5px; rx: 18px; ry: 18px; }
        .card-title { font-family: 'Space Grotesk', -apple-system, sans-serif; font-weight: 700; fill: url(#titleGrad); letter-spacing: -0.2px; }
        .stat-label { font-family: 'Outfit', -apple-system, sans-serif; font-size: 13.5px; fill: #94a3b8; font-weight: 500; }
        .stat-val { font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 15px; fill: #ffffff; font-weight: 700; }
        .big-stat { font-family: 'Space Grotesk', -apple-system, sans-serif; font-weight: 800; fill: #ffffff; letter-spacing: -0.5px; }
        .caption { font-family: 'Outfit', -apple-system, sans-serif; font-size: 12px; fill: #64748b; font-weight: 500; }
        .badge-txt { font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 11px; font-weight: 700; fill: #00f2fe; letter-spacing: 0.8px; }
        .grade-score { font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 27px; font-weight: 800; fill: url(#titleGrad); }
        .repo-desc { font-family: 'Outfit', -apple-system, sans-serif; font-size: 13px; fill: #94a3b8; line-height: 1.45; }
        .repo-lang { font-family: 'Outfit', -apple-system, sans-serif; font-size: 12.5px; fill: #cbd5e1; font-weight: 600; }
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
    
    # Header
    svg.append('<text x="24" y="37" class="card-title" font-size="18">Nishant Ranjan\'s GitHub Stats</text>')
    
    # Metrics
    items = [
        ("Total Stars Earned:", "1", "#f1c40f", "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"),
        ("Total Commits:", "262", "#00f2fe", "M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"),
        ("Total Pull Requests:", "22", "#c084fc", "M18 16a3 3 0 0 0-2.24 1H8.24A3 3 0 0 0 6 16v-2.18A3 3 0 0 0 8.24 11h7.52A3 3 0 0 0 18 10V4.82A3 3 0 0 0 16 2a3 3 0 0 0-3 3v5H8V5a3 3 0 0 0-6 0v11a3 3 0 0 0 3 3h13a3 3 0 0 0 3-3z"),
        ("Total Issues Closed:", "0", "#38ef7d", "M12 22A10 10 0 1 0 2 12a10 10 0 0 0 10 10zm-1-15h2v6h-2zm0 8h2v2h-2z"),
        ("Contributed to:", "3 Repos", "#38ef7d", "M4 6h16M4 12h16M4 18h16")
    ]
    
    start_y = 67
    for idx, (label, val, icon_col, _) in enumerate(items):
        y = start_y + (idx * 27)
        svg.append(f'<circle cx="32" cy="{y - 4}" r="4" fill="{icon_col}" filter="url(#softGlow)" />')
        svg.append(f'<text x="44" y="{y}" class="stat-label">{label}</text>')
        svg.append(f'<text x="215" y="{y}" class="stat-val">{val}</text>')
        
    # Grade Circle (Right Side) - S+ Rank
    cx, cy, r = 378, 114, 46
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="rgba(255,255,255,0.06)" stroke-width="7" fill="none" />')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="url(#ringGrad)" stroke-width="7" stroke-linecap="round" stroke-dasharray="289" stroke-dashoffset="30" fill="none" filter="url(#neonGlow)" />')
    svg.append(f'<text x="{cx}" y="{cy + 10}" text-anchor="middle" class="grade-score">A+</text>')
    svg.append(f'<text x="{cx}" y="{cy + 36}" text-anchor="middle" class="badge-txt">SUPER ARCHITECT</text>')

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
    svg.append(f'<text x="{col_w * 0.5}" y="85" text-anchor="middle" class="big-stat" font-size="34">319</text>')
    svg.append(f'<text x="{col_w * 0.5}" y="112" text-anchor="middle" class="card-title" font-size="13.5">Total Contributions</text>')
    svg.append(f'<text x="{col_w * 0.5}" y="132" text-anchor="middle" class="caption">Sep 14, 2024 - Present</text>')
    
    # Divider 1
    svg.append(f'<line x1="{col_w}" y1="45" x2="{col_w}" y2="160" stroke="rgba(255,255,255,0.08)" stroke-width="1.5" />')
    
    # Col 2: Current Streak (Centerpiece with glowing ring)
    cx, cy = col_w * 1.5, 78
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="36" stroke="rgba(255,255,255,0.06)" stroke-width="5.5" fill="none" />')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="36" stroke="url(#ringGrad)" stroke-width="5.5" stroke-dasharray="226" stroke-dashoffset="50" stroke-linecap="round" fill="none" filter="url(#neonGlow)" />')
    svg.append(f'<text x="{cx}" y="{cy + 8}" text-anchor="middle" class="big-stat" font-size="25">1</text>')
    svg.append(f'<text x="{cx}" y="136" text-anchor="middle" class="card-title" font-size="14">Current Streak</text>')
    svg.append(f'<text x="{cx}" y="154" text-anchor="middle" class="badge-txt" fill="#38ef7d">DAILY ACTIVE</text>')
    
    # Divider 2
    svg.append(f'<line x1="{col_w * 2}" y1="45" x2="{col_w * 2}" y2="160" stroke="rgba(255,255,255,0.08)" stroke-width="1.5" />')
    
    # Col 3: Longest Streak
    svg.append(f'<text x="{col_w * 2.5}" y="85" text-anchor="middle" class="big-stat" font-size="34">3</text>')
    svg.append(f'<text x="{col_w * 2.5}" y="112" text-anchor="middle" class="card-title" font-size="13.5">Longest Streak</text>')
    svg.append(f'<text x="{col_w * 2.5}" y="132" text-anchor="middle" class="caption">Peak Consistency</text>')
    
    svg.append('</svg>')
    return '\n'.join(svg)

def generate_languages_card():
    w, h = 540, 225
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
    svg.append(create_card_defs())
    svg.append(f'<rect width="{w}" height="{h}" class="card-frame" />')
    
    # Header
    svg.append('<text x="24" y="38" class="card-title" font-size="19">Most Used Languages</text>')
    
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
        svg.append(f'<text x="{lx + 15}" y="{ly}" class="stat-val" font-size="14">{name}</text>')
        svg.append(f'<text x="{lx + 150}" y="{ly}" class="caption" font-size="13" font-weight="600">{pct:.2f}%</text>')
        
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
    
    # Title
    svg.append(f'<text x="56" y="38" class="card-title" font-size="17.5">{name}</text>')
    
    # Description
    d = desc if desc else "High-performance software engine & architectural component."
    if len(d) > 65:
        d1 = d[:65]
        d2 = d[65:128] + ('...' if len(d) > 128 else '')
        svg.append(f'<text x="24" y="65" class="repo-desc">{d1}</text>')
        svg.append(f'<text x="24" y="83" class="repo-desc">{d2}</text>')
    else:
        svg.append(f'<text x="24" y="69" class="repo-desc">{d}</text>')
        
    # Language tag
    svg.append(f'<circle cx="28" cy="104" r="4.5" fill="{lang_col}" filter="url(#softGlow)" />')
    svg.append(f'<text x="38" y="108" class="repo-lang">{lang}</text>')
    
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
        <text x="{stat_x + 16}" y="108" class="caption" font-weight="600">{forks}</text>
        ''')
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
                
    print("Generated all cards with Cyber Aurora palette and Space Grotesk typography!")
