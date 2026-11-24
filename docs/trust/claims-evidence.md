# W2-AG-12 claims evidence

Draft `/security` trust page for a-gent.co. Every claim on the page maps to a merged pull request, a live `curl` check run on **24 November 2026, 12:13 PM America/New_York** (response `date` headers: `Tue, 24 Nov 2026 17:13:22 GMT` and `17:13:23 GMT`), or both.

This file is the review table for Eng Lead. Header excerpts below are copied from those `curl -sS -D -` probes. Response bodies are not reproduced here (the Mission Control sign-in page includes a public Supabase publishable key, which does not belong in this document).

Probe request user-agent: `A-Gent-W2-AG12-probe`. Saved header files (not committed): `/workspace/w2-ag12/probes/*.headers`.

## Claims on the page

| # | Claim (paraphrased to the page sentence) | Evidence | Notes |
|---|---|---|---|
| 1 | Mission Control is invite-only. An unauthenticated visitor receives HTTP 401 and a sign-in page, not the application. The page does not offer a way to create an account. | [mission-control#3](https://github.com/Copey007/mission-control/pull/3) (`2a1ffe3`, merged 24 Nov 2026); [mission-control#4](https://github.com/Copey007/mission-control/pull/4) (`24cd6f7`); live `GET https://missioncontrol.a-gent.co/` and `/login` | Live: `HTTP/2 401`, `content-type: text/html`, body 4,245 bytes. Phrase search of the body: no "Create account", "Sign up", "Signup", or "Register". `ALLOW_SELF_SIGNUP` is the Mission Control flag for self-signup; it is unset in production per the approved ship. This page claims only what the live response shows. |
| 4 | a-gent.co, aisdr.a-gent.co, and missioncontrol.a-gent.co are served over HTTPS and send HTTP Strict Transport Security. | Live `curl` of `https://a-gent.co/`, `https://aisdr.a-gent.co/`, `https://missioncontrol.a-gent.co/` | All three returned `HTTP/2` and `strict-transport-security`. Values differ: marketing and Mission Control send `max-age=31536000`; aisdr sends `max-age=31536000; includeSubDomains`. The page does not claim encryption at rest, a TLS configuration audit, or a uniform HSTS policy. |
| 5 | a-gent.co sends `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, and `Referrer-Policy: strict-origin-when-cross-origin`. | Live `GET https://a-gent.co/` | Present. No CSP and no `X-Robots-Tag` on the marketing site; the page does not claim them there. |
| 6 | Mission Control sends CSP `frame-ancestors 'none'`, `X-Frame-Options: DENY`, nosniff, Referrer-Policy, Permissions-Policy, `X-Robots-Tag: noindex, nofollow`, and `Cache-Control: no-store, private` on the sign-in response. | [mission-control#3](https://github.com/Copey007/mission-control/pull/3), [mission-control#4](https://github.com/Copey007/mission-control/pull/4), live `GET https://missioncontrol.a-gent.co/` and `/login` | Header values are in the excerpts below. Permissions-Policy on this host is `camera=(), microphone=(), geolocation=()`. |
| 7 | aisdr `/` and `/signup` send CSP `frame-ancestors 'none'`, `X-Frame-Options: DENY`, nosniff, HSTS with `includeSubDomains`, Referrer-Policy, Permissions-Policy, and `X-Robots-Tag: noindex, nofollow`. `/agent.html` sends noindex, nosniff, HSTS, Referrer-Policy, and Permissions-Policy, but not `X-Frame-Options` or CSP. | [sales-agent#5](https://github.com/Copey007/sales-agent/pull/5) (`e339a82`, headers live on the stopgap); live `GET` of `/`, `/signup`, `/agent.html` | Stated path-by-path so the page does not over-claim a uniform header set. Permissions-Policy on this host is `geolocation=(), payment=(), usb=()`. |
| 8 | On the live Sales Agent host, public access to internal configuration and data files is blocked; those paths now return HTTP 404. The public page does not name the paths. | Live `GET https://aisdr.a-gent.co/package.json` and `https://aisdr.a-gent.co/memory/sent_emails.json` on 24 November 2026 | Both `HTTP/2 404`. The 404s are from the live stopgap (plus redirect rules later merged in sales-agent#4). Specific paths stay in this file only. |
| 9 | The marketing-site demo inquiry form sends `Prefer: return=minimal` so the browser does not read the inserted row back after a submit. | [gtm-revolution-web#1](https://github.com/Copey007/gtm-revolution-web/pull/1) (`b8d880f`) | Merged and on `main`. No new live form submission was made for this draft. |
| 10 | Netlify hosts a-gent.co, aisdr.a-gent.co, and missioncontrol.a-gent.co. | Live `Server: Netlify` header on all three hosts | — |
| 11 | Supabase is used for authentication and database access; the marketing site writes demo and assessment submissions there. | Environment variable names `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and (Sales Agent) `SUPABASE_SERVICE_ROLE_KEY` in the mission-control and sales-agent repositories; [gtm-revolution-web#1](https://github.com/Copey007/gtm-revolution-web/pull/1); [gtm-revolution-web#3](https://github.com/Copey007/gtm-revolution-web/pull/3) | Names only. No secret values are recorded here. #3 is a column-name fix for `assessment_responses.total_score`; it is cited only as evidence that assessment submissions are written to Supabase, not as a security control. |
| 12 | Resend is referenced in the Sales Agent codebase for email delivery (`RESEND_API_KEY`, `RESEND_WEBHOOK_SECRET`). | Environment variable names in sales-agent; [sales-agent#4](https://github.com/Copey007/sales-agent/pull/4) (webhook verification, approval-gated send path) | The public page only says Resend is referenced in the Sales Agent codebase. It does not claim a production send path. |
| 13 | The marketing site loads fonts from Google Fonts. | This page and the live a-gent.co HTML load `fonts.googleapis.com` / `fonts.gstatic.com` | Visible in page source. |
| 14 | The Sales Agent repository also references optional connectors including OpenAI, Stripe, and HeyGen. Presence of a variable name is not a claim that the integration is enabled for every workspace. | Environment variable names in sales-agent: `OPENAI_API_KEY`, `OPENAI_API_BASE`, `STRIPE_WEBHOOK_SECRET`, `HEYGEN_API_KEY` | Other names exist in the same repo (for example Buffer, HubSpot, Hunter, Salesforce, Serper). They are omitted from the public page to keep the list to widely recognized infrastructure and features; this file records that they were found. |
| 15 | No data-retention schedule is published on this page. The security / deletion contact is a `{{MARK: security contact email}}` placeholder. | No retention schedule was found on a-gent.co; contact is intentionally unfilled | Do not invent an address. |
| 16 | We do not have SOC 2, ISO 27001, HIPAA, or similar certification, and we do not claim a GDPR certification. We do not publish an uptime SLA, and we do not claim a completed third-party penetration test. | Honest negative claims. No contrary public page was found (`/security` was 404 before this draft; `/trust` 404). | These are absences, not attestations. |
| 17 | Database row-level security hardening is in progress and is not finished. | [mission-control#5](https://github.com/Copey007/mission-control/pull/5) (`12e1a9e`) added coverage tests and an anon INSERT-only `assessment_responses` policy. The full RLS lockdown migration is **not** applied in production. Eight tables still have RLS disabled. | The public page does not name tables or counts. Reviewers should not treat #5 as “RLS complete.” |
| 18 | We do not yet publish terms of service or a data processing agreement. `/terms` and `/dpa` returned HTTP 404. | Live `GET https://a-gent.co/terms` and `https://a-gent.co/dpa` (also `/terms/` and `/legal`) | All 404 on 24 November 2026. |


## Withheld until deployed

These two claims were drafted for the public page and then withdrawn under the 24 November 2026 Eng Lead ruling: do not describe the live aisdr dashboard as unsigned-in, and do not say that the approval-gated outbound path is not live, or hint at that gap on the page.

They are kept here for reviewers only. They must not be copied back onto `/security` until the TODO below is done and an accurate, then-current line is written.

| # | Withheld claim | Evidence | Notes |
|---|---|---|---|
| 2 | The live Sales Agent dashboard at aisdr.a-gent.co is not yet behind a sign-in gate. A gate and tenant checks are merged in sales-agent and have not been deployed to this host. The dashboard still loads without signing in. | [sales-agent#4](https://github.com/Copey007/sales-agent/pull/4) (`8f8f3e6`, merged, **not deployed** to aisdr); live `GET https://aisdr.a-gent.co/` on 24 November 2026 | Live that day: `HTTP/2 200`, `content-length: 87107`. Do not describe the gate as live, and do not put this sentence on the public page. |
| 3 | In the merged Sales Agent codebase, outbound email is held as a pending draft until a person approves it; approved messages go out with the stored text. This is not yet running on the live Sales Agent dashboard. | [sales-agent#4](https://github.com/Copey007/sales-agent/pull/4) | Code-only claim. The PR description records approval-gated outbound (`pending_approval`, `approve_sends` / `reject_sends`). No live send-path check was run, and the production host was still the stopgap build. Do not put this sentence on the public page. |

**TODO:** Once `SUPABASE_SERVICE_ROLE_KEY` is set and [sales-agent#4](https://github.com/Copey007/sales-agent/pull/4) (the sign-in gate and approval-gated outbound path) is deployed to aisdr.a-gent.co, restore an accurate line on `/security` from a fresh live check. Do not restore the withheld wording above verbatim; rewrite it to match what the live host actually does at that time (for example, a 401 sign-in wall if the gate is holding). Re-run the header and access probes, and update this file, before any such line is published.

## Claims deliberately left off the page

| Topic | Why it is omitted |
|---|---|
| sales-agent#6 / mission-control#6 (Operator Dark tokens and favicons) | Visual work, not a security control. |
| Encryption at rest, key management, pen tests, uptime percentages | Not proven. |
| Full RLS, “all tables protected,” or a completed database lockdown | Eight tables still have RLS disabled; the migration is pending. |
| Live approval-gated outbound on aisdr, or a live sign-in wall on aisdr | Withheld from the public page. See “Withheld until deployed” below. |
| Fleet headers or a Fleet sign-in gate | Headers were not shipped; a server-side Fleet gate is out of scope. |
| People, postal addresses, or real email addresses | Not invented. The only contact is `{{MARK: security contact email}}`. |
| Customer counts, pipeline outcomes, or availability SLAs | Not proven. |

## Live header excerpts (24 November 2026)

### `GET https://a-gent.co/` — HTTP/2 200, 28,802 bytes

```
strict-transport-security: max-age=31536000
x-frame-options: DENY
x-content-type-options: nosniff
referrer-policy: strict-origin-when-cross-origin
server: Netlify
```

No `content-security-policy` or `x-robots-tag`.

### `GET https://a-gent.co/security` and `/security/` — HTTP/2 404 (before this draft)

Same security headers as `/`. `/terms`, `/terms/`, `/dpa`, `/legal`, and `/trust` also returned 404.

### `GET https://aisdr.a-gent.co/` — HTTP/2 200, 87,107 bytes

```
content-security-policy: frame-ancestors 'none'
x-frame-options: DENY
x-content-type-options: nosniff
strict-transport-security: max-age=31536000; includeSubDomains
referrer-policy: strict-origin-when-cross-origin
permissions-policy: geolocation=(), payment=(), usb=()
x-robots-tag: noindex, nofollow
server: Netlify
```

`GET /signup` — HTTP/2 200, 8,752 bytes, same header set.

### `GET https://aisdr.a-gent.co/agent.html` — HTTP/2 200, 36,437 bytes

```
x-content-type-options: nosniff
strict-transport-security: max-age=31536000; includeSubDomains
referrer-policy: strict-origin-when-cross-origin
permissions-policy: geolocation=(), payment=(), usb=()
x-robots-tag: noindex, nofollow
server: Netlify
```

No `content-security-policy` or `x-frame-options`.

### `GET https://aisdr.a-gent.co/package.json` and `/memory/sent_emails.json` — HTTP/2 404

Both 404, with nosniff, HSTS (`includeSubDomains`), Referrer-Policy, Permissions-Policy, and `x-robots-tag: noindex, nofollow`. No `x-frame-options` or CSP on these 404 responses.

### `GET https://missioncontrol.a-gent.co/` and `/login` — HTTP/2 401, 4,245 bytes

```
cache-control: no-store,private
content-security-policy: frame-ancestors 'none'
x-frame-options: DENY
x-content-type-options: nosniff
strict-transport-security: max-age=31536000
referrer-policy: strict-origin-when-cross-origin
permissions-policy: camera=(), microphone=(), geolocation=()
x-robots-tag: noindex, nofollow
server: Netlify
vary: Accept-Encoding, Cookie, Authorization
content-type: text/html; charset=utf-8
```

## Page publishing constraints (this draft)

- `meta name="robots" content="noindex, nofollow"` is on the page.
- `netlify.toml` adds `X-Robots-Tag: noindex, nofollow` for `/security`, `/security/`, and `/security.html`.
- Canonical URL is `/security` (served from `security/index.html`). `/security/` and `/security.html` 301 to `/security`.
- The page is not in the site nav, footer, `sitemap.xml`, or `robots.txt`.
- New files contain no personal webmail addresses.
- The only placeholder is `{{MARK: security contact email}}`.
