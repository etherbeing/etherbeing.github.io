import { useEffect, useState } from "react"

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
    const [comments, setComments] = useState<Array<CommentType>>([]);
    useEffect(() => {
        fetch(`${import.meta.env.PUBLIC_API_URL}/api/${gist_id}/comments/`).then(async (res) => {
            setComments(await res.json())
        })
    }, [])
    return (
        <section>
            <h2 className="text-2xl font-bold cursor-default mb-3">Comments</h2>
            {comments.length ? (
                comments.map((comment, index) => <CommentPanel key={index} comment={comment} />)
            ) : (
                "No comments for the current post, be the first one in comment"
            )}
            <div className="py-5 cursor-default text-center text-sm">
                Our comments are currently disabled, still you can let us know your ideas through this post's official gist at <a href={gist_url}>here</a>
            </div>
        </section>
    )
}