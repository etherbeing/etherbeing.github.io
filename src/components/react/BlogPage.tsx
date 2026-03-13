import ferris from "@/assets/ferris.png";
import { marked } from "marked";
import insane from "insane";
import { useEffect, useMemo, useState } from "react";
import CommentSection from "./CommentSection";

interface Gist {
  content: string;
  html_url: string;
  image_url?: string;
  description?: string | null;
  created_at?: string | null;
}

export default function BlogPage({ apiUrl }: { apiUrl: string }) {
  const [content, setContent] = useState<string>("");
  const [gist, setGist] = useState<Gist>();
  const [error, setError] = useState<string>("");
  const slug = useMemo(() => {
    return new URL(location.href).searchParams.get("slug");
  }, []);
  useEffect(() => {
    if (!slug) {
      setError("No blog post slug was provided.");
      return;
    }

    fetch(`${apiUrl}/api/gist/${slug}/`)
      .then(async (r) => {
        if (!r.ok) {
          throw new Error("There was a problem loading the selected blog post.");
        }
        const t: Gist = await r.json();
        setGist(t);
        setContent(insane(await marked.parse(t["content"] || "Not found")));
      })
      .catch((err) => {
        console.error(err);
        setError("There was a problem with the loading of the content");
      });
  }, [apiUrl, slug]);

  if (error) {
    return (
      <div className="pt-40 px-4">
        <div className="rounded-3xl border border-red-400/20 bg-red-400/10 p-6 text-red-100">
          {error}
        </div>
      </div>
    );
  }

  if (!gist) {
    return (
      <div className="pt-40 px-4">
        <div className="rounded-3xl border border-white/10 bg-white/5 p-6 text-gray-300">
          Loading blog post...
        </div>
      </div>
    );
  }

  return (
    <div className="prose prose-invert max-w-none pt-40 px-4 flex flex-col gap-20">
      <header
        className="not-prose relative min-h-80 overflow-hidden rounded-3xl border border-white/10 bg-cover bg-center"
        style={{ backgroundImage: `url(${gist.image_url || ferris.src})` }}
      >
        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/75 to-black/20" />
        <div className="relative z-10 flex h-full min-h-80 flex-col justify-end gap-3 p-8">
          <p className="text-sm uppercase tracking-[0.25em] text-cyan-200">Blog Post</p>
          <h1 className="m-0 text-3xl font-bold text-white">
            {gist.description || "Untitled gist post"}
          </h1>
          {gist.created_at ? (
            <p className="m-0 text-sm text-gray-300">
              {new Date(gist.created_at).toDateString()}
            </p>
          ) : null}
        </div>
      </header>
      <article dangerouslySetInnerHTML={{ __html: content }} />
      {gist && slug ? (
        <CommentSection gist_id={slug} gist_url={gist.html_url} />
      ) : null}
    </div>
  );
}
