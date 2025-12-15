import { marked } from "marked";
import insane from "insane";
import { useEffect, useMemo, useState } from "react";

export default function BlogPage({ apiUrl }: { apiUrl: string }) {
    const [content, setContent] = useState<string>("");
    const slug = useMemo(() => {
        return new URL(location.href).searchParams.get("slug")
    }, [])
    useEffect(() => {

        console.log(import.meta.env)
        console.log(import.meta.env.DEV)
        console.log(import.meta.env.MODE)
        console.log(import.meta.env.PROD)
        fetch(`${apiUrl}/api/gist/${slug}/`).then(async r => {
            setContent(insane(
                await marked.parse((await r.json())["content"] || "Not found"),
            ));
        }).catch((err) => {
            console.error(err)
            setContent("There was a problem with the loading of the content")
        })
    }, [])
    return (
        <div className="prose prose-invert max-w-none py-20 px-4">
            <article dangerouslySetInnerHTML={{ __html: content }} />
        </div>
    )
}