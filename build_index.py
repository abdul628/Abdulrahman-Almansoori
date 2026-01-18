from pathlib import Path
import html

ROOT = Path('/mnt/data/portfolio_site_final')

PROFILE_HERO = 'assets/profile/profile-hero.jpg'
PROFILE_AVATAR = 'assets/profile/profile-avatar.jpg'
CV_PATH = 'assets/downloads/Abdulrahman_Almansoori_CV.pdf'

LINKEDIN = 'https://www.linkedin.com/in/abdulrahman-mansoori-123a86182/'
INSTAGRAM = 'https://www.instagram.com/a_fbk.s/'


def clean_title(name: str) -> str:
    # Remove extension and tidy whitespace
    name = name.rsplit('.', 1)[0]
    name = name.replace('_', ' ').strip()
    name = ' '.join(name.split())
    return name


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def list_files(dir_path: Path, exts=None):
    exts = None if not exts else {e.lower() for e in exts}
    items = []
    # Non-recursive on purpose (avoids picking up thumbs/ subfolders)
    for p in dir_path.glob('*'):
        if p.is_file():
            if exts and p.suffix.lower() not in exts:
                continue
            items.append(p)
    return sorted(items, key=lambda x: x.name.lower())


def make_badge(text: str):
    return f"<span class='text-xs font-mono text-blue-300 px-2 py-1 bg-blue-950/60 border border-blue-900/60 rounded'>{esc(text)}</span>"


def card_dark(img_src: str, kicker: str, title: str, desc: str, badges: list[str], href: str | None = None):
    img_html = f"<img src='{esc(img_src)}' alt='{esc(title)}' class='w-full h-full object-cover' loading='lazy'>"
    link_open = f"<a href='{esc(href)}' target='_blank' rel='noopener' class='block'>" if href else "<div>"
    link_close = "</a>" if href else "</div>"
    badges_html = "".join(make_badge(b) for b in badges)
    return f"""
    <div class='project-card bg-slate-800/70 rounded-3xl overflow-hidden border border-slate-700/70 shadow-[0_0_0_1px_rgba(255,255,255,0.03)] hover:shadow-[0_30px_60px_-20px_rgba(0,0,0,0.6)]'>
      {link_open}
        <div class='aspect-video overflow-hidden bg-slate-900/60'>
          {img_html}
        </div>
        <div class='p-8 space-y-4'>
          <div class='flex items-center justify-between gap-3'>
            <p class='text-xs uppercase tracking-[0.2em] text-slate-400 font-semibold'>{esc(kicker)}</p>
            <span class='text-[11px] text-slate-500'>Open</span>
          </div>
          <h3 class='text-xl font-bold leading-snug'>{esc(title)}</h3>
          <p class='text-slate-300/80 text-sm leading-relaxed'>{esc(desc)}</p>
          <div class='flex flex-wrap gap-2 pt-1'>
            {badges_html}
          </div>
        </div>
      {link_close}
    </div>
    """


def card_light(img_src: str, title: str, meta: str, href: str):
    return f"""
    <a href='{esc(href)}' target='_blank' rel='noopener' class='group block bg-white rounded-3xl overflow-hidden border border-slate-200 shadow-sm hover:shadow-lg transition'>
      <div class='aspect-[4/3] bg-slate-100 overflow-hidden'>
        <img src='{esc(img_src)}' alt='{esc(title)}' class='w-full h-full object-cover group-hover:scale-[1.02] transition duration-500' loading='lazy'>
      </div>
      <div class='p-6'>
        <h3 class='font-bold text-slate-900 leading-snug'>{esc(title)}</h3>
        <p class='text-sm text-slate-500 mt-1'>{esc(meta)}</p>
      </div>
    </a>
    """


def gallery_item(img_src: str, category: str):
    return f"""
    <button type='button' data-category='{esc(category)}' data-src='{esc(img_src)}'
      class='gallery-item group relative overflow-hidden rounded-2xl bg-slate-100 border border-slate-200 shadow-sm hover:shadow-lg transition'>
      <img src='{esc(img_src)}' alt='Gallery photo' loading='lazy'
        class='w-full h-full object-cover group-hover:scale-[1.03] transition duration-500'>
      <div class='absolute inset-0 bg-gradient-to-t from-black/55 via-black/0 to-transparent opacity-0 group-hover:opacity-100 transition'></div>
      <div class='absolute bottom-3 left-3 right-3 flex items-center justify-between text-white/90 opacity-0 group-hover:opacity-100 transition'>
        <span class='text-[11px] uppercase tracking-[0.2em]'>{esc(category)}</span>
        <span class='text-xs font-semibold'>View</span>
      </div>
    </button>
    """


# Dashboards (fixed list for best copy)
DASHBOARD_CARDS = [
    {
        'img': 'assets/projects/dashboards/executive-dashboard.jpg',
        'kicker': 'Executive Sales Dashboard',
        'title': 'Executive Sales & Margin Monitor',
        'desc': 'High-level view of sales, margin and product mix with drill-down by region, route and SKU.',
        'badges': ['Qlik Sense', 'Revenue Analytics'],
    },
    {
        'img': 'assets/projects/dashboards/transporters-dashboard.jpg',
        'kicker': 'Transporters Dashboard',
        'title': 'Logistics & Fleet Tracking',
        'desc': 'Delivery volume, pallet movement and cost distribution across transporters to improve efficiency.',
        'badges': ['Logistics', 'Cost Efficiency'],
    },
    {
        'img': 'assets/projects/dashboards/returns-dashboard.jpg',
        'kicker': 'Returns Dashboard',
        'title': 'Returns Reason Analysis',
        'desc': 'Breakdown of returns by reason, customer, route and preseller to reduce leakage and improve service.',
        'badges': ['Quality Control', 'CRM'],
    },
    {
        'img': 'assets/projects/dashboards/kpi-matrix.jpg',
        'kicker': 'KPI Matrix',
        'title': 'Customer Retention & Growth',
        'desc': 'Retention, churn and growth tracking by route and channel with actionable KPI framework.',
        'badges': ['KPI Framework', 'Strategy'],
    },
    {
        'img': 'assets/projects/dashboards/dsr-dashboard.jpg',
        'kicker': 'Daily Sales Report',
        'title': 'Daily Sales Performance (DSR)',
        'desc': 'Daily contribution by depot, route and top SKUs with fast operational insights.',
        'badges': ['DSR', 'Operations'],
    },
    {
        'img': 'assets/projects/dashboards/route-planning.jpg',
        'kicker': 'Route Planning',
        'title': 'Route Coverage & Optimization',
        'desc': 'Route design views to improve coverage, reduce distance and support planning decisions.',
        'badges': ['Route Planning', 'Optimization'],
    },
]


def build_dashboards():
    parts = []
    for c in DASHBOARD_CARDS:
        parts.append(card_dark(c['img'], c['kicker'], c['title'], c['desc'], c['badges'], href=c['img']))
    return "\n".join(parts)


def build_file_cards(section_dir: Path, thumbs_dir: Path, rel_files_prefix: str, rel_thumbs_prefix: str, kind_label: str, exts=None):
    # Build light cards for PDFs/DOCX/PPTX displayed as images
    files = list_files(section_dir, exts=exts)
    cards = []
    for f in files:
        title = clean_title(f.name)
        ext = f.suffix.upper().replace('.', '')
        thumb = thumbs_dir / (f.stem + '.jpg')
        # Fallback: if thumb missing, point to a neutral placeholder (we'll generate one later if needed)
        thumb_rel = f"{rel_thumbs_prefix}/{thumb.name}" if thumb.exists() else "assets/placeholder.jpg"
        href_rel = f"{rel_files_prefix}/{f.name}"
        cards.append(card_light(thumb_rel, title, f"{kind_label} • {ext}", href_rel))
    return "\n".join(cards)


def build_gallery():
    base = ROOT / 'assets' / 'gallery'
    items = []
    for cat in ['trips', 'people', 'moments']:
        cat_dir = base / cat
        for p in sorted(cat_dir.glob('*.jpeg')):
            rel = f"assets/gallery/{cat}/{p.name}"
            items.append(gallery_item(rel, cat))
    return "\n".join(items)


def main():
    # Ensure placeholder exists
    placeholder = ROOT / 'assets' / 'placeholder.jpg'
    if not placeholder.exists():
        # create simple placeholder using SVG -> jpg via imagemagick
        svg = ROOT / 'assets' / 'placeholder.svg'
        svg.write_text("""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='900'>
<defs>
<linearGradient id='g' x1='0' x2='1' y1='0' y2='1'>
  <stop offset='0' stop-color='#e2e8f0'/>
  <stop offset='1' stop-color='#f8fafc'/>
</linearGradient>
</defs>
<rect width='100%' height='100%' fill='url(#g)'/>
<rect x='60' y='60' width='1080' height='780' rx='48' fill='#ffffff' opacity='0.75' stroke='#cbd5e1'/>
<text x='600' y='470' text-anchor='middle' font-family='Plus Jakarta Sans, system-ui, -apple-system' font-size='48' fill='#334155'>Preview</text>
<text x='600' y='530' text-anchor='middle' font-family='Plus Jakarta Sans, system-ui, -apple-system' font-size='22' fill='#64748b'>File thumbnail</text>
</svg>""")
        import subprocess
        subprocess.run(['bash','-lc', f"magick {svg} -quality 85 {placeholder}"], check=False)
        try:
            svg.unlink()
        except Exception:
            pass

    dashboards_html = build_dashboards()

    cert_files = ROOT / 'assets' / 'certificates'
    cert_thumbs = cert_files / 'thumbs'
    certificates_html = build_file_cards(
        section_dir=cert_files,
        thumbs_dir=cert_thumbs,
        rel_files_prefix='assets/certificates',
        rel_thumbs_prefix='assets/certificates/thumbs',
        kind_label='Certificate',
        exts={'.jpg', '.jpeg', '.png'}
    )

    uni_files = ROOT / 'assets' / 'university' / 'files'
    uni_thumbs = ROOT / 'assets' / 'university' / 'thumbs'
    university_html = build_file_cards(
        section_dir=uni_files,
        thumbs_dir=uni_thumbs,
        rel_files_prefix='assets/university/files',
        rel_thumbs_prefix='assets/university/thumbs',
        kind_label='University Project'
    )

    tour_files = ROOT / 'assets' / 'tour' / 'files'
    tour_thumbs = ROOT / 'assets' / 'tour' / 'thumbs'
    tour_html = build_file_cards(
        section_dir=tour_files,
        thumbs_dir=tour_thumbs,
        rel_files_prefix='assets/tour/files',
        rel_thumbs_prefix='assets/tour/thumbs',
        kind_label='Work Sample'
    )

    gallery_html = build_gallery()

    # Template with placeholders
    template = r"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Abdulrahman Almansoori | Industrial Engineer & Analytics</title>
  <meta name="description" content="Industrial Engineer focused on Business Excellence, ERP/BI reporting and KPI dashboards. Turning raw operational data into decision-ready insights." />
  <meta property="og:title" content="Abdulrahman Almansoori | Industrial Engineer & Analytics" />
  <meta property="og:description" content="Business Excellence & Analytics (ERP/BI Reporting). Dashboards, automation and operational improvement." />
  <meta property="og:type" content="website" />

  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">

  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .glass-nav { background: rgba(255,255,255,0.78); backdrop-filter: blur(14px); border-bottom: 1px solid rgba(226, 232, 240, 1); }
    .gradient-text { background: linear-gradient(135deg, #1e40af, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .project-card { transition: all 0.32s cubic-bezier(0.4, 0, 0.2, 1); }
    .project-card:hover { transform: translateY(-8px); }
    .tab-btn[aria-selected="true"] { background: rgba(59,130,246,0.18); border-color: rgba(59,130,246,0.45); color: #bfdbfe; }
    /* Masonry-ish gallery */
    @media (min-width: 768px) { .gallery-grid { column-count: 3; column-gap: 1rem; } }
    @media (min-width: 1024px) { .gallery-grid { column-count: 4; } }
    .gallery-grid > * { break-inside: avoid; margin-bottom: 1rem; }
  </style>
</head>
<body class="bg-slate-50 text-slate-900 antialiased">

  <!-- Nav -->
  <nav class="fixed w-full z-50 glass-nav">
    <div class="max-w-7xl mx-auto px-6 h-20 flex justify-between items-center">
      <a href="#top" class="flex items-center gap-3">
        <img src="__PROFILE_AVATAR__" alt="Abdulrahman" class="w-10 h-10 rounded-xl object-cover border border-slate-200 shadow-sm" />
        <span class="text-xl font-extrabold tracking-tight">ALMANSOORI<span class="text-blue-600">.</span></span>
      </a>

      <div class="hidden md:flex items-center gap-10 text-xs font-semibold uppercase tracking-widest text-slate-500">
        <a href="#about" class="hover:text-blue-600 transition">About</a>
        <a href="#skills" class="hover:text-blue-600 transition">Skills</a>
        <a href="#experience" class="hover:text-blue-600 transition">Experience</a>
        <a href="#work" class="hover:text-blue-600 transition">Work</a>
        <a href="#gallery" class="hover:text-blue-600 transition">Gallery</a>
        <a href="#contact" class="hover:text-blue-600 transition">Contact</a>
      </div>

      <div class="flex items-center gap-3">
        <a href="__CV_PATH__" target="_blank" rel="noopener" class="hidden sm:inline-flex px-5 py-3 bg-slate-900 text-white rounded-xl font-bold hover:bg-slate-800 transition shadow-lg shadow-slate-200">
          Download CV
        </a>
        <button id="menuBtn" class="md:hidden inline-flex items-center justify-center w-11 h-11 rounded-xl border border-slate-200 bg-white/70 hover:bg-white transition" aria-label="Open menu">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <div id="mobileMenu" class="md:hidden hidden border-t border-slate-200 bg-white/90 backdrop-blur">
      <div class="max-w-7xl mx-auto px-6 py-4 grid grid-cols-2 gap-3 text-sm font-semibold text-slate-700">
        <a href="#about" class="py-2">About</a>
        <a href="#skills" class="py-2">Skills</a>
        <a href="#experience" class="py-2">Experience</a>
        <a href="#work" class="py-2">Work</a>
        <a href="#gallery" class="py-2">Gallery</a>
        <a href="#contact" class="py-2">Contact</a>
        <a href="__CV_PATH__" target="_blank" rel="noopener" class="col-span-2 mt-2 inline-flex justify-center px-5 py-3 bg-slate-900 text-white rounded-xl font-bold">Download CV</a>
      </div>
    </div>
  </nav>

  <!-- Hero -->
  <header id="top" class="pt-40 pb-24 px-6 bg-white relative overflow-hidden">
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute -top-24 -right-24 w-96 h-96 bg-blue-200/40 blur-3xl rounded-full"></div>
      <div class="absolute -bottom-28 -left-20 w-[34rem] h-[34rem] bg-indigo-200/40 blur-3xl rounded-full"></div>
    </div>

    <div class="max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-16 relative">
      <div class="flex-1 space-y-8 text-center lg:text-left">
        <div class="inline-flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-700 rounded-full text-sm font-bold tracking-wide uppercase">
          <span class="inline-block w-2 h-2 rounded-full bg-blue-600"></span>
          Industrial Engineer • Business Excellence • Analytics
        </div>

        <h1 class="text-5xl lg:text-7xl font-extrabold tracking-tight text-slate-900 leading-tight">
          Transforming data into <br><span class="gradient-text">Operational Excellence.</span>
        </h1>

        <p class="text-xl text-slate-600 max-w-2xl mx-auto lg:mx-0 leading-relaxed">
          I build executive-ready KPI dashboards and automate reporting pipelines (Excel/Power Query/Python) so teams can move faster, reduce leakage, and scale decisions with confidence.
        </p>

        <div class="flex flex-wrap justify-center lg:justify-start gap-4">
          <a href="__CV_PATH__" target="_blank" rel="noopener" class="px-10 py-4 bg-slate-900 text-white rounded-xl font-bold hover:bg-slate-800 transition-all shadow-xl shadow-slate-200">
            Download CV
          </a>
          <a href="#contact" class="px-10 py-4 border-2 border-slate-200 text-slate-900 rounded-xl font-bold hover:bg-slate-50 transition-all">
            Contact
          </a>
        </div>

        <div class="flex flex-wrap justify-center lg:justify-start gap-3 pt-2 text-sm text-slate-600">
          <span class="inline-flex items-center gap-2 px-3 py-2 bg-white border border-slate-200 rounded-xl">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Muscat, Oman
          </span>
          <a href="mailto:rahman.mansoori@hotmail.com" class="inline-flex items-center gap-2 px-3 py-2 bg-white border border-slate-200 rounded-xl hover:border-slate-300 transition">
            <span class="w-2 h-2 rounded-full bg-blue-500"></span> rahman.mansoori@hotmail.com
          </a>
          <a href="__LINKEDIN__" target="_blank" rel="noopener" class="inline-flex items-center gap-2 px-3 py-2 bg-white border border-slate-200 rounded-xl hover:border-slate-300 transition">
            <span class="w-2 h-2 rounded-full bg-indigo-500"></span> LinkedIn
          </a>
          <a href="__INSTAGRAM__" target="_blank" rel="noopener" class="inline-flex items-center gap-2 px-3 py-2 bg-white border border-slate-200 rounded-xl hover:border-slate-300 transition">
            <span class="w-2 h-2 rounded-full bg-pink-500"></span> Instagram
          </a>
        </div>
      </div>

      <div class="flex-1 relative">
        <div class="w-full max-w-md mx-auto aspect-square bg-slate-100 rounded-[3rem] overflow-hidden shadow-2xl rotate-2">
          <img src="__PROFILE_HERO__" alt="Abdulrahman Almansoori" class="w-full h-full object-cover -rotate-2 hover:rotate-0 transition duration-700" />
        </div>
        <div class="hidden lg:block absolute -bottom-10 -left-10 w-56 p-6 bg-white rounded-3xl shadow-xl border border-slate-100">
          <p class="text-xs uppercase tracking-[0.2em] text-slate-500 font-semibold">Current Focus</p>
          <p class="mt-2 font-bold">ERP/BI Reporting</p>
          <p class="text-sm text-slate-600 mt-1">KPI frameworks • Automation • Dashboards</p>
        </div>
      </div>
    </div>
  </header>

  <!-- About -->
  <section id="about" class="py-24 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="grid lg:grid-cols-2 gap-16 items-center">
        <div class="space-y-6">
          <h2 class="text-4xl font-bold tracking-tight">Bridging Engineering and Data</h2>
          <p class="text-lg text-slate-600 leading-relaxed">
            I’m an Industrial Engineering graduate (Honors, GPA 3.66) who works at the intersection of operations, data, and execution.
            I turn complex ERP outputs into clean, reliable KPIs and dashboards—then automate the workflow so reporting becomes a system, not a task.
          </p>
          <p class="text-lg text-slate-600 leading-relaxed">
            My edge is combining classic Industrial Engineering (process improvement, optimization, systems thinking) with hands-on analytics (Power Query, Python, BI) to deliver measurable business impact.
          </p>

          <div class="flex flex-wrap gap-3 pt-2">
            <span class="px-4 py-2 rounded-xl bg-white border border-slate-200 text-sm font-semibold">Business Excellence</span>
            <span class="px-4 py-2 rounded-xl bg-white border border-slate-200 text-sm font-semibold">ERP / Master Data</span>
            <span class="px-4 py-2 rounded-xl bg-white border border-slate-200 text-sm font-semibold">Automation</span>
            <span class="px-4 py-2 rounded-xl bg-white border border-slate-200 text-sm font-semibold">Dashboards</span>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-6">
          <div class="p-8 bg-white rounded-2xl shadow-sm border border-slate-100">
            <span class="text-3xl font-bold text-blue-600">3.66</span>
            <p class="text-slate-500 text-sm mt-2">GPA (Honors)</p>
          </div>
          <div class="p-8 bg-white rounded-2xl shadow-sm border border-slate-100">
            <span class="text-3xl font-bold text-blue-600">1st</span>
            <p class="text-slate-500 text-sm mt-2">Class Rank (IE)</p>
          </div>
          <div class="p-8 bg-white rounded-2xl shadow-sm border border-slate-100">
            <span class="text-3xl font-bold text-blue-600">20+</span>
            <p class="text-slate-500 text-sm mt-2">Dashboards Built</p>
          </div>
          <div class="p-8 bg-white rounded-2xl shadow-sm border border-slate-100">
            <span class="text-3xl font-bold text-blue-600">80+</span>
            <p class="text-slate-500 text-sm mt-2">Volunteers Led</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Skills -->
  <section id="skills" class="py-24 px-6 bg-white">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16 space-y-4">
        <h2 class="text-4xl lg:text-5xl font-bold">Skills Matrix</h2>
        <p class="text-slate-600 max-w-2xl mx-auto">Grouped capabilities that I use to deliver reporting, automation, and performance improvement.</p>
      </div>

      <div class="grid lg:grid-cols-4 gap-6">
        <div class="p-8 rounded-3xl border border-slate-200 bg-slate-50">
          <h3 class="font-bold text-slate-900">Analytics & Reporting</h3>
          <div class="flex flex-wrap gap-2 mt-4">
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">Advanced Excel</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">Power Query</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">KPI Design</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">Dashboards</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">Data Cleansing</span>
          </div>
        </div>

        <div class="p-8 rounded-3xl border border-slate-200 bg-slate-50">
          <h3 class="font-bold text-slate-900">Coding & Automation</h3>
          <div class="flex flex-wrap gap-2 mt-4">
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">Python (pandas)</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">openpyxl</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">HTML / JS (basic)</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">GitHub (familiar)</span>
          </div>
        </div>

        <div class="p-8 rounded-3xl border border-slate-200 bg-slate-50">
          <h3 class="font-bold text-slate-900">Industrial Engineering</h3>
          <div class="flex flex-wrap gap-2 mt-4">
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">Process Optimization</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">Operations Research</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">Supply Chain Design</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">Six Sigma</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">Quality Control</span>
          </div>
        </div>

        <div class="p-8 rounded-3xl border border-slate-200 bg-slate-50">
          <h3 class="font-bold text-slate-900">Tools & Platforms</h3>
          <div class="flex flex-wrap gap-2 mt-4">
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">Qlik Sense</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">Power BI (familiar)</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">Minitab</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">Arena Simulation</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">CPLEX OPL</span>
            <span class="px-3 py-2 text-sm rounded-xl bg-white border border-slate-200">MATLAB</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Experience -->
  <section id="experience" class="py-24 px-6">
    <div class="max-w-4xl mx-auto">
      <h2 class="text-4xl font-bold mb-16 text-center">Professional Experience</h2>

      <div class="space-y-12">
        <div class="flex gap-8 border-l-4 border-blue-600 pl-8 relative">
          <div class="absolute -left-[10px] top-0 w-4 h-4 rounded-full bg-blue-600"></div>
          <div>
            <span class="text-sm font-bold text-blue-600">2025 – Present</span>
            <h3 class="text-2xl font-bold mt-1">National Mineral Water Company (NMWC) — Oman</h3>
            <p class="text-slate-500 font-medium">Business Excellence & Analytics (ERP/BI Reporting)</p>
            <ul class="mt-4 space-y-2 text-slate-600 text-sm leading-relaxed">
              <li>• Built executive-ready dashboards (customer growth, returns, coverage tracking, incentives) for Sales and management.</li>
              <li>• Automated recurring reporting workflows (Excel / Power Query / Python) and standardized master-data rules.</li>
              <li>• Supported ERP reporting alignment via reconciliation checks, KPI definitions, and stakeholder coordination.</li>
            </ul>
          </div>
        </div>

        <div class="flex gap-8 border-l-4 border-slate-200 pl-8 relative">
          <div class="absolute -left-[10px] top-0 w-4 h-4 rounded-full bg-slate-200"></div>
          <div>
            <span class="text-sm font-bold text-slate-400">Mar 2024 – Present</span>
            <h3 class="text-2xl font-bold mt-1">Abdul Wahab Office — Muscat</h3>
            <p class="text-slate-500 font-medium">Salesperson</p>
            <ul class="mt-4 space-y-2 text-slate-600 text-sm leading-relaxed">
              <li>• Supported customers in a service/showroom environment and improved day-to-day operational accuracy.</li>
              <li>• Helped streamline inventory handling and process reliability.</li>
            </ul>
          </div>
        </div>

        <div class="flex gap-8 border-l-4 border-slate-200 pl-8 relative">
          <div class="absolute -left-[10px] top-0 w-4 h-4 rounded-full bg-slate-200"></div>
          <div>
            <span class="text-sm font-bold text-slate-400">Sep 2022 – Aug 2024</span>
            <h3 class="text-2xl font-bold mt-1">Sultan Qaboos University — International Cooperation Office</h3>
            <p class="text-slate-500 font-medium">Head of Volunteer Students</p>
            <ul class="mt-4 space-y-2 text-slate-600 text-sm leading-relaxed">
              <li>• Led volunteer teams delivering major international programs (Russian and Korean delegations, 80+ participants).</li>
              <li>• Coordinated logistics, schedules and communication across stakeholders to deliver high-quality experiences.</li>
            </ul>
          </div>
        </div>

        <div class="flex gap-8 border-l-4 border-slate-200 pl-8 relative">
          <div class="absolute -left-[10px] top-0 w-4 h-4 rounded-full bg-slate-200"></div>
          <div>
            <span class="text-sm font-bold text-slate-400">Jul 2023 – Aug 2023</span>
            <h3 class="text-2xl font-bold mt-1">Oman Refreshment Company</h3>
            <p class="text-slate-500 font-medium">Procurement Trainee</p>
            <ul class="mt-4 space-y-2 text-slate-600 text-sm leading-relaxed">
              <li>• Learned end-to-end procurement processes in a large beverage company environment.</li>
            </ul>
          </div>
        </div>

        <div class="p-8 bg-white rounded-3xl border border-slate-200">
          <h3 class="text-xl font-bold">Additional Experience</h3>
          <ul class="mt-4 grid md:grid-cols-2 gap-3 text-sm text-slate-600">
            <li class="flex items-start gap-2"><span class="mt-2 w-1.5 h-1.5 rounded-full bg-blue-600"></span><span><b>Tour Guide (Freelance)</b> — guided tourists across Oman, showcasing attractions and cultural heritage.</span></li>
            <li class="flex items-start gap-2"><span class="mt-2 w-1.5 h-1.5 rounded-full bg-blue-600"></span><span><b>Earthly Coffee</b> — Barista (customer service and quality standards).</span></li>
            <li class="flex items-start gap-2"><span class="mt-2 w-1.5 h-1.5 rounded-full bg-blue-600"></span><span><b>Tutorial Center</b> — IT & Math Tutor.</span></li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- Work -->
  <section id="work" class="py-24 px-6 bg-slate-900 text-white">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-12 space-y-4">
        <h2 class="text-4xl lg:text-5xl font-bold">Portfolio</h2>
        <p class="text-slate-300 max-w-2xl mx-auto">Dashboards, university projects, certificates, and work samples — presented exactly like a professional portfolio.</p>
      </div>

      <!-- Tabs -->
      <div class="flex flex-wrap justify-center gap-3 mb-12">
        <button class="tab-btn px-4 py-2 rounded-xl border border-slate-700 bg-slate-800/40 text-slate-200 text-sm font-semibold" data-tab="dashboards" aria-selected="true">Dashboards</button>
        <button class="tab-btn px-4 py-2 rounded-xl border border-slate-700 bg-slate-800/40 text-slate-200 text-sm font-semibold" data-tab="university" aria-selected="false">University Projects</button>
        <button class="tab-btn px-4 py-2 rounded-xl border border-slate-700 bg-slate-800/40 text-slate-200 text-sm font-semibold" data-tab="certificates" aria-selected="false">Certificates</button>
        <button class="tab-btn px-4 py-2 rounded-xl border border-slate-700 bg-slate-800/40 text-slate-200 text-sm font-semibold" data-tab="tour" aria-selected="false">Tour Guide Work</button>
      </div>

      <div id="tab-dashboards" class="tab-panel">
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          __DASHBOARD_CARDS__
        </div>
      </div>

      <div id="tab-university" class="tab-panel hidden">
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
          __UNIVERSITY_CARDS__
        </div>
      </div>

      <div id="tab-certificates" class="tab-panel hidden">
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
          __CERTIFICATE_CARDS__
        </div>
      </div>

      <div id="tab-tour" class="tab-panel hidden">
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
          __TOUR_CARDS__
        </div>
      </div>

    </div>
  </section>

  <!-- Gallery -->
  <section id="gallery" class="py-24 px-6 bg-white">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-12 space-y-4">
        <h2 class="text-4xl lg:text-5xl font-bold">Gallery</h2>
        <p class="text-slate-600 max-w-2xl mx-auto">Personal photography and moments — curated into a clean, professional gallery.</p>
      </div>

      <div class="flex flex-wrap justify-center gap-3 mb-10">
        <button class="gallery-filter px-4 py-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-700 text-sm font-semibold" data-filter="all">All</button>
        <button class="gallery-filter px-4 py-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-700 text-sm font-semibold" data-filter="trips">Trips</button>
        <button class="gallery-filter px-4 py-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-700 text-sm font-semibold" data-filter="people">People</button>
        <button class="gallery-filter px-4 py-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-700 text-sm font-semibold" data-filter="moments">Moments</button>
      </div>

      <div class="gallery-grid">
        __GALLERY_ITEMS__
      </div>

      <p class="text-center text-sm text-slate-500 mt-10">Tip: Click any photo to view it large.</p>
    </div>
  </section>

  <!-- Contact -->
  <footer id="contact" class="py-24 bg-slate-900 text-white">
    <div class="max-w-7xl mx-auto px-6">
      <div class="grid lg:grid-cols-2 gap-12 items-start">
        <div>
          <h2 class="text-4xl font-bold mb-4">Let’s Work Together</h2>
          <p class="text-slate-300 mb-8 max-w-xl">If you’re hiring or want help building KPI reporting, automation, or operational dashboards — send me a message.</p>

          <div class="grid sm:grid-cols-2 gap-6 mb-10">
            <div>
              <p class="text-slate-400 text-xs uppercase tracking-widest mb-2">Email</p>
              <a href="mailto:rahman.mansoori@hotmail.com" class="text-lg font-bold hover:text-blue-400 transition">rahman.mansoori@hotmail.com</a>
            </div>
            <div>
              <p class="text-slate-400 text-xs uppercase tracking-widest mb-2">Phone</p>
              <p class="text-lg font-bold">+968 7749 9715</p>
            </div>
            <div>
              <p class="text-slate-400 text-xs uppercase tracking-widest mb-2">Location</p>
              <p class="text-lg font-bold">Muscat, Oman</p>
            </div>
            <div>
              <p class="text-slate-400 text-xs uppercase tracking-widest mb-2">Social</p>
              <div class="flex gap-5 text-sm font-bold uppercase tracking-widest">
                <a href="__LINKEDIN__" target="_blank" rel="noopener" class="hover:text-blue-400 transition">LinkedIn</a>
                <a href="__INSTAGRAM__" target="_blank" rel="noopener" class="hover:text-blue-400 transition">Instagram</a>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-slate-800/60 border border-slate-700/70 rounded-3xl p-8">
          <h3 class="text-xl font-bold">Send a Message</h3>
          <p class="text-slate-300 text-sm mt-2">This form opens your email client with the message pre-filled.</p>

          <form id="contactForm" class="mt-6 grid gap-4">
            <div class="grid sm:grid-cols-2 gap-4">
              <input name="name" required placeholder="Your name" class="w-full px-4 py-3 rounded-xl bg-slate-900/50 border border-slate-700 text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
              <input name="email" required type="email" placeholder="Your email" class="w-full px-4 py-3 rounded-xl bg-slate-900/50 border border-slate-700 text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <input name="subject" placeholder="Subject" class="w-full px-4 py-3 rounded-xl bg-slate-900/50 border border-slate-700 text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            <textarea name="message" required rows="5" placeholder="Write your message..." class="w-full px-4 py-3 rounded-xl bg-slate-900/50 border border-slate-700 text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
            <button type="submit" class="mt-2 px-6 py-4 rounded-xl bg-blue-600 hover:bg-blue-500 font-bold transition">Send</button>
          </form>
        </div>
      </div>

      <div class="pt-12 mt-16 border-t border-slate-800 flex flex-col md:flex-row justify-between items-center gap-6">
        <p class="text-slate-500 text-sm">© 2026 Abdulrahman Almansoori.</p>
        <a href="#top" class="text-sm font-bold uppercase tracking-widest hover:text-blue-400 transition">Back to top</a>
      </div>
    </div>
  </footer>

  <!-- Lightbox -->
  <div id="lightbox" class="fixed inset-0 z-[100] hidden items-center justify-center bg-black/80 p-4">
    <button id="lightboxClose" class="absolute top-5 right-5 w-12 h-12 rounded-xl bg-white/10 hover:bg-white/20 border border-white/10 text-white flex items-center justify-center" aria-label="Close">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="6" x2="6" y2="18" />
        <line x1="6" y1="6" x2="18" y2="18" />
      </svg>
    </button>
    <img id="lightboxImg" src="" alt="Preview" class="max-h-[85vh] max-w-[95vw] rounded-2xl shadow-2xl" />
  </div>

  <script>
    // Mobile menu
    const menuBtn = document.getElementById('menuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    menuBtn?.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));
    mobileMenu?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => mobileMenu.classList.add('hidden')));

    // Tabs
    const tabButtons = Array.from(document.querySelectorAll('.tab-btn'));
    const panels = {
      dashboards: document.getElementById('tab-dashboards'),
      university: document.getElementById('tab-university'),
      certificates: document.getElementById('tab-certificates'),
      tour: document.getElementById('tab-tour'),
    };

    function setTab(key) {
      Object.values(panels).forEach(p => p?.classList.add('hidden'));
      panels[key]?.classList.remove('hidden');
      tabButtons.forEach(b => b.setAttribute('aria-selected', b.dataset.tab === key ? 'true' : 'false'));
    }

    tabButtons.forEach(b => b.addEventListener('click', () => setTab(b.dataset.tab)));

    // Contact form -> mailto
    const contactForm = document.getElementById('contactForm');
    contactForm?.addEventListener('submit', (e) => {
      e.preventDefault();
      const fd = new FormData(contactForm);
      const name = fd.get('name') || '';
      const email = fd.get('email') || '';
      const subject = fd.get('subject') || 'Portfolio Contact';
      const msg = fd.get('message') || '';
      const body = `Name: ${name}\nEmail: ${email}\n\n${msg}`;
      const url = `mailto:rahman.mansoori@hotmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      window.location.href = url;
    });

    // Lightbox
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightboxImg');
    const lightboxClose = document.getElementById('lightboxClose');

    function openLightbox(src) {
      lightboxImg.src = src;
      lightbox.classList.remove('hidden');
      lightbox.classList.add('flex');
      document.body.style.overflow = 'hidden';
    }
    function closeLightbox() {
      lightbox.classList.add('hidden');
      lightbox.classList.remove('flex');
      lightboxImg.src = '';
      document.body.style.overflow = '';
    }

    lightboxClose?.addEventListener('click', closeLightbox);
    lightbox?.addEventListener('click', (e) => { if (e.target === lightbox) closeLightbox(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeLightbox(); });

    // Gallery click
    document.querySelectorAll('.gallery-item').forEach(btn => {
      btn.addEventListener('click', () => openLightbox(btn.dataset.src));
    });

    // Gallery filters
    const filters = Array.from(document.querySelectorAll('.gallery-filter'));
    const galleryItems = Array.from(document.querySelectorAll('.gallery-item'));

    function setFilter(key) {
      filters.forEach(b => {
        const active = b.dataset.filter === key;
        b.classList.toggle('bg-slate-900', active);
        b.classList.toggle('text-white', active);
        b.classList.toggle('border-slate-900', active);
      });

      galleryItems.forEach(it => {
        const show = key === 'all' || it.dataset.category === key;
        it.style.display = show ? '' : 'none';
      });
    }

    filters.forEach(b => b.addEventListener('click', () => setFilter(b.dataset.filter)));
    setFilter('all');
  </script>
</body>
</html>
"""

    html_out = template
    html_out = html_out.replace('__PROFILE_HERO__', PROFILE_HERO)
    html_out = html_out.replace('__PROFILE_AVATAR__', PROFILE_AVATAR)
    html_out = html_out.replace('__CV_PATH__', CV_PATH)
    html_out = html_out.replace('__LINKEDIN__', LINKEDIN)
    html_out = html_out.replace('__INSTAGRAM__', INSTAGRAM)
    html_out = html_out.replace('__DASHBOARD_CARDS__', dashboards_html)
    html_out = html_out.replace('__UNIVERSITY_CARDS__', university_html)
    html_out = html_out.replace('__CERTIFICATE_CARDS__', certificates_html)
    html_out = html_out.replace('__TOUR_CARDS__', tour_html)
    html_out = html_out.replace('__GALLERY_ITEMS__', gallery_html)

    (ROOT / 'index.html').write_text(html_out, encoding='utf-8')


if __name__ == '__main__':
    main()
