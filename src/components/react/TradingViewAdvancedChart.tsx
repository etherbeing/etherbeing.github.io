import { useEffect, useRef } from "react";

type TradingViewAdvancedChartProps = {
  symbol: string;
  title?: string;
};

export default function TradingViewAdvancedChart({
  symbol,
  title,
}: TradingViewAdvancedChartProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    container.innerHTML = "";

    const widgetHost = document.createElement("div");
    widgetHost.className = "tradingview-widget-container__widget h-full w-full";

    const copyright = document.createElement("div");
    copyright.className = "tradingview-widget-copyright";
    copyright.innerHTML = `
      <a
        href="https://www.tradingview.com/symbols/${encodeURIComponent(symbol)}/"
        rel="noopener noreferrer"
        target="_blank"
        class="text-cyan-200/80 hover:text-white"
      >
        Track ${title || symbol} on TradingView
      </a>
    `;

    const script = document.createElement("script");
    script.src =
      "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";
    script.async = true;
    script.type = "text/javascript";
    script.innerHTML = JSON.stringify({
      autosize: true,
      symbol,
      interval: "240",
      timezone: "Etc/UTC",
      theme: "dark",
      style: "1",
      locale: "en",
      height: "1",
      allow_symbol_change: false,
      hide_side_toolbar: false,
      calendar: false,
      support_host: "https://www.tradingview.com",
    });

    container.appendChild(widgetHost);
    container.appendChild(copyright);
    container.appendChild(script);

    return () => {
      container.innerHTML = "";
    };
  }, [symbol, title]);

  return (
    <div
      ref={containerRef}
      className="tradingview-widget-container h-[280px] min-h-[280px] w-full md:min-h-[280px]"
    />
  );
}
