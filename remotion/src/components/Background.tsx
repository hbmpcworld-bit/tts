import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { COLORS } from "../theme";

// Dark glassy backdrop: deep navy gradient, a slow-drifting neon blue glow,
// a faint perspective grid, and floating particles. Shared across all scenes.
export const Background: React.FC<{ accent?: "blue" | "orange" }> = ({
  accent = "blue",
}) => {
  const frame = useCurrentFrame();

  // Slow drift for the primary glow so the background never feels static.
  const driftX = interpolate(
    Math.sin(frame / 90),
    [-1, 1],
    [-120, 120],
  );
  const driftY = interpolate(
    Math.cos(frame / 110),
    [-1, 1],
    [-80, 80],
  );

  const glowColor = accent === "orange" ? COLORS.orange : COLORS.blue;

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 80% at 50% 0%, ${COLORS.bg2} 0%, ${COLORS.bg1} 38%, ${COLORS.bg0} 100%)`,
      }}
    >
      {/* Primary drifting glow */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(40% 30% at calc(50% + ${driftX}px) calc(35% + ${driftY}px), ${glowColor}55 0%, transparent 60%)`,
          filter: "blur(20px)",
        }}
      />
      {/* Secondary cyan rim glow bottom */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(50% 30% at 50% 105%, ${COLORS.cyan}33 0%, transparent 60%)`,
        }}
      />
      {/* Perspective grid */}
      <AbsoluteFill
        style={{
          opacity: 0.18,
          backgroundImage: `linear-gradient(${COLORS.blueBright}22 1px, transparent 1px), linear-gradient(90deg, ${COLORS.blueBright}22 1px, transparent 1px)`,
          backgroundSize: "90px 90px",
          maskImage:
            "radial-gradient(80% 60% at 50% 40%, black 0%, transparent 85%)",
          WebkitMaskImage:
            "radial-gradient(80% 60% at 50% 40%, black 0%, transparent 85%)",
        }}
      />
      <Particles />
      {/* Vignette */}
      <AbsoluteFill
        style={{
          boxShadow: "inset 0 0 400px rgba(0,0,0,0.9)",
        }}
      />
    </AbsoluteFill>
  );
};

const PARTICLES = new Array(26).fill(0).map((_, i) => ({
  x: (i * 97) % 100,
  y: (i * 53) % 100,
  size: 2 + ((i * 7) % 5),
  speed: 0.3 + ((i % 5) * 0.18),
  phase: (i * 41) % 100,
}));

const Particles: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      {PARTICLES.map((p, i) => {
        const y = (p.y - frame * p.speed * 0.12 + p.phase) % 100;
        const yy = y < 0 ? y + 100 : y;
        const twinkle = interpolate(
          Math.sin(frame / 20 + p.phase),
          [-1, 1],
          [0.15, 0.7],
        );
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: `${p.x}%`,
              top: `${yy}%`,
              width: p.size,
              height: p.size,
              borderRadius: "50%",
              background: COLORS.blueBright,
              opacity: twinkle,
              boxShadow: `0 0 ${p.size * 3}px ${COLORS.blueBright}`,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};
