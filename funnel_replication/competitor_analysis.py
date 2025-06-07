
from bs4 import BeautifulSoup
import requests
from typing import Dict, List
import json
from urllib.parse import urlparse
import re

class FunnelAnalyzer:
    def __init__(self):
        self.patterns = {
            'hero_section': {
                'selectors': ['header', '.hero', '#hero'],
                'attributes': ['background-image', 'h1', 'cta']
            },
            'benefits': {
                'selectors': ['.benefits', '.features', '.advantages'],
                'attributes': ['list-items', 'icons', 'headings']
            },
            'social_proof': {
                'selectors': ['.testimonials', '.reviews', '.trust-badges'],
                'attributes': ['quotes', 'ratings', 'logos']
            },
            'cta_elements': {
                'selectors': ['.cta', 'button', '.sign-up'],
                'attributes': ['text', 'color', 'position']
            }
        }

    def extract_page_structure(self, url: str) -> Dict:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            structure = {
                'layout': self.analyze_layout(soup),
                'elements': self.extract_elements(soup),
                'conversion_points': self.identify_conversion_points(soup),
                'schema_org': self.extract_schema_markup(soup)
            }

            return structure
        except Exception as e:
            print(f"Error analyzing {url}: {str(e)}")
            return None

    def analyze_layout(self, soup: BeautifulSoup) -> Dict:
        """Analyze page layout and hierarchy"""
        layout = {
            'sections': [],
            'hierarchy': [],
            'visual_flow': []
        }

        for section in soup.find_all(['section', 'div']):
            if self.is_major_section(section):
                layout['sections'].append({
                    'type': self.determine_section_type(section),
                    'position': self.get_position(section),
                    'emphasis': self.calculate_emphasis(section)
                })

        return layout

    def extract_elements(self, soup: BeautifulSoup) -> Dict:
        """Extract key page elements"""
        elements = {}

        for pattern_name, pattern_data in self.patterns.items():
            elements[pattern_name] = []
            for selector in pattern_data['selectors']:
                found_elements = soup.select(selector)
                for element in found_elements:
                    elements[pattern_name].append({
                        'content': self.extract_content(element),
                        'style': self.extract_styles(element),
                        'attributes': self.extract_attributes(element, pattern_data['attributes'])
                    })

        return elements

    def identify_conversion_points(self, soup: BeautifulSoup) -> List[Dict]:
        """Identify conversion points and their characteristics"""
        conversion_points = []

        for element in soup.find_all(['a', 'button', 'form']):
            if self.is_conversion_point(element):
                conversion_points.append({
                    'type': self.determine_conversion_type(element),
                    'position': self.get_position(element),
                    'visibility': self.calculate_visibility(element),
                    'trigger_type': self.identify_trigger(element)
                })

        return conversion_points

    def extract_schema_markup(self, soup: BeautifulSoup) -> Dict:
        """Extract schema.org markup"""
        schema_data = {}

        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                schema_data.update(data)
            except:
                continue

        return schema_data
