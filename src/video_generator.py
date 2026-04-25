"""
Video Generator Module
Generates video prompts and metadata for text-to-video AI tools
"""

import os
import json
from utils.helpers import load_config, get_timestamp, sanitize_filename, save_json


class VideoGenerator:
    """Generate video prompts for text-to-video AI tools like RunwayML, Pika, etc."""

    def __init__(self):
        self.config = load_config()
        self.video_config = self.config.get('video', {})

    def create_video_prompt(self, script_data, images_data=None):
        """
        Create comprehensive video prompt from script and images

        Args:
            script_data: Dictionary containing script and metadata
            images_data: List of image data (optional)

        Returns:
            dict: Video generation instructions and metadata
        """
        script_text = script_data.get('script', '')
        metadata = script_data.get('metadata', {})

        # Parse script into sections
        sections = self._parse_script_sections(script_text)

        # Create video timeline
        timeline = self._create_timeline(sections, metadata.get('duration', 30))

        # Generate scene descriptions
        scenes = self._generate_scenes(timeline, images_data)

        # Create video prompt
        video_prompt = {
            "project_info": {
                "title": f"{metadata.get('niche', 'TikTok')} Video",
                "duration": metadata.get('duration', 30),
                "format": "vertical",
                "aspect_ratio": "9:16",
                "resolution": "1080x1920"
            },
            "script": {
                "full_text": script_text,
                "sections": sections,
                "language": metadata.get('language', 'urdu')
            },
            "timeline": timeline,
            "scenes": scenes,
            "visual_style": self._get_visual_style(metadata.get('niche')),
            "audio": {
                "voiceover": script_text,
                "background_music": self._suggest_music(metadata.get('niche')),
                "sound_effects": self._suggest_sound_effects(sections)
            },
            "text_overlays": self._create_text_overlays(sections),
            "transitions": self._suggest_transitions(len(scenes)),
            "metadata": {
                "generated_at": get_timestamp(),
                "niche": metadata.get('niche'),
                "sub_niche": metadata.get('sub_niche')
            }
        }

        return video_prompt

    def _parse_script_sections(self, script_text):
        """Parse script into Hook, Main Content, and CTA sections"""
        sections = {
            "hook": "",
            "main_content": "",
            "cta": ""
        }

        lines = script_text.split('\n')
        current_section = None

        for line in lines:
            line = line.strip()
            if '[HOOK]' in line.upper():
                current_section = 'hook'
            elif '[MAIN' in line.upper() or '[CONTENT]' in line.upper():
                current_section = 'main_content'
            elif '[CTA]' in line.upper():
                current_section = 'cta'
            elif line and current_section:
                sections[current_section] += line + '\n'

        # If no sections found, treat entire script as main content
        if not any(sections.values()):
            sections['main_content'] = script_text

        return sections

    def _create_timeline(self, sections, total_duration):
        """Create timeline for video sections"""
        timeline = []

        # Allocate time
        hook_duration = min(3, total_duration * 0.15)  # 15% or 3s max
        cta_duration = min(4, total_duration * 0.15)   # 15% or 4s max
        main_duration = total_duration - hook_duration - cta_duration

        current_time = 0

        if sections['hook']:
            timeline.append({
                "section": "hook",
                "start": current_time,
                "duration": hook_duration,
                "text": sections['hook'].strip()
            })
            current_time += hook_duration

        if sections['main_content']:
            timeline.append({
                "section": "main_content",
                "start": current_time,
                "duration": main_duration,
                "text": sections['main_content'].strip()
            })
            current_time += main_duration

        if sections['cta']:
            timeline.append({
                "section": "cta",
                "start": current_time,
                "duration": cta_duration,
                "text": sections['cta'].strip()
            })

        return timeline

    def _generate_scenes(self, timeline, images_data):
        """Generate scene descriptions for video"""
        scenes = []

        for i, section in enumerate(timeline):
            scene = {
                "scene_number": i + 1,
                "timestamp": f"{section['start']:.1f}s - {section['start'] + section['duration']:.1f}s",
                "duration": section['duration'],
                "type": section['section'],
                "description": self._create_scene_description(section),
                "camera": self._suggest_camera_movement(section['section']),
                "lighting": self._suggest_lighting(section['section'])
            }

            # Add image reference if available
            if images_data and i < len(images_data):
                scene['image_reference'] = images_data[i].get('local_path') or images_data[i].get('url')
                scene['image_prompt'] = images_data[i].get('prompt')

            scenes.append(scene)

        return scenes

    def _create_scene_description(self, section):
        """Create visual description for a scene"""
        scene_type = section['section']

        if scene_type == 'hook':
            return "Dynamic opening shot with bold text overlay, high energy visuals to grab attention immediately"
        elif scene_type == 'main_content':
            return "Clear, focused visuals supporting the main message, smooth transitions between key points"
        elif scene_type == 'cta':
            return "Engaging closing shot with clear call-to-action overlay, encouraging viewer interaction"
        else:
            return "Professional video content with good lighting and composition"

    def _suggest_camera_movement(self, section_type):
        """Suggest camera movement for section"""
        movements = {
            'hook': 'Quick zoom in or dynamic pan',
            'main_content': 'Slow push in or static steady shot',
            'cta': 'Slow zoom out or pull back'
        }
        return movements.get(section_type, 'Static')

    def _suggest_lighting(self, section_type):
        """Suggest lighting for section"""
        if section_type == 'hook':
            return 'Bright, vibrant, high contrast'
        elif section_type == 'cta':
            return 'Warm, inviting, professional'
        else:
            return 'Natural, well-balanced, professional'

    def _get_visual_style(self, niche):
        """Get visual style recommendations based on niche"""
        styles = {
            'motivational': {
                'color_palette': 'Warm tones, golden hour lighting, inspirational',
                'mood': 'Uplifting, energetic, empowering',
                'visual_elements': 'Nature, success imagery, sunrise/sunset'
            },
            'educational': {
                'color_palette': 'Clean, professional, blue and white tones',
                'mood': 'Clear, informative, engaging',
                'visual_elements': 'Graphics, diagrams, text overlays'
            },
            'comedy': {
                'color_palette': 'Bright, colorful, playful',
                'mood': 'Fun, energetic, entertaining',
                'visual_elements': 'Expressive faces, dynamic movements'
            },
            'business': {
                'color_palette': 'Professional, navy and gray tones',
                'mood': 'Confident, authoritative, trustworthy',
                'visual_elements': 'Office, success symbols, graphs'
            }
        }
        return styles.get(niche, styles['educational'])

    def _suggest_music(self, niche):
        """Suggest background music type"""
        music = {
            'motivational': 'Uplifting, inspiring instrumental music',
            'educational': 'Subtle, non-distracting background music',
            'comedy': 'Upbeat, playful music',
            'business': 'Professional, corporate background music',
            'lifestyle': 'Trendy, popular TikTok sounds'
        }
        return music.get(niche, 'Light background music')

    def _suggest_sound_effects(self, sections):
        """Suggest sound effects for sections"""
        effects = []

        if sections.get('hook'):
            effects.append({'timestamp': '0s', 'effect': 'Attention grab sound (whoosh, ding)'})

        if sections.get('cta'):
            effects.append({'timestamp': 'End', 'effect': 'Positive notification sound'})

        return effects

    def _create_text_overlays(self, sections):
        """Create text overlay suggestions"""
        overlays = []

        if sections.get('hook'):
            overlays.append({
                'section': 'hook',
                'text': sections['hook'].strip()[:50] + '...',
                'style': 'Bold, large font, eye-catching color',
                'position': 'Center',
                'animation': 'Fade in with scale'
            })

        if sections.get('cta'):
            overlays.append({
                'section': 'cta',
                'text': sections['cta'].strip(),
                'style': 'Clear, readable, contrasting color',
                'position': 'Bottom third',
                'animation': 'Slide up'
            })

        return overlays

    def _suggest_transitions(self, scene_count):
        """Suggest transitions between scenes"""
        transitions = []

        for i in range(scene_count - 1):
            transitions.append({
                'between_scenes': f"{i+1} → {i+2}",
                'type': 'Smooth fade or quick cut',
                'duration': '0.3s'
            })

        return transitions

    def export_for_runway(self, video_prompt):
        """Export prompt optimized for RunwayML"""
        runway_prompt = {
            "text_prompt": self._create_runway_text_prompt(video_prompt),
            "duration": video_prompt['project_info']['duration'],
            "aspect_ratio": "9:16",
            "motion": 3  # Medium motion
        }
        return runway_prompt

    def export_for_pika(self, video_prompt):
        """Export prompt optimized for Pika"""
        pika_prompt = {
            "prompt": self._create_pika_text_prompt(video_prompt),
            "aspect_ratio": "9:16",
            "fps": 24,
            "motion": 2
        }
        return pika_prompt

    def _create_runway_text_prompt(self, video_prompt):
        """Create text prompt for RunwayML"""
        style = video_prompt['visual_style']
        scenes = video_prompt['scenes']

        prompt_parts = []
        for scene in scenes:
            prompt_parts.append(scene['description'])

        full_prompt = f"{style['mood']} video. {style['color_palette']}. " + " → ".join(prompt_parts)
        return full_prompt[:500]  # RunwayML has character limit

    def _create_pika_text_prompt(self, video_prompt):
        """Create text prompt for Pika"""
        style = video_prompt['visual_style']
        return f"{style['mood']} TikTok video, {style['color_palette']}, {style['visual_elements']}, vertical format, professional quality"

    def save_video_prompt(self, video_prompt, filename=None):
        """Save video prompt to file"""
        if not filename:
            title = sanitize_filename(video_prompt['project_info']['title'])
            filename = f"video_prompt_{title}_{get_timestamp()}.json"

        filepath = os.path.join("output/videos", filename)
        save_json(video_prompt, filepath)

        # Also save a human-readable version
        txt_filepath = filepath.replace('.json', '.txt')
        with open(txt_filepath, 'w', encoding='utf-8') as f:
            f.write(self._format_readable_prompt(video_prompt))

        return filepath

    def _format_readable_prompt(self, video_prompt):
        """Format video prompt as readable text"""
        output = []
        output.append("=" * 60)
        output.append(f"VIDEO PROJECT: {video_prompt['project_info']['title']}")
        output.append("=" * 60)
        output.append(f"\nDuration: {video_prompt['project_info']['duration']}s")
        output.append(f"Format: {video_prompt['project_info']['aspect_ratio']} ({video_prompt['project_info']['resolution']})")

        output.append("\n\n--- SCRIPT ---")
        output.append(video_prompt['script']['full_text'])

        output.append("\n\n--- SCENES ---")
        for scene in video_prompt['scenes']:
            output.append(f"\nScene {scene['scene_number']} [{scene['timestamp']}]:")
            output.append(f"  {scene['description']}")
            output.append(f"  Camera: {scene['camera']}")
            output.append(f"  Lighting: {scene['lighting']}")

        output.append("\n\n--- VISUAL STYLE ---")
        style = video_prompt['visual_style']
        output.append(f"Color Palette: {style['color_palette']}")
        output.append(f"Mood: {style['mood']}")
        output.append(f"Elements: {style['visual_elements']}")

        output.append("\n\n--- AUDIO ---")
        output.append(f"Music: {video_prompt['audio']['background_music']}")

        output.append("\n\n--- TEXT-TO-VIDEO PROMPTS ---")
        output.append("\nRunwayML:")
        runway = self.export_for_runway(video_prompt)
        output.append(f"  {runway['text_prompt']}")

        output.append("\nPika:")
        pika = self.export_for_pika(video_prompt)
        output.append(f"  {pika['prompt']}")

        return '\n'.join(output)


def main():
    """CLI for video prompt generation"""
    print("\n🎬 TikTok Video Prompt Generator\n")

    # Example usage with sample script
    sample_script = {
        "script": """[HOOK]
Kya aap subah jaldi uthna chahte hain?

[MAIN CONTENT]
3 asan tips:
1. Raat ko jaldi so jao
2. Phone door rakho
3. Alarm door set karo

[CTA]
Try karke dekho aur results batao!
""",
        "metadata": {
            "niche": "motivational",
            "sub_niche": "morning routine",
            "duration": 30,
            "language": "urdu"
        }
    }

    generator = VideoGenerator()

    print("Creating video prompt...")
    video_prompt = generator.create_video_prompt(sample_script)

    print("\n✅ Video Prompt Created!")
    print(f"Duration: {video_prompt['project_info']['duration']}s")
    print(f"Scenes: {len(video_prompt['scenes'])}")

    # Save
    filepath = generator.save_video_prompt(video_prompt)
    print(f"\n💾 Saved to: {filepath}")
    print(f"📄 Readable version: {filepath.replace('.json', '.txt')}")


if __name__ == "__main__":
    main()
