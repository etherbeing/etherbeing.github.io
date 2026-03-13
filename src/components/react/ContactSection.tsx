import { type ReactNode, useState } from "react";
import { FaArrowRight } from "react-icons/fa6";

import GlowingHeader from "./GlowingHeader";
import RecaptchaCheckbox from "./RecaptchaCheckbox";
import SpotlightCard from "./SpotlightCard";
import StarBorder from "./StarBorder";
import { useGithubSession } from "./useGithubSession";

type ContactLink = {
  label: string;
  url: string;
  icon: ReactNode;
};

type ContactGroup = {
  title: string;
  links: ContactLink[];
};

type ContactSectionProps = {
  apiUrl: string;
  contactIntro: string;
  contactGroups: ContactGroup[];
};

export default function ContactSection({
  apiUrl,
  contactIntro,
  contactGroups,
}: ContactSectionProps) {
  const { session, isLoading, login, refreshSession } = useGithubSession(apiUrl);
  const [subject, setSubject] = useState("");
  const [content, setContent] = useState("");
  const [status, setStatus] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [recaptchaToken, setRecaptchaToken] = useState("");

  async function submitContactThread() {
    const activeSession = session.csrf_token ? session : await refreshSession();
    if (!activeSession.is_authenticated) {
      login("/#contact");
      return;
    }

    setIsSubmitting(true);
    setStatus("");
    try {
      if (activeSession.recaptcha_enabled && !recaptchaToken) {
        setStatus("Please complete the reCAPTCHA checkbox before sending your message.");
        setIsSubmitting(false);
        return;
      }
      const response = await fetch(`${apiUrl}/api/site/contact/threads/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": activeSession.csrf_token,
        },
        body: JSON.stringify({
          subject,
          content,
          recaptcha_token: recaptchaToken,
        }),
      });
      if (!response.ok) {
        throw new Error("Unable to send contact message.");
      }
      setSubject("");
      setContent("");
      setStatus("Message sent. You can continue the conversation from your inbox.");
    } catch (error) {
      console.error(error);
      setStatus("The message could not be sent right now. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section id="contact" className="py-20 space-y-4 cursor-default select-none text-justify">
      <GlowingHeader>Contact</GlowingHeader>
      <div className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <SpotlightCard className="flex flex-col items-start gap-5">
          {contactIntro}
          {contactGroups.map((group) => (
            <div className="flex w-fit flex-col gap-2" key={group.title}>
              <b className="w-full">{group.title}</b>
              <ul className="flex flex-wrap gap-2">
                {group.links.map((link) => (
                  <li key={`${group.title}-${link.label}`}>
                    <a target="_blank" className="flex items-center gap-1" href={link.url} rel="noreferrer">
                      {link.icon}
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </SpotlightCard>

        <SpotlightCard className="bg-transparent backdrop-blur-2xl">
          <div className="space-y-4">
            <p className="text-xs uppercase tracking-[0.28em] text-cyan-200/75">Authenticated inbox</p>
            <h3 className="text-2xl font-semibold text-white">Send a private platform message</h3>
            <p className="text-sm leading-7 text-slate-300">
              Only authenticated users can contact through the platform. If reCAPTCHA is configured, the contact flow will verify the request before it is stored.
            </p>
            <input
              value={subject}
              onChange={(event) => setSubject(event.target.value)}
              placeholder="Subject"
              className="w-full rounded-[1.5rem] border border-white/10 bg-slate-950/50 px-4 py-3 text-sm text-white outline-none"
            />
            <textarea
              value={content}
              onChange={(event) => setContent(event.target.value)}
              placeholder="Write your message here."
              className="min-h-40 w-full rounded-[1.5rem] border border-white/10 bg-slate-950/50 px-4 py-4 text-sm text-white outline-none"
            />
            {session.recaptcha_enabled ? (
              <RecaptchaCheckbox
                siteKey={session.recaptcha_site_key}
                onTokenChange={setRecaptchaToken}
              />
            ) : null}
            {status ? (
              <div className="rounded-[1.5rem] border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200">
                {status}
              </div>
            ) : null}
            <div className="flex flex-col gap-3 sm:flex-row">
              <button
                type="button"
                disabled={isSubmitting || isLoading || !subject.trim() || !content.trim()}
                onClick={() => void submitContactThread()}
                className="flex-1"
              >
                <StarBorder as="span" className="flex w-full cursor-pointer items-center justify-center gap-3">
                  <span>{session.is_authenticated ? "Send message" : "Login with GitHub to contact"}</span>
                  <FaArrowRight />
                </StarBorder>
              </button>
              {session.is_authenticated ? (
                <a href="/inbox" className="flex-1">
                  <StarBorder as="span" color="cyan" className="flex w-full cursor-pointer items-center justify-center gap-3">
                    <span>Open inbox</span>
                  </StarBorder>
                </a>
              ) : null}
            </div>
          </div>
        </SpotlightCard>
      </div>
    </section>
  );
}
