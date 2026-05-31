import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { Background } from "../components/Background";
import { AnimatedWords } from "../components/AnimatedWords";
import { CaptionBar } from "../components/CaptionBar";
import { COLORS, FONT, EASE, glassCard } from "../theme";

// "You're training your brain in its most impressionable window to be
//  reactive rather than intentional..."
export const Scene3Reactive: React.FC = () => {
  const frame = useCurrentFrame();
  const captionStep = Math.min(4, Math.floor(interpolate(frame, [0, 200], [0, 5])));

  // Toggle slider that slams from "Reactive" to ... staying reactive (the point).
  const slide = interpolate(frame, [60, 90], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(...EASE.out),
  });

  return (
    <AbsoluteFill>
      <Background accent="blue" />

      {/* Section label */}
      <div style={{ position: "absolute", top: 280, width: "100%" }}>
        <AnimatedWords
          words={[{ text: "MOST" }, { text: "IMPRESSIONABLE", blue: true }, { text: "WINDOW" }]}
          fontSize={42}
          startAt={6}
          staggerFrames={2}
        />
      </div>

      {/* Reactive vs Intentional comparison cards */}
      <div
        style={{
          position: "absolute",
          top: 520,
          left: 0,
          right: 0,
          display: "flex",
          flexDirection: "column",
          gap: 40,
          alignItems: "center",
        }}
      >
        <ComparisonCard
          label="REACTIVE"
          desc="Letting the world set your tone"
          color={COLORS.orange}
          active={slide < 0.5}
          startAt={20}
          frame={frame}
        />
        <div
          style={{
            fontFamily: FONT.family,
            fontWeight: 800,
            fontSize: 40,
            color: COLORS.textDim,
            opacity: interpolate(frame, [40, 55], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          }}
        >
          rather than
        </div>
        <ComparisonCard
          label="INTENTIONAL"
          desc="Choosing your own focus"
          color={COLORS.blueBright}
          active={false}
          dimmed
          startAt={48}
          frame={frame}
        />
      </div>

      {/* Headline */}
      <div style={{ position: "absolute", top: 1280, width: "100%" }}>
        <AnimatedWords
          words={[
            { text: "You're" },
            { text: "training" },
            { text: "reactivity", accent: true },
            { text: "." },
          ]}
          fontSize={88}
          startAt={70}
          staggerFrames={4}
        />
      </div>

      <CaptionBar
        segments={["Reactive", "rather", "than", "intentional"]}
        highlightIndex={captionStep}
      />
    </AbsoluteFill>
  );
};

const ComparisonCard: React.FC<{
  label: string;
  desc: string;
  color: string;
  active: boolean;
  dimmed?: boolean;
  startAt: number;
  frame: number;
}> = ({ label, desc, color, active, dimmed, startAt, frame }) => {
  const enter = interpolate(frame, [startAt, startAt + 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(...EASE.out),
  });
  return (
    <div
      style={{
        ...glassCard(28),
        width: 820,
        padding: "34px 42px",
        opacity: enter * (dimmed ? 0.55 : 1),
        transform: `translateY(${interpolate(enter, [0, 1], [40, 0])}px)`,
        border: active ? `2px solid ${color}` : `1px solid ${COLORS.cardStroke}`,
        boxShadow: active
          ? `0 0 60px ${color}55, inset 0 1px 0 rgba(255,255,255,0.07)`
          : "0 30px 80px rgba(0,0,0,0.5)",
        display: "flex",
        alignItems: "center",
        gap: 28,
      }}
    >
      <div
        style={{
          width: 70,
          height: 70,
          borderRadius: 20,
          background: color,
          boxShadow: `0 0 30px ${color}aa`,
          flexShrink: 0,
        }}
      />
      <div>
        <div
          style={{
            fontFamily: FONT.family,
            fontWeight: 800,
            fontSize: 52,
            color: active ? color : COLORS.text,
            letterSpacing: "-0.02em",
          }}
        >
          {label}
        </div>
        <div
          style={{
            fontFamily: FONT.family,
            fontWeight: 500,
            fontSize: 30,
            color: COLORS.textDim,
            marginTop: 4,
          }}
        >
          {desc}
        </div>
      </div>
    </div>
  );
};
