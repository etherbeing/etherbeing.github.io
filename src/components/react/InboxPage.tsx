import { useEffect, useState } from "react";
import { FaArrowRight } from "react-icons/fa6";

import GlowingHeader from "./GlowingHeader";
import RecaptchaCheckbox from "./RecaptchaCheckbox";
import SpotlightCard from "./SpotlightCard";
import StarBorder from "./StarBorder";
import { useGithubSession } from "./useGithubSession";

type ContactMessage = {
  id: number;
  sender_username: string;
  is_staff_reply: boolean;
  content: string;
  created_at: string;
};

type ContactThread = {
  id: number;
  subject: string;
  status: string;
  created_at: string;
  updated_at: string;
  last_message_at: string;
  messages: ContactMessage[];
};

export default function InboxPage({ apiUrl }: { apiUrl: string }) {
  const { session, isLoading, login, refreshSession } = useGithubSession(apiUrl);
  const [threads, setThreads] = useState<ContactThread[]>([]);
  const [activeThreadId, setActiveThreadId] = useState<number | null>(null);
  const [reply, setReply] = useState("");
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [recaptchaToken, setRecaptchaToken] = useState("");

  useEffect(() => {
    if (isLoading) return;
    if (!session.is_authenticated) return;

    fetch(`${apiUrl}/api/site/contact/threads/`, {
      credentials: "include",
    })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("Unable to load inbox.");
        }
        const payload: ContactThread[] = await response.json();
        setThreads(payload);
        setActiveThreadId((current) => current ?? payload[0]?.id ?? null);
      })
      .catch((loadError: Error) => {
        console.error(loadError);
        setError("We could not load your inbox right now.");
      });
  }, [apiUrl, isLoading, session.is_authenticated]);

  const activeThread = threads.find((thread) => thread.id === activeThreadId) ?? null;

  async function sendReply() {
    if (!activeThread) return;
    const activeSession = session.csrf_token ? session : await refreshSession();
    if (!activeSession.is_authenticated) {
      login("/inbox");
      return;
    }

    setIsSubmitting(true);
    setStatus("");
    setError("");
    try {
      if (activeSession.recaptcha_enabled && !recaptchaToken) {
        setError("Please complete the reCAPTCHA checkbox before sending your reply.");
        setIsSubmitting(false);
        return;
      }
      const response = await fetch(`${apiUrl}/api/site/contact/threads/${activeThread.id}/messages/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": activeSession.csrf_token,
        },
        body: JSON.stringify({
          content: reply,
          recaptcha_token: recaptchaToken,
        }),
      });
      if (!response.ok) {
        throw new Error("Unable to send reply.");
      }
      const payload: ContactThread = await response.json();
      setThreads((current) =>
        [payload, ...current.filter((thread) => thread.id !== payload.id)],
      );
      setActiveThreadId(payload.id);
      setReply("");
      setStatus("Reply sent.");
    } catch (replyError) {
      console.error(replyError);
      setError("Your reply could not be sent right now.");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (isLoading) {
    return <section className="py-32"><SpotlightCard>Loading inbox...</SpotlightCard></section>;
  }

  if (!session.is_authenticated) {
    return (
      <section className="py-24 space-y-6">
        <GlowingHeader>Inbox</GlowingHeader>
        <SpotlightCard className="space-y-4 bg-transparent backdrop-blur-2xl">
          <p className="text-slate-300">
            Login with GitHub to access your private inbox and continue platform conversations.
          </p>
          <button type="button" onClick={() => login("/inbox")} className="w-full sm:w-auto">
            <StarBorder as="span" className="flex cursor-pointer items-center justify-center gap-3">
              <span>Login with GitHub</span>
              <FaArrowRight />
            </StarBorder>
          </button>
        </SpotlightCard>
      </section>
    );
  }

  return (
    <section className="py-24 space-y-8">
      <div className="space-y-4 text-center">
        <p className="text-xs uppercase tracking-[0.28em] text-cyan-200/75">Private Inbox</p>
        <GlowingHeader>Platform conversations</GlowingHeader>
      </div>
      <div className="grid gap-6 lg:grid-cols-[0.8fr_1.2fr]">
        <SpotlightCard className="space-y-3 bg-transparent backdrop-blur-2xl">
          {threads.length ? (
            threads.map((thread) => (
              <button
                type="button"
                key={thread.id}
                onClick={() => setActiveThreadId(thread.id)}
                className={`w-full rounded-[1.4rem] border px-4 py-4 text-left transition ${
                  activeThreadId === thread.id
                    ? "border-cyan-300/30 bg-cyan-300/10"
                    : "border-white/10 bg-white/5"
                }`}
              >
                <div className="flex items-center justify-between gap-3">
                  <strong className="text-white">{thread.subject}</strong>
                  <span className="text-xs uppercase tracking-[0.2em] text-slate-400">{thread.status}</span>
                </div>
                <p className="mt-2 line-clamp-2 text-sm text-slate-300">
                  {thread.messages.at(-1)?.content || "No messages yet."}
                </p>
              </button>
            ))
          ) : (
            <p className="text-sm text-slate-300">No conversations yet. Send a message from the contact section.</p>
          )}
        </SpotlightCard>

        <SpotlightCard className="space-y-5 bg-transparent backdrop-blur-2xl">
          {activeThread ? (
            <>
              <div className="border-b border-white/10 pb-4">
                <h2 className="text-2xl font-semibold text-white">{activeThread.subject}</h2>
                <p className="mt-2 text-sm text-slate-400">Status: {activeThread.status}</p>
              </div>
              <div className="max-h-[28rem] space-y-4 overflow-y-auto pr-2">
                {activeThread.messages.map((message) => (
                  <div
                    key={message.id}
                    className={`rounded-[1.5rem] border px-4 py-4 ${
                      message.is_staff_reply
                        ? "border-fuchsia-300/20 bg-fuchsia-400/10"
                        : "border-cyan-300/20 bg-cyan-400/10"
                    }`}
                  >
                    <div className="flex items-center justify-between gap-3">
                      <strong className="text-white">
                        {message.is_staff_reply ? "etherbeing reply" : message.sender_username}
                      </strong>
                      <span className="text-xs text-slate-300">
                        {new Date(message.created_at).toLocaleString()}
                      </span>
                    </div>
                    <p className="mt-3 whitespace-pre-wrap text-sm leading-7 text-slate-100">
                      {message.content}
                    </p>
                  </div>
                ))}
              </div>
              <div className="space-y-3 border-t border-white/10 pt-4">
                <textarea
                  value={reply}
                  onChange={(event) => setReply(event.target.value)}
                  placeholder="Write a reply."
                  className="min-h-32 w-full rounded-[1.5rem] border border-white/10 bg-slate-950/50 px-4 py-4 text-sm text-white outline-none"
                />
                {session.recaptcha_enabled ? (
                  <RecaptchaCheckbox
                    siteKey={session.recaptcha_site_key}
                    onTokenChange={setRecaptchaToken}
                  />
                ) : null}
                {status ? <div className="text-sm text-emerald-200">{status}</div> : null}
                {error ? <div className="text-sm text-red-200">{error}</div> : null}
                <button
                  type="button"
                  onClick={() => void sendReply()}
                  disabled={isSubmitting || !reply.trim()}
                  className="w-full"
                >
                  <StarBorder as="span" className="flex w-full cursor-pointer items-center justify-center gap-3">
                    <span>Send reply</span>
                    <FaArrowRight />
                  </StarBorder>
                </button>
              </div>
            </>
          ) : (
            <p className="text-sm text-slate-300">Choose a conversation from the left to read it here.</p>
          )}
        </SpotlightCard>
      </div>
    </section>
  );
}
