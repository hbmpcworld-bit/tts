# TikTok Content Automation Tool

Automated content creation tool for TikTok that helps you create original, engaging content at scale.

## Features

✅ **Niche Research** - Identify trending topics and niches
✅ **AI Script Writing** - Generate original scripts based on trending topics
✅ **Image Generation** - Create custom images using AI
✅ **Video Prompts** - Generate prompts for text-to-video AI tools
✅ **Smart Scheduling** - Get optimal posting time recommendations
✅ **Bulk Processing** - Create multiple videos at once

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd tts

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Required API Keys

You'll need to obtain the following API keys:

1. **OpenAI API** (for script generation)
   - Get from: https://platform.openai.com/api-keys
   - Add to .env: `OPENAI_API_KEY=your_key`

2. **Anthropic API** (alternative for script generation)
   - Get from: https://console.anthropic.com/
   - Add to .env: `ANTHROPIC_API_KEY=your_key`

3. **Replicate API** (for image/video generation)
   - Get from: https://replicate.com/account/api-tokens
   - Add to .env: `REPLICATE_API_KEY=your_key`

4. **Stability AI** (for image generation - optional)
   - Get from: https://platform.stability.ai/
   - Add to .env: `STABILITY_API_KEY=your_key`

## Usage

### Basic Usage

```bash
# Research trending niches
python main.py research --topic "comedy"

# Generate a script
python main.py generate-script --niche "motivational" --duration 30

# Generate image for script
python main.py generate-image --script "output/scripts/script_001.txt"

# Generate video prompt
python main.py generate-video --script "output/scripts/script_001.txt"

# Bulk create content
python main.py bulk --niche "educational" --count 5
```

### Advanced Usage

```bash
# Full pipeline - research to video prompts
python main.py full-pipeline --topic "fitness" --count 3

# Schedule posts
python main.py schedule --videos "output/videos/" --days 7
```

## Configuration

Edit `config/config.yaml` to customize:
- Video duration preferences
- Niche preferences
- Image styles
- Scheduling rules

## Output Structure

```
output/
├── scripts/          # Generated scripts
├── images/          # Generated images
└── videos/          # Video prompts and metadata
```

## Ethics & Best Practices

⚠️ This tool creates **original content** inspired by trends
✅ Always review and customize generated content
✅ Add your unique perspective and value
✅ Follow TikTok's community guidelines
✅ Respect copyright and intellectual property

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.
