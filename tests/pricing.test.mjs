import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const root = new URL('..', import.meta.url);
const read = (p) => readFileSync(new URL(p, root), 'utf8');

const STARTER = 49900;
const GROWTH = 99900;
const FEATURES = {
  starter: [
    '15-day free trial; card required, no charge until the trial ends',
    'Human-approval Review Queue',
    'Signal Engine with source-linked reasons',
    'Included prospecting volume and a connected sending mailbox',
    'Deliverability guardrails (SPF/DKIM/DMARC checks, daily send caps)',
    'Email support',
  ],
  growth: [
    'Everything in Starter',
    'Higher included prospecting volume, seats, and mailboxes',
    'Loop Engine',
    'CRM sync (A-Gent CRM, HubSpot, and Salesforce)',
    'Mission Control dashboard',
    'Priority support',
  ],
  enterprise: [
    'CRO diagnostic and GTM Brain setup',
    'Custom integrations and workflow design',
    'Managed operations on A-Gent Fleet',
  ],
};

for (const page of ['pricing/index.html', 'dashboard/pricing/index.html']) {
  test(`${page} publishes Starter $499, Growth $999, and Custom Build Talk to us`, () => {
    const html = read(page);
    assert.equal(html.includes('{{MARK'), false);
    assert.equal(/\b\$99\b/.test(html), false);
    assert.match(html, /data-plan="starter"[^>]*data-price-cents="49900"/);
    assert.match(html, /data-plan="growth"[^>]*data-price-cents="99900"/);
    assert.match(html, /data-plan="enterprise"[^>]*data-custom="true"/);
    assert.match(html, /\$499/);
    assert.match(html, /\$999/);
    assert.match(html, /Talk to us/);
    assert.match(html, /Skip to content/);
    assert.match(html, /id="main"/);
    assert.match(html, /https:\/\/aisdr\.a-gent\.co\/signup\.html\?plan=starter/);
    assert.match(html, /https:\/\/aisdr\.a-gent\.co\/signup\.html\?plan=growth/);
    assert.match(html, /href="\/consulting"/);
    assert.match(html, /"price":"499"/);
    assert.match(html, /"price":"999"/);
    for (const f of FEATURES.starter) assert.ok(html.includes(f), f);
    for (const f of FEATURES.growth) assert.ok(html.includes(f), f);
    for (const f of FEATURES.enterprise) assert.ok(html.includes(f), f);
    assert.equal(/testimonial|as featured in|trusted by/i.test(html), false);
    assert.equal(/mark\.cope\.roarr@gmail\.com/.test(html), false);
  });
}

test('root and dashboard pricing pages are identical', () => {
  const a = read('pricing/index.html');
  const b = read('dashboard/pricing/index.html');
  assert.equal(a, b);
});

test('60/40 blend of published prices is $699 (~$700 target)', () => {
  assert.equal(Math.round(STARTER * 0.6 + GROWTH * 0.4), 69900);
});

for (const page of ['fleet.html', 'fleet/index.html', 'dashboard/fleet.html', 'dashboard/fleet/index.html']) {
  test(`${page} View Plans points at /pricing/`, () => {
    const html = read(page);
    assert.match(html, /href="\/pricing\/">View Plans</);
    assert.equal(html.includes('https://fleet.a-gent.co/pricing'), false);
    assert.match(html, /href="\/pricing\/">Pricing</);
  });
}

test('sitemap omits /pricing/ while the page is noindex', () => {
  const xml = read('sitemap.xml');
  assert.equal(/<loc>https:\/\/a-gent\.co\/pricing\/?<\/loc>/.test(xml), false);
});

test('site generators point Fleet pricing at /pricing/ and include a footer Pricing link', () => {
  for (const p of ['generator/generate_site.py', 'tools/generate_site.py']) {
    const src = read(p);
    assert.match(src, /FLEET_PRICING = '\/pricing\/'/);
    assert.equal(src.includes('https://fleet.a-gent.co/pricing'), false);
    assert.match(src, /href="\/pricing\/">Pricing</);
  }
});

for (const page of ['pricing/index.html', 'dashboard/pricing/index.html']) {
  test(`${page} is noindex and has no unbacked claims`, () => {
    const html = read(page);
    assert.match(html, /<meta name="robots" content="noindex, nofollow">/);
    assert.equal(/credit top-ups?/i.test(html), false);
    assert.equal(/buy more credits/i.test(html), false);
    assert.equal(/cancel[^.]{0,80}from Mission Control/i.test(html), false);
    assert.equal(/Stripe customer portal|billing portal/i.test(html), false);
    assert.match(html, /cancel at the end of the current billing period by contacting us/);
    assert.equal(html.includes('Explore Consulting'), false);
    assert.match(html, /Book a Demo/);
  });

  test(`${page} uses the /security drawer, gold focus, and scroll-padding`, () => {
    const html = read(page);
    assert.match(html, /:focus-visible\{outline:2px solid var\(--gold\);outline-offset:2px\}/);
    assert.match(html, /summary:focus-visible\{outline-offset:4px;border-radius:6px\}/);
    assert.match(html, /html\{scroll-padding-top:72px\}/);
    assert.match(html, /class="nav-toggle"/);
    assert.match(html, /id="site-nav"/);
    assert.match(html, /class="nav-scrim"/);
    assert.match(html, /aria-controls="site-nav"/);
    assert.match(html, /html\.classList\.add\('js-nav'\)/);
    assert.match(html, /e\.key==='Escape'/);
    assert.match(html, /setAttribute\('inert'/);
    assert.match(html, /@media \(max-width:880px\)/);
  });

  test(`${page} hero CTA points at #plans and cards use aligned layout`, () => {
    const html = read(page);
    const hero = html.match(/<section class="hero"[\s\S]*?<\/section>/);
    assert.ok(hero, 'hero section present');
    assert.match(hero[0], /href="#plans">Start 15-day trial</);
    assert.equal(/plan=starter/.test(hero[0]), false);
    assert.match(html, /id="plans"/);
    assert.match(html, /grid-template-rows:subgrid/);
    assert.match(html, /\.plan-badge\{position:absolute;top:-11px/);
    assert.match(html, /\.plan-badge\{[^}]*font-size:\.75rem/);
    assert.match(html, /@media \(max-width:920px\) and \(min-width:640px\)[\s\S]*grid-template-columns:repeat\(2,minmax\(0,1fr\)\)/);
    assert.match(html, /@media \(max-width:639px\)[\s\S]*max-width:560px/);
    assert.match(html, /\.plan \.price\{[^}]*font-size:2\.6rem/);
    assert.match(html, /\.plan ul\{[^}]*align-content:start/);
    assert.match(html, /\.plan li\{display:block;position:relative;padding-left:26px\}/);
    assert.match(html, /\.plan li::before\{[^}]*position:absolute;left:0/);
    assert.match(html, /border-radius:var\(--radius\)/);
    // Custom CTA is Book a Demo to the homepage modal, not a preselected plan.
    assert.match(html, /data-plan="enterprise"[\s\S]*href="\/#book-demo">Book a Demo</);
  });
}

test('netlify.toml sends X-Robots-Tag noindex for /pricing and /dashboard/pricing', () => {
  const toml = read('netlify.toml');
  for (const path of ['/pricing', '/pricing/', '/pricing/*', '/dashboard/pricing', '/dashboard/pricing/', '/dashboard/pricing/*']) {
    const block = new RegExp(
      String.raw`\[\[headers\]\]\s+for = "${path.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}"\s+\[headers\.values\]\s+X-Robots-Tag = "noindex, nofollow"`,
    );
    assert.match(toml, block, path);
  }
});
