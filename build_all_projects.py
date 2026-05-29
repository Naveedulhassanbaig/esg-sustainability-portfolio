# -*- coding: utf-8 -*-
"""
Build all 5 ESG Portfolio Datasets for Upwork
"""
import csv
import random
import json
import os

random.seed(42)

# ── PROJECT 1: SASB Mapping (already built) ────────────────────────────────

# ── PROJECT 2: Sustainability Report Analyzer ──────────────────────────────
# Simulates data extracted from 20 real company sustainability reports

companies = [
    ("Apple Inc", "Technology & Communications", "USA"),
    ("Microsoft", "Technology & Communications", "USA"),
    ("Amazon", "Services", "USA"),
    ("Tesla", "Transportation", "USA"),
    ("ExxonMobil", "Extractives & Minerals Processing", "USA"),
    ("BP", "Extractives & Minerals Processing", "UK"),
    ("Shell", "Extractives & Minerals Processing", "Netherlands"),
    ("Unilever", "Consumer Goods", "UK"),
    ("Nestle", "Food & Beverage", "Switzerland"),
    ("Johnson & Johnson", "Health Care", "USA"),
    ("Walmart", "Consumer Goods", "USA"),
    ("Nike", "Consumer Goods", "USA"),
    ("HSBC", "Financials", "UK"),
    ("Goldman Sachs", "Financials", "USA"),
    ("Siemens", "Resource Transformation", "Germany"),
    ("Toyota", "Transportation", "Japan"),
    ("Samsung", "Technology & Communications", "South Korea"),
    ("Alibaba", "Services", "China"),
    ("Reliance Industries", "Extractives & Minerals Processing", "India"),
    ("Saudi Aramco", "Extractives & Minerals Processing", "Saudi Arabia"),
]

gri_topics = [
    "GRI 201: Economic Performance",
    "GRI 202: Market Presence",
    "GRI 205: Anti-Corruption",
    "GRI 301: Materials",
    "GRI 302: Energy",
    "GRI 303: Water",
    "GRI 304: Biodiversity",
    "GRI 305: Emissions",
    "GRI 306: Waste",
    "GRI 401: Employment",
    "GRI 403: Occupational Health & Safety",
    "GRI 404: Training & Education",
    "GRI 405: Diversity & Equal Opportunity",
    "GRI 406: Non-Discrimination",
    "GRI 413: Local Communities",
    "GRI 414: Supplier Social Assessment",
    "GRI 415: Public Policy",
    "GRI 418: Customer Privacy",
]

report_rows = []
for company, sector, country in companies:
    report_year = random.choice([2021, 2022, 2023])
    pages = random.randint(80, 220)
    esg_score = round(random.uniform(40, 95), 1)
    carbon_intensity = round(random.uniform(5, 800), 1)
    renewable_pct = random.randint(10, 95)
    women_leadership = random.randint(20, 55)
    reported_topics = random.sample(gri_topics, random.randint(8, 18))
    report_rows.append({
        "Company": company,
        "Sector": sector,
        "Country": country,
        "Report_Year": report_year,
        "Report_Pages": pages,
        "ESG_Score": esg_score,
        "Carbon_Intensity_tCO2e": carbon_intensity,
        "Renewable_Energy_Pct": renewable_pct,
        "Women_In_Leadership_Pct": women_leadership,
        "GRI_Topics_Reported": len(reported_topics),
        "GRI_Coverage_Pct": round(len(reported_topics)/len(gri_topics)*100, 1),
        "Topics_List": "|".join(reported_topics),
    })

with open("sustainability_reports.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=report_rows[0].keys())
    writer.writeheader()
    writer.writerows(report_rows)
print("Project 2 built: sustainability_reports.csv")

# ── PROJECT 3: GRI Compliance Dashboard ───────────────────────────────────
gri_standards = [
    ("GRI 2", "Universal", "General Disclosures", "Organizational profile, governance, stakeholder engagement"),
    ("GRI 3", "Universal", "Material Topics", "Process for determining material topics"),
    ("GRI 201", "Economic", "Economic Performance", "Direct economic value generated and distributed"),
    ("GRI 202", "Economic", "Market Presence", "Ratios of standard entry level wage by gender"),
    ("GRI 203", "Economic", "Indirect Economic Impacts", "Infrastructure investments and services supported"),
    ("GRI 204", "Economic", "Procurement Practices", "Proportion of spending on local suppliers"),
    ("GRI 205", "Economic", "Anti-Corruption", "Operations assessed for corruption risks"),
    ("GRI 206", "Economic", "Anti-Competitive Behavior", "Legal actions for anti-competitive behavior"),
    ("GRI 207", "Economic", "Tax", "Approach to tax, governance, control"),
    ("GRI 301", "Environmental", "Materials", "Materials used by weight or volume"),
    ("GRI 302", "Environmental", "Energy", "Energy consumption within organization"),
    ("GRI 303", "Environmental", "Water & Effluents", "Water withdrawal by source"),
    ("GRI 304", "Environmental", "Biodiversity", "Operational sites near protected areas"),
    ("GRI 305", "Environmental", "Emissions", "Direct GHG emissions (Scope 1)"),
    ("GRI 306", "Environmental", "Waste", "Waste generated and disposal"),
    ("GRI 308", "Environmental", "Supplier Environmental Assessment", "New suppliers screened on environment"),
    ("GRI 401", "Social", "Employment", "New employee hires and turnover"),
    ("GRI 402", "Social", "Labor/Management Relations", "Minimum notice periods for operational changes"),
    ("GRI 403", "Social", "Occupational Health & Safety", "Management system for health and safety"),
    ("GRI 404", "Social", "Training & Education", "Average hours of training per year"),
    ("GRI 405", "Social", "Diversity & Equal Opportunity", "Diversity of governance bodies"),
    ("GRI 406", "Social", "Non-Discrimination", "Incidents of discrimination"),
    ("GRI 407", "Social", "Freedom of Association", "Operations where rights may be at risk"),
    ("GRI 408", "Social", "Child Labor", "Operations at significant risk for child labor"),
    ("GRI 409", "Social", "Forced Labor", "Operations at risk for forced labor"),
    ("GRI 413", "Social", "Local Communities", "Operations with local community engagement"),
    ("GRI 414", "Social", "Supplier Social Assessment", "New suppliers screened on social criteria"),
    ("GRI 415", "Social", "Public Policy", "Political contributions"),
    ("GRI 416", "Social", "Customer Health & Safety", "Assessment of health and safety impacts"),
    ("GRI 418", "Social", "Customer Privacy", "Substantiated complaints on privacy breaches"),
]

gri_rows = []
for company, sector, country in companies:
    for std in gri_standards:
        disclosed = random.random() > 0.3
        completeness = random.randint(50, 100) if disclosed else 0
        gri_rows.append({
            "Company": company,
            "Sector": sector,
            "GRI_Code": std[0],
            "GRI_Category": std[1],
            "GRI_Topic": std[2],
            "GRI_Description": std[3],
            "Disclosed": disclosed,
            "Completeness_Pct": completeness,
        })

with open("gri_compliance.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=gri_rows[0].keys())
    writer.writeheader()
    writer.writerows(gri_rows)
print("Project 3 built: gri_compliance.csv")

# ── PROJECT 4: ESG Score Calculator ───────────────────────────────────────
sectors_list = [
    "Technology & Communications", "Extractives & Minerals Processing",
    "Financials", "Food & Beverage", "Health Care",
    "Infrastructure", "Consumer Goods", "Transportation", "Services"
]

esg_rows = []
for company, sector, country in companies:
    env_score  = round(random.uniform(30, 95), 1)
    soc_score  = round(random.uniform(35, 90), 1)
    gov_score  = round(random.uniform(40, 95), 1)
    total = round(env_score*0.433 + soc_score*0.341 + gov_score*0.226, 1)
    risk_level = "Low" if total > 70 else "Medium" if total > 50 else "High"
    esg_rows.append({
        "Company": company,
        "Sector": sector,
        "Country": country,
        "Environmental_Score": env_score,
        "Social_Score": soc_score,
        "Governance_Score": gov_score,
        "Total_ESG_Score": total,
        "Risk_Level": risk_level,
        "Industry_Avg_ESG": round(random.uniform(50, 75), 1),
        "ESG_Percentile": random.randint(20, 99),
    })

with open("esg_scores.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=esg_rows[0].keys())
    writer.writeheader()
    writer.writerows(esg_rows)
print("Project 4 built: esg_scores.csv")

# ── PROJECT 5: Carbon Footprint Benchmarker ────────────────────────────────
years = [2018, 2019, 2020, 2021, 2022, 2023]
carbon_rows = []
for company, sector, country in companies:
    base_scope1 = random.uniform(100, 50000)
    base_scope2 = random.uniform(50, 20000)
    base_scope3 = random.uniform(1000, 200000)
    for year in years:
        trend = 1 - (year - 2018) * random.uniform(0.01, 0.08)
        carbon_rows.append({
            "Company": company,
            "Sector": sector,
            "Country": country,
            "Year": year,
            "Scope1_tCO2e": round(base_scope1 * trend, 0),
            "Scope2_tCO2e": round(base_scope2 * trend * 0.9, 0),
            "Scope3_tCO2e": round(base_scope3 * trend * 0.95, 0),
            "Total_tCO2e": round((base_scope1 + base_scope2 + base_scope3) * trend, 0),
            "Revenue_USD_M": round(random.uniform(5000, 500000) * (1 + (year-2018)*0.05), 0),
            "Net_Zero_Target": random.choice([2030, 2035, 2040, 2045, 2050, None]),
        })

with open("carbon_footprint.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=carbon_rows[0].keys())
    writer.writeheader()
    writer.writerows(carbon_rows)
print("Project 5 built: carbon_footprint.csv")

# ── PROJECT 6: UN SDG Tracker ──────────────────────────────────────────────
sdgs = [
    (1, "No Poverty"), (2, "Zero Hunger"), (3, "Good Health & Well-being"),
    (4, "Quality Education"), (5, "Gender Equality"), (6, "Clean Water & Sanitation"),
    (7, "Affordable & Clean Energy"), (8, "Decent Work & Economic Growth"),
    (9, "Industry Innovation & Infrastructure"), (10, "Reduced Inequalities"),
    (11, "Sustainable Cities"), (12, "Responsible Consumption"),
    (13, "Climate Action"), (14, "Life Below Water"), (15, "Life on Land"),
    (16, "Peace Justice & Strong Institutions"), (17, "Partnerships for Goals"),
]

sdg_rows = []
for company, sector, country in companies:
    for sdg_num, sdg_name in sdgs:
        contribution = random.choice(["High", "Medium", "Low", "None"])
        investments_usd_m = round(random.uniform(0, 500), 1) if contribution != "None" else 0
        sdg_rows.append({
            "Company": company,
            "Sector": sector,
            "SDG_Number": sdg_num,
            "SDG_Name": sdg_name,
            "Contribution_Level": contribution,
            "Investment_USD_M": investments_usd_m,
            "Reported_In_Sustainability_Report": contribution != "None",
        })

with open("sdg_tracker.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=sdg_rows[0].keys())
    writer.writeheader()
    writer.writerows(sdg_rows)
print("Project 6 built: sdg_tracker.csv")

print("\nAll 5 datasets ready!")
print("Files in C:/Users/Hp/ESG_Portfolio/:")
for f in ["sasb_esg_mapping.csv","sustainability_reports.csv","gri_compliance.csv",
          "esg_scores.csv","carbon_footprint.csv","sdg_tracker.csv"]:
    print(f"  - {f}")
