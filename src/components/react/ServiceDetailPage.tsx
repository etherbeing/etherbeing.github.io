import { useEffect, useState } from "react";
import { FaArrowRight, FaPaypal, FaShieldHalved } from "react-icons/fa6";

import GlowingHeader from "./GlowingHeader";
import SpotlightCard from "./SpotlightCard";
import StarBorder from "./StarBorder";
import { useGithubSession } from "./useGithubSession";
import type { Service } from "./contentTypes";

type ServiceRequest = {
  id: number;
  status: string;
  message: string;
  created_at: string;
};

function StatusMessage({ message }: { message: string }) {
  return (
    <SpotlightCard className="bg-transparent backdrop-blur-2xl cursor-default select-none">
      {message}
    </SpotlightCard>
  );
}

export default function ServiceDetailPage({
  apiUrl,
  slug,
}: {
  apiUrl: string;
  slug: string;
}) {
  const [service, setService] = useState<Service | null>(null);
  const [message, setMessage] = useState("");
  const [requestResult, setRequestResult] = useState<ServiceRequest | null>(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { session, isLoading: isSessionLoading, login, refreshSession } = useGithubSession(apiUrl);

  useEffect(() => {
    fetch(`${apiUrl}/api/site/service/${slug}/`, { credentials: "include" })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("Unable to load the selected service.");
        }
        const payload: Service = await response.json();
        setService(payload);
      })
      .catch((err: Error) => {
        console.error(err);
        setError("We could not load this service right now.");
      });
  }, [apiUrl, slug]);

  async function acquireService() {
    if (!service) return;
    const activeSession = session.csrf_token ? session : await refreshSession();
    if (!activeSession.is_authenticated) {
      login(`/services/entry?slug=${slug}`);
      return;
    }

    setIsSubmitting(true);
    setError("");
    try {
      const response = await fetch(`${apiUrl}/api/site/service/${slug}/request/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": activeSession.csrf_token,
        },
        body: JSON.stringify({ message }),
      });
      if (!response.ok) {
        throw new Error("Unable to submit service request.");
      }
      const payload: ServiceRequest = await response.json();
      setRequestResult(payload);
    } catch (requestError) {
      console.error(requestError);
      setError("The request could not be submitted. Please try again in a moment.");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (error && !service) {
    return <section className="py-32"><StatusMessage message={error} /></section>;
  }

  if (!service) {
    return <section className="py-32"><StatusMessage message="Loading service details..." /></section>;
  }

  return (
    <section className="py-24 space-y-10">
      <div className="space-y-6 text-center">
        <p className="text-xs uppercase tracking-[0.35em] text-cyan-200/70">Service Detail</p>
        <GlowingHeader>{service.title}</GlowingHeader>
        <p className="mx-auto max-w-3xl text-lg text-cyan-100/90">{service.headline}</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <SpotlightCard className="bg-transparent backdrop-blur-2xl">
          <div className="space-y-6">
            <div className="flex flex-wrap items-center gap-3 text-sm">
              <span className="rounded-full border border-cyan-300/40 bg-cyan-400/10 px-4 py-2 text-cyan-50">
                From {service.starting_price} USD
              </span>
              {service.skills.map((skill) => (
                <span
                  key={skill}
                  className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-slate-200"
                >
                  {skill}
                </span>
              ))}
            </div>
            <p className="text-base leading-8 text-slate-200">{service.overview || service.description}</p>
            <div className="grid gap-4 md:grid-cols-2">
              <div className="rounded-[1.75rem] border border-white/10 bg-slate-950/40 p-5">
                <h2 className="text-lg font-semibold text-white">What You Receive</h2>
                <ul className="mt-4 space-y-3 text-sm text-slate-200">
                  {service.deliverables.map((item) => (
                    <li key={item} className="flex gap-3">
                      <span className="mt-0.5 text-cyan-200"><FaArrowRight /></span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="rounded-[1.75rem] border border-white/10 bg-slate-950/40 p-5">
                <h2 className="text-lg font-semibold text-white">Expected Outcomes</h2>
                <ul className="mt-4 space-y-3 text-sm text-slate-200">
                  {service.outcomes.map((item) => (
                    <li key={item} className="flex gap-3">
                      <span className="mt-0.5 text-fuchsia-200"><FaShieldHalved /></span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <div className="rounded-[1.75rem] border border-white/10 bg-slate-950/40 p-5">
              <h2 className="text-lg font-semibold text-white">How We Work</h2>
              <ol className="mt-4 space-y-4">
                {service.process_steps.map((step, index) => (
                  <li key={step} className="flex gap-4 text-slate-200">
                    <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-white/15 bg-white/5 text-sm font-semibold text-white">
                      {index + 1}
                    </span>
                    <span className="pt-2 text-sm leading-7">{step}</span>
                  </li>
                ))}
              </ol>
            </div>
          </div>
        </SpotlightCard>

        <div className="space-y-6">
          <SpotlightCard className="bg-transparent backdrop-blur-2xl">
            <div className="space-y-4">
              <p className="text-xs uppercase tracking-[0.3em] text-cyan-200/70">Acquire Service</p>
              <h2 className="text-2xl font-semibold text-white">Start a service request</h2>
              <p className="text-sm leading-7 text-slate-300">
                {service.engagement_cta || "Share a bit of context and I will review the request from the admin side."}
              </p>
              <textarea
                className="min-h-36 w-full rounded-[1.5rem] border border-white/10 bg-slate-950/50 px-4 py-4 text-sm text-white outline-none"
                placeholder="Describe your goal, timeline, stack, or the problem you want solved."
                value={message}
                onChange={(event) => setMessage(event.target.value)}
              />
              {requestResult ? (
                <div className="rounded-[1.5rem] border border-emerald-300/20 bg-emerald-400/10 px-4 py-4 text-sm text-emerald-100">
                  Service request submitted. Status: {requestResult.status}.
                </div>
              ) : null}
              {error && service ? (
                <div className="rounded-[1.5rem] border border-red-300/20 bg-red-400/10 px-4 py-4 text-sm text-red-100">
                  {error}
                </div>
              ) : null}
              <button
                type="button"
                onClick={() => void acquireService()}
                disabled={isSubmitting || isSessionLoading}
                className="w-full"
              >
                <StarBorder as="span" className="flex w-full items-center justify-center gap-3 cursor-pointer">
                  <span>
                    {session.is_authenticated ? "Acquire this service" : "Login with GitHub to acquire"}
                  </span>
                  <FaArrowRight />
                </StarBorder>
              </button>
            </div>
          </SpotlightCard>

          <SpotlightCard className="bg-transparent backdrop-blur-2xl">
            <div className="space-y-3">
              <h2 className="text-lg font-semibold text-white">Support the mission</h2>
              <p className="text-sm leading-7 text-slate-300">
                If you want to support ongoing research and tooling independently of a formal service request, you can donate directly.
              </p>
              <a href="https://paypal.me/etherbeing" target="_blank" rel="noreferrer">
                <StarBorder as="span" className="flex items-center justify-center gap-3 cursor-pointer">
                  <span>Donate via PayPal</span>
                  <FaPaypal />
                </StarBorder>
              </a>
            </div>
          </SpotlightCard>
        </div>
      </div>
    </section>
  );
}
