"""
Image Generator Module
Generates images for TikTok videos using AI
"""

import os
import requests
import replicate
from openai import OpenAI
from utils.helpers import load_config, get_api_key, get_timestamp, sanitize_filename, save_json


class ImageGenerator:
    """Generate images for TikTok content using AI"""

    def __init__(self, provider="replicate"):
        """
        Initialize image generator

        Args:
            provider: "replicate", "openai", or "stability"
        """
        self.config = load_config()
        self.provider = provider

        try:
            if provider == "replicate":
                os.environ["REPLICATE_API_TOKEN"] = get_api_key('replicate')
                self.client = replicate
            elif provider == "openai":
                self.client = OpenAI(api_key=get_api_key('openai'))
            elif provider == "stability":
                self.api_key = get_api_key('stability')
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        except ValueError as e:
            print(f"⚠️  Warning: {e}")
            self.client = None

    def generate_image(self, prompt, style="cinematic", aspect_ratio="9:16"):
        """
        Generate an image based on prompt

        Args:
            prompt: Text description of the image
            style: Image style (cinematic, realistic, cartoon, anime)
            aspect_ratio: "9:16" (vertical), "1:1" (square), "16:9" (horizontal)

        Returns:
            dict: Generated image data with URL and metadata
        """
        if not self.client:
            return self._get_placeholder_image(prompt)

        # Enhance prompt with style
        enhanced_prompt = self._enhance_prompt(prompt, style)

        try:
            if self.provider == "replicate":
                return self._generate_replicate(enhanced_prompt, aspect_ratio)
            elif self.provider == "openai":
                return self._generate_openai(enhanced_prompt)
            elif self.provider == "stability":
                return self._generate_stability(enhanced_prompt, aspect_ratio)
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return self._get_placeholder_image(prompt)

    def _enhance_prompt(self, prompt, style):
        """Enhance prompt with style keywords"""
        style_prompts = {
            "cinematic": "cinematic lighting, dramatic, high quality, professional photography",
            "realistic": "photorealistic, detailed, sharp focus, 8k resolution",
            "cartoon": "cartoon style, animated, colorful, illustration",
            "anime": "anime style, manga, vibrant colors, detailed"
        }

        style_suffix = style_prompts.get(style, style_prompts["cinematic"])
        return f"{prompt}, {style_suffix}"

    def _generate_replicate(self, prompt, aspect_ratio):
        """Generate image using Replicate (Stable Diffusion)"""
        # Using SDXL model
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "num_outputs": 1,
                "quality": 90
            }
        )

        image_url = output[0] if isinstance(output, list) else output

        return {
            "url": image_url,
            "prompt": prompt,
            "provider": "replicate",
            "aspect_ratio": aspect_ratio,
            "generated_at": get_timestamp()
        }

    def _generate_openai(self, prompt):
        """Generate image using OpenAI DALL-E"""
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1792",  # Vertical for TikTok
            quality="standard",
            n=1
        )

        image_url = response.data[0].url

        return {
            "url": image_url,
            "prompt": prompt,
            "provider": "openai",
            "aspect_ratio": "9:16",
            "generated_at": get_timestamp()
        }

    def _generate_stability(self, prompt, aspect_ratio):
        """Generate image using Stability AI"""
        # Map aspect ratio to dimensions
        dimensions = {
            "9:16": (768, 1344),
            "1:1": (1024, 1024),
            "16:9": (1344, 768)
        }
        width, height = dimensions.get(aspect_ratio, (768, 1344))

        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 7,
                "height": height,
                "width": width,
                "samples": 1,
                "steps": 30
            }
        )

        if response.status_code == 200:
            data = response.json()
            # Save image from base64
            import base64
            image_data = base64.b64decode(data['artifacts'][0]['base64'])

            filename = f"stability_{get_timestamp()}.png"
            filepath = os.path.join("output/images", filename)

            with open(filepath, 'wb') as f:
                f.write(image_data)

            return {
                "url": filepath,
                "prompt": prompt,
                "provider": "stability",
                "aspect_ratio": aspect_ratio,
                "generated_at": get_timestamp()
            }
        else:
            raise Exception(f"Stability AI error: {response.text}")

    def _get_placeholder_image(self, prompt):
        """Return placeholder when API not available"""
        return {
            "url": "https://via.placeholder.com/1080x1920/FF6B6B/FFFFFF?text=Set+API+Key",
            "prompt": prompt,
            "provider": "placeholder",
            "generated_at": get_timestamp(),
            "note": "Set up API keys to generate real images"
        }

    def download_image(self, image_url, filename=None):
        """
        Download image from URL

        Args:
            image_url: URL of the image
            filename: Custom filename (optional)

        Returns:
            str: Path to downloaded image
        """
        if image_url.startswith("output/"):  # Already local file
            return image_url

        if not filename:
            filename = f"image_{get_timestamp()}.png"

        filepath = os.path.join("output/images", filename)

        response = requests.get(image_url)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return filepath
        else:
            raise Exception(f"Failed to download image: {response.status_code}")

    def generate_from_script(self, script_text, count=3):
        """
        Generate multiple images based on script content

        Args:
            script_text: The script text to analyze
            count: Number of images to generate

        Returns:
            list: List of generated images
        """
        # Extract key scenes/moments from script
        prompts = self._extract_image_prompts(script_text, count)

        images = []
        for i, prompt in enumerate(prompts):
            print(f"  Generating image {i+1}/{count}...")
            image = self.generate_image(prompt)
            if image['url'] != "https://via.placeholder.com/1080x1920/FF6B6B/FFFFFF?text=Set+API+Key":
                # Download if it's a URL
                try:
                    local_path = self.download_image(image['url'], f"img_{get_timestamp()}_{i}.png")
                    image['local_path'] = local_path
                except:
                    pass
            images.append(image)

        return images

    def _extract_image_prompts(self, script_text, count):
        """Extract image prompts from script text"""
        # Simple extraction - in production, use AI to analyze script
        # For now, create generic prompts based on script theme

        base_prompts = [
            "Motivational background with inspiring text overlay",
            "Person achieving success, celebrating victory",
            "Peaceful morning scene with soft lighting",
            "Dynamic action shot with energy and movement",
            "Calm and focused workspace with natural light"
        ]

        # Return requested number of prompts
        return base_prompts[:count]

    def save_metadata(self, images_data, filename=None):
        """Save image generation metadata"""
        if not filename:
            filename = f"images_metadata_{get_timestamp()}.json"

        filepath = os.path.join("output/images", filename)
        save_json(images_data, filepath)
        return filepath


def main():
    """CLI for image generation"""
    print("\n🎨 TikTok Image Generator\n")

    # Try Replicate first
    try:
        generator = ImageGenerator(provider="replicate")
    except:
        try:
            generator = ImageGenerator(provider="openai")
        except:
            print("⚠️  No API keys found. Using placeholder mode.")
            generator = ImageGenerator(provider="replicate")

    # Example generation
    print("Generating sample image...")
    image = generator.generate_image(
        prompt="Motivational sunrise scene with person standing on mountain top, arms raised in victory",
        style="cinematic",
        aspect_ratio="9:16"
    )

    print("\n✅ Image Generated:")
    print(f"URL: {image['url']}")
    print(f"Provider: {image['provider']}")
    print(f"Aspect Ratio: {image['aspect_ratio']}")

    if 'note' not in image:
        print("\n📥 Downloading image...")
        local_path = generator.download_image(image['url'])
        print(f"💾 Saved to: {local_path}")


if __name__ == "__main__":
    main()
