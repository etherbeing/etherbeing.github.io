import { marked } from "marked";
import insane from "insane";
import { useEffect, useMemo, useState } from "react";

export default function BlogPage() {
    const [content, setContent] = useState<string>("");
    const slug = useMemo(() => {
        return new URL(location.href).searchParams.get("slug")
    }, [])
    useEffect(() => {
        fetch(`${import.meta.env.PUBLIC_API_URL}/api/gist/${slug}/`).then(async r => {
            setContent(insane(
                await marked.parse((await r.json())["content"] || "Not found"),
            ));
        }).catch((err) => {
            console.error(err)
            setContent("There was a problem with the loading of the content")
        })
    }, [])
    return (
        <article dangerouslySetInnerHTML={{ __html: content }} />
    )
}