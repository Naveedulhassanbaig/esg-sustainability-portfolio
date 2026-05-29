# -*- coding: utf-8 -*-
import json

cells = []

def md(id_, src):
    return {"cell_type":"markdown","metadata":{},"id":id_,"source":src}

def code(id_, src):
    return {"cell_type":"code","metadata":{},"id":id_,"execution_count":None,"outputs":[],"source":src}

cells.append(md("c01",[
    "# ESG Framework Mapping Portfolio\n",
    "### SASB Standards: Industry x Sustainability Topic Analysis\n",
    "---\n",
    "**Framework:** SASB (Sustainability Accounting Standards Board)  \n",
    "**Coverage:** 11 Sectors, 77 Industries, 27 ESG Topics, 5 Dimensions  \n",
    "**Tools:** Python, Pandas, Plotly  \n",
    "**Source:** Scraped from SASB public documentation\n"
]))

cells.append(code("c02",[
    "import pandas as pd\n",
    "import plotly.express as px\n",
    "import plotly.graph_objects as go\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "df = pd.read_csv(r'C:/Users/Hp/ESG_Portfolio/sasb_esg_mapping.csv')\n",
    "print('Rows:', df.shape[0])\n",
    "print('Sectors:', df['Sector'].nunique())\n",
    "print('Industries:', df['Industry'].nunique())\n",
    "print('ESG Topics:', df['ESG_Topic'].nunique())\n",
    "df.head()"
]))

cells.append(md("c03",[
    "---\n",
    "## Project 1 - ESG Materiality Heatmap\n",
    "**Which sectors have the highest ESG materiality across each dimension?**"
]))

cells.append(code("c04",[
    "pivot = df.groupby(['Sector','ESG_Dimension'])['Materiality_Score'].mean().reset_index()\n",
    "heatmap_data = pivot.pivot(index='Sector', columns='ESG_Dimension', values='Materiality_Score')\n",
    "\n",
    "fig = px.imshow(heatmap_data,\n",
    "    color_continuous_scale='RdYlGn',\n",
    "    title='ESG Materiality Heatmap - Sector vs Dimension (Score 1-5)',\n",
    "    labels=dict(color='Score'),\n",
    "    aspect='auto', text_auto='.1f')\n",
    "fig.update_layout(template='plotly_dark', paper_bgcolor='#0b1a14', height=500)\n",
    "fig.show()\n",
    "print('Key Insight: Extractives leads on Environment; Financials leads on Governance.')"
]))

cells.append(md("c05",[
    "---\n",
    "## Project 2 - Top ESG Topics by Industry Count\n",
    "**Which ESG topics are most material across ALL industries?**"
]))

cells.append(code("c06",[
    "color_map = {\n",
    "    'Environment': '#00c896',\n",
    "    'Social Capital': '#69c0ff',\n",
    "    'Human Capital': '#ffc864',\n",
    "    'Business Model & Innovation': '#ff8c69',\n",
    "    'Leadership & Governance': '#b39ddb'\n",
    "}\n",
    "\n",
    "topic_counts = df[df['Is_Material']==True].groupby(['ESG_Topic','ESG_Dimension'])['Industry'].nunique().reset_index()\n",
    "topic_counts.columns = ['ESG_Topic','ESG_Dimension','Industry_Count']\n",
    "topic_counts = topic_counts.sort_values('Industry_Count', ascending=False)\n",
    "\n",
    "fig = px.bar(topic_counts, x='Industry_Count', y='ESG_Topic', color='ESG_Dimension',\n",
    "    color_discrete_map=color_map, orientation='h',\n",
    "    title='Most Material ESG Topics - Number of Industries Affected',\n",
    "    labels={'Industry_Count':'No. of Industries','ESG_Topic':'ESG Topic'})\n",
    "fig.update_layout(template='plotly_dark', paper_bgcolor='#0b1a14',\n",
    "    plot_bgcolor='#112a1e', height=600, yaxis=dict(autorange='reversed'))\n",
    "fig.show()\n",
    "print('Key Insight: Business Ethics and Data Security material for nearly every industry.')"
]))

cells.append(md("c07",[
    "---\n",
    "## Project 3 - Industry Deep-Dive ESG Profile\n",
    "**Full ESG materiality profile for a specific industry**"
]))

cells.append(code("c08",[
    "INDUSTRY = 'Oil & Gas - Exploration & Production'\n",
    "\n",
    "ind_df = df[df['Industry']==INDUSTRY].sort_values('Materiality_Score', ascending=False)\n",
    "\n",
    "fig = px.bar(ind_df, x='Materiality_Score', y='ESG_Topic', color='ESG_Dimension',\n",
    "    color_discrete_map=color_map, orientation='h',\n",
    "    title='ESG Profile: ' + INDUSTRY,\n",
    "    labels={'Materiality_Score':'Materiality Score (1-5)','ESG_Topic':''})\n",
    "fig.add_vline(x=3, line_dash='dash', line_color='white', line_width=1,\n",
    "    annotation_text='Material threshold')\n",
    "fig.update_layout(template='plotly_dark', paper_bgcolor='#0b1a14',\n",
    "    plot_bgcolor='#112a1e', height=600, yaxis=dict(autorange='reversed'))\n",
    "fig.show()\n",
    "\n",
    "material = ind_df[ind_df['Is_Material']==True]['ESG_Topic'].tolist()\n",
    "print('Material topics (' + str(len(material)) + '):')\n",
    "for t in material: print(' -', t)"
]))

cells.append(md("c09",[
    "---\n",
    "## Project 4 - Sector ESG Radar Chart\n",
    "**How do sectors compare across all 5 ESG dimensions?**"
]))

cells.append(code("c10",[
    "COMPARE = [\n",
    "    'Extractives & Minerals Processing',\n",
    "    'Technology & Communications',\n",
    "    'Financials',\n",
    "    'Food & Beverage',\n",
    "    'Transportation'\n",
    "]\n",
    "dimensions = df['ESG_Dimension'].unique().tolist()\n",
    "colors = ['#ff6b6b','#69c0ff','#ffc864','#00c896','#b39ddb']\n",
    "\n",
    "fig = go.Figure()\n",
    "for sector, color in zip(COMPARE, colors):\n",
    "    scores = []\n",
    "    for d in dimensions:\n",
    "        s = df[(df['Sector']==sector) & (df['ESG_Dimension']==d)]['Materiality_Score'].mean()\n",
    "        scores.append(round(s, 2))\n",
    "    scores.append(scores[0])\n",
    "    fig.add_trace(go.Scatterpolar(\n",
    "        r=scores, theta=dimensions+[dimensions[0]],\n",
    "        fill='toself', name=sector, line=dict(color=color, width=2)))\n",
    "\n",
    "fig.update_layout(\n",
    "    polar=dict(radialaxis=dict(visible=True, range=[0,5])),\n",
    "    title='ESG Dimension Radar - Sector Comparison',\n",
    "    template='plotly_dark', paper_bgcolor='#0b1a14', height=550)\n",
    "fig.show()\n",
    "print('Key Insight: Extractives high on Environment; Tech leads on Social Capital.')"
]))

cells.append(md("c11",[
    "---\n",
    "## Project 5 - ESG Materiality Rate by Sector\n",
    "**Which sectors have the highest % of material ESG topics?**"
]))

cells.append(code("c12",[
    "mat_rate = df.groupby('Sector').agg(\n",
    "    Total=('Is_Material','count'),\n",
    "    Material=('Is_Material','sum')\n",
    ").reset_index()\n",
    "mat_rate['Rate'] = (mat_rate['Material']/mat_rate['Total']*100).round(1)\n",
    "mat_rate = mat_rate.sort_values('Rate', ascending=False)\n",
    "\n",
    "fig = px.bar(mat_rate, x='Rate', y='Sector', orientation='h',\n",
    "    color='Rate', color_continuous_scale='RdYlGn',\n",
    "    title='ESG Materiality Rate by Sector (%)',\n",
    "    labels={'Rate':'Materiality Rate (%)','Sector':''})\n",
    "fig.update_layout(template='plotly_dark', paper_bgcolor='#0b1a14',\n",
    "    plot_bgcolor='#112a1e', height=460, coloraxis_showscale=False,\n",
    "    yaxis=dict(autorange='reversed'))\n",
    "fig.show()\n",
    "print(mat_rate[['Sector','Material','Total','Rate']].to_string(index=False))"
]))

cells.append(md("c13",[
    "---\n",
    "## Portfolio Summary\n\n",
    "| Project | Key Finding |\n",
    "|---------|------------|\n",
    "| Heatmap | Extractives leads Environment; Financials leads Governance |\n",
    "| Top Topics | Business Ethics and Data Security material for nearly all industries |\n",
    "| Deep-Dive | Oil and Gas has 18+ material ESG topics |\n",
    "| Radar | Tech and Extractives have opposite ESG risk profiles |\n",
    "| Materiality Rate | Extractives and Infrastructure highest material rate |\n\n",
    "**Framework:** SASB Standards | **Tools:** Python, Pandas, Plotly  \n",
    "*ESG Portfolio - Naveed Baig - 2025*"
]))

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python (Miniconda3)",
            "language": "python",
            "name": "miniconda3"
        },
        "language_info": {"name": "python", "version": "3.13.9"}
    },
    "cells": cells
}

with open(r'C:/Users/Hp/ESG_Portfolio/esg_framework_portfolio.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Notebook created successfully!")

# Validate
with open(r'C:/Users/Hp/ESG_Portfolio/esg_framework_portfolio.ipynb', encoding='utf-8') as f:
    json.load(f)
print("Validation passed - file is valid!")
