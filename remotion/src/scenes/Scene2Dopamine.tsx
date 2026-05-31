import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { Background } from "../components/Background";
import { PhoneMockup } from "../components/PhoneMockup";
import { AnimatedWords } from "../components/AnimatedWords";
import { CaptionBar } from "../components/CaptionBar";
import { COLORS, FONT, EASE, glassCard } from "../theme";

// "Every notification, every email, every social media post triggers
//  micro doses of dopamine..."
export const Scene2Dopamine: React.FC = () => {
  const frame = useCurrentFrame();
  const captionStep = Math.min(5, Math.floor(interpolate(frame, [0, 230], [0, 6])));

  return (
    <AbsoluteFill>
      <Background accent="blue" />

      {/* Phone with stacking notifications */}
      <div style={{ position: "absolute", top: 150, width: "100%" }}>
        <PhoneMockup startAt={4} />
      </div>

      {/* Floating "dopamine" molecule chips that pop near the phone */}
      {DOPAMINE_HITS.map((d, i) => {
        const t = 70 + i * 10;
        const pop = interpolate(frame, [t, t + 18], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.bezier(...EASE.pop),
        });
        const drift = interpolate(frame, [t, t + 120], [0, -40], {
          extrapolateRight: "clamp",
        });
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: d.x,
              top: d.y + drift,
              opacity: pop * interpolate(frame, [t + 90, t + 130], [1, 0.6], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
              transform: `scale(${pop})`,
              ...glassCard(999),
              padding: "10px 22px",
              border: `1px solid ${COLORS.orange}66`,
              boxShadow: `0 0 30px ${COLORS.orange}66`,
              fontFamily: FONT.family,
              fontWeight: 800,
              fontSize: 30,
              color: COLORS.orangeBright,
            }}
          >
            +dopamine
          </div>
        );
      })}

      {/* Headline */}
      <div style={{ position: "absolute", top: 1180, width: "100%" }}>
        <AnimatedWords
          words={[
            { text: "Every" },
            { text: "ping" },
            { text: "=" },
            { text: "a" },
            { text: "micro", accent: true },
            { text: "dose", accent: true },
          ]}
          fontSize={84}
          startAt={40}
          staggerFrames={4}
        />
      </div>

      <CaptionBar
        segments={["Notifications", "trigger", "micro", "doses", "of", "dopamine"]}
        highlightIndex={captionStep}
      />
    </AbsoluteFill>
  );
};

const DOPAMINE_HITS = [
  { x: 120, y: 380 },
  { x: 720, y: 460 },
  { x: 160, y: 700 },
  { x: 700, y: 760 },
  { x: 110, y: 980 },
];
