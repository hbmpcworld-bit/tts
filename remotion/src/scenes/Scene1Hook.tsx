import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { Background } from "../components/Background";
import { AnimatedWords } from "../components/AnimatedWords";
import { CaptionBar } from "../components/CaptionBar";
import { COLORS, EASE } from "../theme";

// "When you immediately check your phone, you're doing something very specific
//  to your neurochemistry."
export const Scene1Hook: React.FC = () => {
  const frame = useCurrentFrame();

  // A pulsing "brain" orb to introduce the neurochemistry idea.
  const orbPulse = interpolate(Math.sin(frame / 12), [-1, 1], [0.94, 1.06]);
  const orbEnter = interpolate(frame, [30, 55], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(...EASE.out),
  });

  const captionStep = Math.floor(interpolate(frame, [0, 200], [0, 4]));

  return (
    <AbsoluteFill>
      <Background accent="blue" />

      {/* Eyebrow tag */}
      <div style={{ position: "absolute", top: 230, width: "100%" }}>
        <AnimatedWords
          words={[{ text: "THE", blue: true }, { text: "FIRST" }, { text: "5", blue: true }, { text: "MINUTES" }]}
          fontSize={40}
          startAt={6}
          staggerFrames={2}
        />
      </div>

      {/* Brain orb */}
      <div
        style={{
          position: "absolute",
          top: 470,
          left: "50%",
          transform: `translateX(-50%) scale(${orbEnter * orbPulse})`,
          opacity: orbEnter,
          width: 340,
          height: 340,
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: 0,
            borderRadius: "50%",
            background: `radial-gradient(circle at 35% 30%, ${COLORS.cyan}, ${COLORS.blue} 55%, #1e2a66 100%)`,
            boxShadow: `0 0 120px ${COLORS.blue}aa, inset 0 0 80px rgba(0,0,0,0.5)`,
          }}
        />
        {/* Synapse sparks */}
        <div
          style={{
            position: "absolute",
            inset: -30,
            borderRadius: "50%",
            border: `2px solid ${COLORS.blueBright}55`,
            transform: `scale(${interpolate(Math.sin(frame / 12), [-1, 1], [1, 1.25])})`,
            opacity: interpolate(Math.sin(frame / 12), [-1, 1], [0.6, 0]),
          }}
        />
      </div>

      {/* Main headline */}
      <div style={{ position: "absolute", top: 880, width: "100%" }}>
        <AnimatedWords
          words={[
            { text: "Check" },
            { text: "your" },
            { text: "phone" },
            { text: "first?" },
          ]}
          fontSize={104}
          startAt={45}
          staggerFrames={4}
        />
        <div style={{ height: 18 }} />
        <AnimatedWords
          words={[
            { text: "You're" },
            { text: "rewiring" },
            { text: "your" },
            { text: "neurochemistry", blue: true },
            { text: "." },
          ]}
          fontSize={62}
          startAt={70}
          staggerFrames={3}
        />
      </div>

      <CaptionBar
        segments={["You're", "doing", "something", "to", "your", "brain"]}
        highlightIndex={captionStep}
      />
    </AbsoluteFill>
  );
};
