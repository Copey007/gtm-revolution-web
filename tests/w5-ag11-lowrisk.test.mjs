import assert from 'node:assert/strict';
import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { test } from 'node:test';
import { execSync } from 'node:child_process';

const ROOT = join(import.meta.dirname, '..');

function walkHtml(dir = ROOT, acc = []) {
  for (const name of readdirSync(dir)) {
    if (name === 'node_modules' || name === '.git') continue;
    const p = join(dir, name);
    const st = statSync(p);
    if (st.isDirectory()) walkHtml(p, acc);
    else if (name.endsWith('.html')) acc.push(p);
  }
  return acc;
}

function rel(p) {
  return relative(ROOT, p).split('\\').join('/');
}

const htmlFiles = walkHtml().filter((p) => !/^google.+\.html$/.test(rel(p)));
const navPages = htmlFiles.filter((p) => readFileSync(p, 'utf8').includes('<header class="nav">'));

test('favicon suite files exist at site root and dashboard mirror', () => {
  const files = [
    'favicon.ico',
    'favicon-16x16.png',
    'favicon-32x32.png',
    'apple-touch-icon.png',
    'icon.svg',
    'icon-192.png',
    'icon-512.png',
    'icon-512-maskable.png',
    'site.webmanifest',
    'assets/brand/og-image-blog.png',
    'dashboard/favicon.ico',
    'dashboard/favicon-16x16.png',
    'dashboard/favicon-32x32.png',
    'dashboard/apple-touch-icon.png',
    'dashboard/icon.svg',
    'dashboard/site.webmanifest',
    'dashboard/assets/brand/og-image-blog.png',
  ];
  for (const f of files) {
    assert.ok(existsSync(join(ROOT, f)), `missing ${f}`);
  }
});

test('every page (except verification files) has the favicon suite', () => {
  for (const p of htmlFiles) {
    const t = readFileSync(p, 'utf8');
    assert.match(t, /href="\/favicon\.ico"/, rel(p));
    assert.match(t, /href="\/favicon-16x16\.png"/, rel(p));
    assert.match(t, /href="\/favicon-32x32\.png"/, rel(p));
    assert.match(t, /href="\/icon\.svg"/, rel(p));
    assert.match(t, /rel="apple-touch-icon"/, rel(p));
    assert.match(t, /href="\/site\.webmanifest"/, rel(p));
    assert.equal(t.includes('assets/brand/favicon.ico'), false, `legacy favicon left on ${rel(p)}`);
  }
});

test('shared-header pages have skip link, drawer markup, main landmark, logo dimensions, and drawer script', () => {
  assert.ok(navPages.length > 200, `expected a full site of nav pages, got ${navPages.length}`);
  for (const p of navPages) {
    const t = readFileSync(p, 'utf8');
    const r = rel(p);
    assert.match(t, /class="skip-link"[^>]*href="#main"/, r);
    assert.match(t, /class="nav-toggle"/, r);
    assert.match(t, /id="site-nav"/, r);
    assert.match(t, /class="nav-scrim"/, r);
    assert.match(t, /<main[^>]*id="main"[^>]*tabindex="-1"/, r);
    assert.match(t, /querySelector\('\.nav-toggle'\)/, r);
    const logos = t.match(/<img\b[^>]*agent-logo-master\.svg[^>]*>/g) || [];
    assert.ok(logos.length >= 1, `no wordmark logo on ${r}`);
    for (const logo of logos) {
      assert.match(logo, /width="1600"/, `${r} ${logo}`);
      assert.match(logo, /height="420"/, `${r} ${logo}`);
    }
  }
});

test('Google Fonts links use display=swap', () => {
  for (const p of htmlFiles) {
    const t = readFileSync(p, 'utf8');
    const hrefs = t.match(/fonts\.googleapis\.com\/css2\?[^"']+/g) || [];
    for (const href of hrefs) {
      assert.match(href, /display=swap/, `${rel(p)} ${href}`);
    }
  }
});

test('pages with og:image include og:image:alt; /blog/ uses og-image-blog.png', () => {
  const blogIndex = readFileSync(join(ROOT, 'blog/index.html'), 'utf8');
  assert.match(blogIndex, /assets\/brand\/og-image-blog\.png/);
  assert.match(blogIndex, /property="og:image:alt"/);
  for (const p of htmlFiles) {
    const t = readFileSync(p, 'utf8');
    if (t.includes('property="og:image"')) {
      assert.match(t, /property="og:image:alt"/, rel(p));
    }
  }
});

test('contrast Option A tokens are in both design-system stylesheets', () => {
  const root = readFileSync(join(ROOT, 'assets/css/fleet-master.css'), 'utf8');
  const dash = readFileSync(join(ROOT, 'dashboard/assets/css/fleet-master.css'), 'utf8');
  for (const css of [root, dash]) {
    assert.match(css, /--muted:\s*#a1a1a6/);
    assert.match(css, /--dim:\s*#8a8a90/);
    assert.match(css, /\.skip-link/);
    assert.match(css, /@media \(max-width:880px\)/);
    assert.match(css, /\.nav-toggle/);
  }
});

test('sitemap lastmod is refreshed, missing posts are present, and /pricing is absent', () => {
  const xml = readFileSync(join(ROOT, 'sitemap.xml'), 'utf8');
  assert.equal(xml.includes('/pricing'), false);
  assert.doesNotMatch(xml, /<lastmod>2026-06-13<\/lastmod>/);
  assert.match(xml, /<lastmod>2026-11-27<\/lastmod>/);
  assert.match(xml, /a-gent-ava-quinn-daily-ava-054-how-to-build-a-winning-icp-with-ai\//);
  const dash = readFileSync(join(ROOT, 'dashboard/sitemap.xml'), 'utf8');
  assert.equal(dash.includes('/pricing'), false);
  assert.match(dash, /<lastmod>2026-11-27<\/lastmod>/);
});

test('netlify.toml serves webmanifest with the correct Content-Type', () => {
  const toml = readFileSync(join(ROOT, 'netlify.toml'), 'utf8');
  assert.match(toml, /for = "\/\*\.webmanifest"/);
  assert.match(toml, /Content-Type = "application\/manifest\+json"/);
});

test('diff against main introduces no unresolved review slots and touches no pricing/ files', () => {
  const names = execSync('git diff --name-only origin/main...HEAD', { cwd: ROOT, encoding: 'utf8' });
  // During the test run HEAD may equal the working tree if we haven't committed;
  // also inspect the working tree vs origin/main.
  const names2 = execSync('git diff --name-only origin/main', { cwd: ROOT, encoding: 'utf8' });
  const all = `${names}\n${names2}`;
  assert.equal(all.includes('pricing/'), false, all);
  const slot = '{' + '{MARK';
  const markDiff = execSync('git diff origin/main -- . && git diff --cached origin/main -- .', {
    cwd: ROOT,
    encoding: 'utf8',
    maxBuffer: 50 * 1024 * 1024,
  });
  assert.equal(markDiff.includes(slot), false);
});

test('security page copy is untouched (favicon links only)', () => {
  const diff = execSync('git diff origin/main -- security/index.html', { cwd: ROOT, encoding: 'utf8' });
  const minus = diff.split('\n').filter((l) => l.startsWith('-') && !l.startsWith('---'));
  const plus = diff.split('\n').filter((l) => l.startsWith('+') && !l.startsWith('+++'));
  assert.equal(minus.length, 0, `unexpected removals in security/index.html:\n${minus.join('\n')}`);
  assert.ok(plus.every((l) => /favicon|apple-touch|icon\.svg|webmanifest|theme-color|W1 \/ AG-11/.test(l)), plus.join('\n'));
});

test('Gmail contact strings and unresolved review slots are not introduced; form error copy stays on main', () => {
  const slot = '{' + '{MARK';
  for (const f of ['index.html', 'privacy/index.html', 'generator/generate_site.py', 'tools/generate_site.py']) {
    const t = readFileSync(join(ROOT, f), 'utf8');
    assert.equal(t.includes(slot), false, f);
    assert.match(t, /mark\.cope\.roarr@gmail\.com/, f);
  }
  const idx = readFileSync(join(ROOT, 'index.html'), 'utf8');
  assert.match(idx, /sb_publishable_/);
});
