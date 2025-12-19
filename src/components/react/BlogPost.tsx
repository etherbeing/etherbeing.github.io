import { useEffect, useState } from "react";
import SpotlightCard from "./SpotlightCard";
import GlowingHeader from "./GlowingHeader";

export default function Blog({ apiUrl }: { apiUrl: string }) {
  const [posts, setPosts] = useState<
    Array<{
      id: string;
      gist_id: string;
      html_url: string;
      description: string;
      created_at: string;
    }>
  >([]);
  const [justification, setJustification] = useState<
    "justify-start" | "justify-center"
  >("justify-start");
  useEffect(() => {
    fetch(`${apiUrl}/api/gists/`).then(async (response) => {
      if (response.ok) {
        setPosts(await response.json());
        if (posts.length % 3 === 1) {
          setJustification("justify-center");
        }
      }
    });
  }, []);

  return (
    <section className="py-20 space-y-4">
      <GlowingHeader>Blog</GlowingHeader>

      <div className={`grid grid-cols-1 md:grid-cols-3 ${justification}`}>
        {posts.map((post, index) => {
          return (
            <a
              key={index}
              href={`/blog/entry?slug=${post["gist_id"]}`}
              target="_blank"
            >
              <SpotlightCard
                style={{
                  backgroundImage: `url(https://picsum.photos/id/${index}/200)`,
                }}
                className={`bg-cover flex flex-col justify-between shadow hover:shadow-2xl cursor-pointer aspect-square p-4! rounded-lg bg-gray-800 hover:bg-gray-700 transition`}
              >
                <span className="w-full flex justify-start">
                  {new Date(post["created_at"]).toDateString()}
                </span>
                <span className="w-full flex justify-end">
                  {post["description"]}
                </span>
              </SpotlightCard>
            </a>
          );
        })}
      </div>
    </section>
  );
}
