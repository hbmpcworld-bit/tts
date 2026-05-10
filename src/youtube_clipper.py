#!/usr/bin/env python3
"""
YouTube Viral Clips Extractor
Pipeline: download → transcribe → AI analysis → extract clips → copyright-safe audio
"""

import os
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


class YouTubeClipper:
    def __init__(self):
        self.output_dir = Path("output/clips")
        self.temp_dir = Path("output/temp")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self._check_dependencies()

    # ------------------------------------------------------------------
    # Dependency checks
    # ------------------------------------------------------------------

    def _check_dependencies(self):
        missing = []
        for tool in ("ffmpeg", "ffprobe"):
            if not shutil.which(tool):
                missing.append(tool)
        if missing:
            raise EnvironmentError(
                f"Missing system tools: {', '.join(missing)}. "
                "Install ffmpeg: https://ffmpeg.org/download.html"
            )
        try:
            import yt_dlp  # noqa: F401
        except ImportError:
            raise ImportError("yt-dlp not installed. Run: pip install yt-dlp")

    # ------------------------------------------------------------------
    # Step 1 – Download
    # ------------------------------------------------------------------

    def download_video(self, url: str) -> tuple[str, dict]:
        """Download a YouTube video and return (local_path, info_dict)."""
        import yt_dlp

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_tmpl = str(self.temp_dir / f"yt_{timestamp}.%(ext)s")

        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": out_tmpl,
            "quiet": True,
            "no_warnings": True,
            "merge_output_format": "mp4",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)
            # yt-dlp may produce .mp4 after merging
            if not os.path.exists(video_path):
                video_path = video_path.rsplit(".", 1)[0] + ".mp4"

        return video_path, info

    # ------------------------------------------------------------------
    # Step 2 – Transcribe
    # ------------------------------------------------------------------

    def extract_audio_for_transcription(self, video_path: str) -> str:
        """Extract a mono 16 kHz MP3 from the video (Whisper-friendly)."""
        audio_path = video_path.replace(".mp4", "_mono.mp3")
        cmd = [
            "ffmpeg", "-y", "-i", video_path,
            "-vn", "-ac", "1", "-ar", "16000",
            "-q:a", "4", audio_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg audio extraction failed:\n{result.stderr}")
        return audio_path

    def transcribe(self, audio_path: str) -> list[dict]:
        """
        Transcribe audio using OpenAI Whisper API.
        Returns a list of segments: [{start, end, text}, ...]
        Falls back to empty list if API key is missing.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("  [warn] OPENAI_API_KEY not set – skipping AI transcription.")
            return []

        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        with open(audio_path, "rb") as f:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
            )

        segments = []
        for seg in response.segments:
            segments.append({
                "start": seg.start,
                "end": seg.end,
                "text": seg.text.strip(),
            })
        return segments

    # ------------------------------------------------------------------
    # Step 3 – AI viral-moment analysis
    # ------------------------------------------------------------------

    def _segments_to_text(self, segments: list[dict]) -> str:
        return "\n".join(
            f"[{s['start']:.1f}s – {s['end']:.1f}s]: {s['text']}"
            for s in segments
        )

    def identify_viral_clips(
        self,
        segments: list[dict],
        video_title: str,
        video_duration: float,
        min_clip_seconds: int = 60,
        max_clip_seconds: int = 90,
    ) -> list[dict]:
        """
        Ask Claude to pick the best viral windows.
        Returns list of clip dicts with start_time, end_time, title, etc.
        """
        api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
        use_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))

        if not api_key:
            print("  [warn] No AI API key found – falling back to equal-split clips.")
            return self._fallback_clips(video_duration, min_clip_seconds)

        transcript_text = self._segments_to_text(segments) if segments else "(no transcript available)"

        prompt = f"""You are a viral short-form content strategist for TikTok, YouTube Shorts, and Instagram Reels.

Video title: {video_title}
Total duration: {video_duration:.0f} seconds

Full transcript with timestamps:
{transcript_text}

Task: Identify 3 to 5 segments that would make the most viral standalone short clips.

Rules for each clip:
- Duration: {min_clip_seconds}–{max_clip_seconds} seconds
- Must open with a strong hook (surprising fact, bold claim, relatable moment, or cliffhanger)
- Must be self-contained – a viewer with zero context should follow along
- Must end with a satisfying conclusion or a clear call-to-action
- Prefer moments with high emotion, humour, controversy, or surprising information

Return ONLY valid JSON with no markdown fences, matching this exact schema:
{{
  "clips": [
    {{
      "clip_number": 1,
      "start_time": 45.0,
      "end_time": 108.0,
      "title": "Short punchy clip title (max 60 chars)",
      "hook": "First sentence / opening line of this clip",
      "why_viral": "One sentence explaining viral potential",
      "virality_score": 8.5
    }}
  ]
}}"""

        try:
            if use_anthropic:
                import anthropic
                client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                msg = client.messages.create(
                    model="claude-opus-4-7",
                    max_tokens=2048,
                    messages=[{"role": "user", "content": prompt}],
                )
                raw = msg.content[0].text
            else:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                resp = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                )
                raw = resp.choices[0].message.content

            data = json.loads(raw)
            return data.get("clips", [])

        except Exception as exc:
            print(f"  [warn] AI analysis failed ({exc}) – using fallback clips.")
            return self._fallback_clips(video_duration, min_clip_seconds)

    def _fallback_clips(self, duration: float, clip_len: int) -> list[dict]:
        """Evenly divide video into ~60-second segments as a fallback."""
        clips = []
        n = max(1, int(duration // clip_len))
        step = duration / n
        for i in range(n):
            start = i * step
            end = min(start + clip_len, duration)
            clips.append({
                "clip_number": i + 1,
                "start_time": round(start, 1),
                "end_time": round(end, 1),
                "title": f"Clip {i + 1}",
                "hook": "",
                "why_viral": "Auto-generated segment",
                "virality_score": 5.0,
            })
        return clips

    # ------------------------------------------------------------------
    # Step 4 – Extract clip with ffmpeg
    # ------------------------------------------------------------------

    def extract_clip(self, video_path: str, start: float, end: float, out_path: str) -> str:
        """Cut a segment from the source video using ffmpeg (no re-encode for speed)."""
        duration = end - start
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start),
            "-i", video_path,
            "-t", str(duration),
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart",
            out_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg clip extraction failed:\n{result.stderr}")
        return out_path

    # ------------------------------------------------------------------
    # Step 5 – Copyright-safe audio processing
    # ------------------------------------------------------------------

    def make_copyright_safe(self, clip_path: str) -> str:
        """
        Isolate the spoken voice band and suppress background music.

        Technique:
        1. Apply a bandpass filter centred on human speech (200 Hz – 3 400 Hz)
           to attenuate music frequencies.
        2. Apply dynamic compression so speech stays clear.

        This does NOT guarantee copyright clearance, but it significantly
        reduces recognisable copyrighted music while keeping speech intelligible.
        The output is ready to upload; further music replacement is optional.
        """
        out_path = clip_path.replace(".mp4", "_safe.mp4")
        cmd = [
            "ffmpeg", "-y", "-i", clip_path,
            "-af", (
                "highpass=f=180,"
                "lowpass=f=3800,"
                "equalizer=f=1000:width_type=o:width=2:g=3,"
                "compand=attacks=0.1:decays=0.3:points=-80/-80|-40/-20|0/-10"
            ),
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "128k",
            out_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  [warn] Audio safety pass failed – keeping original audio.")
            return clip_path
        os.remove(clip_path)
        return out_path

    # ------------------------------------------------------------------
    # Step 6 – Burn captions (optional)
    # ------------------------------------------------------------------

    def _write_srt(self, segments: list[dict], srt_path: str) -> None:
        def ts(sec: float) -> str:
            h = int(sec // 3600)
            m = int((sec % 3600) // 60)
            s = int(sec % 60)
            ms = int((sec - int(sec)) * 1000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        with open(srt_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(segments, 1):
                f.write(f"{i}\n{ts(seg['start'])} --> {ts(seg['end'])}\n{seg['text']}\n\n")

    def burn_captions(self, clip_path: str, segments: list[dict], clip_start: float) -> str:
        """Burn SRT subtitles into the clip (shifted relative to clip start)."""
        if not segments:
            return clip_path

        shifted = [
            {"start": max(0, s["start"] - clip_start), "end": max(0, s["end"] - clip_start), "text": s["text"]}
            for s in segments
        ]

        srt_path = clip_path.replace(".mp4", ".srt")
        self._write_srt(shifted, srt_path)

        out_path = clip_path.replace("_safe.mp4", "_captioned.mp4").replace(".mp4", "_captioned.mp4")
        cmd = [
            "ffmpeg", "-y", "-i", clip_path,
            "-vf", f"subtitles={srt_path}:force_style='FontName=Arial,FontSize=22,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Bold=1'",
            "-c:a", "copy",
            out_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("  [warn] Caption burn failed – skipping captions.")
            return clip_path

        os.remove(srt_path)
        return out_path

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def process(
        self,
        url: str,
        min_virality: float = 7.0,
        add_captions: bool = True,
        min_clip_seconds: int = 60,
        max_clip_seconds: int = 90,
        keep_temp: bool = False,
    ) -> list[dict]:
        """
        Full pipeline for one YouTube URL.

        Returns a list of result dicts:
          {clip_number, title, hook, why_viral, virality_score,
           start_time, end_time, duration, file_path}
        """
        print(f"\n[1/5] Downloading video…")
        video_path, info = self.download_video(url)
        video_title = info.get("title", "Unknown")
        video_duration = float(info.get("duration", 0))
        print(f"      '{video_title}'  ({video_duration:.0f}s)")

        print("[2/5] Extracting audio for transcription…")
        audio_path = self.extract_audio_for_transcription(video_path)

        print("[3/5] Transcribing with Whisper…")
        segments = self.transcribe(audio_path)
        print(f"      {len(segments)} segments found.")

        print("[4/5] Identifying viral moments with AI…")
        clips = self.identify_viral_clips(
            segments, video_title, video_duration,
            min_clip_seconds, max_clip_seconds,
        )
        print(f"      {len(clips)} candidate clips identified.")

        print("[5/5] Extracting & processing clips…")
        results = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for clip in clips:
            score = clip.get("virality_score", 0)
            if score < min_virality:
                print(f"      Clip {clip['clip_number']} skipped (score {score:.1f} < {min_virality})")
                continue

            print(f"      Clip {clip['clip_number']}: '{clip['title']}' (score {score:.1f})")

            raw_path = str(
                self.output_dir / f"clip{clip['clip_number']}_{timestamp}_raw.mp4"
            )

            self.extract_clip(video_path, clip["start_time"], clip["end_time"], raw_path)
            safe_path = self.make_copyright_safe(raw_path)

            final_path = safe_path
            if add_captions and segments:
                clip_segs = [
                    s for s in segments
                    if s["end"] > clip["start_time"] and s["start"] < clip["end_time"]
                ]
                final_path = self.burn_captions(safe_path, clip_segs, clip["start_time"])

            results.append({
                **{k: clip[k] for k in ("clip_number", "title", "hook", "why_viral", "virality_score",
                                         "start_time", "end_time")},
                "duration": round(clip["end_time"] - clip["start_time"], 1),
                "file_path": final_path,
            })
            print(f"        Saved → {final_path}")

        # Cleanup temp files
        if not keep_temp:
            for tmp in [audio_path, video_path]:
                try:
                    os.remove(tmp)
                except OSError:
                    pass

        self._save_report(results, video_title, timestamp)
        return results

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------

    def _save_report(self, results: list[dict], video_title: str, timestamp: str) -> None:
        report = {
            "video_title": video_title,
            "generated_at": timestamp,
            "total_clips": len(results),
            "clips": results,
        }
        report_path = self.output_dir / f"report_{timestamp}.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n      Report saved → {report_path}")
