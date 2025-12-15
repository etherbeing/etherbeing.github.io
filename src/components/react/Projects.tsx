import { useEffect, useState } from "react";

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
        .filter((repo) => {
          return repo["description"] && repo["description"].length > 0;
        })
        .map((repo, index) => (
          <a
            key={index}
            className="p-4 rounded-lg bg-gray-800 hover:bg-gray-700 transition flex flex-col gap-5"
            href={repo.html_url}
            target="_blank"
          >
            <span className="cursor-default">{repo.name}</span>
            <div className="cursor-default flex justify-between flex-row text-sm">
              <span>{repo.language}</span>
              <span>{new Date(repo.created_at).toDateString()}</span>
            </div>
          </a>
        ))}
    </section>
  );
}
