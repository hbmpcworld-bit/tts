# Usage Guide - TikTok Content Automation Tool

Complete guide ke saath examples!

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and add your API keys

# Test installation
python main.py setup
```

---

## 📋 Commands

### 1. Research Niches

**Saare niches dekhne ke liye:**
```bash
python main.py research
```

**Specific niche research:**
```bash
python main.py research --topic motivational
python main.py research --topic educational
python main.py research --topic comedy
```

**Output:**
- Niche details
- Target audience
- Content suggestions
- Keywords

---

### 2. Generate Scripts

**Single script:**
```bash
python main.py generate-script --niche motivational
```

**Urdu mein script:**
```bash
python main.py generate-script --niche motivational --language urdu
```

**English mein script:**
```bash
python main.py generate-script --niche educational --language english
```

**Multiple scripts:**
```bash
python main.py generate-script --niche business --count 5
```

**Custom duration:**
```bash
python main.py generate-script --niche fitness --duration 60
```

**Complete example:**
```bash
python main.py generate-script \
  --niche motivational \
  --sub-niche "morning motivation" \
  --duration 30 \
  --language urdu \
  --count 3
```

---

### 3. Generate Images

**Simple image:**
```bash
python main.py generate-image --prompt "Motivational sunrise scene"
```

**Specific style:**
```bash
python main.py generate-image \
  --prompt "Business meeting in modern office" \
  --style realistic
```

**Available styles:**
- `cinematic` - Movie-like quality (default)
- `realistic` - Photorealistic
- `cartoon` - Animated style
- `anime` - Anime/manga style

**Different providers:**
```bash
# Using Replicate (recommended)
python main.py generate-image --prompt "..." --provider replicate

# Using OpenAI DALL-E
python main.py generate-image --prompt "..." --provider openai

# Using Stability AI
python main.py generate-image --prompt "..." --provider stability
```

---

### 4. Generate Video Prompts

**From script file:**
```bash
python main.py generate-video --script output/scripts/script_motivational_20240425_120000.json
```

**With images:**
```bash
python main.py generate-video \
  --script output/scripts/script_001.json \
  --images output/images/images_metadata.json
```

**Output:**
- JSON file with complete video instructions
- TXT file with human-readable prompt
- Ready for text-to-video tools (RunwayML, Pika, etc.)

---

### 5. Create Posting Schedule

**10 videos over 7 days:**
```bash
python main.py schedule --count 10 --days 7
```

**Custom schedule:**
```bash
python main.py schedule --count 30 --days 30
```

**Check best times:**
```bash
python main.py best-times
```

---

### 6. Bulk Processing (Full Pipeline) ⭐

**Complete automation:**
```bash
python main.py bulk --niche motivational --count 5
```

**Yeh command:**
1. ✅ Niche research karega
2. ✅ 5 scripts generate karega
3. ✅ Har script ke liye 3 images banayega
4. ✅ Video prompts create karega
5. ✅ Posting schedule banayega

**Custom settings:**
```bash
python main.py bulk \
  --niche educational \
  --count 10 \
  --duration 45 \
  --language english \
  --ai-provider anthropic \
  --image-provider replicate
```

---

## 🎯 Complete Workflows

### Workflow 1: Quick Single Video

```bash
# Step 1: Generate script
python main.py generate-script --niche motivational --language urdu

# Step 2: Generate images (optional)
python main.py generate-image --prompt "Morning success motivation"

# Step 3: Create video prompt
python main.py generate-video --script output/scripts/script_xxx.json

# Done! Use the video prompt in RunwayML/Pika
```

---

### Workflow 2: Week's Content (Recommended)

```bash
# One command for everything!
python main.py bulk --niche lifestyle --count 7 --duration 30

# Output:
# - 7 scripts in output/scripts/
# - 21 images in output/images/
# - 7 video prompts in output/videos/
# - Posting schedule
```

---

### Workflow 3: Multiple Niches

```bash
# Monday: Motivational content
python main.py bulk --niche motivational --count 2

# Wednesday: Educational content
python main.py bulk --niche educational --count 2

# Friday: Business tips
python main.py bulk --niche business --count 2
```

---

## 📁 Output Structure

```
output/
├── scripts/
│   ├── script_motivational_20240425_120000.json
│   ├── script_motivational_20240425_120000.txt
│   └── ...
├── images/
│   ├── img_20240425_120530_0.png
│   ├── img_20240425_120530_1.png
│   └── images_metadata_20240425.json
├── videos/
│   ├── video_prompt_motivational_20240425.json
│   ├── video_prompt_motivational_20240425.txt
│   └── ...
└── bulk_results_motivational_20240425.json
```

---

## ⚙️ Configuration

Edit `config/config.yaml` to customize:

```yaml
video:
  default_duration: 30  # Change default duration

script:
  language: "urdu"  # Default language
  tone: "engaging"  # engaging, casual, professional, humorous

image:
  style: "cinematic"  # Default image style
  count_per_script: 3  # Images per script

niches:
  preferred:  # Your favorite niches
    - motivational
    - educational

scheduling:
  best_times:  # Customize posting times
    - "09:00"
    - "12:00"
    - "18:00"
    - "21:00"
  timezone: "Asia/Karachi"
  posts_per_day: 3
```

---

## 💡 Pro Tips

### 1. **Start Small**
```bash
# Test with 1-2 videos first
python main.py bulk --niche motivational --count 2
```

### 2. **Review Content**
Always review and customize generated content:
- Scripts: Add personal touch
- Images: Select best ones
- Video prompts: Adjust as needed

### 3. **Batch Processing**
Generate content in batches for efficiency:
```bash
# Weekend batch
python main.py bulk --niche comedy --count 10
```

### 4. **Mix Languages**
Create bilingual content:
```bash
python main.py generate-script --niche business --language both
```

### 5. **Use Scheduling**
Plan ahead with schedules:
```bash
python main.py schedule --count 30 --days 30
```

---

## 🎬 Using Video Prompts

Generated video prompts can be used in:

### RunwayML
1. Open RunwayML Gen-2
2. Copy text prompt from output file
3. Upload reference images
4. Generate video

### Pika
1. Open Pika.art
2. Paste prompt
3. Select vertical format (9:16)
4. Generate

### Manual Editing
Use prompts as guide for manual video editing:
- Follow scene descriptions
- Use suggested transitions
- Add text overlays as specified

---

## 📊 Track Your Content

Keep track of generated content:

```bash
# All bulk results are saved
ls output/bulk_results_*.json

# View specific result
cat output/bulk_results_motivational_20240425.json
```

---

## 🔄 Daily Routine Example

```bash
# Morning: Generate week's content
python main.py bulk --niche motivational --count 7

# Review scripts (customize if needed)
# Generate videos using prompts
# Follow posting schedule

# Repeat weekly!
```

---

## ❓ Common Questions

**Q: API keys kahan store karein?**
A: `.env` file mein (never commit to git)

**Q: Kitna cost hoga?**
A: ~$0.60-$1.20 for 10 videos (details in API_KEYS_GUIDE.md)

**Q: Bulk processing mein kitna time lagega?**
A: ~2-3 minutes per video (depends on API speed)

**Q: Kya offline use kar sakte hain?**
A: No, API keys required (online)

**Q: Multiple languages support?**
A: Yes! Urdu, English, or both

---

**JazakAllah khair!** Happy content creating! 🎬✨
