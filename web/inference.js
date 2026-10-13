/* ===== SentimentGreen - Main Inference Engine ===== */

let MODEL = null;
let METRICS = null;

// ── Load model & metrics ──────────────────────────────────────────
async function loadModel() {
  const [mRes, meRes] = await Promise.all([
    fetch("model/model.json"),
    fetch("model/metrics.json"),
  ]);
  MODEL = await mRes.json();
  METRICS = await meRes.json();
  MODEL._stopSet = new Set(MODEL.stopwords);
  MODEL._vocabMap = {};
  MODEL.vocab.forEach((w, i) => (MODEL._vocabMap[w] = i));
  return { MODEL, METRICS };
}

// ── TF-IDF inference (sparse, browser-side) ───────────────────────
function tfidfVector(tokens) {
  const V = MODEL.vocab.length;
  const idf = MODEL.idf;
  const vocabMap = MODEL._vocabMap;
  const tf = {};
  const ngrams = [];
  // unigrams
  tokens.forEach((w) => ngrams.push(w));
  // bigrams
  for (let i = 0; i < tokens.length - 1; i++) ngrams.push(tokens[i] + " " + tokens[i + 1]);
  ngrams.forEach((g) => { tf[g] = (tf[g] || 0) + 1; });
  const total = ngrams.length || 1;
  const vec = new Float64Array(V);
  Object.entries(tf).forEach(([g, cnt]) => {
    const idx = vocabMap[g];
    if (idx !== undefined) vec[idx] = (cnt / total) * idf[idx];
  });
  // L2 norm
  let norm = 0;
  vec.forEach((v) => (norm += v * v));
  norm = Math.sqrt(norm) || 1;
  for (let i = 0; i < V; i++) vec[i] /= norm;
  return vec;
}

function predictNB(vec) {
  const { class_log_prior, feature_log_prob } = MODEL.nb;
  const labels = MODEL.labels;
  const scores = class_log_prior.map((prior, c) => {
    let s = prior;
    for (let i = 0; i < vec.length; i++) if (vec[i] > 0) s += feature_log_prob[c][i];
    return s;
  });
  const maxS = Math.max(...scores);
  const exps = scores.map((s) => Math.exp(s - maxS));
  const sum = exps.reduce((a, b) => a + b, 0);
  const probs = exps.map((e) => e / sum);
  const idx = probs.indexOf(Math.max(...probs));
  return { label: labels[idx], probs: Object.fromEntries(labels.map((l, i) => [l, probs[i]])) };
}

function predictSVM(vec) {
  const { coef, intercept } = MODEL.svm;
  const labels = MODEL.labels;
  const scores = coef.map((c, ci) => {
    let s = intercept[ci];
    for (let i = 0; i < vec.length; i++) s += c[i] * vec[i];
    return s;
  });
  const idx = scores.indexOf(Math.max(...scores));
  const exps = scores.map((s) => Math.exp(s));
  const sum = exps.reduce((a, b) => a + b, 0);
  const probs = exps.map((e) => e / sum);
  return { label: labels[idx], probs: Object.fromEntries(labels.map((l, i) => [l, probs[i]])) };
}

function analyze(text, algo = "svm") {
  const { cleanText, filterStem } = window.PreprocessLib;
  const cleaned = cleanText(text);
  const tokens = filterStem(cleaned, MODEL._stopSet);
  if (tokens.length === 0) return { label: "netral", probs: { negatif: 0.0, netral: 1.0, positif: 0.0 }, tokens, cleaned };
  const vec = tfidfVector(tokens);
  const result = algo === "nb" ? predictNB(vec) : predictSVM(vec);
  return { ...result, tokens, cleaned };
}

if (typeof module !== "undefined") module.exports = { loadModel, analyze };
