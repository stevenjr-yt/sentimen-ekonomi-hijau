// Preprocessing identik dengan ml/preprocess.py + Porter Stemmer (algoritma asli 1980)
const Porter = (() => {
  const step2list = { ational: "ate", tional: "tion", enci: "ence", anci: "ance", izer: "ize", abli: "able", alli: "al", entli: "ent", eli: "e", ousli: "ous", ization: "ize", ation: "ate", ator: "ate", alism: "al", iveness: "ive", fulness: "ful", ousness: "ous", aliti: "al", iviti: "ive", biliti: "ble" };
  const step3list = { icate: "ic", ative: "", alize: "al", iciti: "ic", ical: "ic", ful: "", ness: "" };
  const c = "[^aeiou]", v = "[aeiouy]", C = c + "[^aeiouy]*", V = v + "[aeiou]*";
  const mgr0 = new RegExp("^(" + C + ")?" + V + C);
  const meq1 = new RegExp("^(" + C + ")?" + V + C + "(" + V + ")?$");
  const mgr1 = new RegExp("^(" + C + ")?" + V + C + V + C);
  const s_v = new RegExp("^(" + C + ")?" + v);
  return function stem(w) {
    let stem, suffix, re, re2, re3, re4, fp;
    if (w.length < 3) return w;
    const firstch = w[0];
    if (firstch === "y") w = "Y" + w.slice(1);
    re = /^(.+?)(ss|i)es$/; re2 = /^(.+?)([^s])s$/;
    if (re.test(w)) w = w.replace(re, "$1$2");
    else if (re2.test(w)) w = w.replace(re2, "$1$2");
    re = /^(.+?)eed$/; re2 = /^(.+?)(ed|ing)$/;
    if (re.test(w)) {
      fp = re.exec(w);
      if (mgr0.test(fp[1])) w = w.slice(0, -1);
    } else if (re2.test(w)) {
      fp = re2.exec(w); stem = fp[1];
      if (s_v.test(stem)) {
        w = stem;
        re2 = /(at|bl|iz)$/; re3 = /([^aeiouylsz])\1$/; re4 = new RegExp("^" + C + v + "[^aeiouwxy]$");
        if (re2.test(w)) w += "e";
        else if (re3.test(w)) w = w.slice(0, -1);
        else if (re4.test(w)) w += "e";
      }
    }
    re = /^(.+?)y$/;
    if (re.test(w)) { fp = re.exec(w); stem = fp[1]; if (s_v.test(stem)) w = stem + "i"; }
    re = /^(.+?)(ational|tional|enci|anci|izer|bli|alli|entli|eli|ousli|ization|ation|ator|alism|iveness|fulness|ousness|aliti|iviti|biliti|abli)$/;
    if (re.test(w)) { fp = re.exec(w); stem = fp[1]; suffix = fp[2]; if (mgr0.test(stem) && step2list[suffix] !== undefined) w = stem + step2list[suffix]; }
    re = /^(.+?)(icate|ative|alize|iciti|ical|ful|ness)$/;
    if (re.test(w)) { fp = re.exec(w); stem = fp[1]; suffix = fp[2]; if (mgr0.test(stem)) w = stem + step3list[suffix]; }
    re = /^(.+?)(al|ance|ence|er|ic|able|ible|ant|ement|ment|ent|ou|ism|ate|iti|ous|ive|ize)$/; re2 = /^(.+?)(s|t)(ion)$/;
    if (re.test(w)) { fp = re.exec(w); stem = fp[1]; if (mgr1.test(stem)) w = stem; }
    else if (re2.test(w)) { fp = re2.exec(w); stem = fp[1] + fp[2]; if (mgr1.test(stem)) w = stem; }
    re = /^(.+?)e$/;
    if (re.test(w)) {
      fp = re.exec(w); stem = fp[1]; re3 = new RegExp("^" + C + v + "[^aeiouwxy]$");
      if (mgr1.test(stem) || (meq1.test(stem) && !re3.test(stem))) w = stem;
    }
    if (/ll$/.test(w) && mgr1.test(w)) w = w.slice(0, -1);
    if (firstch === "y") w = "y" + w.slice(1);
    return w;
  };
})();

function cleanText(t) {
  t = String(t)
    .replace(/https?:\/\/\S+|www\.\S+/g, " ")
    .replace(/@\w+/g, " ")
    .replace(/#\w+/g, " ")
    .replace(/&\w+;/g, " ")
    .toLowerCase()
    .replace(/\brt\b/g, " ")
    .replace(/\d+/g, " ")
    .replace(/[^a-z\s]/g, " ");
  return t.replace(/\s+/g, " ").trim();
}

function filterStem(text, stopwords) {
  return text.split(" ").filter(w => w.length >= 2 && !stopwords.has(w)).map(Porter);
}

if (typeof module !== "undefined") module.exports = { Porter, cleanText, filterStem };
