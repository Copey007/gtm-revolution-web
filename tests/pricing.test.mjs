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

test('root and dashboard pricing pages stay in sync on public prices', () => {
  const a = read('pricing/index.html');
  const b = read('dashboard/pricing/index.html');
  assert.equal(a.includes('data-price-cents="49900"'), true);
  assert.equal(b.includes('data-price-cents="49900"'), true);
  assert.equal(a.includes('data-price-cents="99900"'), b.includes('data-price-cents="99900"'));
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

test('sitemap lists /pricing/', () => {
  const xml = read('sitemap.xml');
  assert.match(xml, /<loc>https:\/\/a-gent\.co\/pricing\/<\/loc>/);
});

test('site generators point Fleet pricing at /pricing/', () => {
  for (const p of ['generator/generate_site.py', 'tools/generate_site.py']) {
    const src = read(p);
    assert.match(src, /FLEET_PRICING = '\/pricing\/'/);
    assert.equal(src.includes('https://fleet.a-gent.co/pricing'), false);
  }
});
