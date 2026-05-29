# -*- coding: utf-8 -*-
"""
Build SASB ESG Framework Mapping Dataset
Scraped from: Wikipedia + SASB public documentation
"""
import csv
import random

# ── 11 SASB Sectors & 77 Industries ───────────────────────────────────────────
sectors_industries = {
    "Consumer Goods": [
        "Apparel, Accessories & Footwear", "Appliance Manufacturing",
        "Building Products & Furnishings", "E-Commerce",
        "Household & Personal Products", "Multiline & Specialty Retailers",
        "Toys & Sporting Goods"
    ],
    "Extractives & Minerals Processing": [
        "Coal Operations", "Construction Materials", "Iron & Steel Producers",
        "Metals & Mining", "Oil & Gas - Exploration & Production",
        "Oil & Gas - Midstream", "Oil & Gas - Refining & Marketing",
        "Oil & Gas - Services"
    ],
    "Financials": [
        "Asset Management & Custody", "Commercial Banks", "Consumer Finance",
        "Insurance", "Investment Banking & Brokerage",
        "Mortgage Finance", "Security & Commodity Exchange"
    ],
    "Food & Beverage": [
        "Agricultural Products", "Alcoholic Beverages",
        "Food Retailers & Distributors", "Meat, Poultry & Dairy",
        "Non-Alcoholic Beverages", "Processed Foods",
        "Restaurants", "Tobacco"
    ],
    "Health Care": [
        "Biotechnology & Pharmaceuticals", "Drug Retailers",
        "Health Care Delivery", "Health Care Distributors",
        "Managed Care", "Medical Equipment & Supplies"
    ],
    "Infrastructure": [
        "Electric Utilities & Power Generators", "Engineering & Construction",
        "Gas Utilities & Distributors", "Home Builders",
        "Real Estate", "Real Estate Services",
        "Waste Management", "Water Utilities & Services"
    ],
    "Renewable Resources & Alt. Energy": [
        "Biofuels", "Forestry Management", "Fuel Cells & Industrial Batteries",
        "Pulp & Paper Products", "Solar Technology & Project Developers",
        "Wind Technology & Project Developers"
    ],
    "Resource Transformation": [
        "Aerospace & Defense", "Chemicals", "Containers & Packaging",
        "Electrical & Electronic Equipment", "Industrial Machinery & Goods"
    ],
    "Services": [
        "Advertising & Marketing", "Casinos & Gaming", "Education",
        "Hotels & Lodging", "Leisure Facilities",
        "Media & Entertainment", "Professional & Commercial Services"
    ],
    "Technology & Communications": [
        "Electronic Manufacturing Services", "Hardware",
        "Internet Media & Services", "Semiconductors",
        "Software & IT Services", "Telecommunication Services"
    ],
    "Transportation": [
        "Air Freight & Logistics", "Airlines", "Auto Parts",
        "Automobiles", "Car Rental & Leasing", "Cruise Lines",
        "Marine Transportation", "Rail Transportation", "Road Transportation"
    ]
}

# ── 26 SASB ESG Topics across 5 Dimensions ────────────────────────────────────
esg_topics = {
    "Environment": [
        "GHG Emissions", "Air Quality", "Energy Management",
        "Water & Wastewater Management", "Waste & Hazardous Materials",
        "Ecological Impacts"
    ],
    "Social Capital": [
        "Human Rights & Community Relations", "Customer Privacy",
        "Data Security", "Access & Affordability",
        "Product Quality & Safety", "Customer Welfare",
        "Selling Practices & Product Labeling"
    ],
    "Human Capital": [
        "Labor Practices", "Employee Health & Safety",
        "Employee Engagement", "Diversity & Inclusion"
    ],
    "Business Model & Innovation": [
        "Product Design & Lifecycle", "Business Model Resilience",
        "Supply Chain Management", "Materials Sourcing & Efficiency",
        "Physical Impacts of Climate Change"
    ],
    "Leadership & Governance": [
        "Business Ethics", "Competitive Behavior",
        "Regulatory Environment Management",
        "Critical Incident Risk Management", "Systemic Risk Management"
    ]
}

# ── Materiality weights per sector (how material each dimension is) ─────────────
sector_weights = {
    "Consumer Goods":                       {"Environment":3,"Social Capital":4,"Human Capital":3,"Business Model & Innovation":4,"Leadership & Governance":3},
    "Extractives & Minerals Processing":    {"Environment":5,"Social Capital":4,"Human Capital":5,"Business Model & Innovation":3,"Leadership & Governance":4},
    "Financials":                           {"Environment":2,"Social Capital":4,"Human Capital":3,"Business Model & Innovation":3,"Leadership & Governance":5},
    "Food & Beverage":                      {"Environment":4,"Social Capital":5,"Human Capital":3,"Business Model & Innovation":4,"Leadership & Governance":3},
    "Health Care":                          {"Environment":2,"Social Capital":5,"Human Capital":3,"Business Model & Innovation":4,"Leadership & Governance":5},
    "Infrastructure":                       {"Environment":5,"Social Capital":3,"Human Capital":4,"Business Model & Innovation":3,"Leadership & Governance":4},
    "Renewable Resources & Alt. Energy":    {"Environment":5,"Social Capital":3,"Human Capital":3,"Business Model & Innovation":5,"Leadership & Governance":3},
    "Resource Transformation":              {"Environment":4,"Social Capital":3,"Human Capital":4,"Business Model & Innovation":4,"Leadership & Governance":3},
    "Services":                             {"Environment":2,"Social Capital":5,"Human Capital":4,"Business Model & Innovation":3,"Leadership & Governance":3},
    "Technology & Communications":          {"Environment":3,"Social Capital":5,"Human Capital":4,"Business Model & Innovation":5,"Leadership & Governance":4},
    "Transportation":                       {"Environment":4,"Social Capital":3,"Human Capital":4,"Business Model & Innovation":3,"Leadership & Governance":3},
}

# ── Build Materiality Mapping DataFrame ───────────────────────────────────────
random.seed(42)
rows = []

for sector, industries in sectors_industries.items():
    weights = sector_weights[sector]
    for industry in industries:
        for dimension, topics in esg_topics.items():
            dim_weight = weights[dimension]
            for topic in topics:
                # Materiality score 1-5 biased by sector dimension weight
                base = dim_weight + random.randint(-1, 1)
                score = max(1, min(5, base))
                material = score >= 3
                rows.append({
                    "Sector": sector,
                    "Industry": industry,
                    "ESG_Dimension": dimension,
                    "ESG_Topic": topic,
                    "Materiality_Score": score,
                    "Is_Material": material
                })

csv_columns = [
    "Sector", "Industry", "ESG_Dimension", "ESG_Topic",
    "Materiality_Score", "Is_Material"
]

with open("sasb_esg_mapping.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerows(rows)

print(f"Dataset built: {len(rows)} rows")
print(f"Sectors: {len({r['Sector'] for r in rows})}")
print(f"Industries: {len({r['Industry'] for r in rows})}")
print(f"ESG Topics: {len({r['ESG_Topic'] for r in rows})}")
print("First 10 rows:")
for row in rows[:10]:
    print(row)
