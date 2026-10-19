// Count Math engine - arrangements, pairs and repeated letters, counted exactly.
// Mirrored by oracle.py; keep the op order identical.
// Arithmetic is exact (big integers). Numbers over 15 digits are shown as about d.dd x 10^e.

function _int(text, label, lo, hi) {
  var t = typeof text === "string" ? text.trim() : "";
  var err = label + " must be a whole number from " + lo + " to " + hi;
  if (!/^[0-9]{1,8}$/.test(t)) throw new Error(err);
  var v = BigInt(t);
  if (v < BigInt(lo) || v > BigInt(hi)) throw new Error(err);
  return v;
}

function _fact(n) { var r = 1n; for (var i = 2n; i <= n; i++) r *= i; return r; }

// A count as text: commas every 3 digits, or about d.dd x 10^e when it is over 15 digits.
function _num(x) {
  var s = String(x);
  if (s.length <= 15) return s.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  var r = (BigInt(s.slice(0, 4)) + 5n) / 10n, ex = s.length - 1;
  if (r === 1000n) { r = 100n; ex += 1; }
  var lo = String(r % 100n);
  while (lo.length < 2) lo = "0" + lo;
  return "about " + (r / 100n) + "." + lo + " x 10^" + ex;
}
function _ways(x) { return _num(x) + (x === 1n ? " way" : " ways"); }

// The order truth: picking k of n things, with and without order mattering.
function orderTruth(n, k) {
  var nn = _int(n, "things", 1, 100), kk = _int(k, "picks", 0, 100);
  if (kk > nn) throw new Error("picks cannot be more than things");
  var perm = 1n;
  for (var i = 0n; i < kk; i++) perm *= nn - i;
  var comb = perm / _fact(kk);
  var prod = "";
  if (kk >= 2n && kk <= 6n) {
    var f = [];
    for (var j = 0n; j < kk; j++) f.push(String(nn - j));
    prod = " (" + f.join(" x ") + ")";
  }
  return "Picking " + kk + " of " + nn + (nn === 1n ? " thing" : " things") + ": " + _ways(perm) + " when order matters" + prod +
    ", " + _ways(comb) + " when order does not matter.";
}

// The pair truth: everyone paired with everyone else once.
function pairTruth(n) {
  var nn = _int(n, "people", 2, 1000000);
  var pairs = nn * (nn - 1n) / 2n;
  return nn + " people each shaking hands once with every other person make " + _num(pairs) + (pairs === 1n ? " handshake" : " handshakes") +
    " (" + nn + " x " + (nn - 1n) + " / 2, not " + nn + " x " + (nn - 1n) + " = " + _num(nn * (nn - 1n)) + ").";
}

// The word truth: different orders of the letters of a word.
function wordTruth(word) {
  var w = typeof word === "string" ? word.trim().toUpperCase() : "";
  if (!/^[A-Z]{2,20}$/.test(w)) throw new Error("enter 2 to 20 letters, A to Z only");
  var counts = {};
  for (var i = 0; i < w.length; i++) counts[w[i]] = (counts[w[i]] || 0) + 1;
  var n = BigInt(w.length), total = _fact(n), den = 1n, reps = [];
  Object.keys(counts).sort().forEach(function (c) {
    den *= _fact(BigInt(counts[c]));
    if (counts[c] > 1) reps.push(c + " appears " + counts[c] + " times");
  });
  var orders = total / den;
  var why;
  if (reps.length === 0) why = "because no letter repeats";
  else if (reps.length === 1) why = "instead of " + _num(total) + ", because " + reps[0];
  else why = "instead of " + _num(total) + ", because " + reps.slice(0, -1).join(", ") + " and " + reps[reps.length - 1];
  return "The letters of " + w + " (" + w.length + " letters) can be arranged in " + _num(orders) + (orders === 1n ? " different order, " : " different orders, ") + why + ".";
}
