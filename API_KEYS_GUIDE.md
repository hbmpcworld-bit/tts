# API Keys Guide - TikTok Content Automation Tool

Is guide mein aapko bataya jayega ke kaise API keys hasil karein aur setup karein.

## 🔑 Required API Keys

### 1. OpenAI API Key (Script Generation)

**Kya hai:** AI-powered script generation ke liye
**Cost:** Pay-as-you-go ($0.01 per 1K tokens approximately)

**Kaise hasil karein:**

1. Visit karein: https://platform.openai.com/signup
2. Account banayein (email/Google se)
3. Billing section mein payment method add karein
4. API Keys section mein jayein: https://platform.openai.com/api-keys
5. "Create new secret key" par click karein
6. Key copy karein (yeh dobara nahi dikhegi!)

**Setup:**
```bash
# .env file mein add karein:
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

**Alternative:** Anthropic API (neeche dekhen)

---

### 2. Anthropic API Key (Alternative Script Generation)

**Kya hai:** OpenAI ka alternative (Claude AI)
**Cost:** Pay-as-you-go pricing

**Kaise hasil karein:**

1. Visit karein: https://console.anthropic.com/
2. Sign up karein
3. Billing setup karein
4. API Keys section se key create karein

**Setup:**
```bash
# .env file mein add karein:
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

---

### 3. Replicate API Key (Image Generation) ⭐ RECOMMENDED

**Kya hai:** AI image generation (Stable Diffusion)
**Cost:** Pay-per-use ($0.0025 per image approximately)

**Kaise hasil karein:**

1. Visit karein: https://replicate.com/signin
2. GitHub account se sign in karein
3. Billing add karein
4. Account settings mein API tokens dekhen: https://replicate.com/account/api-tokens
5. Token copy karein

**Setup:**
```bash
# .env file mein add karein:
REPLICATE_API_KEY=r8_xxxxxxxxxxxxx
```

---

### 4. Stability AI API Key (Optional - Alternative Image Generation)

**Kya hai:** High-quality image generation
**Cost:** Credits-based ($10 for 1000 credits)

**Kaise hasil karein:**

1. Visit karein: https://platform.stability.ai/
2. Sign up karein
3. Membership plan choose karein
4. API keys section se key create karein

**Setup:**
```bash
# .env file mein add karein:
STABILITY_API_KEY=sk-xxxxxxxxxxxxx
```

---

## 💰 Cost Estimation

**For 10 videos (example):**

| Item | Quantity | Cost (Approx) |
|------|----------|---------------|
| Scripts (OpenAI GPT-4) | 10 scripts | $0.50 - $1.00 |
| Images (Replicate) | 30 images | $0.10 - $0.20 |
| **TOTAL** | | **$0.60 - $1.20** |

**Monthly (100 videos):**
- Approximately $6 - $12 per month for 100 videos

**Note:** Prices are approximate and may change. Always check current pricing.

---

## ⚙️ Setup Instructions

### Step 1: Copy Environment File

```bash
cp .env.example .env
```

### Step 2: Edit .env File

```bash
# Linux/Mac
nano .env

# Windows
notepad .env
```

### Step 3: Add Your API Keys

```env
# Required: Choose one
OPENAI_API_KEY=your_openai_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_key_here

# Recommended for images
REPLICATE_API_KEY=your_replicate_key_here

# Optional
STABILITY_API_KEY=your_stability_key_here
```

### Step 4: Save and Test

```bash
# Test script generation
python main.py generate-script --niche motivational

# Test image generation
python main.py generate-image --prompt "Sunrise on mountain"
```

---

## 🔒 Security Best Practices

1. **.env file ko NEVER commit na karein**
   - Already .gitignore mein hai
   - Check karein: `git status` (yeh show nahi hona chahiye)

2. **API keys ko publicly share na karein**
   - Screenshots mein hide karein
   - Code examples mein remove karein

3. **Regular monitoring karein**
   - OpenAI: https://platform.openai.com/usage
   - Replicate: https://replicate.com/account/billing

4. **Rate limits set karein**
   - Billing dashboards mein monthly limits set kar sakte hain

---

## ❓ Troubleshooting

### "API key not found" error

**Solution:**
1. Check ke `.env` file root directory mein hai
2. Check ke key sahi copy hui hai (no spaces)
3. Restart script/terminal

### "Insufficient quota" error

**Solution:**
1. OpenAI/Replicate dashboard check karein
2. Credits/billing add karein
3. Wait karein for activation (5-10 minutes)

### "Invalid API key" error

**Solution:**
1. Key dobara generate karein
2. Copy karke .env mein paste karein
3. Make sure koi extra spaces nahi hain

---

## 📞 Support Links

- **OpenAI Support:** https://help.openai.com/
- **Anthropic Support:** https://support.anthropic.com/
- **Replicate Support:** https://replicate.com/docs
- **Stability AI Support:** https://platform.stability.ai/docs

---

## 🎯 Recommended Setup (Budget-Friendly)

**Minimum (Free Trial):**
- OpenAI (with free credits) OR Anthropic

**Recommended:**
- OpenAI OR Anthropic (for scripts)
- Replicate (for images)

**Full Featured:**
- OpenAI (primary) + Anthropic (backup)
- Replicate (primary) + Stability AI (backup)

---

**JazakAllah khair!** Tool enjoy karein aur original content create karein! 🚀
