import GlowingText from "./GlowingText";

export default function GlowingHeader({ children }: { children: string }) {
  return (
    <div className="text-center animate-fade-up mb-20 cursor-default select-none">
      <GlowingText>
        <h2 className="text-3xl font-bold">{children}</h2>
        <span> ╰─〔❨✧✧❩〕─╯ </span>
      </GlowingText>
    </div>
  );
}
