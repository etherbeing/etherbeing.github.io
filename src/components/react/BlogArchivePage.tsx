import { useEffect, useMemo, useState } from "react";

import GlowingHeader from "./GlowingHeader";
import ShinyText from "./ShinyText";
import SpotlightCard from "./SpotlightCard";
import { BlogCard } from "./contentCards";
import type { BlogEntry } from "./contentTypes";

export default function BlogArchivePage({ apiUrl }: { apiUrl: string }) {
  const [posts, setPosts] = useState<BlogEntry[]>([]);
  const [query, setQuery] = useState("");

  useEffect(() => {
    fetch(`${apiUrl}/api/gists/`).then(async (response) => {
      if (response.ok) {
        setPosts(await response.json());
      }
    });
  }, [apiUrl]);

  const filteredPosts = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    if (!normalized) {
      return posts;
    }
    return posts.filter((post) =>
      [post.description, post.gist_id, post.content]
        .filter(Boolean)
        .some((value) => value!.toLowerCase().includes(normalized)),
    );
  }, [posts, query]);

  return (
    <section className="pt-40 pb-20 space-y-8">
      <div className="space-y-4 text-center">
        <GlowingHeader>Blog Archive</GlowingHeader>
        <p className="max-w-2xl mx-auto text-gray-400">
          <ShinyText
            text="Every public GitHub gist is treated as a blog post here. Search by topic, description, or gist id."
            disabled={false}
            speed={4}
          />
        </p>
      </div>

      <SpotlightCard className="bg-transparent backdrop-blur-2xl">
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          type="search"
          placeholder="Search blog posts..."
          className="w-full bg-transparent outline-none text-lg placeholder:text-gray-500"
        />
      </SpotlightCard>

      {filteredPosts.length ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {filteredPosts.map((post, index) => (
            <BlogCard key={post.gist_id} post={post} index={index} />
          ))}
        </div>
      ) : (
        <SpotlightCard className="bg-transparent backdrop-blur-2xl">
          No gists matched your search.
        </SpotlightCard>
      )}
    </section>
  );
}
