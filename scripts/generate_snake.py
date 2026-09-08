import os

def generate_snake_svg(theme='dark'):
    is_dark = (theme == 'dark')
    bg_color = '#0d1117' if is_dark else '#ffffff'
    empty_color = '#161b22' if is_dark else '#ebedf0'
    
    # Authentic GitHub Contribution Green palette
    c1 = '#0e4429' if is_dark else '#9be9a8'
    c2 = '#006d32' if is_dark else '#40c463'
    c3 = '#26a641' if is_dark else '#30a14e'
    c4 = '#39d353' if is_dark else '#216e39'
    levels = [empty_color, c1, c2, c3, c4]
    
    # Grid: 7 rows x 53 columns
    grid = [[0 for _ in range(53)] for _ in range(7)]
    
    # Dot matrix definitions for "N I S H A N T"
    # Each letter is designed for clean readability on a 7-row grid
    LETTERS = {
        'N': [
            [4, 0, 0, 4],
            [4, 4, 0, 4],
            [4, 3, 0, 4],
            [4, 0, 3, 4],
            [4, 0, 4, 4],
            [4, 0, 0, 4],
            [4, 0, 0, 4]
        ],
        'I': [
            [3, 4, 3],
            [0, 4, 0],
            [0, 4, 0],
            [0, 4, 0],
            [0, 4, 0],
            [0, 4, 0],
            [3, 4, 3]
        ],
        'S': [
            [0, 4, 4, 3],
            [4, 0, 0, 0],
            [4, 4, 4, 0],
            [0, 0, 0, 4],
            [0, 0, 0, 4],
            [4, 0, 0, 4],
            [0, 4, 4, 0]
        ],
        'H': [
            [4, 0, 0, 4],
            [4, 0, 0, 4],
            [4, 0, 0, 4],
            [4, 4, 4, 4],
            [4, 0, 0, 4],
            [4, 0, 0, 4],
            [4, 0, 0, 4]
        ],
        'A': [
            [0, 4, 4, 0],
            [4, 0, 0, 4],
            [4, 0, 0, 4],
            [4, 4, 4, 4],
            [4, 0, 0, 4],
            [4, 0, 0, 4],
            [4, 0, 0, 4]
        ],
        'T': [
            [4, 4, 4, 4, 4],
            [0, 0, 4, 0, 0],
            [0, 0, 4, 0, 0],
            [0, 0, 4, 0, 0],
            [0, 0, 4, 0, 0],
            [0, 0, 4, 0, 0],
            [0, 0, 4, 0, 0]
        ]
    }
    
    word = ['N', 'I', 'S', 'H', 'A', 'N', 'T']
    col_start = 9
    for char in word:
        pattern = LETTERS[char]
        char_w = len(pattern[0])
        for r in range(7):
            for c in range(char_w):
                if pattern[r][c] > 0:
                    grid[r][col_start + c] = pattern[r][c]
        col_start += char_w + 1

    cell_size = 10
    cell_gap = 3
    pad_x = 20
    pad_y = 18
    
    svg_w = pad_x * 2 + 53 * (cell_size + cell_gap) - cell_gap
    grid_h = 7 * (cell_size + cell_gap) - cell_gap
    svg_h = pad_y + grid_h + 26
    
    # Snake colors - sleek vibrant purple neon as requested and shown in user's profile
    head_fill = '#f0abfc' if is_dark else '#9333ea'
    head_glow = '#e879f9' if is_dark else '#7c3aed'
    seg_colors = (
        ['#e879f9', '#d946ef', '#c026d3', '#a21caf', '#86198f', '#701a75']
        if is_dark else
        ['#c084fc', '#a855f7', '#9333ea', '#7e22ce', '#6b21a8', '#581c87']
    )
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="100%" height="auto">')
    svg.append('<style>')
    svg.append(f'''
        .bg {{ fill: {bg_color}; rx: 12px; }}
        .cell {{ rx: 2px; ry: 2px; }}
        .snake-head {{ fill: {head_fill}; filter: drop-shadow(0 0 8px {head_glow}); rx: 3px; ry: 3px; }}
        .snake-eye {{ fill: #ffffff; }}
        @keyframes pulse-dot {{
            0%, 100% {{ opacity: 1; filter: drop-shadow(0 0 1px #38ef7d); }}
            50% {{ opacity: 0.88; filter: drop-shadow(0 0 4px #11998e); }}
        }}
        .active-dot {{ animation: pulse-dot 3.5s ease-in-out infinite; }}
    ''')
    for idx, col in enumerate(seg_colors):
        svg.append(f'.seg-{idx} {{ fill: {col}; rx: 2.5px; ry: 2.5px; }}')
    svg.append('</style>')
    
    svg.append(f'<rect width="{svg_w}" height="{svg_h}" class="bg" />')
    
    # Render all 53 x 7 cells
    for c in range(53):
        for r in range(7):
            x = pad_x + c * (cell_size + cell_gap)
            y = pad_y + r * (cell_size + cell_gap)
            lvl = grid[r][c]
            fill = levels[lvl]
            if lvl > 0:
                svg.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{fill}" class="cell active-dot" />')
            else:
                svg.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{fill}" class="cell" />')

    # Progress bar at bottom
    bar_y = pad_y + grid_h + 12
    bar_w = svg_w - (pad_x * 2)
    track_color = '#0e4429' if is_dark else '#e1e4e8'
    fill_color_1 = '#006d32' if is_dark else '#40c463'
    fill_color_2 = '#26a641' if is_dark else '#30a14e'
    fill_color_3 = '#39d353' if is_dark else '#216e39'
    
    svg.append(f'<rect x="{pad_x}" y="{bar_y}" width="{bar_w}" height="5" rx="2.5" fill="{track_color}" />')
    svg.append(f'<rect x="{pad_x + int(bar_w * 0.6)}" y="{bar_y}" width="{int(bar_w * 0.22)}" height="5" fill="{fill_color_1}" />')
    svg.append(f'<rect x="{pad_x + int(bar_w * 0.82)}" y="{bar_y}" width="{int(bar_w * 0.1)}" height="5" fill="{fill_color_2}" />')
    svg.append(f'<rect x="{pad_x + int(bar_w * 0.92)}" y="{bar_y}" width="{int(bar_w * 0.08)}" height="5" rx="2.5" fill="{fill_color_3}" />')

    # Continuous snake patrol path crawling across the letters N-I-S-H-A-N-T
    # Points in grid coordinates: (col, row)
    grid_coords = [
        # Start top-left
        (0, 0), (7, 0),
        # N
        (9, 6), (9, 0), (12, 6), (12, 0),
        # I
        (14, 0), (15, 6), (16, 0),
        # S
        (18, 0), (18, 3), (21, 3), (21, 6), (18, 6),
        # H
        (23, 6), (23, 0), (24, 3), (26, 3), (26, 6), (26, 0),
        # A
        (28, 6), (29, 0), (31, 0), (32, 6), (30, 3),
        # N
        (34, 6), (34, 0), (37, 6), (37, 0),
        # T
        (39, 0), (43, 0), (41, 1), (41, 6),
        # End traverse
        (48, 6), (52, 6), (52, 0), (45, 0), (33, 0), (22, 0), (10, 0), (0, 0)
    ]
    
    path_pts = []
    for gc, gr in grid_coords:
        px = pad_x + gc * (cell_size + cell_gap) + (cell_size / 2)
        py = pad_y + gr * (cell_size + cell_gap) + (cell_size / 2)
        path_pts.append((px, py))
        
    d_path = f'M {path_pts[0][0]:.1f} {path_pts[0][1]:.1f} ' + ' '.join([f'L {p[0]:.1f} {p[1]:.1f}' for p in path_pts[1:]]) + ' Z'
    svg.append(f'<path id="snakePath" d="{d_path}" fill="none" stroke="none" />')
    
    # Animated snake head and body segments
    # Total duration 14s for majestic slither speed
    dur = "16s"
    step_delay = 0.14
    
    # Segments in reverse order so head is drawn on top
    for idx in reversed(range(len(seg_colors))):
        delay = f"-{(idx + 1) * step_delay:.2f}s"
        svg.append(f'''
        <g>
            <rect x="-4.5" y="-4.5" width="9" height="9" class="seg-{idx}">
                <animateMotion dur="{dur}" repeatCount="indefinite" begin="{delay}">
                    <mpath href="#snakePath" />
                </animateMotion>
            </rect>
        </g>''')
        
    # Head
    svg.append(f'''
    <g>
        <rect x="-5.5" y="-5.5" width="11" height="11" class="snake-head">
            <animateMotion dur="{dur}" repeatCount="indefinite" begin="0s">
                <mpath href="#snakePath" />
            </animateMotion>
        </rect>
    </g>''')
    
    svg.append('</svg>')
    return '\n'.join(svg)

if __name__ == '__main__':
    os.makedirs('assets', exist_ok=True)
    os.makedirs('dist', exist_ok=True)
    
    dark = generate_snake_svg('dark')
    light = generate_snake_svg('light')
    
    for folder in ['assets', 'dist']:
        with open(os.path.join(folder, 'github-snake-dark.svg'), 'w') as f:
            f.write(dark)
        with open(os.path.join(folder, 'github-snake.svg'), 'w') as f:
            f.write(light)
            
    print('Successfully generated NISHANT Snake SVGs in assets/ and dist/')
