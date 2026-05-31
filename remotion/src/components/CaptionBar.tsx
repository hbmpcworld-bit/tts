import { useCurrentFrame, interpolate, Easing } from "remotion";
import { COLORS, FONT, EASE, glassCard } from "../theme";

// Bottom karaoke-style caption chip — present in every scene for short-form
// readability. Words highlight (orange) as they are "spoken".
export const CaptionBar: React.FC<{
  segments: string[];
  highlightIndex: number;
}> = ({ segments, highlightIndex }) => {
  const frame = useCurrentFrame();
  const enter = interpolate(frame, [0, 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(...EASE.out),
  });

  return (
    <div
      style={{
        position: "absolute",
        bottom: 150,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        opacity: enter,
        transform: `translateY(${interpolate(enter, [0, 1], [30, 0])}px)`,
      }}
    >
      <div
        style={{
          ...glassCard(22),
          padding: "20px 34px",
          maxWidth: 900,
          display: "flex",
          flexWrap: "wrap",
          gap: "6px 14px",
          justifyContent: "center",
        }}
      >
        {segments.map((s, i) => (
          <span
            key={i}
            style={{
              fontFamily: FONT.family,
              fontWeight: i === highlightIndex ? 800 : 600,
              fontSize: 38,
              color: i === highlightIndex ? COLORS.orange : COLORS.textDim,
              textShadow:
                i === highlightIndex ? `0 0 18px ${COLORS.orange}88` : "none",
              transition: "none",
            }}
          >
            {s}
          </span>
        ))}
      </div>
    </div>
  );
};
