from pathlib import Path
from html import escape
import json
import shutil

AGENT_LOGO_MASTER_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="420" viewBox="0 0 1600 420" role="img" aria-labelledby="title desc">\n  <title id="title">A-Gent Logo</title>\n  <desc id="desc">Stylized metallic gold A mark followed by cream -Gent wordmark on a transparent background.</desc>\n  <defs>\n    <linearGradient id="goldStroke" x1="0" y1="0" x2="1" y2="1">\n      <stop offset="0%" stop-color="#fffdf0"/>\n      <stop offset="14%" stop-color="#ffffff"/>\n      <stop offset="32%" stop-color="#ffe98e"/>\n      <stop offset="57%" stop-color="#d4af37"/>\n      <stop offset="82%" stop-color="#b68b20"/>\n      <stop offset="100%" stop-color="#7c5d12"/>\n    </linearGradient>\n    <linearGradient id="goldDeep" x1="0" y1="0" x2="1" y2="1">\n      <stop offset="0%" stop-color="#fff1a8"/>\n      <stop offset="28%" stop-color="#edcf63"/>\n      <stop offset="62%" stop-color="#d4af37"/>\n      <stop offset="100%" stop-color="#876916"/>\n    </linearGradient>\n    <linearGradient id="creamText" x1="0" y1="0" x2="0" y2="1">\n      <stop offset="0%" stop-color="#fffdf4"/>\n      <stop offset="62%" stop-color="#f1ead3"/>\n      <stop offset="100%" stop-color="#d8cfad"/>\n    </linearGradient>\n  </defs>\n\n  <g transform="translate(72 42)">\n    <!-- restrained glow, built as translucent vector strokes to stay crisp on dark backgrounds -->\n    <path d="M42 274 L189 74" fill="none" stroke="#d4af37" stroke-width="52" stroke-linecap="round" stroke-linejoin="round" opacity="0.16"/>\n    <path d="M188 74 L286 277" fill="none" stroke="#d4af37" stroke-width="52" stroke-linecap="round" stroke-linejoin="round" opacity="0.16"/>\n    <path d="M121 187 L244 158" fill="none" stroke="#d4af37" stroke-width="43" stroke-linecap="round" stroke-linejoin="round" opacity="0.14"/>\n\n    <!-- metallic angular A / check-arrow mark -->\n    <path d="M42 274 L189 74" fill="none" stroke="url(#goldStroke)" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/>\n    <path d="M188 74 L286 277" fill="none" stroke="url(#goldDeep)" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/>\n    <path d="M121 187 L244 158" fill="none" stroke="url(#goldStroke)" stroke-width="27" stroke-linecap="round" stroke-linejoin="round"/>\n\n    <!-- specular highlights matching the reference’s white-to-gold upper glint -->\n    <path d="M55 258 L177 91" fill="none" stroke="#ffffff" stroke-width="8" stroke-linecap="round" opacity="0.86"/>\n    <path d="M204 97 L261 216" fill="none" stroke="#fff0a6" stroke-width="7" stroke-linecap="round" opacity="0.58"/>\n  </g>\n\n  <text x="350" y="250" font-family="DejaVu Sans, Arial Rounded MT Bold, Avenir Next, Nunito Sans, Inter, Helvetica Neue, Arial, sans-serif" font-size="142" font-weight="800" letter-spacing="-4" fill="#f6efd8">-Gent</text>\n</svg>'

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'deploy'
SITE = 'https://a-gent.co'
FLEET = 'https://fleet.a-gent.co/'
FLEET_LOGIN = 'https://fleet.a-gent.co/login'
FLEET_PRICING = 'https://fleet.a-gent.co/pricing'
LASTMOD = '2026-06-13'

platform_pages = [
    ('find-and-research', 'Find & Research', 'Fleet identifies qualified accounts and enriches them with credible evidence before a human ever opens a spreadsheet.', 'Prospect discovery, enrichment, signal capture, and account fit scoring become one governed workflow inside A-Gent Fleet.'),
    ('real-time-company-lead-database', 'Real-Time Company & Lead Database', 'A living account graph keeps company, contact, role, and activity data organized for outbound execution.', 'Fleet turns scattered lead data into a structured, reviewable revenue workspace.'),
    ('ai-prospecting', 'Autonomous Prospecting', 'AI SDR agents source, score, and prioritize accounts using ICP rules and current-market signals.', 'The system helps lean B2B SaaS teams focus on best-fit accounts instead of manually building lists.'),
    ('lead-qualification', 'Lead Qualification', 'Qualification logic filters accounts by fit, urgency, relevance, and reachable decision-maker context.', 'Fleet keeps outbound focused on prospects that match the offer and deserve human attention.'),
    ('signal-trigger-detection', 'Signal Trigger Detection', 'Fleet watches for useful buying signals so outreach is anchored in timely, specific context.', 'Signals can include hiring, funding, product launches, market moves, role changes, and other revenue triggers.'),
    ('deep-account-research', 'Deep Account Research', 'Account briefs convert public evidence into concise talking points, pains, and hypotheses.', 'Revenue teams get strategic context without spending hours researching each target.'),
    ('ai-personalization', 'AI Personalization', 'Every message can pull from account evidence, offer context, proof points, and ICP-specific pain.', 'Fleet supports personalization that reads like research, not mail-merge decoration.'),
    ('engage-and-convert', 'Engage & Convert', 'Sequences move from research to relevant outreach, review, reply handling, and next-step routing.', 'The platform supports the workflow between first signal and booked conversation.'),
    ('multi-step-email-sequences', 'Multi-Step Email Sequences', 'Build governed outbound sequences that maintain message quality across multiple touches.', 'Fleet helps teams ship consistent outreach while preserving approval control and brand standards.'),
    ('gap-selling-messaging', 'GAP Selling Messaging', 'Messaging connects current-state pain, desired future state, and the measurable cost of inaction.', 'A-Gent uses the mechanism to make AI-generated outreach more business-relevant and less generic.'),
    ('smart-replies', 'Smart Replies', 'Inbound replies can be classified, summarized, and routed into the right next action.', 'Fleet helps teams respond faster while keeping human judgment in the loop.'),
    ('review-queue', 'Review Queue', 'Human-in-the-loop approval lets teams approve, edit, or reject generated outreach before it is sent.', 'Fleet gives operators control over quality, compliance, and customer-facing tone.'),
    ('inbound-reply-handling', 'Inbound Reply Handling', 'Replies are organized by intent so positive interest, objections, referrals, and opt-outs are easy to manage.', 'The workflow helps teams avoid missed opportunities after the first campaign touch.'),
    ('intelligent-lead-routing', 'Intelligent Lead Routing', 'Qualified responses can be routed to the right owner, queue, or next action based on rules.', 'Fleet keeps promising conversations from getting buried in inboxes or spreadsheets.'),
    ('measure-and-scale', 'Measure & Scale', 'Dashboards track campaign performance, message quality, reviews, replies, and pipeline movement.', 'The operating layer gives founders and revenue leaders a clearer view of what is working.'),
    ('mission-control-dashboard', 'Fleet Operating Dashboard', 'A retained route for the platform operations dashboard, now framed as a Fleet capability rather than a separate public product.', 'Use it to understand campaign status, account movement, review velocity, and team-level execution.'),
    ('deliverability-mailbox-health', 'Deliverability & Mailbox Health', 'Protect sender reputation with safer pacing, mailbox-health workflows, and quality controls.', 'Fleet treats deliverability as an operating requirement, not an afterthought.'),
    ('social-media-scheduling', 'Social Signal Scheduling', 'Coordinate outbound with social touches, content prompts, and campaign moments where appropriate.', 'The platform supports broader revenue motion without turning the public site into a list of internal tools.'),
    ('crm-integration', 'CRM Workflow Integration', 'Keep customer-system updates aligned with outreach, replies, ownership, and next-step status.', 'Fleet can connect with a company’s CRM workflow without advertising A-Gent’s internal operating tools.'),
    ('supabase-backend', 'Secure Data Foundation', 'The platform is built around structured data, tenant isolation, and secure operational workflows.', 'A-Gent Fleet is designed for multi-tenant execution and governed customer data handling.'),
    ('multi-tenant-scaling', 'Multi-Tenant Scaling', 'Each organization gets isolated workflows, role-aware access, and scalable outbound operations.', 'Fleet is designed to grow from focused teams to more complex revenue organizations.'),
]

core_routes = ['/', '/platform', '/platform/loop-engine', '/consulting', '/fleet', '/signup', '/assessment', '/privacy', '/blog']
all_routes = core_routes + [f'/platform/{slug}' for slug, *_ in platform_pages]

CSS = r'''
:root {
  --bg: #030404;
  --bg-2: #060707;
  --surface: #101010;
  --surface-2: #151515;
  --surface-3: #1b1b1b;
  --line: rgba(255,255,255,.10);
  --line-strong: rgba(212,175,55,.38);
  --gold: #d4af37;
  --gold-soft: rgba(212,175,55,.12);
  --gold-mid: rgba(212,175,55,.24);
  --green: #00ff88;
  --green-soft: rgba(0,255,136,.10);
  --text: #f4f4f2;
  --muted: #a2a2a0;
  --dim: #70706d;
  --danger: #ff5c7a;
  --max: 1180px;
  --radius: 14px;
  --shadow: 0 24px 80px rgba(0,0,0,.48);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; background: var(--bg); }
body {
  margin: 0;
  color: var(--text);
  background:
    radial-gradient(circle at 16% 12%, rgba(212,175,55,.11), transparent 28rem),
    radial-gradient(circle at 88% 8%, rgba(0,255,136,.07), transparent 24rem),
    linear-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px),
    var(--bg);
  background-size: auto, auto, 96px 96px, 96px 96px, auto;
  font-family: 'IBM Plex Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  line-height: 1.65;
  overflow-x: hidden;
}
a { color: inherit; text-decoration: none; }
p { color: var(--muted); margin: 0 0 1rem; }
strong { color: var(--text); }
img { max-width: 100%; height: auto; display: block; }
::selection { background: rgba(212,175,55,.35); color: var(--text); }
.site-shell { min-height: 100vh; display: flex; flex-direction: column; }
.container { width: min(var(--max), calc(100% - 2rem)); margin: 0 auto; }
.nav {
  position: sticky;
  top: 0;
  z-index: 50;
  border-bottom: 1px solid var(--line);
  background: rgba(3,4,4,.88);
  backdrop-filter: blur(16px);
}
.nav-inner { height: 58px; display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.wordmark {
  color: var(--gold);
  font-family: 'Orbitron', sans-serif;
  font-weight: 800;
  letter-spacing: .18em;
  font-size: 1rem;
  text-shadow: 0 0 16px rgba(212,175,55,.34);
}
.nav-links { display: flex; align-items: center; gap: .32rem; }
.nav-link, .launch-link {
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  min-height: 34px;
  padding: .48rem .82rem;
  border: 1px solid transparent;
  border-radius: 7px;
  color: #deded9;
  font-family: 'Rajdhani', 'IBM Plex Mono', monospace;
  font-size: .86rem;
  font-weight: 600;
  letter-spacing: .11em;
  text-transform: uppercase;
  transition: color .18s ease, border-color .18s ease, background .18s ease, box-shadow .18s ease;
}
.nav-link::before, .launch-link::before {
  content: '';
  width: 5px;
  height: 5px;
  border-radius: 999px;
  background: var(--green);
  box-shadow: 0 0 6px var(--green);
}
.nav-link:hover { color: var(--gold); border-color: rgba(212,175,55,.25); background: rgba(212,175,55,.045); }
.launch-link { color: var(--gold); border-color: rgba(212,175,55,.42); box-shadow: 0 0 11px rgba(212,175,55,.22); }
.launch-link:hover { background: rgba(212,175,55,.10); box-shadow: 0 0 18px rgba(212,175,55,.34); }
.mobile-nav { display: none; }
.hero { position: relative; padding: 7.8rem 0 5.2rem; border-bottom: 1px solid var(--line); overflow: hidden; }
.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(90deg, rgba(3,4,4,.82), rgba(3,4,4,.38) 48%, rgba(3,4,4,.9));
}
.hero-grid { position: relative; z-index: 1; display: grid; grid-template-columns: minmax(0, 1.08fr) minmax(320px, .72fr); gap: 3.2rem; align-items: center; }
.status-pill, .eyebrow {
  display: inline-flex;
  align-items: center;
  gap: .45rem;
  width: max-content;
  color: var(--green);
  border: 1px solid rgba(0,255,136,.25);
  background: rgba(0,255,136,.07);
  border-radius: 999px;
  padding: .28rem .64rem;
  font-family: 'Rajdhani', 'IBM Plex Mono', monospace;
  font-weight: 700;
  letter-spacing: .11em;
  text-transform: uppercase;
  font-size: .74rem;
}
.status-pill::before { content: ''; width: 6px; height: 6px; border-radius: 999px; background: var(--green); box-shadow: 0 0 8px var(--green); }
.eyebrow { color: var(--gold); border-color: rgba(212,175,55,.26); background: rgba(212,175,55,.06); }
.eyebrow::before { content: ''; width: 6px; height: 6px; border-radius: 999px; background: var(--gold); box-shadow: 0 0 8px var(--gold); }
h1, h2, .display {
  font-family: 'Orbitron', 'Rajdhani', sans-serif;
  line-height: 1.05;
  letter-spacing: -.045em;
  margin: 0;
}
h1 { margin: 1.25rem 0 1.25rem; font-size: clamp(2.9rem, 7vw, 5.9rem); font-weight: 800; }
h2 { font-size: clamp(2rem, 4vw, 3.15rem); font-weight: 800; }
h3 { margin: 0 0 .55rem; color: var(--text); font-family: 'Rajdhani', 'IBM Plex Mono', monospace; font-size: 1.18rem; letter-spacing: .02em; }
.gold { color: var(--gold); text-shadow: 0 0 28px rgba(212,175,55,.24); }
.lede { color: #b6b6b3; max-width: 690px; font-size: clamp(1rem, 1.8vw, 1.18rem); line-height: 1.75; }
.cta-row { display: flex; flex-wrap: wrap; gap: .75rem; margin-top: 2rem; }
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: .6rem;
  min-height: 44px;
  padding: .82rem 1.08rem;
  border-radius: 7px;
  border: 1px solid transparent;
  font-family: 'Rajdhani', 'IBM Plex Mono', monospace;
  font-weight: 700;
  letter-spacing: .065em;
  text-transform: uppercase;
  font-size: .9rem;
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease, background .18s ease;
}
.btn:hover { transform: translateY(-1px); }
.btn-primary { background: var(--gold); color: #050505; box-shadow: 0 0 20px rgba(212,175,55,.24); }
.btn-primary:hover { box-shadow: 0 0 30px rgba(212,175,55,.34); }
.assessment-primary { min-height:50px; padding-inline:1.28rem; box-shadow:0 0 26px rgba(212,175,55,.34), 0 0 18px rgba(0,255,136,.10); }
.assessment-primary::after { content:'↗'; font-size:.78em; opacity:.82; }
.btn-secondary { color: var(--gold); border-color: rgba(212,175,55,.38); background: rgba(212,175,55,.035); }
.btn-secondary:hover { background: rgba(212,175,55,.09); border-color: rgba(212,175,55,.58); }
.console-card, .card, .plan-card, .feature-card {
  position: relative;
  background: linear-gradient(180deg, rgba(22,22,22,.94), rgba(12,12,12,.96));
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}
.console-card { padding: 1.15rem; overflow: hidden; }

.wordmark img { display:block; width:auto; height:clamp(34px,4.2vw,49px); max-width:238px; object-fit:contain; filter:drop-shadow(0 0 7px rgba(212,175,55,.28)); }
.hero-motion-card { min-height: 438px; border-color: rgba(212,175,55,.36); background: radial-gradient(circle at 22% 18%, rgba(0,255,136,.16), transparent 35%), radial-gradient(circle at 86% 72%, rgba(212,175,55,.12), transparent 36%), linear-gradient(180deg, rgba(17,17,17,.96), rgba(5,6,6,.98)); }
.sdr-motion { --sdr-cycle: 8s; position:relative; min-height:400px; display:grid; gap:.82rem; overflow:hidden; }
.sdr-motion::before { content:''; position:absolute; inset:-34% -28%; background:linear-gradient(110deg, transparent 0 32%, rgba(0,255,136,.12) 39%, rgba(0,255,136,.28) 45%, rgba(212,175,55,.34) 50%, rgba(212,175,55,.16) 55%, transparent 66% 100%); transform:translateX(-62%); animation:sdrSweep var(--sdr-cycle) linear infinite; pointer-events:none; mix-blend-mode:screen; opacity:.95; }
.sdr-motion::after { content:''; position:absolute; inset:0; pointer-events:none; background:radial-gradient(circle at 50% 50%, rgba(212,175,55,.10), transparent 58%); opacity:.42; animation:sdrAmbient var(--sdr-cycle) ease-in-out infinite; }
.sdr-topbar { position:relative; z-index:1; display:flex; justify-content:space-between; gap:1rem; align-items:center; padding-bottom:.8rem; border-bottom:1px solid var(--line); }
.sdr-title { font-family:'Orbitron',sans-serif; color:var(--text); letter-spacing:.08em; text-transform:uppercase; font-size:.9rem; }
.sdr-live { color:var(--green); border:1px solid rgba(0,255,136,.42); background:rgba(0,255,136,.10); border-radius:999px; padding:.22rem .5rem; font-size:.64rem; letter-spacing:.11em; text-transform:uppercase; box-shadow:0 0 14px rgba(0,255,136,.16); }
.sdr-stage { position:relative; z-index:1; display:grid; grid-template-columns:42px 1fr; gap:.75rem; align-items:start; padding:.82rem .95rem .82rem .82rem; border:1px solid rgba(255,255,255,.09); border-radius:12px; background:rgba(255,255,255,.026); opacity:.52; transform:translateX(0) translateY(0) scale(.982); transition:filter .2s ease; animation:sdrStage var(--sdr-cycle) cubic-bezier(.4,0,.2,1) infinite; will-change:transform,opacity,box-shadow,background,border-color; }
.sdr-stage::before { content:''; position:absolute; inset:-1px; border-radius:inherit; background:linear-gradient(135deg, rgba(212,175,55,.0), rgba(0,255,136,.0)); opacity:0; animation:sdrStageGlow var(--sdr-cycle) ease-in-out infinite; pointer-events:none; }
.sdr-stage::after { content:'•••'; position:absolute; top:.58rem; right:.72rem; color:var(--green); font-family:'IBM Plex Mono',monospace; font-size:.82rem; letter-spacing:.08em; opacity:0; filter:drop-shadow(0 0 8px rgba(0,255,136,.65)); animation:sdrDots var(--sdr-cycle) steps(4,end) infinite; }
.sdr-stage:nth-of-type(2), .sdr-stage:nth-of-type(2)::before, .sdr-stage:nth-of-type(2)::after { animation-delay:0s; }
.sdr-stage:nth-of-type(3), .sdr-stage:nth-of-type(3)::before, .sdr-stage:nth-of-type(3)::after { animation-delay:2s; }
.sdr-stage:nth-of-type(4), .sdr-stage:nth-of-type(4)::before, .sdr-stage:nth-of-type(4)::after { animation-delay:4s; }
.sdr-stage:nth-of-type(5), .sdr-stage:nth-of-type(5)::before, .sdr-stage:nth-of-type(5)::after { animation-delay:6s; }
.sdr-icon { width:42px; height:42px; display:grid; place-items:center; border-radius:10px; border:1px solid rgba(212,175,55,.32); color:var(--gold); background:rgba(212,175,55,.08); font-family:'Orbitron',sans-serif; font-size:.72rem; box-shadow:0 0 16px rgba(212,175,55,.11); }
.sdr-copy strong { display:block; color:#f4f4f2; font-family:'Rajdhani',monospace; font-size:1.02rem; letter-spacing:.03em; }
.sdr-copy span { display:block; color:#9d9d99; font-size:.78rem; line-height:1.45; margin-top:.18rem; }
.sdr-pipeline { position:relative; z-index:1; height:14px; border:1px solid rgba(212,175,55,.32); border-radius:999px; background:rgba(255,255,255,.055); overflow:hidden; margin-top:.35rem; box-shadow:inset 0 0 12px rgba(0,0,0,.38); }
.sdr-bar { height:100%; width:100%; border-radius:999px; background:linear-gradient(90deg,var(--gold) 0%, #ffe083 32%, var(--green) 100%); transform-origin:left center; animation:sdrProgress var(--sdr-cycle) cubic-bezier(.3,0,.2,1) infinite; box-shadow:0 0 20px rgba(0,255,136,.34), 0 0 12px rgba(212,175,55,.20); }
.demo-modal { position:fixed; inset:0; z-index:1000; display:none; place-items:center; padding:1rem; background:rgba(0,0,0,.72); backdrop-filter:blur(10px); }
.demo-modal[aria-hidden="false"] { display:grid; }
.demo-dialog { width:min(720px,100%); border:1px solid rgba(212,175,55,.34); border-radius:18px; background:linear-gradient(180deg,rgba(18,18,18,.98),rgba(6,7,7,.98)); box-shadow:0 30px 100px rgba(0,0,0,.65); padding:1.35rem; }
.demo-head { display:flex; justify-content:space-between; gap:1rem; align-items:flex-start; margin-bottom:1rem; }
.demo-head h2 { font-size:clamp(1.55rem,3vw,2.15rem); margin:.35rem 0 .45rem; }
.demo-close { width:38px; height:38px; border-radius:999px; border:1px solid rgba(212,175,55,.35); background:rgba(212,175,55,.06); color:var(--gold); font:700 1.4rem/1 'IBM Plex Mono',monospace; cursor:pointer; }
.form-message { margin-top:.7rem; color:var(--muted); font-size:.82rem; }
.form-message.success { color:var(--green); }
.form-message.error { color:var(--danger); }
@keyframes sdrSweep { 0% { transform:translateX(-68%); opacity:.42; } 42% { opacity:.98; } 100% { transform:translateX(68%); opacity:.54; } }
@keyframes sdrAmbient { 0%,100% { transform:scale(.98); opacity:.28; } 50% { transform:scale(1.04); opacity:.54; } }
@keyframes sdrStage { 0%,24% { opacity:1; transform:translateX(8px) translateY(-4px) scale(1.035); border-color:rgba(212,175,55,.72); background:linear-gradient(90deg,rgba(212,175,55,.18),rgba(0,255,136,.105)); box-shadow:0 0 0 1px rgba(212,175,55,.14), 0 0 34px rgba(212,175,55,.23), 0 0 28px rgba(0,255,136,.16); } 30%,100% { opacity:.48; transform:translateX(0) translateY(0) scale(.982); border-color:rgba(255,255,255,.09); background:rgba(255,255,255,.026); box-shadow:none; } }
@keyframes sdrStageGlow { 0%,24% { opacity:1; background:linear-gradient(135deg, rgba(212,175,55,.22), rgba(0,255,136,.13)); } 30%,100% { opacity:0; background:linear-gradient(135deg, rgba(212,175,55,0), rgba(0,255,136,0)); } }
@keyframes sdrDots { 0% { opacity:1; content:'•'; } 8% { content:'••'; } 16%,24% { opacity:1; content:'•••'; } 30%,100% { opacity:0; content:'•••'; } }
@keyframes sdrProgress { 0% { transform:scaleX(.035); } 12% { transform:scaleX(.22); } 25% { transform:scaleX(.36); } 37% { transform:scaleX(.49); } 50% { transform:scaleX(.63); } 62% { transform:scaleX(.76); } 75% { transform:scaleX(.90); } 92%,100% { transform:scaleX(1); } }
@media (prefers-reduced-motion: reduce) { .sdr-motion::before, .sdr-motion::after, .sdr-stage, .sdr-stage::before, .sdr-stage::after, .sdr-bar { animation:none !important; } .sdr-motion::before { opacity:.18; transform:translateX(0); } .sdr-stage { opacity:.72; transform:none; } .sdr-stage:nth-of-type(2) { opacity:1; border-color:rgba(212,175,55,.55); background:linear-gradient(90deg,rgba(212,175,55,.14),rgba(0,255,136,.08)); box-shadow:0 0 22px rgba(212,175,55,.16); } .sdr-bar { transform:scaleX(.72); } }
.console-card::before, .feature-card::before, .plan-card::before {
  content: '';
  position: absolute;
  inset: 0 auto auto 0;
  width: 18px;
  height: 18px;
  border-top: 2px solid rgba(255,255,255,.72);
  border-left: 2px solid rgba(255,255,255,.72);
  border-top-left-radius: var(--radius);
  opacity: .75;
}
.console-top { display: flex; justify-content: space-between; gap: 1rem; align-items: center; padding-bottom: 1rem; border-bottom: 1px solid var(--line); }
.console-kicker { color: var(--gold); font-size: .72rem; letter-spacing: .16em; text-transform: uppercase; }
.console-title { font-family: 'Orbitron', sans-serif; font-size: 1.25rem; margin-top: .25rem; }
.metric-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .75rem; margin-top: 1rem; }
.metric { padding: .85rem; border: 1px solid rgba(212,175,55,.16); border-radius: 10px; background: rgba(212,175,55,.045); }
.metric strong { display: block; color: var(--gold); font-size: 1.4rem; line-height: 1; }
.metric span { display: block; margin-top: .3rem; color: var(--dim); font-size: .66rem; letter-spacing: .08em; text-transform: uppercase; }
.section { padding: 5.2rem 0; border-bottom: 1px solid rgba(255,255,255,.07); }
.section-header { text-align: center; max-width: 780px; margin: 0 auto 2.8rem; }
.section-header .eyebrow { margin: 0 auto .9rem; }
.section-header p { margin: 1rem auto 0; max-width: 690px; }
.grid-2 { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 1rem; }
.grid-3 { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 1rem; }
.grid-4 { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 1rem; }
.card, .feature-card, .plan-card { padding: 1.45rem; }
.card.featured, .plan-card.featured { border-color: rgba(212,175,55,.52); box-shadow: 0 0 0 1px rgba(212,175,55,.08), 0 0 34px rgba(212,175,55,.16), var(--shadow); }
.icon-box { width: 38px; height: 38px; display: grid; place-items: center; margin-bottom: 1rem; border: 1px solid rgba(212,175,55,.22); border-radius: 8px; color: var(--gold); background: rgba(212,175,55,.10); }
.card p, .feature-card p, .plan-card p { font-size: .92rem; color: #a9a9a6; }
.card ul, .plan-card ul { list-style: none; padding: 0; margin: 1rem 0 0; display: grid; gap: .55rem; }
.card li, .plan-card li { color: var(--muted); font-size: .9rem; }
.card li::before, .plan-card li::before { content: '✓'; color: var(--gold); margin-right: .55rem; }
.offer-label { color: var(--gold); font-size: .7rem; letter-spacing: .16em; text-transform: uppercase; margin-bottom: .55rem; }
.split { display: grid; grid-template-columns: .9fr 1.1fr; gap: 2rem; align-items: start; }
.copy-block { max-width: 760px; }
.copy-block h1 { font-size: clamp(2.4rem, 5vw, 4.3rem); }
.copy-block p { font-size: 1rem; }
.price { margin: .8rem 0 .2rem; font-family: 'Orbitron', sans-serif; font-size: 2.1rem; color: var(--text); }
.price small { font-family: 'IBM Plex Mono', monospace; font-size: .82rem; color: var(--dim); }
.footer { padding: 3rem 0; color: var(--dim); }
.footer-grid { display: flex; align-items: flex-start; justify-content: space-between; gap: 1.5rem; border-top: 1px solid var(--line); padding-top: 1.6rem; }
.footer-links { display: flex; flex-wrap: wrap; gap: 1rem; }
.footer a { color: var(--muted); font-size: .86rem; }
.footer a:hover { color: var(--gold); }
.form-panel { max-width: 760px; margin: 0 auto; }
.form-grid { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: .85rem; }
.field { display: grid; gap: .35rem; }
.field.wide { grid-column: 1 / -1; }
label { color: var(--dim); font-size: .72rem; letter-spacing: .11em; text-transform: uppercase; }
input, textarea, select { width: 100%; min-height: 44px; border: 1px solid rgba(255,255,255,.12); border-radius: 8px; background: rgba(255,255,255,.035); color: var(--text); padding: .75rem .85rem; font: inherit; }
textarea { min-height: 120px; resize: vertical; }
input:focus, textarea:focus, select:focus { outline: none; border-color: rgba(212,175,55,.6); box-shadow: 0 0 0 3px rgba(212,175,55,.09); }
.notice { border: 1px solid rgba(0,255,136,.18); color: #c8d4c2; background: rgba(0,255,136,.045); padding: 1rem; border-radius: 12px; }
.assessment-shell { max-width: 920px; margin: 0 auto; display:grid; gap:1rem; }
.assessment-progress { height: 10px; border-radius: 999px; background: rgba(255,255,255,.07); overflow:hidden; border:1px solid rgba(255,255,255,.09); }
.assessment-progress span { display:block; height:100%; width:20%; border-radius:999px; background:linear-gradient(90deg,var(--gold),var(--green)); box-shadow:0 0 18px rgba(212,175,55,.28); transition:width .28s ease; }
.assessment-step { display:none; }
.assessment-step.is-active { display:block; }
.assessment-options { display:grid; gap:.72rem; margin:1.2rem 0; }
.assessment-option { display:flex; align-items:flex-start; gap:.72rem; padding:.92rem 1rem; border:1px solid rgba(255,255,255,.11); border-radius:12px; background:rgba(255,255,255,.035); cursor:pointer; transition:border-color .18s ease, background .18s ease, transform .18s ease; }
.assessment-option:hover { border-color:rgba(212,175,55,.5); background:rgba(212,175,55,.07); transform:translateY(-1px); }
.assessment-option input { width:auto; min-height:auto; margin-top:.2rem; accent-color:#d4af37; }
.assessment-option strong { display:block; color:var(--text); font-size:.96rem; }
.assessment-option span { display:block; color:var(--muted); font-size:.86rem; margin-top:.16rem; }
.assessment-actions { display:flex; justify-content:space-between; gap:.75rem; flex-wrap:wrap; margin-top:1.15rem; }
.assessment-result { display:none; }
.assessment-result.is-active { display:block; }
.assessment-score { font-family:'Orbitron',sans-serif; color:var(--gold); font-size:clamp(2rem,5vw,3.4rem); margin:.6rem 0; }
.assessment-pill-row { display:flex; flex-wrap:wrap; gap:.55rem; margin-top:1rem; }
.assessment-pill-row span { border:1px solid rgba(212,175,55,.22); background:rgba(212,175,55,.08); color:#e9ddb4; border-radius:999px; padding:.45rem .7rem; font-size:.78rem; letter-spacing:.05em; text-transform:uppercase; }
.faq { display: grid; gap: .75rem; max-width: 900px; margin: 0 auto; }
details { border: 1px solid var(--line); border-radius: 12px; padding: 1rem; background: rgba(255,255,255,.025); }
summary { cursor: pointer; color: var(--text); font-family: 'Rajdhani', monospace; font-weight: 700; font-size: 1.05rem; }
details p { margin-top: .8rem; }
@media (max-width: 920px) {
  .hero-grid, .grid-2, .grid-3, .grid-4, .split { grid-template-columns: 1fr; }
  .hero { padding-top: 5.5rem; }
  .console-card { max-width: 620px; }
}
@media (max-width: 760px) {
  .nav-inner { height: auto; min-height: 58px; flex-wrap: wrap; padding: .65rem 0; }
  .nav-links { width: 100%; display: grid; grid-template-columns: 1fr; gap: .45rem; }
  .nav-link, .launch-link { justify-content: center; }
  .wordmark img { height:36px; max-width:192px; }
  h1 { font-size: clamp(2.35rem, 14vw, 3.6rem); }
  .section { padding: 4rem 0; }
  .form-grid { grid-template-columns: 1fr; }
  .field.wide { grid-column: auto; }
  .footer-grid { flex-direction: column; }
}
'''


def org_schema():
    return {
        '@context': 'https://schema.org',
        '@type': 'Organization',
        'name': 'A-Gent',
        'url': SITE,
        'description': 'A-Gent builds A-Gent Fleet, an AI SDR platform for B2B SaaS teams, and provides AI consulting for bespoke revenue automation systems.',
        'email': 'mark.cope.roarr@gmail.com',
        'sameAs': [FLEET]
    }


def service_schema(name, url, description):
    return {
        '@context': 'https://schema.org',
        '@type': 'Service',
        'name': name,
        'url': url,
        'provider': {'@type': 'Organization', 'name': 'A-Gent', 'url': SITE},
        'areaServed': 'B2B SaaS companies',
        'serviceType': 'AI SDR platform and AI consulting',
        'description': description
    }


def faq_schema(items):
    return {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in items]}


def breadcrumb_schema(items):
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': idx + 1, 'name': name, 'item': url}
            for idx, (name, url) in enumerate(items)
        ]
    }


def head(title, description, path, extra_schema=None):
    canonical = SITE + ('' if path == '/' else path)
    schemas = [org_schema()]
    if extra_schema:
        schemas.extend(extra_schema)
    schema_html = '\n'.join(f'<script type="application/ld+json">{json.dumps(s, separators=(",", ":"))}</script>' for s in schemas)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&family=Orbitron:wght@500;600;700;800;900&family=Rajdhani:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/fleet-master.css">
  {schema_html}
</head>
<body>
<div class="site-shell">
'''


def nav():
    return f'''<header class="nav">
  <div class="container nav-inner">
    <a class="wordmark" href="/" aria-label="A-Gent home"><img src="/assets/brand/agent-logo-master.svg" alt="A-Gent"></a>
    <nav class="nav-links" aria-label="Primary navigation">
      <a class="nav-link" href="/consulting">AI Consulting</a>
      <a class="nav-link" href="/platform">Platform</a>
      <a class="nav-link" href="/about">About</a>
      <a class="nav-link" href="/blog/">Blog</a>
      <a class="nav-link demo-link" data-demo-open href="/#book-demo">Book a Demo</a>
      <a class="launch-link" href="{FLEET_LOGIN}">Launch Console</a>
    </nav>
  </div>
</header>
'''


def footer():
    return f'''<footer class="footer">
  <div class="container footer-grid">
    <div>
      <a class="wordmark" href="/" aria-label="A-Gent home"><img src="/assets/brand/agent-logo-master.svg" alt="A-Gent"></a>
      <p style="margin-top:.7rem;max-width:520px">A-Gent Fleet is the packaged AI SDR platform. A-Gent Consulting designs bespoke AI revenue systems for teams that need deeper implementation support.</p>
      <p>© 2026 A-Gent. All rights reserved.</p>
    </div>
    <div class="footer-links">
      <a href="/consulting">AI Consulting</a>
      <a href="/platform">Platform</a>
      <a href="/fleet">Fleet</a>
      <a href="/assessment">Assessment</a>
      <a href="/signup">Signup</a>
      <a href="/privacy">Privacy</a>
      <a href="{FLEET_LOGIN}">Launch Console</a>
    </div>
  </div>
</footer>
</div>
</body>
</html>
'''


def card(title, text, icon='◆', link=None, label=None, featured=False):
    cls = 'card featured' if featured else 'card'
    body = f'<article class="{cls}"><div class="icon-box">{icon}</div>'
    if label:
        body += f'<div class="offer-label">{escape(label)}</div>'
    body += f'<h3>{escape(title)}</h3><p>{escape(text)}</p>'
    if link:
        body += f'<div class="cta-row" style="margin-top:1.15rem"><a class="btn btn-secondary" href="{link}">Explore</a></div>'
    body += '</article>'
    return body


def write_route(route, html):
    if route == '/':
        paths = [OUT / 'index.html']
    else:
        rel = route.strip('/')
        paths = [OUT / rel / 'index.html', OUT / f'{rel}.html']
    for p in paths:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(html, encoding='utf-8')


def home_page():
    desc = 'A-Gent offers A-Gent Fleet, a packaged AI SDR platform, and AI Consulting for bespoke revenue automation systems for B2B SaaS teams.'
    faq = faq_schema([
        ('What is A-Gent Fleet?', 'A-Gent Fleet is the packaged AI SDR platform for researching accounts, generating relevant outreach, reviewing messages, and operating outbound workflows.'),
        ('How is AI Consulting different?', 'AI Consulting is the bespoke service offer for teams that need custom AI revenue systems, integrations, workflow design, or strategic implementation support.'),
        ('Where do users launch the product?', 'The Launch Console opens the A-Gent Fleet login and signup route at the Fleet app.')
    ])
    return head('A-Gent | AI SDR Platform and AI Consulting for B2B SaaS', desc, '/', [service_schema('A-Gent Fleet and AI Consulting', SITE, desc), faq]) + nav() + f'''
<main>
  <section class="hero">
    <div class="container hero-grid">
      <div>
        <div class="status-pill">Systems Online</div>
        <h1>A-Gent, <span class="gold">always-on SDR.</span></h1>
        <p class="lede">Pipeline built in the background while your team focuses on revenue execution. Or engage AI Consulting to design a bespoke revenue automation system around your stack.</p>
        <div class="cta-row">
          <a class="btn btn-primary" data-demo-open href="/#book-demo">Book Demo</a>
          <a class="btn btn-secondary" href="/consulting">Explore Consulting</a>
        </div>
      </div>
      <aside class="console-card hero-motion-card" aria-label="A-Gent AI SDR product motion loop">
        <div class="sdr-motion" role="img" aria-label="Looping product motion showing an AI SDR prospecting, researching, drafting outreach, and updating pipeline.">
          <div class="sdr-topbar"><div class="sdr-title">AI SDR Running</div><div class="sdr-live">Live Loop</div></div>
          <div class="sdr-stage"><div class="sdr-icon">01</div><div class="sdr-copy"><strong>Prospects matched</strong><span>ICP fit, buying signals, and target account data enrich automatically.</span></div></div>
          <div class="sdr-stage"><div class="sdr-icon">02</div><div class="sdr-copy"><strong>Accounts researched</strong><span>Company context and signal evidence are compressed into a sales brief.</span></div></div>
          <div class="sdr-stage"><div class="sdr-icon">03</div><div class="sdr-copy"><strong>Emails drafted</strong><span>Personalized GAP-style outreach is generated with the current-state signal.</span></div></div>
          <div class="sdr-stage"><div class="sdr-icon">04</div><div class="sdr-copy"><strong>Pipeline updated</strong><span>CRM status, next steps, and review queue stay current in the background.</span></div></div>
          <div class="sdr-pipeline"><div class="sdr-bar"></div></div>
        </div>
      </aside>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-header"><div class="eyebrow">Choose the right path</div><h2>Productized AI SDR platform or bespoke AI revenue build.</h2><p>A-Gent Fleet is for teams ready to operate outbound inside a packaged console. AI Consulting is for companies that need custom architecture, integrations, and operating design.</p></div>
      <div class="grid-2">
        <article class="card featured"><div class="offer-label">Packaged product</div><h3>A-Gent Fleet</h3><p>Autonomous AI SDR agents research prospects, generate relevant outreach, route replies, and keep humans in control through a review queue.</p><ul><li>Best for lean B2B SaaS teams that want a deployable outbound engine.</li><li>Launch Console opens the Fleet app login and signup experience.</li><li>Platform pages below explain the Fleet capability layer.</li></ul><div class="cta-row"><a class="btn btn-primary" href="{FLEET_LOGIN}">Launch Console</a><a class="btn btn-secondary" href="/fleet">View Fleet</a></div></article>
        <article class="card"><div class="offer-label">Service offer</div><h3>AI Consulting</h3><p>Strategic AI implementation for teams that need custom workflows, data architecture, GTM systems, automation, and internal enablement.</p><ul><li>Best for teams with complex stacks or bespoke operating requirements.</li><li>Includes advisory, design, build, and implementation support.</li><li>Starts with a focused assessment of the revenue workflow.</li></ul><div class="cta-row"><a class="btn btn-primary" href="/assessment">Start Assessment</a><a class="btn btn-secondary" href="/consulting">View Consulting</a></div></article>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-header"><div class="eyebrow">Fleet capabilities</div><h2>The public Platform is now the Fleet operating layer.</h2><p>The platform story has been reframed around Fleet capabilities instead of advertising internal A-Gent tools as standalone public products.</p></div>
      <div class="grid-4">
        {card('Research prospects', 'Find accounts, enrich contacts, and capture the evidence needed for credible outreach.', '⌁', '/platform/find-and-research')}
        {card('Personalize outreach', 'Generate messages from ICP rules, pain points, signals, and proof instead of generic templates.', '✦', '/platform/ai-personalization')}
        {card('Review before send', 'Use a human review queue to keep message quality and brand control intact.', '✓', '/platform/review-queue')}
        {card('Measure and scale', 'Track campaign performance, reply quality, workflow throughput, and pipeline movement.', '▣', '/platform/measure-and-scale')}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container section-header"><div class="eyebrow">Ready to deploy?</div><h2>Open the Launch Console or start with a strategy assessment.</h2><p>Use Fleet when you want the product. Use Consulting when you want A-Gent to help design and build the operating system around your team.</p><div class="cta-row" style="justify-content:center"><a class="btn btn-primary" href="{FLEET_LOGIN}">Launch Console</a><a class="btn btn-secondary" href="/assessment">Start Assessment</a></div></div>
  </section>
</main>
''' + '''
<div class="demo-modal" id="book-demo" aria-hidden="true">
  <div class="demo-dialog" role="dialog" aria-modal="true" aria-labelledby="demoTitle">
    <div class="demo-head">
      <div>
        <div class="eyebrow">Book a Demo</div>
        <h2 id="demoTitle">Start the A-Gent demo flow.</h2>
        <p>Share a few details and A-Gent will create a new CRM lead for follow-up.</p>
      </div>
      <button class="demo-close" type="button" data-demo-close aria-label="Close demo form">×</button>
    </div>
    <form id="demoLeadForm" class="form-grid" data-supabase-url="https://byospmliiokgrdjjxsde.supabase.co" data-supabase-key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ5b3NwbWxpaW9rZ3Jkamp4c2RlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk4MjQ0NzUsImV4cCI6MjA5NTQwMDQ3NX0.KvzaEuEH9nRlBBSUOyg7kTKHvLFfR6CvmZbjVHZQ83I">
      <div class="field"><label for="demoName">Name</label><input id="demoName" name="name" autocomplete="name" required></div>
      <div class="field"><label for="demoEmail">Work email</label><input id="demoEmail" name="email" type="email" autocomplete="email" required></div>
      <div class="field wide"><label for="demoCompany">Company</label><input id="demoCompany" name="company" autocomplete="organization" required></div>
      <div class="field wide"><label for="demoMessage">Optional message</label><textarea id="demoMessage" name="message" placeholder="Tell us about your revenue motion, SDR workflow, or current stack."></textarea></div>
      <div class="field wide"><button class="btn btn-primary" type="submit">Submit Demo Request</button><div id="demoFormMessage" class="form-message" role="status" aria-live="polite"></div></div>
    </form>
  </div>
</div>
<script>
(function() {
  var modal = document.getElementById('book-demo');
  var form = document.getElementById('demoLeadForm');
  var msg = document.getElementById('demoFormMessage');
  function openDemo(evt) { if (evt) evt.preventDefault(); if (modal) { modal.setAttribute('aria-hidden','false'); setTimeout(function(){ var first = document.getElementById('demoName'); if (first) first.focus(); }, 30); } }
  function closeDemo(evt) { if (evt) evt.preventDefault(); if (modal) modal.setAttribute('aria-hidden','true'); }
  Array.prototype.slice.call(document.querySelectorAll('[data-demo-open]')).forEach(function(el) { el.addEventListener('click', openDemo); });
  Array.prototype.slice.call(document.querySelectorAll('[data-demo-close]')).forEach(function(el) { el.addEventListener('click', closeDemo); });
  if (modal) modal.addEventListener('click', function(evt) { if (evt.target === modal) closeDemo(evt); });
  document.addEventListener('keydown', function(evt) { if (evt.key === 'Escape') closeDemo(evt); });
  if (!form) return;
  form.addEventListener('submit', async function(evt) {
    evt.preventDefault();
    var fd = new FormData(form);
    var name = String(fd.get('name') || '').trim();
    var email = String(fd.get('email') || '').trim();
    var company = String(fd.get('company') || '').trim();
    var message = String(fd.get('message') || '').trim();
    var payload = { name: name, email: email, company_name: company, type: 'Lead', source: 'a-gent.co Book Demo form' + (message ? ' — ' + message : ''), created_at: new Date().toISOString() };
    msg.className = 'form-message'; msg.textContent = 'Submitting demo request...';
    try {
      var res = await fetch(form.dataset.supabaseUrl + '/rest/v1/contacts', {
        method: 'POST',
        headers: { apikey: form.dataset.supabaseKey, Authorization: 'Bearer ' + form.dataset.supabaseKey, 'Content-Type': 'application/json', Accept: 'application/json', Prefer: 'return=representation' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error(await res.text());
      msg.className = 'form-message success'; msg.textContent = 'Demo request received. We created your CRM lead.';
      form.reset();
    } catch (err) {
      msg.className = 'form-message error'; msg.textContent = 'Submission failed. Please email mark.cope.roarr@gmail.com and mention Book Demo.';
      console.warn('Demo lead submission failed', err);
    }
  });
})();
</script>
''' + footer()


def platform_index():
    desc = 'Explore A-Gent Fleet platform capabilities for AI SDR research, personalization, review, reply handling, routing, and revenue workflow measurement.'
    cards = '\n'.join(card(title, short, '◆', f'/platform/{slug}') for slug, title, short, _ in platform_pages)
    flagship_cards = f'''
        <article class="card featured" style="border-color:rgba(212,175,55,.46);background:radial-gradient(circle at 18% 8%,rgba(212,175,55,.18),transparent 34%),linear-gradient(180deg,rgba(22,22,22,.98),rgba(7,7,7,.98));">
          <div class="eyebrow">Flagship Differentiator</div>
          <h3 style="margin-top:1rem">Signal Engine</h3>
          <p>Source-linked buying signals give every AI SDR message a timely, verifiable reason for reaching out instead of generic personalization.</p>
          <div class="cta-row" style="margin-top:1.15rem"><a class="btn btn-secondary" href="/platform/signal-engine">Explore</a></div>
        </article>
        <article class="card featured" style="border-color:rgba(212,175,55,.46);background:radial-gradient(circle at 18% 8%,rgba(212,175,55,.20),transparent 34%),linear-gradient(180deg,rgba(22,22,22,.98),rgba(7,7,7,.98));">
          <div class="eyebrow">Flagship Differentiator</div>
          <h3 style="margin-top:1rem">Loop Engine</h3>
          <p>Self-optimizing outbound uses an LLM-judge keep-or-revert loop to improve email strategy under hard sales-quality guardrails.</p>
          <div class="cta-row" style="margin-top:1.15rem"><a class="btn btn-secondary" href="/platform/loop-engine">Explore</a></div>
        </article>
    '''
    return head('A-Gent Platform | Fleet AI SDR Capabilities', desc, '/platform', [service_schema('A-Gent Fleet Platform', SITE + '/platform', desc), faq_schema([
        ('Is the Platform a separate product from Fleet?', 'The public Platform pages describe the capability layer inside A-Gent Fleet and the implementation patterns A-Gent Consulting can extend.'),
        ('What are the flagship differentiators?', 'Signal Engine adds source-linked buying signals. Loop Engine adds a self-optimizing outbound quality loop that keeps winning strategy changes and reverts weaker ones.'),
        ('Does A-Gent publish its internal operating tools here?', 'No. Internal A-Gent tools remain separate and are not promoted as public products on the marketing site.')
    ])]) + nav() + f'''
<main>
  <section class="hero"><div class="container hero-grid"><div><div class="status-pill">Platform Online</div><h1>The <span class="gold">Fleet platform</span> capability layer.</h1><p class="lede">A clear map of the workflows behind A-Gent Fleet: prospect discovery, account research, personalized outreach, human review, reply handling, routing, optimization, and measurement.</p><div class="cta-row"><a class="btn btn-primary" href="{FLEET_LOGIN}">Launch Console</a><a class="btn btn-secondary" href="/fleet">View Fleet</a></div></div><aside class="console-card"><div class="console-top"><div><div class="console-kicker">Capability Map</div><div class="console-title">Research → Review → Optimize → Revenue</div></div></div><div class="metric-grid"><div class="metric"><strong>23</strong><span>Public routes</span></div><div class="metric"><strong>2</strong><span>Differentiators</span></div><div class="metric"><strong>1</strong><span>Public platform</span></div><div class="metric"><strong>AA</strong><span>Contrast target</span></div></div></aside></div></section>
  <section class="section"><div class="container"><div class="section-header"><div class="eyebrow">Flagship Differentiators</div><h2>Signals create relevance. Loops compound quality.</h2><p>Signal Engine and Loop Engine are the proprietary layers that make Fleet more than another outbound sequencer: one finds verifiable reasons to reach out, and the other improves what the system does next.</p></div><div class="grid-2">{flagship_cards}</div></div></section>
  <section class="section"><div class="container"><div class="section-header"><div class="eyebrow">Capabilities</div><h2>Every platform page now points back to Fleet outcomes.</h2><p>Existing SEO/AEO routes remain intact, but the positioning has been cleaned up so prospects understand A-Gent Fleet and AI Consulting without seeing internal tools advertised.</p></div><div class="grid-3">{cards}</div></div></section>
</main>
''' + footer()



def consulting_page():
    desc = 'A-Gent AI Consulting designs and implements custom AI revenue systems, GTM automation, workflow integrations, and agentic operating models for B2B SaaS teams.'
    return head('AI Consulting | A-Gent Bespoke Revenue Automation', desc, '/consulting', [service_schema('A-Gent AI Consulting', SITE + '/consulting', desc)]) + nav() + f'''
<main>
  <section class="hero"><div class="container hero-grid"><div><div class="status-pill">Consulting Track</div><h1>Bespoke <span class="gold">AI revenue systems</span> for serious teams.</h1><p class="lede">When the packaged Fleet product is not enough, A-Gent Consulting maps your GTM workflow, designs the agentic operating model, and helps build the automations, data flows, and governance needed to run it.</p><div class="cta-row"><a class="btn btn-primary assessment-primary" href="/assessment">Start Free AI Assessment</a><a class="btn btn-secondary" href="/platform">View Platform</a></div></div><aside class="console-card"><div class="console-top"><div><div class="console-kicker">Consulting System</div><div class="console-title">Diagnose → Design → Deploy</div></div></div><div class="metric-grid"><div class="metric"><strong>ICP</strong><span>Workflow audit</span></div><div class="metric"><strong>AI</strong><span>System design</span></div><div class="metric"><strong>Ops</strong><span>Implementation</span></div><div class="metric"><strong>KPI</strong><span>Measurement</span></div></div></aside></div></section>
  <section class="section"><div class="container"><div class="section-header"><div class="eyebrow">Engagement model</div><h2>For teams that need more than software access.</h2><p>Consulting is the service lane: strategy, architecture, build support, and enablement around the systems that create pipeline and operational leverage.</p></div><div class="grid-3">{card('Revenue workflow diagnosis','Map current-state friction, data gaps, manual work, message quality, and where AI can create measurable leverage.','⌁')}{card('Agentic system design','Define the agents, approval gates, data objects, integrations, and operating rules needed for a credible AI revenue system.','✦', featured=True)}{card('Implementation support','Build, iterate, and operationalize the workflows so the team can adopt the system without losing control.','✓')}</div></div></section>
</main>
''' + footer()


def fleet_page():
    desc = 'A-Gent Fleet is the packaged AI SDR platform for B2B SaaS teams that need prospect research, personalized outbound, review queues, and scalable pipeline automation.'
    return head('A-Gent Fleet | AI SDR Platform', desc, '/fleet', [service_schema('A-Gent Fleet', SITE + '/fleet', desc)]) + nav() + f'''
<main>
  <section class="hero"><div class="container hero-grid"><div><div class="status-pill">Fleet Product</div><h1>Deploy your <span class="gold">AI SDR command center</span>.</h1><p class="lede">Fleet is the packaged product: autonomous research, AI-personalized outbound, review queues, reply workflows, and measurement in one focused console.</p><div class="cta-row"><a class="btn btn-primary" href="{FLEET_LOGIN}">Launch Console</a><a class="btn btn-secondary" href="{FLEET_PRICING}">View Plans</a></div></div><aside class="console-card"><div class="console-top"><div><div class="console-kicker">Fleet Console</div><div class="console-title">AI SDR Platform</div></div></div><div class="metric-grid"><div class="metric"><strong>AI</strong><span>Research agents</span></div><div class="metric"><strong>HITL</strong><span>Review queue</span></div><div class="metric"><strong>RLS</strong><span>Tenant isolation</span></div><div class="metric"><strong>Live</strong><span>Console login</span></div></div></aside></div></section>
  <section class="section"><div class="container"><div class="section-header"><div class="eyebrow">Core product</div><h2>Built for outbound teams that need speed and control.</h2></div><div class="grid-4">{card('AI SDR agents','Research target accounts and draft relevant outreach using real account context.','⚡')}{card('Offer Brain','Store your value proposition, pain points, proof, and message rules for better generation.','◈')}{card('Review Queue','Approve, edit, or reject generated messages before they go out.','✓')}{card('Tenant isolation','Designed for multi-tenant customer workflows and secure data separation.','▣')}</div></div></section>
</main>
''' + footer()


def signup_page():
    desc = 'Sign up for A-Gent Fleet or request A-Gent AI Consulting support for a B2B SaaS revenue automation build.'
    return head('Signup | A-Gent', desc, '/signup') + nav() + f'''
<main><section class="hero"><div class="container"><div class="section-header"><div class="status-pill" style="margin:0 auto">Start Here</div><h1>Choose your <span class="gold">A-Gent path</span>.</h1><p>Open the Fleet Launch Console for product access, or start the assessment if you want A-Gent Consulting to evaluate a bespoke AI revenue build.</p><div class="cta-row" style="justify-content:center"><a class="btn btn-primary" href="{FLEET_LOGIN}">Launch Console</a><a class="btn btn-secondary" href="/assessment">Start Assessment</a></div></div></div></section><section class="section"><div class="container grid-2">{card('Use A-Gent Fleet','For teams ready to deploy the packaged AI SDR platform and manage outbound through the Fleet console.','◆', FLEET_LOGIN, 'Product', True)}{card('Use AI Consulting','For teams that need strategic implementation, workflow architecture, or custom AI automation around their stack.','✦','/assessment','Service')}</div></section></main>
''' + footer()


def assessment_page():
    desc = 'Start the A-Gent AI Assessment questionnaire to evaluate outbound workflow, AI readiness, data quality, automation risk, and the best next revenue automation path.'
    return head('AI Revenue Assessment | A-Gent', desc, '/assessment') + nav() + '''
<main>
  <section class="hero"><div class="container hero-grid"><div><div class="status-pill">AI Assessment</div><h1>Map the gap before you <span class="gold">automate revenue</span>.</h1><p class="lede">Answer five practical questions about your current outbound workflow, data quality, buying-signal visibility, AI readiness, and implementation risk. The result recommends whether A-Gent Fleet or A-Gent Consulting is the better next step.</p><div class="cta-row"><a class="btn btn-primary" href="#assessment-flow">Start Free AI Assessment</a><a class="btn btn-secondary" href="/consulting">Explore Consulting</a></div></div><aside class="console-card"><div class="console-top"><div><div class="console-kicker">Assessment Flow</div><div class="console-title">Current - Future - Gap</div></div></div><div class="metric-grid"><div class="metric"><strong>5</strong><span>Questions</span></div><div class="metric"><strong>2</strong><span>Pathways</span></div><div class="metric"><strong>0</strong><span>Cost</span></div><div class="metric"><strong>Live</strong><span>Results</span></div></div></aside></div></section>
  <section class="section" id="assessment-flow"><div class="container"><div class="assessment-shell card" data-assessment-flow><div class="offer-label">Free AI Assessment</div><h2 style="font-size:2rem;margin-bottom:.7rem">Find the best AI revenue automation path.</h2><p class="notice">This questionnaire gives an immediate recommendation and next step. No browser login is required.</p><div class="assessment-progress" aria-label="Assessment progress"><span data-assessment-progress></span></div><form id="aiAssessmentForm">
    <fieldset class="assessment-step is-active" data-step="1"><legend><h3>1. How repeatable is your outbound motion today?</h3></legend><div class="assessment-options"><label class="assessment-option"><input type="radio" name="workflow" value="1" required><span><strong>Mostly manual</strong><span>Lists, research, writing, and follow-up are still handled ad hoc.</span></span></label><label class="assessment-option"><input type="radio" name="workflow" value="2"><span><strong>Partly documented</strong><span>The team has a process, but execution depends heavily on rep discipline.</span></span></label><label class="assessment-option"><input type="radio" name="workflow" value="3"><span><strong>Operationally repeatable</strong><span>ICP, messaging, review, and CRM workflows are already structured.</span></span></label></div></fieldset>
    <fieldset class="assessment-step" data-step="2"><legend><h3>2. How strong is your account and contact data?</h3></legend><div class="assessment-options"><label class="assessment-option"><input type="radio" name="data" value="1" required><span><strong>Fragmented</strong><span>Data quality, ownership, and enrichment are inconsistent.</span></span></label><label class="assessment-option"><input type="radio" name="data" value="2"><span><strong>Usable but incomplete</strong><span>Core CRM data exists, but enrichment and fit scoring need work.</span></span></label><label class="assessment-option"><input type="radio" name="data" value="3"><span><strong>Ready for automation</strong><span>Segments, contacts, CRM fields, and ownership are mostly reliable.</span></span></label></div></fieldset>
    <fieldset class="assessment-step" data-step="3"><legend><h3>3. How visible are buying signals?</h3></legend><div class="assessment-options"><label class="assessment-option"><input type="radio" name="signals" value="1" required><span><strong>Low visibility</strong><span>Personalization is mostly generic or based on manual research.</span></span></label><label class="assessment-option"><input type="radio" name="signals" value="2"><span><strong>Some signal tracking</strong><span>The team uses a few triggers, but they are not operationalized.</span></span></label><label class="assessment-option"><input type="radio" name="signals" value="3"><span><strong>Strong signal strategy</strong><span>Signals can be connected to ICP fit, messaging, and prioritization.</span></span></label></div></fieldset>
    <fieldset class="assessment-step" data-step="4"><legend><h3>4. What level of AI implementation support do you need?</h3></legend><div class="assessment-options"><label class="assessment-option"><input type="radio" name="support" value="1" required><span><strong>Need architecture first</strong><span>We need help designing the system, rules, data flow, and governance.</span></span></label><label class="assessment-option"><input type="radio" name="support" value="2"><span><strong>Need guided deployment</strong><span>We can adopt a product, but want implementation support.</span></span></label><label class="assessment-option"><input type="radio" name="support" value="3"><span><strong>Ready for product access</strong><span>We can use a focused AI SDR platform with minimal custom work.</span></span></label></div></fieldset>
    <fieldset class="assessment-step" data-step="5"><legend><h3>5. What is the cost of staying manual?</h3></legend><div class="assessment-options"><label class="assessment-option"><input type="radio" name="gap" value="1" required><span><strong>Not yet clear</strong><span>We are still defining the business case and measurement model.</span></span></label><label class="assessment-option"><input type="radio" name="gap" value="2"><span><strong>Moderately painful</strong><span>Manual execution slows pipeline creation, but the team can still manage.</span></span></label><label class="assessment-option"><input type="radio" name="gap" value="3"><span><strong>Material revenue drag</strong><span>Slow research, weak personalization, or messy CRM follow-through is costing pipeline.</span></span></label></div></fieldset>
    <div class="assessment-actions"><button class="btn btn-secondary" type="button" data-assessment-prev disabled>Back</button><button class="btn btn-primary" type="button" data-assessment-next>Next</button></div>
  </form><div class="assessment-result" data-assessment-result><div class="offer-label">Assessment result</div><h2 data-result-title>Recommended next step</h2><div class="assessment-score" data-result-score></div><p class="notice" data-result-copy></p><div class="assessment-pill-row"><span>ICP fit</span><span>Data readiness</span><span>Signal strategy</span><span>Execution gap</span></div><div class="cta-row"><a class="btn btn-primary" data-result-primary href="/consulting">Talk Through the Assessment</a><a class="btn btn-secondary" href="https://fleet.a-gent.co/login">Launch Console</a></div></div></div></div></section>
</main>
<script>
(function(){
  var form = document.getElementById('aiAssessmentForm');
  if (!form) return;
  var steps = Array.prototype.slice.call(form.querySelectorAll('.assessment-step'));
  var progress = document.querySelector('[data-assessment-progress]');
  var prev = document.querySelector('[data-assessment-prev]');
  var next = document.querySelector('[data-assessment-next]');
  var result = document.querySelector('[data-assessment-result]');
  var current = 0;
  function showStep(i){
    current = Math.max(0, Math.min(i, steps.length - 1));
    steps.forEach(function(step, idx){ step.classList.toggle('is-active', idx === current); });
    if (progress) progress.style.width = ((current + 1) / steps.length * 100) + '%';
    if (prev) prev.disabled = current === 0;
    if (next) next.textContent = current === steps.length - 1 ? 'Show Results' : 'Next';
  }
  function answered(){ return !!steps[current].querySelector('input[type="radio"]:checked'); }
  function score(){ return Array.prototype.slice.call(form.querySelectorAll('input[type="radio"]:checked')).reduce(function(sum, input){ return sum + Number(input.value || 0); }, 0); }
  function showResult(){
    if (!form.reportValidity()) return;
    var total = score();
    var pct = Math.round(total / 15 * 100);
    var workflow = Number((form.querySelector('input[name="workflow"]:checked') || {}).value || 0);
    var support = Number((form.querySelector('input[name="support"]:checked') || {}).value || 0);
    var customBias = support <= 2 || workflow <= 2;
    var title = customBias ? 'AI Consulting is likely your best first move.' : 'A-Gent Fleet is likely ready to deploy.';
    var copy = customBias ? 'Your answers suggest the gap is not just tooling. Start with Consulting to design the workflow, data model, review gates, and operating rules before scaling automation.' : 'Your answers suggest your GTM motion is structured enough for the packaged AI SDR platform. Use Fleet to operationalize research, personalization, review, and pipeline updates.';
    form.style.display = 'none';
    if (progress) progress.style.width = '100%';
    if (result) result.classList.add('is-active');
    document.querySelector('[data-result-title]').textContent = title;
    document.querySelector('[data-result-score]').textContent = pct + '% readiness';
    document.querySelector('[data-result-copy]').textContent = copy;
    document.querySelector('[data-result-primary]').href = customBias ? '/consulting' : 'https://fleet.a-gent.co/login';
  }
  next.addEventListener('click', function(){
    if (!answered()) { steps[current].querySelector('input[type="radio"]').reportValidity(); return; }
    if (current === steps.length - 1) showResult(); else showStep(current + 1);
  });
  prev.addEventListener('click', function(){ showStep(current - 1); });
  form.addEventListener('change', function(evt){ if (evt.target.matches('input[type="radio"]') && current < steps.length - 1) setTimeout(function(){ showStep(current + 1); }, 180); });
  showStep(0);
})();
</script>
''' + footer()



def privacy_page():
    desc = 'A-Gent privacy information for the public marketing site, A-Gent Fleet, and AI Consulting inquiries.'
    return head('Privacy | A-Gent', desc, '/privacy') + nav() + '''
<main><section class="hero"><div class="container copy-block"><div class="status-pill">Privacy</div><h1>Privacy and <span class="gold">data handling</span>.</h1><p class="lede">A-Gent’s public marketing site explains Fleet and Consulting. Customer data for product workflows is handled through the appropriate Fleet application environment and agreed implementation scope.</p></div></section><section class="section"><div class="container copy-block"><h2>Public site privacy</h2><p>This marketing site is designed to provide information about A-Gent Fleet and AI Consulting. If you contact A-Gent, the information you provide may be used to respond to your request, evaluate fit, and coordinate next steps.</p><h2 style="margin-top:2rem">Product and consulting data</h2><p>Fleet product workflows and consulting engagements may involve separate customer data, access controls, and implementation agreements. A-Gent aims to use only the information necessary to provide the requested service and operate the relevant workflow.</p><h2 style="margin-top:2rem">Contact</h2><p>For privacy questions, contact mark.cope.roarr@gmail.com.</p></div></section></main>
''' + footer()


def compatibility_page(name, route, target=FLEET_LOGIN):
    desc = f'{name} access page for A-Gent.'
    return head(f'{name} | A-Gent', desc, route) + nav() + f'''
<main><section class="hero"><div class="container section-header"><div class="status-pill" style="margin:0 auto">Access</div><h1>{escape(name)} has moved to the <span class="gold">Launch Console</span>.</h1><p>The public marketing site now routes product access through A-Gent Fleet. Internal operating tools are not advertised as standalone public products here.</p><div class="cta-row" style="justify-content:center"><a class="btn btn-primary" href="{target}">Launch Console</a><a class="btn btn-secondary" href="/">Back to A-Gent</a></div></div></section></main>
''' + footer()


def loop_engine_page():
    route = '/platform/loop-engine'
    desc = 'Loop Engine is A-Gent Fleet\'s self-optimizing outbound layer: an LLM-judge keep-or-revert loop that improves email strategy under hard sales-quality guardrails.'
    faq_items = [
        ('What is the A-Gent Loop Engine?', 'Loop Engine is A-Gent Fleet\'s proprietary optimization layer for outbound email. It proposes strategy variations, scores them with an LLM judge, keeps improvements, and reverts weaker changes so outbound quality can compound safely.'),
        ('What does keep-or-revert mean?', 'Keep-or-revert means the system tests a candidate strategy change against a current baseline, accepts the change only when the judge score improves, and rolls back when the change weakens the message quality.'),
        ('What guardrails does Loop Engine enforce?', 'Loop Engine keeps outbound aligned to GAP methodology, never fabricates signals, favors brevity and a single CTA, and preserves the A-Gent Fleet signature and brand constraints.'),
        ('Is Loop Engine optimizing real reply rates yet?', 'Phase 1 quality-score optimization is live and has demonstrated a 78 to 82 baseline lift. Phase 2 reply-rate optimization is scoped and activates when statistically useful reply data is available.')
    ]
    schemas = [
        service_schema('Loop Engine', SITE + route, desc),
        faq_schema(faq_items),
        breadcrumb_schema([('Home', SITE + '/'), ('Platform', SITE + '/platform'), ('Loop Engine', SITE + route)])
    ]
    return head('Loop Engine | Self-Optimizing Outbound for AI SDR Teams', desc, route, schemas) + nav() + f'''
<main>
  <section class="hero">
    <div class="container hero-grid">
      <div>
        <div class="eyebrow">Flagship Differentiator</div>
        <h1>Loop Engine — <span class="gold">self-optimizing outbound.</span></h1>
        <p class="lede">A-Gent Fleet does not stop at generating emails. Loop Engine creates a governed optimization loop that tests outbound strategy changes, scores them with an LLM judge, keeps stronger variants, and reverts weaker ones before quality drifts.</p>
        <div class="cta-row"><a class="btn btn-primary" href="{FLEET_LOGIN}">Launch Console</a><a class="btn btn-secondary" href="/platform">View Platform</a></div>
      </div>
      <aside class="console-card" style="border-color:rgba(212,175,55,.42);background:radial-gradient(circle at 20% 10%,rgba(212,175,55,.20),transparent 36%),linear-gradient(180deg,rgba(17,17,17,.98),rgba(5,6,6,.99));">
        <div class="console-top"><div><div class="console-kicker">Optimization Loop</div><div class="console-title">Propose → Judge → Keep or Revert</div></div></div>
        <div class="metric-grid" style="margin-top:1rem"><div class="metric"><strong>78→82</strong><span>Phase 1 quality lift</span></div><div class="metric"><strong>Live</strong><span>aisdr.a-gent.co</span></div><div class="metric"><strong>LLM</strong><span>Judge scoring</span></div><div class="metric"><strong>Safe</strong><span>Hard guardrails</span></div></div>
      </aside>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-header"><div class="eyebrow">How it works</div><h2>A closed quality loop for outbound strategy.</h2><p>Loop Engine is designed around measured iteration, not uncontrolled automation. It improves email strategy only when the candidate version beats the current baseline against the rules A-Gent wants every message to follow.</p></div>
      <div class="grid-4">
        {card('Generate candidate','The system proposes a revised outbound strategy or email pattern based on the current baseline and campaign context.','01')}
        {card('Score with judge','An LLM judge evaluates the candidate against relevance, problem clarity, evidence use, brevity, and CTA discipline.','02', featured=True)}
        {card('Keep improvements','If the candidate improves the quality score, Loop Engine records the gain and promotes the stronger strategy.','03')}
        {card('Revert drift','If the candidate weakens quality or violates guardrails, the system rejects it and preserves the safer baseline.','04')}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-header"><div class="eyebrow">Hard guardrails</div><h2>Optimization stays inside A-Gent sales-quality rules.</h2><p>The loop is intentionally constrained. It is not allowed to chase superficial novelty, fabricate context, or turn outbound into long-form copy.</p></div>
      <div class="grid-2">
        <article class="card featured"><h3>Message strategy rules</h3><ul><li><strong>GAP methodology:</strong> connect current state, desired future state, and the cost of the gap.</li><li><strong>Never fabricate signals:</strong> use only available, source-linked evidence from the workflow.</li><li><strong>Brevity and one CTA:</strong> keep the email easy to read and easy to answer.</li><li><strong>A-Gent Fleet signature:</strong> preserve the product voice and sender standard.</li></ul></article>
        <article class="card"><h3>Operating state</h3><p><strong>Phase 1 is live:</strong> Loop Engine is already optimizing quality scores, including a demonstrated lift from a 78 baseline to 82.</p><p><strong>Phase 2 is scoped:</strong> real reply-rate optimization will activate when enough reply data exists to judge business outcomes rather than only message quality.</p><p><strong>Source:</strong> live on aisdr.a-gent.co as part of A-Gent's AI SDR operating layer.</p></article>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container faq">
      <details open><summary>What makes Loop Engine different from ordinary A/B testing?</summary><p>Loop Engine is a strategy-quality loop rather than a subject-line testing widget. It evaluates whether the outbound logic is more credible, problem-centric, concise, and evidence-based before keeping a change.</p></details>
      <details><summary>Does Loop Engine replace human review?</summary><p>No. It improves the strategy baseline that feeds Fleet workflows, while review queues and approval gates still give operators control over what reaches prospects.</p></details>
      <details><summary>How does it work with Signal Engine?</summary><p>Signal Engine supplies verifiable current-state evidence. Loop Engine evaluates how that evidence is turned into messaging and keeps changes that improve the sales-quality score.</p></details>
      <details><summary>Where should buyers go next?</summary><p>Teams ready to use the product should open the Launch Console. Teams that need a bespoke build should start with A-Gent Consulting or review the broader Platform capability map.</p></details>
    </div>
  </section>

  <section class="section"><div class="container section-header"><div class="eyebrow">Ready to compound outbound quality?</div><h2>Launch Fleet or explore the platform layer.</h2><p>Loop Engine is one of the flagship differentiators inside the A-Gent AI SDR system.</p><div class="cta-row" style="justify-content:center"><a class="btn btn-primary" href="{FLEET_LOGIN}">Launch Console</a><a class="btn btn-secondary" href="/platform">View Platform</a></div></div></section>
</main>
''' + footer()


def platform_subpage(slug, title, short, detail):
    route = f'/platform/{slug}'
    desc = f'{title} is an A-Gent Fleet capability for B2B SaaS teams: {short}'
    faq = faq_schema([
        (f'What is {title} in A-Gent Fleet?', f'{title} is part of the Fleet platform capability layer. {short}'),
        (f'Can {title} be extended through consulting?', 'Yes. A-Gent Consulting can extend Fleet patterns into bespoke workflows, integrations, and operating models when a customer needs more than the packaged product.'),
        ('Does this page link to internal A-Gent tools?', 'No. The public site describes platform capabilities and links to Fleet or Consulting paths only.')
    ])
    return head(f'{title} | A-Gent Platform', desc, route, [service_schema(title, SITE + route, desc), faq]) + nav() + f'''
<main>
  <section class="hero"><div class="container hero-grid"><div><div class="status-pill">Fleet Capability</div><h1>{escape(title)} for <span class="gold">AI SDR teams</span>.</h1><p class="lede">{escape(short)}</p><div class="cta-row"><a class="btn btn-primary" href="{FLEET_LOGIN}">Launch Console</a><a class="btn btn-secondary" href="/platform">All Capabilities</a></div></div><aside class="console-card"><div class="console-top"><div><div class="console-kicker">Capability Detail</div><div class="console-title">{escape(title)}</div></div></div><p style="margin-top:1rem">{escape(detail)}</p></aside></div></section>
  <section class="section"><div class="container"><div class="section-header"><div class="eyebrow">How it fits</div><h2>One capability inside the Fleet operating layer.</h2><p>This route is preserved for SEO and buyer education, but the page is now framed around A-Gent Fleet and A-Gent Consulting instead of separate internal operating tools.</p></div><div class="grid-3">{card('Inputs','ICP rules, account evidence, offer context, data quality, and workflow constraints.','⌁')}{card('Fleet workflow','A packaged AI SDR process with governed research, message generation, review, and routing.','✦', featured=True)}{card('Consulting extension','A-Gent can adapt this capability into custom architectures when the packaged workflow is not enough.','✓')}</div></div></section>
  <section class="section"><div class="container faq"><details open><summary>What outcome does this create?</summary><p>{escape(detail)}</p></details><details><summary>Where should buyers go next?</summary><p>Teams ready to use the product should open the Launch Console. Teams that need a bespoke build should start with the AI Consulting assessment.</p></details></div></section>
</main>
''' + footer()


def preserve_existing_routes():
    preserve_names = ['blog', 'about']
    preserve_nested = [Path('platform/signal-engine'), Path('platform/loop-engine')]
    temp = BASE / '.preserve-public-routes'
    if temp.exists():
        shutil.rmtree(temp)
    temp.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        for name in preserve_names:
            src = OUT / name
            if src.exists():
                shutil.copytree(src, temp / name)
        for rel in preserve_nested:
            src = OUT / rel
            if src.exists():
                dest = temp / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(src, dest)
    return temp


def restore_preserved_routes(temp):
    if not temp.exists():
        return
    for item in temp.iterdir():
        if item.name == 'platform':
            continue
        dest = OUT / item.name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(item, dest)
    platform_temp = temp / 'platform'
    if platform_temp.exists():
        for item in platform_temp.iterdir():
            dest = OUT / 'platform' / item.name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
    shutil.rmtree(temp)


def build():
    preserved = preserve_existing_routes()
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / 'assets/css').mkdir(parents=True, exist_ok=True)
    (OUT / 'assets/css/fleet-master.css').write_text(CSS, encoding='utf-8')
    src_brand = BASE / 'deploy_backup_brand'
    old_brand = BASE / 'deploy' / 'assets' / 'brand'
    master_brand = Path('/home/ubuntu/a-gent-logo-master') / 'assets' / 'brand'
    if old_brand.exists():
        src_brand = old_brand
    elif master_brand.exists():
        src_brand = master_brand
    if src_brand.exists():
        shutil.copytree(src_brand, OUT / 'assets/brand', dirs_exist_ok=True)
    write_route('/', home_page())
    write_route('/platform', platform_index())
    write_route('/platform/loop-engine', loop_engine_page())
    write_route('/consulting', consulting_page())
    write_route('/fleet', fleet_page())
    write_route('/signup', signup_page())
    write_route('/assessment', assessment_page())
    write_route('/privacy', privacy_page())
    write_route('/login', compatibility_page('A-Gent Login', '/login'))
    # /dashboard is intentionally preserved, but reframed to the public Fleet console rather than internal tooling.
    write_route('/dashboard', compatibility_page('A-Gent Dashboard', '/dashboard'))
    for slug, title, short, detail in platform_pages:
        write_route(f'/platform/{slug}', platform_subpage(slug, title, short, detail))

    sitemap_routes = all_routes
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for route in sitemap_routes:
        loc = SITE + ('' if route == '/' else route)
        priority = '1.0' if route == '/' else ('0.8' if route in core_routes else '0.7')
        sitemap.append(f'  <url><loc>{loc}</loc><lastmod>{LASTMOD}</lastmod><changefreq>weekly</changefreq><priority>{priority}</priority></url>')
    sitemap.append('</urlset>')
    restore_preserved_routes(preserved)
    (OUT / 'sitemap.xml').write_text('\n'.join(sitemap) + '\n', encoding='utf-8')
    (OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://a-gent.co/sitemap.xml\n', encoding='utf-8')
    (OUT / 'llms.txt').write_text('''# A-Gent\n\nA-Gent offers A-Gent Fleet, a packaged AI SDR platform for B2B SaaS outbound teams, and AI Consulting for bespoke AI revenue automation systems.\n\n## Public navigation\n\n- AI Consulting: https://a-gent.co/consulting\n- Platform: https://a-gent.co/platform\n- Loop Engine: https://a-gent.co/platform/loop-engine\n- Fleet: https://a-gent.co/fleet\n- Launch Console: https://fleet.a-gent.co/login\n\n## Positioning\n\nA-Gent Fleet is the product. AI Consulting is the service. The public Platform pages describe Fleet capabilities and consulting extension points; internal operating tools are not advertised as public products. Flagship differentiators include Signal Engine for source-linked buying signals and Loop Engine for self-optimizing outbound quality under hard guardrails.\n''', encoding='utf-8')
    (OUT / 'netlify.toml').write_text('''[build]\n  publish = "."\n\n[[headers]]\n  for = "/*"\n  [headers.values]\n    X-Frame-Options = "DENY"\n    X-Content-Type-Options = "nosniff"\n    Referrer-Policy = "strict-origin-when-cross-origin"\n''', encoding='utf-8')


    logo_dir = OUT / 'assets' / 'brand'
    logo_dir.mkdir(parents=True, exist_ok=True)
    (logo_dir / 'agent-logo-master.svg').write_text(AGENT_LOGO_MASTER_SVG + '\n', encoding='utf-8')

    # Keep the known publish quirk safe: duplicate the full public artifact under dashboard/ as a compatibility subtree.
    dash = OUT / 'dashboard'
    dash.mkdir(parents=True, exist_ok=True)
    for item in list(OUT.iterdir()):
        if item.name == 'dashboard':
            continue
        dest = dash / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

if __name__ == '__main__':
    build()
    print(f'Built {OUT}')
    print(f'HTML files: {sum(1 for _ in OUT.rglob("*.html"))}')
