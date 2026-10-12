# -*- coding: utf-8 -*-
"""
Independent HHI verifier for Macau industry concentration.
HHI = sum of squared sector shares (shares in percent).
Change any number below and re-run:  python verify_hhi.py
"""

SECTORS = ['Manufacturing','Utilities','Construction','Wholesale&Retail','Hotels',
           'Restaurants','Transport','Banking','Insurance','RealEstate','RentalBiz',
           'PublicAdmin','Education','Health','Gaming','OtherServices']

# OFFICIAL DSEC producer-price sector shares (%) — SC_PIBP bulletins
DATA = {
 2015: [0.6,0.7,6.5,5.6,3.8,1.8,2.7,5.3,1.0,10.0,4.1,4.2,1.8,1.3,48.0,2.6],
 2019: [0.6,0.6,3.1,5.6,4.6,1.6,2.7,5.5,1.3, 9.1,4.3,4.3,1.9,1.5,50.9,2.3],
 2024: [0.7,0.8,3.3,6.2,6.0,2.2,2.8,5.1,2.7,10.2,4.7,5.5,2.6,2.0,43.3,1.8],
}

# How 16 detailed sectors roll up into 7 aggregated categories
GROUPS = {
 'Gaming'        : ['Gaming'],
 'Finance'       : ['Banking','Insurance'],
 'PublicAdminGrp': ['PublicAdmin','Education','Health','OtherServices'],
 'RealEstate'    : ['RealEstate'],
 'Construction'  : ['Construction'],
 'WholesaleRetail': ['Wholesale&Retail'],
 'Others'        : ['Manufacturing','Utilities','Hotels','Restaurants','Transport','RentalBiz'],
}

def hhi(vals):
    return int(round(sum(v*v for v in vals)))

for year, row in DATA.items():
    d = dict(zip(SECTORS, row))
    h16 = hhi(row)
    seven = [sum(d[s] for s in names) for names in GROUPS.values()]
    h7 = hhi(seven)
    print(f'\n{year}:  16-sector HHI = {h16}   |   7-sector HHI = {h7}')
    for g, names in GROUPS.items():
        print(f'    {g:16s} = {sum(d[s] for s in names):5.1f}%')
    print(f'    column total = {sum(row):.1f}%')
