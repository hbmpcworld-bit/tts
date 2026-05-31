import "./index.css";
import { Composition } from "remotion";
import { DopamineShort, TOTAL_FRAMES } from "./DopamineShort";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="DopamineShort"
        component={DopamineShort}
        durationInFrames={TOTAL_FRAMES}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
