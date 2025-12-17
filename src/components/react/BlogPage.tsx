import { marked } from "marked";
import insane from "insane";
import { useEffect, useMemo, useState } from "react";
import CommentSection from "./CommentSection";

interface Gist {
    content: string
    html_url: string
}

export default function BlogPage({ apiUrl }: { apiUrl: string }) {
    const [content, setContent] = useState<string>("");
    const [gist, setGist] = useState<Gist>()
    const slug = useMemo(() => {
        return new URL(location.href).searchParams.get("slug")
    }, [])
    useEffect(() => {
        fetch(`${apiUrl}/api/gist/${slug}/`).then(async r => {
            const t: Gist = await r.json()
            setGist(t)
            setContent(insane(
                await marked.parse(t["content"] || "Not found"),
            ));
        }).catch((err) => {
            console.error(err)
            setContent("There was a problem with the loading of the content")
        })
    }, [])
    return (
        <div className="prose prose-invert max-w-none py-20 px-4 flex flex-col gap-20">
            <article dangerouslySetInnerHTML={{ __html: content }} />
            {gist && slug ? (
                <CommentSection gist_id={slug} gist_url={gist.html_url} />
            ) : null}
        </div>
    )
}