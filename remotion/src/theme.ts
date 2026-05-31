// Shared visual language for the "Dopamine" short.
// Dark glassy SaaS aesthetic (deep navy/black, neon-blue glows, glassmorphic cards)
// with orange used as a sparing, high-energy accent.

export const COLORS = {
  bg0: "#05070f", // deepest background
  bg1: "#0a1024", // navy base
  bg2: "#111a3a", // raised navy
  blue: "#3b82f6", // primary neon blue
  blueBright: "#60a5fa",
  cyan: "#22d3ee", // cyan edge glow
  orange: "#ff7a1a", // accent
  orangeBright: "#ff9d4d",
  text: "#f4f7ff",
  textDim: "#9fb0d6",
  cardStroke: "rgba(120,150,255,0.18)",
  cardFill: "rgba(20,30,66,0.55)",
} as const;

export const FONT = {
  family:
    '"SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif',
} as const;

// Glassmorphic card style used across scenes.
export const glassCard = (radius = 28): React.CSSProperties => ({
  background: COLORS.cardFill,
  border: `1px solid ${COLORS.cardStroke}`,
  borderRadius: radius,
  boxShadow:
    "0 30px 80px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.07)",
  backdropFilter: "blur(20px)",
  WebkitBackdropFilter: "blur(20px)",
});

// Easing curves (CSS cubic-bezier equivalents).
export const EASE = {
  // Crisp UI entrance — strong ease-out, no overshoot.
  out: [0.16, 1, 0.3, 1] as const,
  // Editorial balanced ease-in-out.
  inOut: [0.45, 0, 0.55, 1] as const,
  // Playful overshoot — use sparingly for emphasis.
  pop: [0.34, 1.56, 0.64, 1] as const,
};
