import { FormEvent, useEffect, useState } from "react"
import { useGithubSession } from "./useGithubSession";

interface CommentType {
    username: string
    content: string
    date: string
}

export function CommentPanel({ comment }: { comment: CommentType }) {
    return (
        <div className="cursor-default shadow transition-all hover:bg-gray-600 hover:shadow-lg rounded p-5 gap-3 flex flex-col">
            <div className="text-justify">
                {comment.content}
            </div>
            <div className="w-full flex gap-3 justify-end">
                <small>
                    @{comment.username}
                </small>
                <small>
                    {new Date(comment.date).toDateString()}
                </small>
            </div>
        </div>
    )
}
export default function CommentSection({ gist_id, gist_url }: { gist_id: string, gist_url: string }) { // NOTE To do this first you'd need to implement github authentication with permission to write comment on gists as that is how the user is going to be authenticated in our system
    const apiUrl = import.meta.env.PUBLIC_API_URL;
    const [comments, setComments] = useState<Array<CommentType>>([]);
    const [draft, setDraft] = useState("");
    const [error, setError] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);
    const { session, login, refreshSession } = useGithubSession(apiUrl);

    async function loadComments() {
        const response = await fetch(`${apiUrl}/api/gist/${gist_id}/comments/`, {
            credentials: "include",
        });
        setComments(await response.json());
    }

    useEffect(() => {
        loadComments().catch(() => {
            setComments([]);
        })
    }, [gist_id])

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        setError("");
        setIsSubmitting(true);
        try {
            const activeSession = session.csrf_token ? session : await refreshSession();
            const response = await fetch(`${apiUrl}/api/gist/${gist_id}/comments/`, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": activeSession.csrf_token,
                },
                body: JSON.stringify({ content: draft }),
            });
            if (!response.ok) {
                throw new Error("There was a problem publishing your comment.");
            }
            setDraft("");
            await loadComments();
        } catch (err) {
            console.error(err);
            setError("There was a problem publishing your comment.");
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <section className="not-prose rounded-[28px] border border-white/10 bg-slate-950/45 p-6 shadow-2xl shadow-black/30 backdrop-blur-xl">
            <h2 className="text-2xl font-bold cursor-default mb-3">Comments</h2>
            <div className="flex flex-col gap-4">
                {comments.length ? (
                    comments.map((comment, index) => <CommentPanel key={index} comment={comment} />)
                ) : (
                    <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-slate-300">
                        No comments for the current post yet. Be the first one to leave feedback.
                    </div>
                )}
            </div>
            <div className="mt-6 rounded-2xl border border-cyan-200/10 bg-cyan-200/5 p-4">
                {session.is_authenticated ? (
                    session.can_comment_on_gists ? (
                    <form className="flex flex-col gap-3" onSubmit={(event) => void handleSubmit(event)}>
                        <div className="text-sm text-cyan-50">
                            Commenting as <strong>@{session.github_login || session.username}</strong>. Your comment will be posted to the real GitHub gist.
                        </div>
                        <textarea
                            value={draft}
                            onChange={(event) => setDraft(event.target.value)}
                            placeholder="Share your thoughts about this post..."
                            className="min-h-32 rounded-2xl border border-white/12 bg-slate-950/80 px-4 py-3 text-sm text-white outline-none transition focus:border-cyan-300/60"
                            required
                        />
                        {error ? (
                            <div className="rounded-xl border border-red-400/20 bg-red-400/10 px-4 py-3 text-sm text-red-100">
                                {error}
                            </div>
                        ) : null}
                        <div className="flex flex-wrap items-center gap-3">
                            <button
                                type="submit"
                                disabled={isSubmitting || !draft.trim()}
                                className="rounded-full border border-cyan-300/30 bg-cyan-300/10 px-5 py-2 text-sm font-semibold text-cyan-100 transition hover:bg-cyan-300/20 disabled:opacity-50"
                            >
                                {isSubmitting ? "Publishing..." : "Publish comment"}
                            </button>
                            <a href={gist_url} className="text-sm text-slate-300 underline underline-offset-4">
                                Open original gist
                            </a>
                        </div>
                    </form>
                    ) : (
                    <div className="flex flex-col gap-3">
                        <p className="m-0 text-sm text-slate-300">
                            You are signed in, but gist permission is still needed before you can comment on this admin-owned gist.
                        </p>
                        <div className="flex flex-wrap items-center gap-3">
                            <button
                                type="button"
                                onClick={() => login(`${location.pathname}${location.search}${location.hash}`, "comment")}
                                className="rounded-full border border-cyan-300/30 bg-cyan-300/10 px-5 py-2 text-sm font-semibold text-cyan-100 transition hover:bg-cyan-300/20"
                            >
                                Enable gist comments
                            </button>
                            <a href={gist_url} className="text-sm text-slate-300 underline underline-offset-4">
                                Open original gist
                            </a>
                        </div>
                    </div>
                    )
                ) : (
                    <div className="flex flex-col gap-3">
                        <p className="m-0 text-sm text-slate-300">
                            Log in with GitHub to comment directly on the real gist with your own account.
                        </p>
                        <div className="flex flex-wrap items-center gap-3">
                            <button
                                type="button"
                                onClick={() => login(`${location.pathname}${location.search}${location.hash}`, "comment")}
                                className="rounded-full border border-cyan-300/30 bg-cyan-300/10 px-5 py-2 text-sm font-semibold text-cyan-100 transition hover:bg-cyan-300/20"
                            >
                                Login with GitHub
                            </button>
                            <a href={gist_url} className="text-sm text-slate-300 underline underline-offset-4">
                                Comment on GitHub instead
                            </a>
                        </div>
                    </div>
                )}
            </div>
        </section>
    )
}
