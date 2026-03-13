import { useState } from "react";

export default function AlterEgoCard({
  alterSrc,
  baseSrc,
}: {
  alterSrc: string;
  baseSrc: string;
}) {
  const [split, setSplit] = useState(100);

  return (
    <div
      role="img"
      className="relative h-80 w-full overflow-hidden"
      onMouseEnter={(event) => {
        setSplit((event.nativeEvent.offsetX * 100) / event.currentTarget.clientWidth);
      }}
      onMouseMove={(event) => {
        setSplit((event.nativeEvent.offsetX * 100) / event.currentTarget.clientWidth);
      }}
      onMouseLeave={() => {
        setSplit(100);
      }}
    >
      <img
        alt="Esteban portrait"
        src={baseSrc}
        className="absolute inset-0 h-full w-full object-cover"
      />
      <img
        alt="Esteban alter ego illustration"
        src={alterSrc}
        className="absolute inset-0 h-full w-full object-cover"
        style={{
          maskImage: `linear-gradient(to right, transparent 0%, transparent ${split}%, black ${split}%, black 100%)`,
          WebkitMaskImage: `linear-gradient(to right, transparent 0%, transparent ${split}%, black ${split}%, black 100%)`,
        }}
      />
    </div>
  );
}
