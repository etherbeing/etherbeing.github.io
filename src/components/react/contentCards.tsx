import ferris from "@/assets/ferris.png";
import SpotlightCard from "./SpotlightCard";
import { oklchGradient } from "@/lib/utils";
import type { BlogEntry, Project } from "./contentTypes";

export function ProjectCard({
  project,
  background,
}: {
  project: Project;
  background?: string;
}) {
  const secondaryLanguages = project.languages.filter(
    (language) => language !== project.language,
  );

  return (
    <SpotlightCard
      style={background ? { backgroundColor: background } : undefined}
      spotlightColor="rgba(0, 229, 255, 0.2)"
    >
      <a
        className="p-4 flex flex-col gap-5 h-full"
        href={project.html_url || "#"}
        target={project.html_url ? "_blank" : undefined}
      >
        <div className="flex flex-col gap-1 justify-between">
          <span>{project.name}</span>
          {project.description ? (
            <small className="text-gray-400">
              {project.description.slice(0, 150)}
              {project.description.length > 150 ? "..." : ""}
            </small>
          ) : null}
        </div>
        <div className="flex flex-wrap gap-2 text-xs">
          {project.language ? (
            <span className="rounded-full border border-cyan-300/60 bg-cyan-400/10 px-3 py-1 font-semibold text-cyan-100">
              Main: {project.language}
            </span>
          ) : null}
          {secondaryLanguages.map((language) => (
            <span
              key={language}
              className="rounded-full border border-white/15 bg-white/5 px-3 py-1 text-gray-300"
            >
              {language}
            </span>
          ))}
        </div>
        <div className="flex justify-between flex-row text-sm mt-auto">
          <span>{project.languages.length || 0} languages</span>
          <span>
            {project.created_at
              ? new Date(project.created_at).toDateString()
              : "No date"}
          </span>
        </div>
      </a>
    </SpotlightCard>
  );
}

export function BlogCard({
  post,
}: {
  post: BlogEntry;
  index: number;
}) {
  const imageUrl = post.image_url || ferris.src;

  return (
    <a href={`/blog/entry?slug=${post.gist_id}`}>
      <SpotlightCard
        style={{
          backgroundImage: `url(${imageUrl})`,
        }}
        className="relative overflow-hidden bg-cover bg-center flex flex-col justify-end shadow hover:shadow-2xl cursor-pointer aspect-square p-4! rounded-lg bg-gray-800 hover:bg-gray-700 transition"
      >
        <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/55 to-black/10" />
        <div className="relative z-10 flex h-full flex-col justify-between rounded-xl border border-white/10 bg-black/25 p-4 backdrop-blur-[2px]">
          <span className="w-full flex justify-start text-sm text-gray-100">
            {post.created_at ? new Date(post.created_at).toDateString() : "Draft"}
          </span>
          <span className="w-full flex justify-end text-right font-semibold text-white">
            {post.description || "Open entry"}
          </span>
        </div>
      </SpotlightCard>
    </a>
  );
}

export function projectGradient(index: number, total: number) {
  return oklchGradient(20, 10, 0.025, 330, index, total);
}
