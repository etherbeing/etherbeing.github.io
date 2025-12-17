import { useEffect, useState } from "react";
import ElectricBorder from "./ElectricBorder";
import SpotlightCard from "./SpotlightCard";

interface Repo {
  name: string;
  html_url: string;
  description: string | null;
  updated_at: string;
  pushed_at: string;
  created_at: string;
  language: string;
}
export default function Projects({ apiUrl }: { apiUrl: string }) {
  const [repos, setRepos] = useState<Array<Repo>>([]);
  useEffect(() => {
    fetch(`${apiUrl}/api/projects/`).then(
      async (res) => {
        if (res.ok) setRepos(await res.json())
      },
    );
  }, []);
  return (
    <section className="py-20 space-y-4">
      <h2 className="text-3xl font-bold text-green-400">Projects</h2>
      {repos.slice(0, 5)
        .sort((last_repo, repo) => {
          // sort by last updated date
          return (
            new Date(repo["pushed_at"]).getTime() -
            new Date(last_repo["pushed_at"]).getTime()
          );
        })
        .map((repo, index) => (
          <ElectricBorder
            key={index}
            color="#7df9ff"
            speed={2}
            chaos={0}
            thickness={1}
            style={{ borderRadius: 16 }}
          >
            <SpotlightCard
              spotlightColor="rgba(0, 229, 255, 0.2)">
              <a
                className="p-4 flex flex-col gap-5"
                href={repo.html_url}
                target="_blank"
              >
                <div className="flex flex-col gap-1 justify-between">
                  <span>{repo.name}</span>
                  {repo.description ? (
                    <small className="text-gray-400">{repo.description.slice(0, 150) + (repo.description.length > 150 ? "..." : "")}</small>
                  ) : null}
                </div>
                <div className="flex justify-between flex-row text-sm">
                  <span>{repo.language}</span>
                  <span>{new Date(repo.created_at).toDateString()}</span>
                </div>
              </a>
            </SpotlightCard>
          </ElectricBorder>
        ))}
    </section>
  );
}
