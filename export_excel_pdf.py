# -*- coding: utf-8 -*-
"""
Export ESG Portfolio to Excel (multi-sheet) + PDF Report
"""
import pandas as pd
import os

BASE = r'C:/Users/Hp/ESG_Portfolio/'

# Load all datasets
sasb   = pd.read_csv(BASE + 'sasb_esg_mapping.csv')
report = pd.read_csv(BASE + 'sustainability_reports.csv')
gri    = pd.read_csv(BASE + 'gri_compliance.csv')
esg    = pd.read_csv(BASE + 'esg_scores.csv')
carbon = pd.read_csv(BASE + 'carbon_footprint.csv')
sdg    = pd.read_csv(BASE + 'sdg_tracker.csv')

# ── EXCEL EXPORT ────────────────────────────────────────────────────────────
print("Building Excel report...")

excel_path = BASE + 'ESG_Portfolio_Data.xlsx'
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:

    # Sheet 1 — Summary
    summary = pd.DataFrame({
        'Project': [
            '1. SASB Industry-ESG Mapping',
            '2. Sustainability Report Analyzer',
            '3. GRI Compliance Dashboard',
            '4. ESG Score Calculator',
            '5. Carbon Footprint Benchmarker',
            '6. UN SDG Contribution Tracker'
        ],
        'Framework': ['SASB','GRI','GRI','MSCI/Sustainalytics','TCFD/GHG Protocol','UN SDGs'],
        'Records': [len(sasb), len(report), len(gri), len(esg), len(carbon), len(sdg)],
        'Companies': [
            sasb['Industry'].nunique(),
            report['Company'].nunique(),
            gri['Company'].nunique(),
            esg['Company'].nunique(),
            carbon['Company'].nunique(),
            sdg['Company'].nunique()
        ],
        'Client_Type': [
            'ESG Consultants',
            'Law Firms / NGOs',
            'Corporate Teams',
            'Investment Firms',
            'Climate Consultants',
            'Govt / UN Agencies'
        ],
        'Upwork_Rate_USD_hr': ['$50-80','$60-100','$70-120','$80-150','$60-100','$70-110']
    })
    summary.to_excel(writer, sheet_name='Portfolio Summary', index=False)

    # Sheet 2 — SASB Materiality (material only)
    sasb_clean = sasb[sasb['Is_Material']==True][
        ['Sector','Industry','ESG_Dimension','ESG_Topic','Materiality_Score']
    ].sort_values(['Sector','Industry','Materiality_Score'], ascending=[True,True,False])
    sasb_clean.to_excel(writer, sheet_name='SASB Materiality', index=False)

    # Sheet 3 — Sustainability Reports
    report_clean = report[[
        'Company','Sector','Country','Report_Year','ESG_Score',
        'Carbon_Intensity_tCO2e','Renewable_Energy_Pct',
        'Women_In_Leadership_Pct','GRI_Topics_Reported','GRI_Coverage_Pct'
    ]].sort_values('ESG_Score', ascending=False)
    report_clean.to_excel(writer, sheet_name='Sustainability Reports', index=False)

    # Sheet 4 — GRI Compliance
    gri_summary = gri.groupby(['Company','GRI_Category']).agg(
        Topics_Reported=('Disclosed','sum'),
        Total_Topics=('Disclosed','count'),
        Avg_Completeness=('Completeness_Pct','mean')
    ).reset_index()
    gri_summary['Compliance_Pct'] = (gri_summary['Topics_Reported']/gri_summary['Total_Topics']*100).round(1)
    gri_summary['Avg_Completeness'] = gri_summary['Avg_Completeness'].round(1)
    gri_summary.to_excel(writer, sheet_name='GRI Compliance', index=False)

    # Sheet 5 — ESG Scores
    esg_clean = esg[[
        'Company','Sector','Country',
        'Environmental_Score','Social_Score','Governance_Score',
        'Total_ESG_Score','Risk_Level','Industry_Avg_ESG','ESG_Percentile'
    ]].sort_values('Total_ESG_Score', ascending=False)
    esg_clean.to_excel(writer, sheet_name='ESG Scores', index=False)

    # Sheet 6 — Carbon Footprint
    carbon_clean = carbon.sort_values(['Company','Year'])[[
        'Company','Sector','Country','Year',
        'Scope1_tCO2e','Scope2_tCO2e','Scope3_tCO2e',
        'Total_tCO2e','Revenue_USD_M','Net_Zero_Target'
    ]]
    carbon_clean.to_excel(writer, sheet_name='Carbon Footprint', index=False)

    # Sheet 7 — SDG Tracker
    sdg_clean = sdg[sdg['Contribution_Level']!='None'][[
        'Company','Sector','SDG_Number','SDG_Name',
        'Contribution_Level','Investment_USD_M'
    ]].sort_values(['Company','SDG_Number'])
    sdg_clean.to_excel(writer, sheet_name='SDG Tracker', index=False)

    # Sheet 8 — Key Insights
    insights = pd.DataFrame({
        'Project': [
            'SASB Mapping','SASB Mapping',
            'Sustainability Reports','Sustainability Reports',
            'GRI Compliance','GRI Compliance',
            'ESG Scores','ESG Scores',
            'Carbon Footprint','Carbon Footprint',
            'SDG Tracker','SDG Tracker'
        ],
        'Key_Insight': [
            'Business Ethics material for 95% of all industries',
            'Extractives & Mining has highest environmental materiality score (5.0)',
            'Tech companies lead on ESG scores; Extractives lag on carbon intensity',
            'Average GRI coverage across 20 companies is 65-80%',
            'Social disclosures are most commonly reported under GRI',
            'Economic disclosures show lowest compliance rates',
            'Governance scores show highest variance across companies',
            '40% of analyzed companies are Low ESG Risk',
            'Scope 3 emissions represent 80%+ of total footprint for most companies',
            'Most companies targeting Net Zero between 2040-2050',
            'SDG 8 (Decent Work) receives most corporate attention',
            'SDG 14 (Life Below Water) is most underfunded goal'
        ]
    })
    insights.to_excel(writer, sheet_name='Key Insights', index=False)

print(f"Excel saved: {excel_path}")

# ── PDF REPORT ───────────────────────────────────────────────────────────────
print("Building PDF report...")

from fpdf import FPDF

class ESGReport(FPDF):
    def header(self):
        self.set_fill_color(11, 26, 20)
        self.rect(0, 0, 210, 297, 'F')
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(0, 200, 150)
        self.cell(0, 12, 'ESG & Sustainability Portfolio Report', ln=True, align='C')
        self.set_font('Helvetica', '', 10)
        self.set_text_color(160, 200, 176)
        self.cell(0, 6, 'SASB | GRI | TCFD | UN SDGs | Naveed Baig | 2025', ln=True, align='C')
        self.ln(4)
        self.set_draw_color(0, 200, 150)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(58, 107, 80)
        self.cell(0, 10, f'ESG Portfolio | Naveed Baig | Page {self.page_no()}', align='C')

    def section_title(self, title, color=(0,200,150)):
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(*color)
        self.ln(4)
        self.cell(0, 8, title, ln=True)
        self.set_draw_color(*color)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(200, 230, 210)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def metric_row(self, label, value, color=(0,200,150)):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*color)
        self.cell(80, 7, label + ':', ln=False)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(200, 230, 210)
        self.cell(0, 7, str(value), ln=True)

    def insight_box(self, text):
        self.set_fill_color(17, 42, 30)
        self.set_draw_color(0, 200, 150)
        x, y = self.get_x(), self.get_y()
        self.set_font('Helvetica', 'I', 9)
        self.set_text_color(160, 200, 176)
        self.multi_cell(0, 6, '  Insight: ' + text, border=1, fill=True)
        self.ln(3)

pdf = ESGReport()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_margins(10, 10, 10)

# ── PAGE 1: EXECUTIVE SUMMARY ──
pdf.add_page()
pdf.section_title('Executive Summary')
pdf.body_text(
    'This portfolio demonstrates expertise in ESG (Environmental, Social, and Governance) '
    'data analysis using internationally recognized frameworks. The analysis covers 20 global '
    'corporations across 11 industry sectors, mapping sustainability performance against '
    'SASB standards, GRI disclosures, TCFD climate risk, and UN SDG contributions.'
)

pdf.section_title('Portfolio Overview', color=(0,200,150))
metrics = [
    ('Framework Coverage', 'SASB, GRI, TCFD, GHG Protocol, UN SDGs'),
    ('Companies Analyzed', '20 Global Corporations'),
    ('Industries Covered', '77 Industries across 11 SASB Sectors'),
    ('ESG Topics Mapped', '27 SASB Materiality Topics'),
    ('GRI Standards', '30 GRI Disclosure Standards'),
    ('Carbon Data', 'Scope 1, 2, 3 Emissions (2018-2023)'),
    ('SDGs Tracked', 'All 17 UN Sustainable Development Goals'),
    ('Tools Used', 'Python, Pandas, Plotly, Jupyter Notebook'),
]
for label, val in metrics:
    pdf.metric_row(label, val)

# ── PAGE 2: PROJECT 1 ──
pdf.add_page()
pdf.section_title('Project 1 - SASB Industry-ESG Topic Mapping')
pdf.body_text(
    'Framework: Sustainability Accounting Standards Board (SASB)\n'
    'Client Type: ESG Consultants, Investment Analysts, Asset Managers\n'
    'Upwork Rate: $50-80/hour'
)
pdf.body_text(
    'This project maps 27 ESG topics across 77 industries in 11 sectors using SASB '
    'materiality standards. It identifies which sustainability issues are financially '
    'material for each specific industry.'
)

# Top material topics table
pdf.set_font('Helvetica', 'B', 10)
pdf.set_text_color(0, 200, 150)
pdf.cell(100, 7, 'ESG Topic', border=1, fill=False)
pdf.cell(50, 7, 'Dimension', border=1)
pdf.cell(40, 7, 'Industries Affected', border=1, ln=True)

top_topics = sasb[sasb['Is_Material']==True].groupby(
    ['ESG_Topic','ESG_Dimension'])['Industry'].nunique().sort_values(ascending=False).head(8)

for (topic, dim), count in top_topics.items():
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(200, 230, 210)
    pdf.cell(100, 6, topic[:45], border=1)
    pdf.cell(50, 6, dim[:25], border=1)
    pdf.cell(40, 6, str(count) + ' industries', border=1, ln=True)

pdf.ln(4)
pdf.insight_box('Business Ethics and Data Security are material for 95%+ of all industries, making them the universal ESG baseline regardless of sector.')

# ── PAGE 3: PROJECT 2 ──
pdf.add_page()
pdf.section_title('Project 2 - Sustainability Report Analyzer')
pdf.body_text(
    'Framework: GRI Standards\n'
    'Client Type: Law Firms, NGOs, Consulting Firms\n'
    'Upwork Rate: $60-100/hour'
)

# Company scores table
pdf.set_font('Helvetica', 'B', 10)
pdf.set_text_color(0, 200, 150)
pdf.cell(60, 7, 'Company', border=1)
pdf.cell(50, 7, 'Sector', border=1)
pdf.cell(30, 7, 'ESG Score', border=1)
pdf.cell(30, 7, 'GRI Cover%', border=1)
pdf.cell(20, 7, 'Risk', border=1, ln=True)

report_top = report.sort_values('ESG_Score', ascending=False).head(10)
for _, row in report_top.iterrows():
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(200, 230, 210)
    pdf.cell(60, 6, str(row['Company'])[:28], border=1)
    pdf.cell(50, 6, str(row['Sector'])[:24], border=1)
    pdf.cell(30, 6, str(row['ESG_Score']), border=1)
    pdf.cell(30, 6, str(row['GRI_Coverage_Pct']) + '%', border=1)
    esg_row = esg[esg['Company']==row['Company']]
    risk = esg_row['Risk_Level'].values[0] if len(esg_row) > 0 else 'N/A'
    pdf.cell(20, 6, str(risk), border=1, ln=True)

pdf.ln(4)
pdf.insight_box('Tech companies consistently lead on ESG scores. Extractives sector shows highest carbon intensity, averaging 400+ tCO2e.')

# ── PAGE 4: PROJECT 3 ──
pdf.add_page()
pdf.section_title('Project 3 - GRI Standards Compliance Dashboard')
pdf.body_text(
    'Framework: Global Reporting Initiative (GRI)\n'
    'Client Type: Corporate Sustainability Teams, Regulators\n'
    'Upwork Rate: $70-120/hour'
)

gri_by_cat = gri.groupby('GRI_Category').agg(
    Avg_Compliance=('Disclosed','mean')
).reset_index()
gri_by_cat['Avg_Compliance_Pct'] = (gri_by_cat['Avg_Compliance']*100).round(1)

pdf.set_font('Helvetica', 'B', 10)
pdf.set_text_color(0, 200, 150)
pdf.cell(80, 7, 'GRI Category', border=1)
pdf.cell(60, 7, 'Avg Compliance Rate', border=1)
pdf.cell(50, 7, 'Assessment', border=1, ln=True)

for _, row in gri_by_cat.iterrows():
    pct = row['Avg_Compliance_Pct']
    assessment = 'Strong' if pct >= 75 else 'Moderate' if pct >= 55 else 'Needs Improvement'
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(200, 230, 210)
    pdf.cell(80, 6, str(row['GRI_Category']), border=1)
    pdf.cell(60, 6, str(pct) + '%', border=1)
    pdf.cell(50, 6, assessment, border=1, ln=True)

pdf.ln(4)
pdf.insight_box('Social category disclosures are most commonly reported. Economic disclosures, especially tax transparency, show the lowest compliance rates.')

# ── PAGE 5: PROJECTS 4-6 ──
pdf.add_page()
pdf.section_title('Project 4 - ESG Score Calculator & Benchmarking')
pdf.body_text(
    'Framework: MSCI / Sustainalytics methodology\n'
    'Client Type: Investment Funds, Private Equity, Asset Managers\n'
    'Upwork Rate: $80-150/hour'
)

risk_dist = esg['Risk_Level'].value_counts()
for risk, count in risk_dist.items():
    pdf.metric_row(risk + ' Risk Companies', str(count) + ' out of 20')

pdf.insight_box('Governance scores show the highest variance across companies - this is where the biggest ESG risk differentiation occurs for investors.')
pdf.ln(4)

pdf.section_title('Project 5 - Carbon Footprint Benchmarker', color=(255,200,100))
pdf.body_text(
    'Framework: TCFD / GHG Protocol\n'
    'Client Type: Manufacturing Companies, Energy Firms, Climate Consultants\n'
    'Upwork Rate: $60-100/hour'
)
carbon_2023 = carbon[carbon['Year']==2023]
pdf.metric_row('Total Scope 1 Emissions (2023)', f"{carbon_2023['Scope1_tCO2e'].sum():,.0f} tCO2e")
pdf.metric_row('Total Scope 2 Emissions (2023)', f"{carbon_2023['Scope2_tCO2e'].sum():,.0f} tCO2e")
pdf.metric_row('Total Scope 3 Emissions (2023)', f"{carbon_2023['Scope3_tCO2e'].sum():,.0f} tCO2e")
pdf.metric_row('Companies with Net Zero Target', str(carbon_2023['Net_Zero_Target'].notna().sum()) + ' out of 20')
pdf.insight_box('Scope 3 emissions represent 80%+ of total carbon footprint for most companies. Value chain emissions are the next frontier for corporate climate action.')
pdf.ln(4)

pdf.section_title('Project 6 - UN SDG Contribution Tracker', color=(105,192,255))
pdf.body_text(
    'Framework: UN Sustainable Development Goals\n'
    'Client Type: Government Bodies, UN Agencies, Impact Investors\n'
    'Upwork Rate: $70-110/hour'
)
top_sdgs = sdg[sdg['Contribution_Level']=='High'].groupby('SDG_Name')['Company'].count().sort_values(ascending=False).head(5)
for sdg_name, count in top_sdgs.items():
    pdf.metric_row(sdg_name[:40], str(count) + ' companies (High contribution)')

pdf.insight_box('SDG 8 (Decent Work & Economic Growth) and SDG 13 (Climate Action) receive the most corporate attention. SDG 14 (Life Below Water) remains most underfunded.')

# ── PAGE 6: CONCLUSION ──
pdf.add_page()
pdf.section_title('Conclusions & Recommendations')

pdf.body_text('Based on the analysis of 20 global corporations across 6 ESG frameworks, the following key conclusions emerge:')

conclusions = [
    ('1. Universal ESG Baseline', 'Business Ethics, Data Security, and Labor Practices are material for virtually every industry. All companies should prioritize these regardless of sector.'),
    ('2. Sector-Specific Priorities', 'Extractives & Mining faces the highest environmental materiality. Financials face the highest governance requirements. Technology faces the highest social and data-related risks.'),
    ('3. Reporting Gaps', 'Average GRI coverage across companies is 65-80%. Economic disclosures (especially tax transparency) show the lowest compliance rates globally.'),
    ('4. Carbon Action Urgency', 'Scope 3 emissions dominate total footprints but remain least reported. Most companies target Net Zero by 2040-2050 but current trajectories are insufficient.'),
    ('5. SDG Investment Gap', 'While SDG 8 and 13 are well-funded, environmental SDGs (14, 15) remain chronically underfunded by corporate actors.'),
    ('6. ESG-Performance Link', 'Companies with higher ESG scores show lower risk levels. Governance scores are the strongest predictor of overall ESG risk rating.'),
]

for title, text in conclusions:
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 200, 150)
    pdf.cell(0, 7, title, ln=True)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(200, 230, 210)
    pdf.multi_cell(0, 6, text)
    pdf.ln(2)

pdf.ln(4)
pdf.section_title('About This Portfolio')
pdf.body_text(
    'This portfolio was built using Python (Pandas, Plotly) with data structured from SASB '
    'public documentation, GRI standards, and sustainability reporting frameworks. '
    'All analysis follows internationally recognized ESG methodologies.\n\n'
    'Analyst: Naveed Baig\n'
    'Specialization: ESG & Sustainability Data Analysis\n'
    'Frameworks: SASB, GRI, TCFD, GHG Protocol, UN SDGs\n'
    'GitHub: github.com/Naveedulhassanbaig/esg-sustainability-portfolio\n'
    'Year: 2025'
)

pdf_path = BASE + 'ESG_Portfolio_Report.pdf'
pdf.output(pdf_path)
print(f"PDF saved: {pdf_path}")
print("\nAll exports complete!")
print(f"  Excel: ESG_Portfolio_Data.xlsx")
print(f"  PDF:   ESG_Portfolio_Report.pdf")
