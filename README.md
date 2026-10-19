# Count Math

Counting arrangements arithmetic. A group of 10 people makes 45 handshakes, not 90.

## What it computes

- **The order truth** - picking k of n different things, with order mattering and without.
- **The pair truth** - everyone paired with everyone else once (handshakes, matches, links), n x (n - 1) / 2 rather than n x (n - 1).
- **The word truth** - different orders of the letters of a word, dividing out repeated letters (BANANA is 60, not 720).

Things are from 1 to 100, people from 2 to 1000000, words from 2 to 20 letters (A to Z). Arithmetic is exact with big integers. Counts over 15 digits are shown as about d.dd x 10^e.

## Boundary

Arithmetic only. It assumes the counting rules it states, such as every pick being different. It does not know your real situation, so check the rules fit it.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror (math.perm, math.comb, brute force for short words) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (47 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/countmath/
Repo: https://github.com/iLanis-agent/countmath
