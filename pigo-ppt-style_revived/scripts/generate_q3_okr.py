#!/usr/bin/env python3
"""
Pigo PPT Style - Test Generator
Generate a 5-page Q3 OKR sample presentation using Pigo brand style
"""

import os
import sys
from datetime import datetime

# Brand colors
PIGO_BLUE = "#3B82F6"
PIGO_PURPLE = "#8B5CF6"
PIGO_CYAN = "#06B6D4"
PIGO_DARK = "#111827"
PIGO_TEXT = "#111827"
PIGO_TEXT_SEC = "#6B7280"
PIGO_SURFACE = "#F9FAFB"
PIGO_WHITE = "#FFFFFF"
PIGO_SUCCESS = "#10B981"
PIGO_WARNING = "#F59E0B"

OUTPUT_DIR = "/home/pigo/pigo-ppt-test"

def create_project():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/svg_output", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/sources", exist_ok=True)
    print(f"[OK] Created project at {OUTPUT_DIR}")

def generate_cover():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{PIGO_DARK}"/>
      <stop offset="100%" stop-color="#1f2937"/>
    </linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#bg)"/>
  <rect x="0" y="0" width="1280" height="8" fill="{PIGO_BLUE}"/>
  <rect x="60" y="200" width="100" height="6" rx="3" fill="{PIGO_BLUE}"/>
  <text x="60" y="300" font-family="Inter, Arial, sans-serif" font-size="56" font-weight="700" fill="{PIGO_WHITE}">Q3 OKR</text>
  <text x="60" y="380" font-family="Inter, Arial, sans-serif" font-size="24" fill="{PIGO_TEXT_SEC}">Objectives &amp; Key Results</text>
  <text x="60" y="620" font-family="Inter, Arial, sans-serif" font-size="14" fill="{PIGO_TEXT_SEC}">{datetime.now().strftime("%Y-%m-%d")} | Pigo</text>
  <text x="640" y="680" font-family="Inter, Arial, sans-serif" font-size="12" fill="{PIGO_TEXT_SEC}" text-anchor="middle">1</text>
</svg>'''
    with open(f"{OUTPUT_DIR}/svg_output/01_cover.svg", "w") as f:
        f.write(svg)
    print(f"[OK] Generated 01_cover.svg")

def generate_chapter():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="{PIGO_WHITE}"/>
  <rect x="0" y="0" width="1280" height="8" fill="{PIGO_BLUE}"/>
  <rect x="60" y="300" width="6" height="120" rx="3" fill="{PIGO_BLUE}"/>
  <text x="100" y="320" font-family="Inter, Arial, sans-serif" font-size="20" font-weight="600" fill="{PIGO_TEXT_SEC}">OBJECTIVES</text>
  <text x="100" y="380" font-family="Inter, Arial, sans-serif" font-size="48" font-weight="700" fill="{PIGO_TEXT}">Our Strategic Goals</text>
  <text x="640" y="680" font-family="Inter, Arial, sans-serif" font-size="12" fill="{PIGO_TEXT_SEC}" text-anchor="middle">2</text>
</svg>'''
    with open(f"{OUTPUT_DIR}/svg_output/02_chapter.svg", "w") as f:
        f.write(svg)
    print(f"[OK] Generated 02_chapter.svg")

def generate_content():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="{PIGO_WHITE}"/>
  <rect x="0" y="0" width="1280" height="6" fill="{PIGO_BLUE}"/>
  <text x="60" y="45" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="600" fill="{PIGO_BLUE}" letter-spacing="1">OVERVIEW</text>
  <text x="60" y="95" font-family="Inter, Arial, sans-serif" font-size="32" font-weight="700" fill="{PIGO_TEXT}">Q3 Focus Areas</text>
  
  <!-- OKR Card 1 -->
  <rect x="60" y="140" width="360" height="180" rx="8" fill="{PIGO_SURFACE}" stroke="{PIGO_BLUE}" stroke-width="2"/>
  <text x="80" y="180" font-family="Inter, Arial, sans-serif" font-size="16" font-weight="700" fill="{PIGO_BLUE}">O1: Growth</text>
  <text x="80" y="210" font-family="Inter, Arial, sans-serif" font-size="14" fill="{PIGO_TEXT_SEC}">Revenue +30%</text>
  <text x="80" y="240" font-family="Inter, Arial, sans-serif" font-size="12" fill="{PIGO_SUCCESS}">● On Track</text>
  
  <!-- OKR Card 2 -->
  <rect x="460" y="140" width="360" height="180" rx="8" fill="{PIGO_SURFACE}" stroke="{PIGO_PURPLE}" stroke-width="2"/>
  <text x="480" y="180" font-family="Inter, Arial, sans-serif" font-size="16" font-weight="700" fill="{PIGO_PURPLE}">O2: Efficiency</text>
  <text x="480" y="210" font-family="Inter, Arial, sans-serif" font-size="14" fill="{PIGO_TEXT_SEC}">Process automation 50%</text>
  <text x="480" y="240" font-family="Inter, Arial, sans-serif" font-size="12" fill="{PIGO_WARNING}">● At Risk</text>
  
  <!-- OKR Card 3 -->
  <rect x="860" y="140" width="360" height="180" rx="8" fill="{PIGO_SURFACE}" stroke="{PIGO_CYAN}" stroke-width="2"/>
  <text x="880" y="180" font-family="Inter, Arial, sans-serif" font-size="16" font-weight="700" fill="{PIGO_CYAN}">O3: Culture</text>
  <text x="880" y="210" font-family="Inter, Arial, sans-serif" font-size="14" fill="{PIGO_TEXT_SEC}">Team engagement +20%</text>
  <text x="880" y="240" font-family="Inter, Arial, sans-serif" font-size="12" fill="{PIGO_SUCCESS}">● On Track</text>
  
  <line x1="60" y1="670" x2="1220" y2="670" stroke="#E5E7EB" stroke-width="1"/>
  <text x="640" y="695" font-family="Inter, Arial, sans-serif" font-size="12" fill="{PIGO_TEXT_SEC}" text-anchor="middle">3</text>
</svg>'''
    with open(f"{OUTPUT_DIR}/svg_output/03_content.svg", "w") as f:
        f.write(svg)
    print(f"[OK] Generated 03_content.svg")

def generate_data():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="{PIGO_WHITE}"/>
  <rect x="0" y="0" width="1280" height="6" fill="{PIGO_BLUE}"/>
  <text x="60" y="45" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="600" fill="{PIGO_BLUE}" letter-spacing="1">KEY RESULTS</text>
  <text x="60" y="95" font-family="Inter, Arial, sans-serif" font-size="32" font-weight="700" fill="{PIGO_TEXT}">Progress Metrics</text>
  
  <!-- Progress bars -->
  <text x="60" y="160" font-family="Inter, Arial, sans-serif" font-size="14" fill="{PIGO_TEXT}">KR1: Revenue Target</text>
  <rect x="60" y="175" width="600" height="24" rx="4" fill="#E5E7EB"/>
  <rect x="60" y="175" width="420" height="24" rx="4" fill="{PIGO_BLUE}"/>
  <text x="680" y="192" font-family="Inter, Arial, sans-serif" font-size="14" fill="{PIGO_TEXT}">70%</text>
  
  <text x="60" y="230" font-family="Inter, Arial, sans-serif" font-size="14" fill="{PIGO_TEXT}">KR2: Customer Acquisition</text>
  <rect x="60" y="245" width="600" height="24" rx="4" fill="#E5E7EB"/>
  <rect x="60" y="245" width="360" height="24" rx="4" fill="{PIGO_PURPLE}"/>
  <text x="680" y="262" font-family="Inter, Arial, sans-serif" font-size="14" fill="{PIGO_TEXT}">60%</text>
  
  <text x="60" y="300" font-family="Inter, Arial, sans-serif" font-size="14" fill="{PIGO_TEXT}">KR3: NPS Score</text>
  <rect x="60" y="315" width="600" height="24" rx="4" fill="#E5E7EB"/>
  <rect x="60" y="315" width="540" height="24" rx="4" fill="{PIGO_SUCCESS}"/>
  <text x="680" y="332" font-family="Inter, Arial, sans-serif" font-size="14" fill="{PIGO_TEXT}">90%</text>
  
  <!-- Summary stats -->
  <rect x="800" y="160" width="180" height="120" rx="8" fill="{PIGO_SURFACE}"/>
  <text x="890" y="200" font-family="Inter, Arial, sans-serif" font-size="32" font-weight="700" fill="{PIGO_BLUE}" text-anchor="middle">73%</text>
  <text x="890" y="240" font-family="Inter, Arial, sans-serif" font-size="12" fill="{PIGO_TEXT_SEC}" text-anchor="middle">Avg. Progress</text>
  
  <rect x="1000" y="160" width="180" height="120" rx="8" fill="{PIGO_SURFACE}"/>
  <text x="1090" y="200" font-family="Inter, Arial, sans-serif" font-size="32" font-weight="700" fill="{PIGO_SUCCESS}" text-anchor="middle">2/3</text>
  <text x="1090" y="240" font-family="Inter, Arial, sans-serif" font-size="12" fill="{PIGO_TEXT_SEC}" text-anchor="middle">On Track</text>
  
  <line x1="60" y1="670" x2="1220" y2="670" stroke="#E5E7EB" stroke-width="1"/>
  <text x="640" y="695" font-family="Inter, Arial, sans-serif" font-size="12" fill="{PIGO_TEXT_SEC}" text-anchor="middle">4</text>
</svg>'''
    with open(f"{OUTPUT_DIR}/svg_output/04_data.svg", "w") as f:
        f.write(svg)
    print(f"[OK] Generated 04_data.svg")

def generate_ending():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <defs>
    <linearGradient id="bgEnd" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{PIGO_DARK}"/>
      <stop offset="100%" stop-color="#1f2937"/>
    </linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#bgEnd)"/>
  <rect x="0" y="0" width="1280" height="8" fill="{PIGO_BLUE}"/>
  <text x="640" y="260" font-family="Inter, Arial, sans-serif" font-size="44" font-weight="700" fill="{PIGO_WHITE}" text-anchor="middle">Let's Achieve Our Goals</text>
  <text x="640" y="340" font-family="Inter, Arial, sans-serif" font-size="20" fill="{PIGO_TEXT_SEC}" text-anchor="middle">Q3 2026 | Pigo</text>
  <text x="640" y="550" font-family="Inter, Arial, sans-serif" font-size="14" fill="{PIGO_TEXT_SEC}" text-anchor="middle">contact@pigo.com</text>
  <text x="640" y="680" font-family="Inter, Arial, sans-serif" font-size="12" fill="{PIGO_TEXT_SEC}" text-anchor="middle">5</text>
</svg>'''
    with open(f"{OUTPUT_DIR}/svg_output/05_ending.svg", "w") as f:
        f.write(svg)
    print(f"[OK] Generated 05_ending.svg")

def main():
    print("="*50)
    print("Pigo PPT Style - Q3 OKR Test Generator")
    print("="*50)
    create_project()
    generate_cover()
    generate_chapter()
    generate_content()
    generate_data()
    generate_ending()
    print("="*50)
    print(f"[DONE] Generated 5 pages at {OUTPUT_DIR}/svg_output/")
    print("Files:", os.listdir(f"{OUTPUT_DIR}/svg_output/"))

if __name__ == "__main__":
    main()