import { AbsoluteFill } from "remotion";
import {
  TransitionSeries,
  linearTiming,
} from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { Scene1Hook } from "./scenes/Scene1Hook";
import { Scene2Dopamine } from "./scenes/Scene2Dopamine";
import { Scene3Reactive } from "./scenes/Scene3Reactive";
import { Scene4Agenda } from "./scenes/Scene4Agenda";
import { COLORS } from "./theme";

// Scene lengths (frames @ 30fps). Transitions overlap and shorten the total.
export const SCENE_FRAMES = {
  s1: 210,
  s2: 240,
  s3: 220,
  s4: 280,
} as const;
export const TRANSITION_FRAMES = 18;

// Total = sum(scenes) - 3 transitions = 950 - 54 = 896 frames.
export const TOTAL_FRAMES =
  SCENE_FRAMES.s1 +
  SCENE_FRAMES.s2 +
  SCENE_FRAMES.s3 +
  SCENE_FRAMES.s4 -
  3 * TRANSITION_FRAMES;

export const DopamineShort: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg0 }}>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={SCENE_FRAMES.s1}>
          <Scene1Hook />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        <TransitionSeries.Sequence durationInFrames={SCENE_FRAMES.s2}>
          <Scene2Dopamine />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={slide({ direction: "from-right" })}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        <TransitionSeries.Sequence durationInFrames={SCENE_FRAMES.s3}>
          <Scene3Reactive />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        <TransitionSeries.Sequence durationInFrames={SCENE_FRAMES.s4}>
          <Scene4Agenda />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
