#!/usr/bin/env node
/**
 * validate-data.js — integrity + statistical-consistency checks for the canonical
 * dataset (data/mortality-data.json). Run before shipping data updates.
 *
 *   node scripts/validate-data.js
 *
 * Exits 0 if all ERROR-level checks pass (WARN-level notes don't fail the run),
 * non-zero otherwise. Mirrors the invariants the credibility process relies on.
 */
const fs = require('fs');
const path = require('path');

const FILE = path.join(__dirname, '..', 'data', 'mortality-data.json');
const errors = [];
const warns = [];
const ok = [];
const check = (cond, label, list = errors) => (cond ? ok.push(label) : list.push(label));

let d;
try {
  d = JSON.parse(fs.readFileSync(FILE, 'utf8'));
} catch (e) {
  console.error(`FATAL: ${FILE} is not valid JSON — ${e.message}`);
  process.exit(2);
}

const m = d.metadata;
const incidents = d.incidents || [];
const platforms = d.platforms || [];
const sum = (arr, k) => arr.reduce((s, x) => s + (Number(x[k]) || 0), 0);

// ── structural integrity ───────────────────────────────────────
check(incidents.length === m.total_incidents,
  `incidents array (${incidents.length}) === metadata.total_incidents (${m.total_incidents})`);

const ids = incidents.map(i => i.id);
check(new Set(ids).size === ids.length, 'no duplicate incident ids');

const required = ['id', 'date', 'platform', 'verification_level', 'sources'];
const missing = incidents.filter(i => required.some(k => i[k] == null ||
  (k === 'sources' && (!Array.isArray(i.sources) || i.sources.length === 0))));
check(missing.length === 0,
  `every incident has ${required.join('/')}` + (missing.length ? ` (offenders: ${missing.map(i => i.id).join(', ')})` : ''));

const badDate = incidents.filter(i => !/^\d{4}(-\d{2}(-\d{2})?)?$/.test(i.date || ''));
check(badDate.length === 0,
  'all incident dates are YYYY[-MM[-DD]]' + (badDate.length ? ` (bad: ${badDate.map(i => i.id).join(', ')})` : ''));

// ── statistical consistency ─────────────────────────────────────
check(m.ai_users_deceased + m.third_party_victims === m.total_fatalities,
  `ai_users_deceased (${m.ai_users_deceased}) + third_party_victims (${m.third_party_victims}) === total_fatalities (${m.total_fatalities})`);

check(sum(platforms, 'deaths') === m.ai_users_deceased,
  `Σ platform.deaths (${sum(platforms, 'deaths')}) === ai_users_deceased (${m.ai_users_deceased})`);

// Known, documented exception: Margaux Whittemore is in the third-party total but
// not in any platform's third_party_fatalities (killer found not criminally responsible).
const tpSum = sum(platforms, 'third_party_fatalities');
check(tpSum + 1 === m.third_party_victims,
  `Σ platform.third_party_fatalities (${tpSum}) + 1 documented exception === third_party_victims (${m.third_party_victims})`);

const dby = (d.statistics && d.statistics.deaths_by_year) || {};
const dbySum = Object.values(dby).reduce((s, n) => s + Number(n), 0);
check(dbySum === m.total_incidents,
  `Σ deaths_by_year (${dbySum}) === total_incidents (${m.total_incidents})`, warns);

// ── currency ────────────────────────────────────────────────────
const maxDate = incidents.map(i => i.date).sort().slice(-1)[0];
check((m.last_updated || '') >= (maxDate || ''),
  `last_updated (${m.last_updated}) >= latest incident date (${maxDate})`, warns);

// ── report ──────────────────────────────────────────────────────
ok.forEach(l => console.log(`  PASS  ${l}`));
warns.forEach(l => console.log(`  WARN  ${l}`));
errors.forEach(l => console.log(`  FAIL  ${l}`));
console.log(`\n${ok.length} passed · ${warns.length} warnings · ${errors.length} errors`);
process.exit(errors.length ? 1 : 0);
