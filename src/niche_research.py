"""
Niche Research Module
Analyzes trending topics and suggests content niches
"""

import json
from datetime import datetime
from utils.helpers import load_config, save_json, get_timestamp


class NicheResearcher:
    """Research and identify trending niches for TikTok content"""

    def __init__(self):
        self.config = load_config()
        self.niches_database = self._load_niches_database()

    def _load_niches_database(self):
        """Load built-in niches database"""
        return {
            "motivational": {
                "keywords": ["success", "motivation", "inspiration", "goals", "mindset"],
                "sub_niches": ["morning motivation", "business motivation", "fitness motivation", "study motivation"],
                "content_types": ["quotes", "stories", "tips", "routines"],
                "target_audience": "18-35 years",
                "engagement_rate": "high"
            },
            "educational": {
                "keywords": ["learn", "knowledge", "tutorial", "tips", "howto"],
                "sub_niches": ["tech tips", "language learning", "study hacks", "skill development"],
                "content_types": ["quick tips", "tutorials", "facts", "demonstrations"],
                "target_audience": "16-40 years",
                "engagement_rate": "medium-high"
            },
            "comedy": {
                "keywords": ["funny", "humor", "comedy", "entertainment", "laughs"],
                "sub_niches": ["relatable comedy", "observational humor", "sketch comedy", "reactions"],
                "content_types": ["skits", "reactions", "parodies", "memes"],
                "target_audience": "13-35 years",
                "engagement_rate": "very high"
            },
            "lifestyle": {
                "keywords": ["daily", "routine", "life", "vlog", "aesthetic"],
                "sub_niches": ["morning routine", "productivity", "minimalism", "self-care"],
                "content_types": ["routines", "day in life", "tips", "aesthetic videos"],
                "target_audience": "18-40 years",
                "engagement_rate": "medium"
            },
            "business": {
                "keywords": ["entrepreneur", "business", "money", "success", "startup"],
                "sub_niches": ["side hustles", "passive income", "business tips", "entrepreneurship"],
                "content_types": ["tips", "stories", "advice", "case studies"],
                "target_audience": "20-45 years",
                "engagement_rate": "medium-high"
            },
            "fitness": {
                "keywords": ["workout", "fitness", "gym", "health", "exercise"],
                "sub_niches": ["home workouts", "gym motivation", "nutrition", "transformation"],
                "content_types": ["routines", "tips", "motivation", "demonstrations"],
                "target_audience": "18-40 years",
                "engagement_rate": "high"
            },
            "food": {
                "keywords": ["recipe", "cooking", "food", "tasty", "delicious"],
                "sub_niches": ["quick recipes", "street food", "desserts", "healthy meals"],
                "content_types": ["recipes", "food review", "cooking tips", "hacks"],
                "target_audience": "18-45 years",
                "engagement_rate": "very high"
            },
            "tech": {
                "keywords": ["technology", "gadgets", "apps", "software", "AI"],
                "sub_niches": ["phone tips", "app reviews", "tech news", "AI tools"],
                "content_types": ["reviews", "tips", "comparisons", "tutorials"],
                "target_audience": "18-40 years",
                "engagement_rate": "medium-high"
            }
        }

    def research_niche(self, topic=None):
        """
        Research a specific niche or get recommendations

        Args:
            topic: Specific topic to research (optional)

        Returns:
            dict: Niche information and recommendations
        """
        if topic and topic.lower() in self.niches_database:
            niche_data = self.niches_database[topic.lower()]
            return {
                "niche": topic.lower(),
                "data": niche_data,
                "recommended": True,
                "suggestions": self._get_content_suggestions(topic.lower())
            }

        # Return top niches if no specific topic
        return {
            "all_niches": list(self.niches_database.keys()),
            "recommended_niches": self._get_recommended_niches(),
            "high_engagement": self._get_high_engagement_niches()
        }

    def _get_recommended_niches(self):
        """Get recommended niches based on configuration"""
        preferred = self.config.get('niches', {}).get('preferred', [])
        return [n for n in preferred if n in self.niches_database]

    def _get_high_engagement_niches(self):
        """Get niches with high engagement rates"""
        high_engagement = []
        for niche, data in self.niches_database.items():
            if 'high' in data.get('engagement_rate', '').lower():
                high_engagement.append({
                    "niche": niche,
                    "engagement": data['engagement_rate']
                })
        return high_engagement

    def _get_content_suggestions(self, niche):
        """Get content suggestions for a specific niche"""
        niche_data = self.niches_database.get(niche, {})
        sub_niches = niche_data.get('sub_niches', [])
        content_types = niche_data.get('content_types', [])

        suggestions = []
        for sub_niche in sub_niches[:3]:  # Top 3 sub-niches
            for content_type in content_types[:2]:  # Top 2 content types
                suggestions.append({
                    "sub_niche": sub_niche,
                    "content_type": content_type,
                    "idea": f"{content_type.title()} about {sub_niche}"
                })

        return suggestions[:5]  # Return top 5 suggestions

    def get_niche_ideas(self, niche, count=5):
        """
        Generate specific content ideas for a niche

        Args:
            niche: The niche to generate ideas for
            count: Number of ideas to generate

        Returns:
            list: List of content ideas
        """
        if niche.lower() not in self.niches_database:
            return []

        niche_data = self.niches_database[niche.lower()]
        ideas = []

        # Generate ideas based on sub-niches and content types
        for sub_niche in niche_data['sub_niches']:
            for content_type in niche_data['content_types']:
                if len(ideas) >= count:
                    break
                ideas.append({
                    "title": f"{content_type.title()}: {sub_niche.title()}",
                    "niche": niche,
                    "sub_niche": sub_niche,
                    "format": content_type,
                    "target_audience": niche_data['target_audience']
                })
            if len(ideas) >= count:
                break

        return ideas[:count]

    def save_research(self, niche, data):
        """Save research data to file"""
        timestamp = get_timestamp()
        filename = f"output/research_{niche}_{timestamp}.json"
        save_json(data, filename)
        return filename


def main():
    """CLI for niche research"""
    researcher = NicheResearcher()

    print("\n🔍 TikTok Niche Research Tool\n")
    print("Available niches:")
    all_niches = researcher.research_niche()
    for i, niche in enumerate(all_niches['all_niches'], 1):
        print(f"{i}. {niche.title()}")

    print("\n💡 High Engagement Niches:")
    for item in all_niches['high_engagement']:
        print(f"  - {item['niche'].title()} ({item['engagement']})")

    print("\n✨ Recommended Niches (from config):")
    for niche in all_niches['recommended_niches']:
        print(f"  - {niche.title()}")


if __name__ == "__main__":
    main()
