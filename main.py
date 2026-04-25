#!/usr/bin/env python3
"""
TikTok Content Automation Tool - Main CLI
"""

import click
import sys
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

from src.niche_research import NicheResearcher
from src.script_generator import ScriptGenerator
from src.image_generator import ImageGenerator
from src.video_generator import VideoGenerator
from src.scheduler import ContentScheduler
from src.bulk_processor import BulkProcessor
from utils.helpers import ensure_output_dirs, load_json


def print_banner():
    """Print tool banner"""
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     🎬 TikTok Content Automation Tool 🎬                 ║
║                                                           ║
║     Create Original, Engaging Content at Scale            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """TikTok Content Automation Tool - Create engaging content at scale"""
    ensure_output_dirs()


@cli.command()
@click.option('--topic', '-t', help='Specific topic to research')
def research(topic):
    """Research trending niches and get content ideas"""
    print(f"\n{Fore.YELLOW}🔍 Researching Niches...{Style.RESET_ALL}\n")

    researcher = NicheResearcher()

    if topic:
        result = researcher.research_niche(topic)
        print(f"{Fore.GREEN}✓ Research for: {topic.upper()}{Style.RESET_ALL}\n")

        if result.get('recommended'):
            data = result['data']
            print(f"📊 Niche: {topic}")
            print(f"🎯 Target Audience: {data['target_audience']}")
            print(f"📈 Engagement: {data['engagement_rate']}")
            print(f"\n💡 Content Types: {', '.join(data['content_types'])}")
            print(f"\n🔑 Keywords: {', '.join(data['keywords'])}")

            print(f"\n{Fore.CYAN}💡 Content Suggestions:{Style.RESET_ALL}")
            for i, suggestion in enumerate(result['suggestions'], 1):
                print(f"  {i}. {suggestion['idea']}")
        else:
            print(f"{Fore.YELLOW}⚠️  Topic not in database{Style.RESET_ALL}")
    else:
        result = researcher.research_niche()
        print(f"{Fore.GREEN}✓ Available Niches:{Style.RESET_ALL}\n")

        for i, niche in enumerate(result['all_niches'], 1):
            print(f"  {i}. {niche.title()}")

        print(f"\n{Fore.CYAN}💎 High Engagement Niches:{Style.RESET_ALL}")
        for item in result['high_engagement']:
            print(f"  • {item['niche'].title()} ({item['engagement']})")


@cli.command()
@click.option('--niche', '-n', required=True, help='Content niche')
@click.option('--sub-niche', '-s', help='Specific sub-niche')
@click.option('--duration', '-d', default=30, help='Video duration in seconds')
@click.option('--language', '-l', default='urdu', type=click.Choice(['urdu', 'english', 'both']))
@click.option('--count', '-c', default=1, help='Number of scripts to generate')
@click.option('--provider', '-p', default='openai', type=click.Choice(['openai', 'anthropic']))
def generate_script(niche, sub_niche, duration, language, count, provider):
    """Generate TikTok scripts using AI"""
    print(f"\n{Fore.YELLOW}📝 Generating Scripts...{Style.RESET_ALL}\n")

    generator = ScriptGenerator(ai_provider=provider)

    if count == 1:
        script = generator.generate_script(
            niche=niche,
            sub_niche=sub_niche,
            duration=duration,
            language=language
        )

        print(f"{Fore.GREEN}✓ Script Generated!{Style.RESET_ALL}\n")
        print("=" * 70)
        print(script['script'])
        print("=" * 70)

        filepath = generator.save_script(script)
        print(f"\n{Fore.CYAN}💾 Saved to: {filepath}{Style.RESET_ALL}")
    else:
        scripts = generator.generate_multiple(
            niche=niche,
            sub_niche=sub_niche,
            duration=duration,
            language=language,
            count=count
        )

        print(f"\n{Fore.GREEN}✓ Generated {len(scripts)} scripts!{Style.RESET_ALL}")

        for i, script in enumerate(scripts, 1):
            filepath = generator.save_script(script)
            print(f"  {i}. {filepath}")


@cli.command()
@click.option('--prompt', '-p', required=True, help='Image description')
@click.option('--style', '-s', default='cinematic', type=click.Choice(['cinematic', 'realistic', 'cartoon', 'anime']))
@click.option('--provider', default='replicate', type=click.Choice(['replicate', 'openai', 'stability']))
def generate_image(prompt, style, provider):
    """Generate images for videos"""
    print(f"\n{Fore.YELLOW}🎨 Generating Image...{Style.RESET_ALL}\n")

    generator = ImageGenerator(provider=provider)

    image = generator.generate_image(prompt, style=style, aspect_ratio="9:16")

    print(f"{Fore.GREEN}✓ Image Generated!{Style.RESET_ALL}")
    print(f"URL: {image['url']}")
    print(f"Provider: {image['provider']}")

    if 'note' not in image:
        try:
            local_path = generator.download_image(image['url'])
            print(f"{Fore.CYAN}💾 Saved to: {local_path}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Download failed: {e}{Style.RESET_ALL}")


@cli.command()
@click.option('--script', '-s', required=True, help='Path to script file (JSON)')
@click.option('--images', '-i', help='Path to images JSON file')
def generate_video(script, images):
    """Generate video prompts from script"""
    print(f"\n{Fore.YELLOW}🎬 Creating Video Prompt...{Style.RESET_ALL}\n")

    generator = VideoGenerator()

    # Load script
    script_data = load_json(script)

    # Load images if provided
    images_data = None
    if images:
        images_data = load_json(images)

    # Generate video prompt
    video_prompt = generator.create_video_prompt(script_data, images_data)

    print(f"{Fore.GREEN}✓ Video Prompt Created!{Style.RESET_ALL}")
    print(f"Duration: {video_prompt['project_info']['duration']}s")
    print(f"Scenes: {len(video_prompt['scenes'])}")

    filepath = generator.save_video_prompt(video_prompt)
    print(f"\n{Fore.CYAN}💾 Saved to:{Style.RESET_ALL}")
    print(f"  JSON: {filepath}")
    print(f"  TXT:  {filepath.replace('.json', '.txt')}")


@cli.command()
@click.option('--count', '-c', default=10, help='Number of videos')
@click.option('--days', '-d', default=7, help='Days to spread over')
def schedule(count, days):
    """Create posting schedule"""
    print(f"\n{Fore.YELLOW}📅 Creating Schedule...{Style.RESET_ALL}\n")

    scheduler = ContentScheduler()

    # Create schedule
    schedule_data = scheduler.create_schedule(count, days)

    print(f"{Fore.GREEN}✓ Schedule Created for {count} videos over {days} days{Style.RESET_ALL}\n")

    # Show first few
    for item in schedule_data[:5]:
        print(f"Video #{item['video_number']}: {item['date']} at {item['time']}")

    if len(schedule_data) > 5:
        print(f"... and {len(schedule_data) - 5} more")

    # Save
    filepath = scheduler.save_schedule(schedule_data)
    print(f"\n{Fore.CYAN}💾 Full schedule saved to: {filepath}{Style.RESET_ALL}")


@cli.command()
@click.option('--niche', '-n', required=True, help='Content niche')
@click.option('--count', '-c', default=5, help='Number of videos to create')
@click.option('--duration', '-d', default=30, help='Video duration in seconds')
@click.option('--language', '-l', default='urdu', type=click.Choice(['urdu', 'english', 'both']))
@click.option('--ai-provider', default='openai', type=click.Choice(['openai', 'anthropic']))
@click.option('--image-provider', default='replicate', type=click.Choice(['replicate', 'openai', 'stability']))
def bulk(niche, count, duration, language, ai_provider, image_provider):
    """Run full pipeline in bulk: research → scripts → images → videos"""
    print_banner()

    processor = BulkProcessor(ai_provider=ai_provider, image_provider=image_provider)

    results = processor.process_full_pipeline(
        niche=niche,
        count=count,
        duration=duration,
        language=language
    )

    print(f"\n{Fore.GREEN}{'=' * 70}")
    print(f"✅ SUCCESS! All content generated.")
    print(f"{'=' * 70}{Style.RESET_ALL}")

    print(f"\n📁 Check the following folders:")
    print(f"  • output/scripts/  - Generated scripts")
    print(f"  • output/images/   - Generated images")
    print(f"  • output/videos/   - Video prompts")


@cli.command()
def best_times():
    """Show best posting times analysis"""
    print(f"\n{Fore.YELLOW}⏰ Best Posting Times Analysis{Style.RESET_ALL}\n")

    scheduler = ContentScheduler()
    analysis = scheduler.analyze_best_times()

    print(f"{Fore.CYAN}📈 Weekday Best Times:{Style.RESET_ALL}")
    for time_info in analysis['weekday_best_times']:
        print(f"  {time_info['time']} - {time_info['reason']}")

    print(f"\n{Fore.CYAN}📈 Weekend Best Times:{Style.RESET_ALL}")
    for time_info in analysis['weekend_best_times']:
        print(f"  {time_info['time']} - {time_info['reason']}")

    print(f"\n{Fore.RED}❌ Times to Avoid:{Style.RESET_ALL}")
    for time_info in analysis['avoid_times']:
        print(f"  {time_info['time']} - {time_info['reason']}")

    print(f"\n{Fore.YELLOW}💡 Tips:{Style.RESET_ALL}")
    for tip in analysis['tips']:
        print(f"  • {tip}")


@cli.command()
def setup():
    """Show setup instructions and API key information"""
    print_banner()

    print(f"{Fore.YELLOW}📋 SETUP INSTRUCTIONS{Style.RESET_ALL}\n")

    print(f"{Fore.CYAN}Step 1: Install Dependencies{Style.RESET_ALL}")
    print("  pip install -r requirements.txt\n")

    print(f"{Fore.CYAN}Step 2: Get API Keys{Style.RESET_ALL}\n")

    apis = [
        {
            'name': 'OpenAI (for script generation)',
            'url': 'https://platform.openai.com/api-keys',
            'env': 'OPENAI_API_KEY',
            'required': 'Yes (or Anthropic)'
        },
        {
            'name': 'Anthropic (alternative for scripts)',
            'url': 'https://console.anthropic.com/',
            'env': 'ANTHROPIC_API_KEY',
            'required': 'Yes (or OpenAI)'
        },
        {
            'name': 'Replicate (for images)',
            'url': 'https://replicate.com/account/api-tokens',
            'env': 'REPLICATE_API_KEY',
            'required': 'Recommended'
        },
        {
            'name': 'Stability AI (alternative for images)',
            'url': 'https://platform.stability.ai/',
            'env': 'STABILITY_API_KEY',
            'required': 'Optional'
        }
    ]

    for api in apis:
        print(f"  {Fore.GREEN}• {api['name']}{Style.RESET_ALL}")
        print(f"    URL: {api['url']}")
        print(f"    Env Variable: {api['env']}")
        print(f"    Required: {api['required']}\n")

    print(f"{Fore.CYAN}Step 3: Configure Environment{Style.RESET_ALL}")
    print("  1. Copy .env.example to .env")
    print("  2. Add your API keys to .env file")
    print("  3. Customize config/config.yaml if needed\n")

    print(f"{Fore.CYAN}Step 4: Test Setup{Style.RESET_ALL}")
    print("  python main.py research")
    print("  python main.py generate-script --niche motivational\n")

    print(f"{Fore.GREEN}✅ Ready to create content!{Style.RESET_ALL}")


if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠️  Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
