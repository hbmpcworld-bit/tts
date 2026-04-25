"""
Bulk Processor Module
Process multiple videos in bulk
"""

import time
from tqdm import tqdm
from utils.helpers import load_config, save_json, get_timestamp
from src.niche_research import NicheResearcher
from src.script_generator import ScriptGenerator
from src.image_generator import ImageGenerator
from src.video_generator import VideoGenerator
from src.scheduler import ContentScheduler


class BulkProcessor:
    """Process multiple TikTok videos in bulk"""

    def __init__(self, ai_provider="openai", image_provider="replicate"):
        """
        Initialize bulk processor

        Args:
            ai_provider: AI provider for scripts ("openai" or "anthropic")
            image_provider: Image provider ("replicate", "openai", or "stability")
        """
        self.config = load_config()
        self.bulk_config = self.config.get('bulk', {})

        self.niche_researcher = NicheResearcher()
        self.script_generator = ScriptGenerator(ai_provider=ai_provider)
        self.image_generator = ImageGenerator(provider=image_provider)
        self.video_generator = VideoGenerator()
        self.scheduler = ContentScheduler()

    def process_full_pipeline(self, niche, count=5, duration=30, language="urdu"):
        """
        Run full pipeline: research → script → images → video prompts

        Args:
            niche: Content niche
            count: Number of videos to create
            duration: Video duration in seconds
            language: Script language

        Returns:
            dict: Results with all generated content
        """
        print(f"\n🚀 Starting bulk processing: {count} videos in '{niche}' niche")
        print("=" * 70)

        results = {
            'niche': niche,
            'count': count,
            'videos': [],
            'summary': {},
            'generated_at': get_timestamp()
        }

        # Step 1: Research niche
        print("\n📊 Step 1: Researching niche...")
        niche_data = self.niche_researcher.research_niche(niche)

        if not niche_data.get('recommended'):
            print(f"⚠️  Niche '{niche}' not in database. Using generic approach.")

        # Get content ideas
        ideas = self.niche_researcher.get_niche_ideas(niche, count)

        # Step 2: Generate scripts
        print(f"\n📝 Step 2: Generating {count} scripts...")
        scripts = []

        for i in tqdm(range(count), desc="Scripts"):
            idea = ideas[i] if i < len(ideas) else None
            sub_niche = idea['sub_niche'] if idea else None

            script = self.script_generator.generate_script(
                niche=niche,
                sub_niche=sub_niche,
                duration=duration,
                language=language
            )

            script_path = self.script_generator.save_script(script)
            scripts.append({
                'data': script,
                'path': script_path,
                'idea': idea
            })

            # Delay between requests
            delay = self.bulk_config.get('delay_between', 2)
            if i < count - 1:  # Don't delay after last item
                time.sleep(delay)

        # Step 3: Generate images
        print(f"\n🎨 Step 3: Generating images...")
        image_config = self.config.get('image', {})
        images_per_script = image_config.get('count_per_script', 3)

        for i, script_item in enumerate(tqdm(scripts, desc="Images")):
            script_text = script_item['data']['script']

            images = self.image_generator.generate_from_script(
                script_text,
                count=images_per_script
            )

            script_item['images'] = images

            # Delay between requests
            delay = self.bulk_config.get('delay_between', 2)
            if i < len(scripts) - 1:
                time.sleep(delay)

        # Step 4: Generate video prompts
        print(f"\n🎬 Step 4: Creating video prompts...")

        for i, script_item in enumerate(tqdm(scripts, desc="Video prompts")):
            video_prompt = self.video_generator.create_video_prompt(
                script_item['data'],
                script_item.get('images')
            )

            video_path = self.video_generator.save_video_prompt(video_prompt)

            script_item['video_prompt'] = {
                'data': video_prompt,
                'path': video_path
            }

        # Step 5: Create posting schedule
        print(f"\n📅 Step 5: Creating posting schedule...")
        schedule = self.scheduler.create_schedule(count, days=7)
        schedule_path = self.scheduler.save_schedule(schedule)

        # Compile results
        for i, script_item in enumerate(scripts):
            results['videos'].append({
                'video_number': i + 1,
                'idea': script_item.get('idea'),
                'script': {
                    'path': script_item['path'],
                    'preview': script_item['data']['script'][:100] + '...'
                },
                'images': [
                    {
                        'path': img.get('local_path'),
                        'url': img.get('url')
                    }
                    for img in script_item.get('images', [])
                ],
                'video_prompt_path': script_item['video_prompt']['path'],
                'scheduled_time': schedule[i] if i < len(schedule) else None
            })

        results['summary'] = {
            'total_videos': count,
            'scripts_generated': len(scripts),
            'images_generated': sum(len(s.get('images', [])) for s in scripts),
            'schedule_path': schedule_path,
            'niche': niche
        }

        # Save complete results
        results_path = f"output/bulk_results_{niche}_{get_timestamp()}.json"
        save_json(results, results_path)

        print("\n" + "=" * 70)
        print("✅ BULK PROCESSING COMPLETE!")
        print("=" * 70)
        print(f"\n📊 Summary:")
        print(f"  ✓ {results['summary']['scripts_generated']} scripts generated")
        print(f"  ✓ {results['summary']['images_generated']} images created")
        print(f"  ✓ {count} video prompts created")
        print(f"  ✓ Posting schedule created")
        print(f"\n💾 Results saved to: {results_path}")

        return results

    def process_scripts_only(self, niche, count=10, **kwargs):
        """Generate scripts only (no images/videos)"""
        print(f"\n📝 Generating {count} scripts for '{niche}'...")

        scripts = []
        for i in tqdm(range(count)):
            script = self.script_generator.generate_script(niche=niche, **kwargs)
            path = self.script_generator.save_script(script)
            scripts.append({'data': script, 'path': path})

            delay = self.bulk_config.get('delay_between', 2)
            if i < count - 1:
                time.sleep(delay)

        print(f"\n✅ Generated {len(scripts)} scripts!")
        return scripts

    def process_images_only(self, script_files, count_per_script=3):
        """Generate images for existing scripts"""
        print(f"\n🎨 Generating images for {len(script_files)} scripts...")

        results = []
        for script_file in tqdm(script_files):
            # Load script
            with open(script_file, 'r', encoding='utf-8') as f:
                script_text = f.read()

            images = self.image_generator.generate_from_script(
                script_text,
                count=count_per_script
            )

            results.append({
                'script_file': script_file,
                'images': images
            })

            delay = self.bulk_config.get('delay_between', 2)
            time.sleep(delay)

        print(f"\n✅ Generated images for {len(results)} scripts!")
        return results


def main():
    """CLI for bulk processing"""
    print("\n🔄 TikTok Bulk Processor\n")

    # Example: Full pipeline
    processor = BulkProcessor(ai_provider="openai", image_provider="replicate")

    results = processor.process_full_pipeline(
        niche="motivational",
        count=3,
        duration=30,
        language="urdu"
    )

    print(f"\n📁 Check 'output/' folder for all generated content!")


if __name__ == "__main__":
    main()
