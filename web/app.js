/* ===========================
   SentimentGreen – app.js
   Main application controller
   =========================== */

const GH_TOKEN = ""; // token tidak disimpan di client
const COLORS = { positif: "#34d399", netral: "#94a3b8", negatif: "#f87171" };
const LABELS = ["negatif", "netral", "positif"];

let currentAlgo = "svm";
let modelReady = false;

// ── Init ──────────────────────────────────────────────────────────
window.addEventListener("DOMContentLoaded", async () => {
  setupNavScroll();
  setupCharCount();
  await initModel();
});

async function initModel() {
  try {
    const { MODEL, METRICS } = await loadModel();
    modelReady = true;
    populateStats(METRICS);
    renderMetricsGrid(METRICS);
    renderPerClass(METRICS);
    drawPieChart(METRICS);
    drawBarChart(METRICS);
    console.log("✅ Model loaded:", MODEL.vocab.length, "vocab");
  } catch (e) {
    console.error("Model load error:", e);
    showModelFallback();
  }
}

// ── Nav scroll effect ─────────────────────────────────────────────
function setupNavScroll() {
  window.addEventListener("scroll", () => {
    const nav = document.getElementById("navbar");
    nav.style.background = window.scrollY > 60
      ? "rgba(6,11,18,0.95)" : "rgba(6,11,18,0.75)";
  });
}

// ── Char count ────────────────────────────────────────────────────
function setupCharCount() {
  const ta = document.getElementById("tweetInput");
  const cc = document.getElementById("charCount");
  ta.addEventListener("input", () => {
    const n = ta.value.length;
    cc.textContent = `${n} / 280`;
    cc.style.color = n > 260 ? "#f87171" : "var(--text3)";
  });
  ta.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && e.ctrlKey) runSingle();
  });
}

// ── Model selector ────────────────────────────────────────────────
function selectModel(algo) {
  currentAlgo = algo;
  document.getElementById("btnSVM").classList.toggle("active", algo === "svm");
  document.getElementById("btnNB").classList.toggle("active", algo === "nb");
}

// ── Example ───────────────────────────────────────────────────────
function setExample(txt) {
  const ta = document.getElementById("tweetInput");
  ta.value = txt;
  ta.dispatchEvent(new Event("input"));
  runSingle();
}

// ── Single analysis ───────────────────────────────────────────────
async function runSingle() {
  if (!modelReady) { alert("Model masih loading, tunggu sebentar..."); return; }
  const text = document.getElementById("tweetInput").value.trim();
  if (!text) { document.getElementById("tweetInput").focus(); return; }

  setAnalyzeLoading(true);
  await sleep(120); // allow repaint
  const res = analyze(text, currentAlgo);
  setAnalyzeLoading(false);
  renderResult(res);
}

function setAnalyzeLoading(on) {
  document.getElementById("btnAnalyzeLabel").textContent = on ? "Menganalisis..." : "Analisis Sentimen";
  document.getElementById("btnSpinner").classList.toggle("hidden", !on);
}

function renderResult(res) {
  const box = document.getElementById("resultBox");
  box.classList.remove("hidden");

  // badge
  const badge = document.getElementById("resultBadge");
  badge.textContent = res.label;
  badge.className = `sentiment-badge badge-${res.label}`;

  // confidence
  const conf = res.probs[res.label];
  document.getElementById("resultConf").textContent =
    `Confidence: ${(conf * 100).toFixed(1)}%`;

  // prob bars
  const bars = document.getElementById("probBars");
  bars.innerHTML = LABELS.map(l => `
    <div class="prob-row">
      <span class="prob-label">${l}</span>
      <div class="prob-bar-bg">
        <div class="prob-bar-fill fill-${l}" style="width:${(res.probs[l]*100).toFixed(1)}%"></div>
      </div>
      <span class="prob-pct">${(res.probs[l]*100).toFixed(1)}%</span>
    </div>`).join("");

  // tokens
  document.getElementById("tokenList").innerHTML =
    res.tokens.slice(0, 30).map(t => `<span class="token">${t}</span>`).join("") +
    (res.tokens.length > 30 ? `<span class="token">+${res.tokens.length-30}</span>` : "");
}

// ── Batch CSV ─────────────────────────────────────────────────────
function handleDrop(e) {
  e.preventDefault();
  document.getElementById("dropZone").classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file) processCSV(file);
}
function handleFile(e) { if (e.target.files[0]) processCSV(e.target.files[0]); }

async function processCSV(file) {
  if (!modelReady) { alert("Model masih loading..."); return; }
  const text = await file.text();
  const lines = text.split("\n").filter(l => l.trim());
  const headers = lines[0].split(",").map(h => h.trim().replace(/"/g, "").toLowerCase());
  const msgIdx = headers.indexOf("message") >= 0 ? headers.indexOf("message") : 0;
  const rows = lines.slice(1).filter(l => l.trim());

  document.getElementById("batchProgress").classList.remove("hidden");
  document.getElementById("batchResult").classList.add("hidden");

  const results = [];
  const CHUNK = 50;
  for (let i = 0; i < rows.length; i++) {
    if (i % CHUNK === 0) {
      document.getElementById("progressBar").style.width = `${(i/rows.length*100).toFixed(0)}%`;
      document.getElementById("progressText").textContent = `Memproses ${i}/${rows.length} tweet...`;
      await sleep(0);
    }
    const cols = parseCSVLine(rows[i]);
    const msg = cols[msgIdx] || cols[0] || "";
    const res = analyze(msg, currentAlgo);
    results.push({ tweet: msg.slice(0, 80), label: res.label, conf: (res.probs[res.label]*100).toFixed(1) });
  }

  document.getElementById("progressBar").style.width = "100%";
  document.getElementById("progressText").textContent = `Selesai! ${results.length} tweet dianalisis.`;
  await sleep(400);
  document.getElementById("batchProgress").classList.add("hidden");
  renderBatchResult(results);
}

function parseCSVLine(line) {
  const result = []; let cur = ""; let inQ = false;
  for (const c of line) {
    if (c === '"') inQ = !inQ;
    else if (c === ',' && !inQ) { result.push(cur.trim()); cur = ""; }
    else cur += c;
  }
  result.push(cur.trim());
  return result;
}

function renderBatchResult(results) {
  const box = document.getElementById("batchResult");
  box.classList.remove("hidden");
  const counts = { positif: 0, netral: 0, negatif: 0 };
  results.forEach(r => counts[r.label]++);
  const total = results.length;

  const dlCSV = () => {
    const csv = "tweet,sentimen,confidence\n" +
      results.map(r => `"${r.tweet.replace(/"/g,'""')}",${r.label},${r.conf}%`).join("\n");
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([csv], {type:"text/csv"}));
    a.download = "hasil_sentimen.csv"; a.click();
  };

  box.innerHTML = `
    <div class="batch-summary">
      ${Object.entries(counts).map(([l,n]) => `
        <span class="batch-chip badge-${l}">${l.charAt(0).toUpperCase()+l.slice(1)}: ${n} (${(n/total*100).toFixed(1)}%)</span>`).join("")}
      <span class="batch-chip" style="background:var(--surface2);color:var(--text2)">Total: ${total}</span>
    </div>
    <button class="btn-primary" onclick="(${dlCSV.toString()})()" style="margin-bottom:14px;font-size:0.82rem;padding:8px 18px">
      ⬇ Download Hasil CSV
    </button>
    <div class="batch-table-wrap">
      <table class="batch-table">
        <thead><tr><th>#</th><th>Tweet</th><th>Sentimen</th><th>Conf.</th></tr></thead>
        <tbody>${results.slice(0, 50).map((r,i) => `
          <tr>
            <td style="color:var(--text3)">${i+1}</td>
            <td style="max-width:280px;word-break:break-word">${escHtml(r.tweet)}${results[i]?.tweet?.length>=80?"…":""}</td>
            <td><span class="sentiment-badge badge-${r.label}" style="font-size:0.75rem;padding:2px 10px">${r.label}</span></td>
            <td style="color:var(--green)">${r.conf}%</td>
          </tr>`).join("")}
          ${results.length > 50 ? `<tr><td colspan="4" style="text-align:center;color:var(--text3);padding:12px">…dan ${results.length-50} lainnya (download CSV untuk data lengkap)</td></tr>` : ""}
        </tbody>
      </table>
    </div>`;
}

// ── Stats from metrics.json ───────────────────────────────────────
function populateStats(m) {
  const fmt = (n) => (n >= 1000 ? (n/1000).toFixed(1)+"k" : n.toLocaleString());
  const pct = (n) => (n*100).toFixed(1)+"%";
  document.getElementById("statTotal").textContent = fmt(m.dataset?.used || 0);
  document.getElementById("statAcc").textContent = pct(m.svm?.accuracy || 0);
  document.getElementById("statF1").textContent = pct(m.svm?.f1_macro || 0);
  document.getElementById("statVocab").textContent = fmt(m.dataset?.vocab || 0);
}

function renderMetricsGrid(m) {
  const best = m.best_model || "svm";
  const bm = m[best];
  const grid = document.getElementById("metricsGrid");
  const items = [
    { icon: "🎯", val: (bm.accuracy*100).toFixed(2)+"%", label: "Akurasi", sub: `Model: ${best.toUpperCase()}` },
    { icon: "📐", val: (bm.precision_macro*100).toFixed(2)+"%", label: "Precision (Macro)", sub: "Rata-rata 3 kelas" },
    { icon: "🔁", val: (bm.recall_macro*100).toFixed(2)+"%", label: "Recall (Macro)", sub: "Rata-rata 3 kelas" },
    { icon: "⚖️", val: (bm.f1_macro*100).toFixed(2)+"%", label: "F1-Score (Macro)", sub: "Harmonic mean P&R" },
  ];
  grid.innerHTML = items.map(i => `
    <div class="metric-card">
      <div class="metric-icon">${i.icon}</div>
      <div class="metric-value">${i.val}</div>
      <div class="metric-label">${i.label}</div>
      <div class="metric-sub">${i.sub}</div>
    </div>`).join("");
}

function renderPerClass(m) {
  const best = m.best_model || "svm";
  const pc = m[best]?.per_class || {};
  const grid = document.getElementById("perClassGrid");
  const clrMap = { positif: "var(--green)", netral: "var(--gray)", negatif: "var(--red)" };
  grid.innerHTML = LABELS.map(lab => {
    const d = pc[lab] || {};
    return `
      <div class="class-card">
        <div class="class-name" style="color:${clrMap[lab]}">● ${lab}</div>
        <div class="class-row"><span>Precision</span><span>${((d.precision||0)*100).toFixed(2)}%</span></div>
        <div class="class-row"><span>Recall</span><span>${((d.recall||0)*100).toFixed(2)}%</span></div>
        <div class="class-row"><span>F1-Score</span><span>${((d["f1-score"]||0)*100).toFixed(2)}%</span></div>
        <div class="class-row"><span>Support</span><span>${d.support||0}</span></div>
      </div>`;
  }).join("");
}

// ── Charts ────────────────────────────────────────────────────────
function drawPieChart(m) {
  const canvas = document.getElementById("pieChart");
  const ctx = canvas.getContext("2d");
  const dist = m.dataset?.distribution || {};
  const data = LABELS.map(l => dist[l] || 0);
  const total = data.reduce((a,b)=>a+b,0);
  const colors = LABELS.map(l => COLORS[l]);
  const CX = canvas.width/2, CY = canvas.height/2, R = Math.min(CX,CY)-30, IR = R*0.52;

  ctx.clearRect(0,0,canvas.width,canvas.height);
  let start = -Math.PI/2;
  data.forEach((v,i) => {
    const angle = (v/total)*Math.PI*2;
    ctx.beginPath(); ctx.moveTo(CX,CY);
    ctx.arc(CX,CY,R,start,start+angle);
    ctx.closePath(); ctx.fillStyle = colors[i]; ctx.fill();
    // label
    const mid = start + angle/2;
    const lx = CX + (R*0.75)*Math.cos(mid);
    const ly = CY + (R*0.75)*Math.sin(mid);
    ctx.fillStyle="#fff"; ctx.font="bold 11px Inter"; ctx.textAlign="center"; ctx.textBaseline="middle";
    if (v/total > 0.05) ctx.fillText(`${(v/total*100).toFixed(1)}%`, lx, ly);
    start += angle;
  });
  // donut hole
  ctx.beginPath(); ctx.arc(CX,CY,IR,0,Math.PI*2);
  ctx.fillStyle="#0b1520"; ctx.fill();
  // center text
  ctx.fillStyle="var(--text)"; ctx.font="bold 14px Inter"; ctx.textAlign="center"; ctx.textBaseline="middle";
  ctx.fillStyle="#e2e8f0"; ctx.fillText(total.toLocaleString(), CX, CY-8);
  ctx.font="11px Inter"; ctx.fillStyle="#64748b"; ctx.fillText("total tweet", CX, CY+10);
  // legend
  const ly0 = canvas.height - 18;
  LABELS.forEach((l,i) => {
    const lx = 24 + i * (canvas.width/3);
    ctx.fillStyle=COLORS[l]; ctx.fillRect(lx,ly0-6,12,12);
    ctx.fillStyle="#94a3b8"; ctx.font="11px Inter"; ctx.textAlign="left";
    ctx.fillText(l.charAt(0).toUpperCase()+l.slice(1), lx+16, ly0+1);
  });
}

function drawBarChart(m) {
  const canvas = document.getElementById("barChart");
  const ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height;
  const PAD = { top: 30, right: 20, bottom: 50, left: 50 };
  const metrics = ["accuracy","precision_macro","recall_macro","f1_macro"];
  const labels = ["Accuracy","Precision","Recall","F1-Score"];
  const nbVals = metrics.map(k => (m.naive_bayes?.[k]||0)*100);
  const svmVals = metrics.map(k => (m.svm?.[k]||0)*100);

  ctx.clearRect(0,0,W,H);
  const cW = W - PAD.left - PAD.right;
  const cH = H - PAD.top - PAD.bottom;
  const grpW = cW / metrics.length;
  const barW = grpW * 0.3;

  // Y gridlines
  for (let y = 0; y <= 100; y += 20) {
    const py = PAD.top + cH - (y/100)*cH;
    ctx.strokeStyle = "rgba(255,255,255,0.06)"; ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(PAD.left, py); ctx.lineTo(PAD.left+cW, py); ctx.stroke();
    ctx.fillStyle="#64748b"; ctx.font="10px Inter"; ctx.textAlign="right";
    ctx.fillText(y+"%", PAD.left-6, py+4);
  }

  [nbVals, svmVals].forEach((vals, mi) => {
    const color = mi===0 ? "#60a5fa" : "#34d399";
    vals.forEach((v,i) => {
      const x = PAD.left + i*grpW + (mi===0 ? grpW*0.12 : grpW*0.52);
      const h = (v/100)*cH;
      const y = PAD.top + cH - h;
      const grad = ctx.createLinearGradient(0,y,0,y+h);
      grad.addColorStop(0, color); grad.addColorStop(1, color+"55");
      ctx.fillStyle = grad;
      const rx = 4;
      ctx.beginPath();
      ctx.moveTo(x+rx,y); ctx.lineTo(x+barW-rx,y);
      ctx.arcTo(x+barW,y,x+barW,y+rx,rx); ctx.lineTo(x+barW,y+h);
      ctx.lineTo(x,y+h); ctx.arcTo(x,y,x+rx,y,rx); ctx.closePath();
      ctx.fill();
      ctx.fillStyle="#fff"; ctx.font="bold 9px Inter"; ctx.textAlign="center";
      ctx.fillText(v.toFixed(1), x+barW/2, y-4);
    });
  });

  // X labels
  labels.forEach((l,i) => {
    const x = PAD.left + i*grpW + grpW/2;
    ctx.fillStyle="#94a3b8"; ctx.font="11px Inter"; ctx.textAlign="center";
    ctx.fillText(l, x, H-PAD.bottom+18);
  });

  // Legend
  [["Naive Bayes","#60a5fa"],["SVM","#34d399"]].forEach(([name,color],i) => {
    const lx = PAD.left + i*130;
    ctx.fillStyle=color; ctx.fillRect(lx,10,14,10);
    ctx.fillStyle="#94a3b8"; ctx.font="11px Inter"; ctx.textAlign="left";
    ctx.fillText(name, lx+18, 20);
  });
}

// ── Fallback ──────────────────────────────────────────────────────
function showModelFallback() {
  document.getElementById("metricsGrid").innerHTML = `
    <div class="metric-card" style="grid-column:1/-1;text-align:center;color:var(--text2)">
      <div style="font-size:2rem;margin-bottom:12px">⚠️</div>
      <p>Model belum tersedia. Pastikan file <code>model/model.json</code> ada di folder web.</p>
      <p style="font-size:0.8rem;margin-top:8px">Jalankan <code>python ml/train.py</code> untuk generate model.</p>
    </div>`;
}

// ── Helpers ───────────────────────────────────────────────────────
const sleep = ms => new Promise(r => setTimeout(r, ms));
const escHtml = s => s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");

// ── Code Tab Switcher ─────────────────────────────────────────────
function switchCodeTab(tabId, btn) {
  document.querySelectorAll(".code-tab-panel").forEach(p => p.classList.add("hidden"));
  document.querySelectorAll(".code-tab-btn").forEach(b => b.classList.remove("active"));
  const target = document.getElementById(tabId);
  if (target) target.classList.remove("hidden");
  if (btn) btn.classList.add("active");

  const tag = document.getElementById("codeLangTag");
  if (tag) {
    if (tabId === "tab-train") tag.textContent = "Python 3.10 / scikit-learn";
    else if (tabId === "tab-stem") tag.textContent = "JavaScript (ES6) / Regex Engine";
    else if (tabId === "tab-infer") tag.textContent = "JavaScript (ES6) / Math Vector";
  }
}
