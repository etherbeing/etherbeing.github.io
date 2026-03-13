import { useEffect, useId, useState } from "react";

declare global {
  interface Window {
    grecaptcha?: {
      render: (
        container: HTMLElement | string,
        parameters: {
          sitekey: string;
          callback?: (token: string) => void;
          "expired-callback"?: () => void;
          "error-callback"?: () => void;
        },
      ) => number;
      reset: (widgetId?: number) => void;
    };
  }
}

let recaptchaScriptPromise: Promise<void> | null = null;

function loadRecaptchaScript() {
  if (typeof window === "undefined") {
    return Promise.resolve();
  }
  if (window.grecaptcha?.render) {
    return Promise.resolve();
  }
  if (recaptchaScriptPromise) {
    return recaptchaScriptPromise;
  }

  recaptchaScriptPromise = new Promise<void>((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "https://www.google.com/recaptcha/api.js?render=explicit";
    script.async = true;
    script.defer = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Unable to load reCAPTCHA."));
    document.head.appendChild(script);
  });

  return recaptchaScriptPromise;
}

export default function RecaptchaCheckbox({
  siteKey,
  onTokenChange,
}: {
  siteKey?: string;
  onTokenChange: (token: string) => void;
}) {
  const containerId = useId().replace(/:/g, "");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!siteKey) {
      onTokenChange("");
      return;
    }

    let active = true;
    let widgetId: number | null = null;

    loadRecaptchaScript()
      .then(() => {
        if (!active || !window.grecaptcha?.render) return;
        const container = document.getElementById(containerId);
        if (!container) return;
        container.innerHTML = "";
        widgetId = window.grecaptcha.render(container, {
          sitekey: siteKey,
          callback: (token: string) => {
            if (!active) return;
            setError("");
            onTokenChange(token);
          },
          "expired-callback": () => {
            if (!active) return;
            onTokenChange("");
          },
          "error-callback": () => {
            if (!active) return;
            onTokenChange("");
            setError("reCAPTCHA could not be loaded correctly.");
          },
        });
      })
      .catch((scriptError: Error) => {
        if (!active) return;
        onTokenChange("");
        setError(scriptError.message);
      });

    return () => {
      active = false;
      if (widgetId !== null && window.grecaptcha?.reset) {
        window.grecaptcha.reset(widgetId);
      }
    };
  }, [containerId, onTokenChange, siteKey]);

  if (!siteKey) {
    return null;
  }

  return (
    <div className="space-y-2">
      <div id={containerId} className="min-h-[78px]" />
      {error ? <p className="text-sm text-red-200">{error}</p> : null}
    </div>
  );
}
