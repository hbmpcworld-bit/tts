import { useCurrentFrame, interpolate, Easing } from "remotion";
import { COLORS, FONT, EASE } from "../theme";

type Word = {
  text: string;
  accent?: boolean; // orange highlight
  blue?: boolean; // blue highlight
};

// Kinetic typography: words rise + fade in, staggered. Accent words get an
// orange glow, blue words a neon-blue glow. Local frame (use inside a Sequence).
export const AnimatedWords: React.FC<{
  words: Word[];
  fontSize?: number;
  startAt?: number;
  staggerFrames?: number;
  lineHeight?: number;
  align?: "center" | "left";
  maxWidth?: number;
}> = ({
  words,
  fontSize = 96,
  startAt = 0,
  staggerFrames = 3,
  lineHeight = 1.12,
  align = "center",
  maxWidth = 920,
}) => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        gap: `${fontSize * 0.12}px ${fontSize * 0.26}px`,
        justifyContent: align === "center" ? "center" : "flex-start",
        alignItems: "baseline",
        maxWidth,
        margin: "0 auto",
        padding: "0 60px",
        lineHeight,
      }}
    >
      {words.map((w, i) => {
        const t = startAt + i * staggerFrames;
        const enter = interpolate(frame, [t, t + 14], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.bezier(...EASE.out),
        });
        const y = interpolate(enter, [0, 1], [38, 0]);
        const blur = interpolate(enter, [0, 1], [10, 0]);

        const color = w.accent
          ? COLORS.orange
          : w.blue
            ? COLORS.blueBright
            : COLORS.text;
        const glow = w.accent
          ? `0 0 28px ${COLORS.orange}99`
          : w.blue
            ? `0 0 26px ${COLORS.blueBright}88`
            : "0 2px 18px rgba(0,0,0,0.5)";

        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              fontFamily: FONT.family,
              fontWeight: w.accent || w.blue ? 800 : 700,
              fontSize,
              color,
              opacity: enter,
              transform: `translateY(${y}px)`,
              filter: `blur(${blur}px)`,
              textShadow: glow,
              letterSpacing: "-0.02em",
            }}
          >
            {w.text}
          </span>
        );
      })}
    </div>
  );
};
