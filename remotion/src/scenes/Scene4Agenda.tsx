import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { Background } from "../components/Background";
import { AnimatedWords } from "../components/AnimatedWords";
import { CaptionBar } from "../components/CaptionBar";
import { COLORS, FONT, EASE, glassCard } from "../theme";

// "You're essentially letting other people's agendas set the emotional tone of
//  your day before you've had a chance to set your own."
export const Scene4Agenda: React.FC = () => {
  const frame = useCurrentFrame();
  const captionStep = Math.min(5, Math.floor(interpolate(frame, [0, 250], [0, 6])));

  // The "your day" dial swings from others' colors to a calm orange when the
  // resolution lands.
  const claim = interpolate(frame, [150, 180], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(...EASE.out),
  });

  return (
    <AbsoluteFill>
      <Background accent={claim > 0.5 ? "orange" : "blue"} />

      {/* Incoming "agenda" cards flying toward a central day-disc */}
      {AGENDAS.map((a, i) => {
        const t = 20 + i * 8;
        const fly = interpolate(frame, [t, t + 22], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.bezier(...EASE.out),
        });
        const gone = interpolate(frame, [150, 170], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: interpolate(fly, [0, 1], [a.fromX, a.toX]),
              top: interpolate(fly, [0, 1], [a.fromY, a.toY]),
              opacity: fly * gone,
              transform: `scale(${interpolate(fly, [0, 1], [0.6, 1])})`,
              ...glassCard(18),
              padding: "14px 24px",
              border: `1px solid ${a.color}88`,
              boxShadow: `0 0 26px ${a.color}66`,
              fontFamily: FONT.family,
              fontWeight: 700,
              fontSize: 28,
              color: COLORS.text,
            }}
          >
            {a.label}
          </div>
        );
      })}

      {/* Central "your day" disc */}
      <div
        style={{
          position: "absolute",
          top: 700,
          left: "50%",
          transform: "translateX(-50%)",
          width: 360,
          height: 360,
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: 0,
            borderRadius: "50%",
            background: `conic-gradient(from ${frame * 1.5}deg, ${COLORS.blue}, #ec4899, ${COLORS.cyan}, ${COLORS.orange}, ${COLORS.blue})`,
            filter: `saturate(${interpolate(claim, [0, 1], [1, 0.2])})`,
            opacity: 0.85,
            boxShadow: `0 0 90px ${claim > 0.5 ? COLORS.orange : COLORS.blue}88`,
          }}
        />
        {/* Calm orange core that takes over when you reclaim the day */}
        <div
          style={{
            position: "absolute",
            inset: interpolate(claim, [0, 1], [180, 18]),
            borderRadius: "50%",
            background: `radial-gradient(circle at 40% 35%, ${COLORS.orangeBright}, ${COLORS.orange} 70%)`,
            boxShadow: `0 0 80px ${COLORS.orange}aa`,
            opacity: claim,
          }}
        />
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontFamily: FONT.family,
            fontWeight: 800,
            fontSize: 44,
            color: COLORS.text,
            textShadow: "0 2px 20px rgba(0,0,0,0.6)",
          }}
        >
          {claim > 0.5 ? "YOUR DAY" : "?"}
        </div>
      </div>

      {/* Headline / payoff */}
      <div style={{ position: "absolute", top: 1200, width: "100%" }}>
        <AnimatedWords
          words={[
            { text: "Set" },
            { text: "your" },
            { text: "own" },
            { text: "tone", accent: true },
            { text: "first." },
          ]}
          fontSize={96}
          startAt={170}
          staggerFrames={4}
        />
      </div>

      <CaptionBar
        segments={["Don't", "let", "others", "set", "your", "tone"]}
        highlightIndex={captionStep}
      />
    </AbsoluteFill>
  );
};

const AGENDAS = [
  { label: "📧 Boss's email", color: COLORS.blue, fromX: -300, fromY: 300, toX: 180, toY: 760 },
  { label: "🔴 Breaking news", color: "#ef4444", fromX: 1300, fromY: 360, toX: 620, toY: 720 },
  { label: "❤️ 42 likes", color: "#ec4899", fromX: -300, fromY: 1000, toX: 200, toY: 900 },
  { label: "💬 Group chat", color: COLORS.cyan, fromX: 1300, fromY: 980, toX: 640, toY: 880 },
];
