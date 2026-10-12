# -*- coding: utf-8 -*-
"""
Full-decade (2015-2024) Macau industry concentration (HHI) from DSEC sector shares.
Reads sector_shares_allyears.json (DSEC producer-price 16-sector shares).
Outputs:
  - HHI_full_decade.csv : yearly gaming share, non-gaming share, HHI(7), HHI(16)
  - gaming_hhi_trend.png : gaming share + HHI dual-axis line, 10 years
  - structure_area.png  : 7-category stacked area, 10 years
7-category aggregation kept IDENTICAL to fix_figures.py (consistent with Fig.1).
"""
import os, json, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)
plt.rcParams['font.family'] = 'DejaVu Sans'

with open(os.path.join(DATA, "sector_shares_allyears.json"), encoding="utf-8") as f:
    data = json.load(f)
years = list(range(2015, 2025))

def aggregate(d):
    return {
        'Gaming': d['Gaming'],
        'Finance': d['Banking'] + d['Insurance'],
        'Public Admin, Edu, Health & Other': d['PubAdmin'] + d['Education'] + d['Health'] + d['Other'],
        'Real Estate': d['RealEstate'],
        'Construction': d['Construction'],
        'Wholesale & Retail': d['Retail'],
        'Others': d['Manufacturing'] + d['Utilities'] + d['Hotels'] +
                  d['Restaurants'] + d['Transport'] + d['RentalBiz'],
    }

agg, raw16 = {}, {}
for y in years:
    d = {k: (data[str(y)].get(k, 0) or 0) for k in
         ['Manufacturing','Utilities','Construction','Retail','Hotels','Restaurants',
          'Transport','Banking','Insurance','RealEstate','RentalBiz','PubAdmin',
          'Education','Health','Gaming','Other']}
    raw16[y] = d
    agg[y] = aggregate(d)

def hhi(d): return int(round(sum(v*v for v in d.values())))

rows = []
print(f"{'Year':<6}{'Gaming%':<9}{'NonGame%':<10}{'HHI7':<7}{'HHI16'}")
for y in years:
    g = agg[y]['Gaming']
    rows.append([y, round(g,1), round(100-g,1), hhi(agg[y]), hhi(raw16[y])])
    print(f"{y:<6}{g:<9.1f}{100-g:<10.1f}{hhi(agg[y]):<7}{hhi(raw16[y])}")

with open(os.path.join(DATA,"HHI_full_decade.csv"),"w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["Year","Gaming_share_pct","NonGaming_share_pct","HHI_7cat","HHI_16cat"]); w.writerows(rows)

# ---------- Figure 4: gaming share + HHI dual axis ----------
gaming = [agg[y]['Gaming'] for y in years]
h7 = [hhi(agg[y]) for y in years]
fig, ax1 = plt.subplots(figsize=(11,6))
ax1.plot(years, gaming, '-o', color='#8B0000', lw=2.4, ms=7, label='Gaming share of GDP (%)')
for x,v in zip(years,gaming): ax1.annotate(f'{v:.1f}',(x,v),textcoords="offset points",xytext=(0,9),ha='center',fontsize=9,color='#8B0000')
ax1.set_xlabel('Year',fontsize=12); ax1.set_ylabel('Gaming value-added share (%)',color='#8B0000',fontsize=12)
ax1.set_ylim(0,60); ax1.set_xticks(years); ax1.tick_params(axis='y',labelcolor='#8B0000')
ax1.axvspan(2019.5,2022.5,color='#FFE9B0',alpha=0.5,zorder=0)
ax1.text(2021,56,'COVID-19 border closure',ha='center',fontsize=9.5,style='italic')
ax2=ax1.twinx()
ax2.plot(years,h7,'--s',color='#1f4e79',lw=1.8,ms=6,label='HHI (7 sectors)')
for x,v in zip(years,h7): ax2.annotate(f'{v}',(x,v),textcoords="offset points",xytext=(0,-15),ha='center',fontsize=8.5,color='#1f4e79')
ax2.axhline(2500,color='gray',ls=':',lw=1.3); ax2.text(2015.05,2525,'HHI 2,500 high-concentration line',fontsize=9,color='gray')
ax2.set_ylabel('Herfindahl-Hirschman Index',color='#1f4e79',fontsize=12); ax2.set_ylim(1500,3300)
ax2.tick_params(axis='y',labelcolor='#1f4e79')
l1,la1=ax1.get_legend_handles_labels(); l2,la2=ax2.get_legend_handles_labels()
ax1.legend(l1+l2,la1+la2,loc='upper right',frameon=False,fontsize=10)
ax1.set_title("Gaming Share and Sectoral Concentration (HHI), Macau 2015-2024",fontsize=13,pad=12)
ax1.spines['top'].set_visible(False)
fig.text(0.055,0.015,"Source: DSEC Industrial Structure reports 2015-2024 (producer prices). HHI computed by author under the 7-category aggregation defined in this repo.",fontsize=8.8)
plt.tight_layout(rect=[0,0.03,1,1])
p4=os.path.join(FIG,"gaming_hhi_trend.png"); plt.savefig(p4,dpi=200,bbox_inches='tight'); plt.close(); print("saved",p4)

# ---------- Figure 5: 7-cat stacked area ----------
cats=['Gaming','Finance','Public Admin, Edu, Health & Other','Real Estate','Construction','Wholesale & Retail','Others']
colors=['#8B0000','#2ECC40','#6B6B6B','#B0B0B0','#D9A441','#7FA8D0','#CFE0F0']
M=np.array([[agg[y][c] for y in years] for c in cats])
fig,ax=plt.subplots(figsize=(11,6))
ax.stackplot(years,M,labels=cats,colors=colors,edgecolor='white',lw=0.5,alpha=0.95)
ax.set_xlim(2015,2024); ax.set_ylim(0,100); ax.set_xticks(years)
ax.set_xlabel('Year',fontsize=12); ax.set_ylabel('Share of GDP (%)',fontsize=12)
ax.set_title("Structural Composition of Macau GDP, 2015-2024 (7 sectors)",fontsize=13,pad=12)
ax.legend(loc='upper left',bbox_to_anchor=(1.01,1),frameon=False,fontsize=9.5)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.text(0.055,0.015,"Source: DSEC Industrial Structure reports 2015-2024 (producer prices); categories aggregated by author.",fontsize=8.8)
plt.tight_layout(rect=[0,0.03,0.82,1])
p5=os.path.join(FIG,"structure_area.png"); plt.savefig(p5,dpi=200,bbox_inches='tight'); plt.close(); print("saved",p5)
