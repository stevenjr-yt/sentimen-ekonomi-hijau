"""Generate synthetic dataset apabila dataset Kaggle belum tersedia.
Dataset sintetis berisi 10.000 tweet tentang isu iklim/ekonomi hijau
berlabel positif, negatif, netral berimbang.

Jalankan: python ml/generate_synthetic.py
"""
import random, csv
from pathlib import Path

random.seed(42)
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

POS = [
    "Solar energy is the future of clean power generation",
    "Renewable energy creates thousands of green jobs",
    "Electric vehicles reduce carbon emissions significantly",
    "Wind farms provide sustainable electricity for communities",
    "Green technology investments boost economic growth",
    "Carbon credits incentivize sustainable business practices",
    "Climate action protects biodiversity and ecosystems",
    "Net zero targets are achievable with political will",
    "Green hydrogen will transform heavy industry emissions",
    "Rooftop solar adoption is accelerating worldwide",
    "Sustainable agriculture can feed the world while protecting climate",
    "Carbon capture technology offers real climate solutions",
    "Ocean energy is an untapped renewable resource",
    "Green buildings save energy and reduce operating costs",
    "Electric public transport drastically cuts urban pollution",
]
NEG = [
    "Climate change policies destroy jobs and hurt the economy",
    "Renewable energy is too expensive and unreliable",
    "Carbon taxes punish ordinary people and businesses",
    "Electric vehicles are not affordable for average families",
    "Green policies will never solve the climate problem",
    "Climate alarmism is exaggerated and based on flawed models",
    "Wind turbines kill birds and ruin landscapes",
    "Solar panels create toxic waste when disposed",
    "Net zero targets are unrealistic and economically damaging",
    "Climate regulations choke small business growth",
    "Fossil fuels are still essential for energy security",
    "Climate activists ignore developing nations energy needs",
    "Carbon trading is a scam that helps corporations greenwash",
    "Electric grid cannot handle all electric vehicles charging",
    "Green energy subsidies waste taxpayer money",
]
NEU = [
    "Study shows climate change affects agricultural yields",
    "Government announces new renewable energy targets for 2030",
    "Electric vehicle sales increased by 40 percent last year",
    "Scientists publish findings on ocean temperature rise",
    "Report examines cost benefit analysis of carbon capture",
    "Conference discusses international climate finance mechanisms",
    "Data shows renewable energy capacity doubled in five years",
    "Analysis of green economy impact on employment trends",
    "Survey reveals public awareness of climate change issues",
    "Research on battery storage technology advancements",
    "Government releases climate adaptation strategy document",
    "Carbon market prices fluctuate amid policy uncertainty",
    "Comparison of different countries climate pledges published",
    "Study on electric vehicle adoption barriers in rural areas",
    "Overview of international climate agreements and progress",
]

templates = {
    "positif": POS * 220,
    "negatif": NEG * 220,
    "netral": NEU * 220,
}

rows = []
tid = 1000000
augments = [
    "{}", "RT @greenactivist: {}", "{} #ClimateChange",
    "Just read: {}", "{} via @reuters", "{} #GreenEconomy",
    "{} 2030 goals matter", "Breaking: {}", "{} @UN",
]
for label, sents in templates.items():
    for s in random.sample(sents, min(3000, len(sents))):
        tmpl = random.choice(augments)
        rows.append({"tweetid": tid, "sentiment": {"positif": 1, "negatif": -1, "netral": 0}[label],
                      "message": tmpl.format(s)})
        tid += 1

random.shuffle(rows)
out = DATA / "twitter_sentiment_data.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["tweetid", "sentiment", "message"])
    w.writeheader(); w.writerows(rows)
print(f"Generated {len(rows)} rows -> {out}")
