"""
Script Generator Module
Generates original TikTok scripts using AI
"""

import os
from openai import OpenAI
from anthropic import Anthropic
from utils.helpers import load_config, get_api_key, save_json, get_timestamp, sanitize_filename


class ScriptGenerator:
    """Generate original TikTok scripts using AI"""

    def __init__(self, ai_provider="openai"):
        """
        Initialize script generator

        Args:
            ai_provider: "openai" or "anthropic"
        """
        self.config = load_config()
        self.provider = ai_provider

        try:
            if ai_provider == "openai":
                self.client = OpenAI(api_key=get_api_key('openai'))
                self.model = "gpt-4-turbo-preview"
            elif ai_provider == "anthropic":
                self.client = Anthropic(api_key=get_api_key('anthropic'))
                self.model = "claude-3-5-sonnet-20241022"
            else:
                raise ValueError(f"Unsupported AI provider: {ai_provider}")
        except ValueError as e:
            print(f"⚠️  Warning: {e}")
            print(f"   Please set the API key in .env file to use {ai_provider}")
            self.client = None

    def generate_script(self, niche, sub_niche=None, duration=30, tone="engaging", language="urdu"):
        """
        Generate an original TikTok script

        Args:
            niche: Main niche (e.g., "motivational")
            sub_niche: Specific sub-niche (optional)
            duration: Video duration in seconds
            tone: Script tone (engaging, casual, professional, humorous)
            language: Script language (urdu, english, both)

        Returns:
            dict: Generated script with metadata
        """
        if not self.client:
            return self._get_template_script(niche, sub_niche, duration)

        # Calculate approximate word count (150 words per minute for Urdu/English)
        words_per_second = 2.5
        target_words = int(duration * words_per_second)

        prompt = self._create_prompt(niche, sub_niche, target_words, tone, language)

        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a creative TikTok content writer who creates engaging, original scripts."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                    max_tokens=1000
                )
                script_content = response.choices[0].message.content

            else:  # anthropic
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    temperature=0.8,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                script_content = response.content[0].text

            return self._format_script(script_content, niche, sub_niche, duration, tone, language)

        except Exception as e:
            print(f"❌ Error generating script: {e}")
            return self._get_template_script(niche, sub_niche, duration)

    def _create_prompt(self, niche, sub_niche, target_words, tone, language):
        """Create prompt for AI script generation"""
        script_config = self.config.get('script', {})
        include_hook = script_config.get('include_hooks', True)
        include_cta = script_config.get('include_cta', True)

        topic = sub_niche if sub_niche else niche

        if language.lower() == "urdu":
            lang_instruction = "Write the script in URDU (Roman Urdu or Urdu script both acceptable)"
        elif language.lower() == "english":
            lang_instruction = "Write the script in ENGLISH"
        else:
            lang_instruction = "Write the script in both URDU and ENGLISH (provide both versions)"

        prompt = f"""Create an original, engaging TikTok script about: {topic}

Requirements:
- Niche: {niche}
- Tone: {tone}
- Target length: {target_words} words (approximately)
- Language: {lang_instruction}
- Make it ORIGINAL and UNIQUE (not copied from existing content)
- Add value and insights
"""

        if include_hook:
            prompt += "\n- Start with a strong hook in first 2 seconds to grab attention"

        if include_cta:
            prompt += "\n- End with a clear call-to-action (like, follow, comment, share)"

        prompt += """

Format:
[HOOK] - First 2 seconds attention grabber
[MAIN CONTENT] - Core message/value
[CTA] - Call to action

Make it conversational, relatable, and valuable. Focus on providing unique insights or entertainment."""

        return prompt

    def _format_script(self, script_content, niche, sub_niche, duration, tone, language):
        """Format the generated script with metadata"""
        return {
            "script": script_content,
            "metadata": {
                "niche": niche,
                "sub_niche": sub_niche,
                "duration": duration,
                "tone": tone,
                "language": language,
                "generated_at": get_timestamp(),
                "ai_provider": self.provider
            }
        }

    def _get_template_script(self, niche, sub_niche, duration):
        """Get a template script when AI is not available"""
        topic = sub_niche if sub_niche else niche
        template = f"""[HOOK]
Kya aap {topic} ke baare mein yeh baat jante hain?

[MAIN CONTENT]
Aaj main aap ko {topic} ke 3 important tips bataunga:

1. [First tip about {topic}]
2. [Second tip about {topic}]
3. [Third tip about {topic}]

[CTA]
Agar yeh tips helpful lage toh like aur follow zaroor karein!
Comment mein bataye ke aap kaun sa tip try karenge.

#tiktok #{niche} #{topic}
"""
        return {
            "script": template,
            "metadata": {
                "niche": niche,
                "sub_niche": sub_niche,
                "duration": duration,
                "tone": "template",
                "language": "urdu",
                "generated_at": get_timestamp(),
                "ai_provider": "template"
            },
            "note": "This is a template. Set up API keys to generate AI-powered scripts."
        }

    def save_script(self, script_data, filename=None):
        """
        Save script to file

        Args:
            script_data: Script data dictionary
            filename: Custom filename (optional)

        Returns:
            str: Path to saved file
        """
        if not filename:
            niche = script_data['metadata']['niche']
            timestamp = get_timestamp()
            filename = f"script_{sanitize_filename(niche)}_{timestamp}.json"

        filepath = os.path.join("output/scripts", filename)
        save_json(script_data, filepath)

        # Also save plain text version
        txt_filepath = filepath.replace('.json', '.txt')
        with open(txt_filepath, 'w', encoding='utf-8') as f:
            f.write(script_data['script'])

        return filepath

    def generate_multiple(self, niche, count=5, **kwargs):
        """
        Generate multiple scripts for a niche

        Args:
            niche: The niche to generate scripts for
            count: Number of scripts to generate
            **kwargs: Additional arguments for generate_script

        Returns:
            list: List of generated scripts
        """
        scripts = []
        for i in range(count):
            print(f"  Generating script {i+1}/{count}...")
            script = self.generate_script(niche, **kwargs)
            scripts.append(script)

        return scripts


def main():
    """CLI for script generation"""
    print("\n📝 TikTok Script Generator\n")

    # Try OpenAI first, fallback to Anthropic
    try:
        generator = ScriptGenerator(ai_provider="openai")
    except:
        try:
            generator = ScriptGenerator(ai_provider="anthropic")
        except:
            print("⚠️  No API keys found. Using template mode.")
            generator = ScriptGenerator(ai_provider="openai")

    # Example generation
    print("Generating sample script...")
    script = generator.generate_script(
        niche="motivational",
        sub_niche="morning motivation",
        duration=30,
        tone="engaging",
        language="urdu"
    )

    print("\n✅ Script Generated:\n")
    print(script['script'])
    print("\n" + "="*50)
    print(f"Niche: {script['metadata']['niche']}")
    print(f"Duration: {script['metadata']['duration']}s")
    print(f"Language: {script['metadata']['language']}")

    # Save script
    filepath = generator.save_script(script)
    print(f"\n💾 Saved to: {filepath}")


if __name__ == "__main__":
    main()
