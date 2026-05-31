import { useCurrentFrame, interpolate, Easing } from "remotion";
import { COLORS, FONT, EASE, glassCard } from "../theme";

// A glassy phone with notification cards stacking in — used for scene 1 & 2.
export const PhoneMockup: React.FC<{
  startAt?: number;
  notifications?: { app: string; text: string; color: string }[];
}> = ({ startAt = 0, notifications = DEFAULT_NOTIFS }) => {
  const frame = useCurrentFrame();

  const enter = interpolate(frame, [startAt, startAt + 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(...EASE.out),
  });
  const float = interpolate(Math.sin(frame / 40), [-1, 1], [-10, 10]);

  return (
    <div
      style={{
        position: "relative",
        width: 460,
        height: 940,
        margin: "0 auto",
        opacity: enter,
        transform: `translateY(${interpolate(enter, [0, 1], [80, float])}px) scale(${interpolate(
          enter,
          [0, 1],
          [0.9, 1],
        )})`,
      }}
    >
      {/* Outer device */}
      <div
        style={{
          ...glassCard(56),
          position: "absolute",
          inset: 0,
          background:
            "linear-gradient(160deg, rgba(30,44,90,0.75), rgba(10,16,36,0.85))",
          border: `2px solid ${COLORS.cardStroke}`,
          boxShadow: `0 50px 120px rgba(0,0,0,0.6), 0 0 80px ${COLORS.blue}33, inset 0 1px 0 rgba(255,255,255,0.08)`,
        }}
      />
      {/* Notch */}
      <div
        style={{
          position: "absolute",
          top: 26,
          left: "50%",
          transform: "translateX(-50%)",
          width: 150,
          height: 30,
          borderRadius: 18,
          background: "rgba(0,0,0,0.7)",
        }}
      />
      {/* Notification stack */}
      <div
        style={{
          position: "absolute",
          top: 110,
          left: 26,
          right: 26,
          display: "flex",
          flexDirection: "column",
          gap: 22,
        }}
      >
        {notifications.map((n, i) => {
          const t = startAt + 14 + i * 12;
          const ne = interpolate(frame, [t, t + 16], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(...EASE.pop),
          });
          return (
            <div
              key={i}
              style={{
                ...glassCard(24),
                padding: "20px 22px",
                display: "flex",
                alignItems: "center",
                gap: 18,
                opacity: ne,
                transform: `translateX(${interpolate(ne, [0, 1], [60, 0])}px)`,
              }}
            >
              <div
                style={{
                  width: 54,
                  height: 54,
                  borderRadius: 14,
                  background: n.color,
                  boxShadow: `0 0 24px ${n.color}aa`,
                  flexShrink: 0,
                }}
              />
              <div style={{ flex: 1 }}>
                <div
                  style={{
                    fontFamily: FONT.family,
                    fontWeight: 700,
                    fontSize: 26,
                    color: COLORS.text,
                  }}
                >
                  {n.app}
                </div>
                <div
                  style={{
                    fontFamily: FONT.family,
                    fontWeight: 500,
                    fontSize: 22,
                    color: COLORS.textDim,
                    marginTop: 2,
                  }}
                >
                  {n.text}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const DEFAULT_NOTIFS = [
  { app: "Messages", text: "3 new texts", color: "#34d399" },
  { app: "Mail", text: "12 unread", color: COLORS.blue },
  { app: "Instagram", text: "@alex liked your post", color: "#ec4899" },
  { app: "Slack", text: "5 mentions", color: COLORS.orange },
];
