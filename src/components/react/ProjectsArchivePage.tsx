import { useEffect, useMemo, useState } from "react";
import {
  SiAstro,
  SiC,
  SiCplusplus,
  SiCss3,
  SiDart,
  SiDocker,
  SiGo,
  SiHtml5,
  SiJavascript,
  SiJsonwebtokens,
  SiJupyter,
  SiKotlin,
  SiLua,
  SiPhp,
  SiPython,
  SiReact,
  SiRuby,
  SiRust,
  SiShell,
  SiSwift,
  SiSvelte,
  SiTypescript,
} from "react-icons/si";
import { FaCode } from "react-icons/fa";
import type { IconType } from "react-icons";

import GlowingHeader from "./GlowingHeader";
import ShinyText from "./ShinyText";
import SpotlightCard from "./SpotlightCard";
import { ProjectCard, projectGradient } from "./contentCards";
import type { Project } from "./contentTypes";

const languageIcons: Record<string, IconType> = {
  Astro: SiAstro,
  C: SiC,
  "C++": SiCplusplus,
  CSS: SiCss3,
  Dart: SiDart,
  Dockerfile: SiDocker,
  Go: SiGo,
  HTML: SiHtml5,
  JavaScript: SiJavascript,
  Jupyter: SiJupyter,
  Kotlin: SiKotlin,
  Lua: SiLua,
  PHP: SiPhp,
  Python: SiPython,
  React: SiReact,
  Ruby: SiRuby,
  Rust: SiRust,
  Shell: SiShell,
  Swift: SiSwift,
  Svelte: SiSvelte,
  TypeScript: SiTypescript,
  JSON: SiJsonwebtokens,
};

export default function ProjectsArchivePage({ apiUrl }: { apiUrl: string }) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [query, setQuery] = useState("");
  const [selectedLanguage, setSelectedLanguage] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${apiUrl}/api/projects/`).then(async (response) => {
      if (response.ok) {
        setProjects(await response.json());
      }
    });
  }, [apiUrl]);

  const filteredProjects = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    return projects.filter((project) => {
      const matchesQuery =
        !normalized ||
        [project.name, project.description, project.language, ...project.languages]
          .filter(Boolean)
          .some((value) => value!.toLowerCase().includes(normalized));
      const matchesLanguage =
        !selectedLanguage || project.languages.includes(selectedLanguage);
      return matchesQuery && matchesLanguage;
    });
  }, [projects, query, selectedLanguage]);

  const languageCards = useMemo(() => {
    const counts = new Map<string, number>();
    for (const project of projects) {
      for (const language of project.languages.length ? project.languages : [project.language || "Unknown"]) {
        counts.set(language, (counts.get(language) || 0) + 1);
      }
    }
    return Array.from(counts.entries())
      .map(([language, count]) => ({ language, count }))
      .sort((left, right) => right.count - left.count || left.language.localeCompare(right.language));
  }, [projects]);

  return (
    <section className="pt-40 pb-20 space-y-8">
      <div className="space-y-4 text-center">
        <GlowingHeader>Project Archive</GlowingHeader>
        <p className="max-w-2xl mx-auto text-gray-400">
          <ShinyText
            text="Browse the public GitHub repositories backing the work showcased on the homepage."
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
          placeholder="Search projects..."
          className="w-full bg-transparent outline-none text-lg placeholder:text-gray-500"
        />
      </SpotlightCard>

      <div className="space-y-4">
        <div className="flex items-center justify-between gap-3">
          <GlowingHeader>Languages</GlowingHeader>
          {selectedLanguage ? (
            <button
              type="button"
              className="text-sm text-cyan-200 underline underline-offset-4"
              onClick={() => setSelectedLanguage(null)}
            >
              Clear filter
            </button>
          ) : null}
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {languageCards.map(({ language, count }, index) => {
            const Icon = languageIcons[language] || FaCode;
            const isActive = selectedLanguage === language;
            return (
              <button
                type="button"
                key={language}
                onClick={() => setSelectedLanguage(language)}
                className="text-left"
              >
                <SpotlightCard
                  className={`h-full bg-transparent backdrop-blur-2xl cursor-pointer transition ${isActive ? "ring-2 ring-cyan-300" : ""}`}
                  style={{ backgroundColor: projectGradient(index, Math.max(languageCards.length, 1)) }}
                >
                  <div className="flex h-full flex-col justify-between gap-5">
                    <Icon className="text-3xl text-cyan-100" />
                    <div>
                      <div className="font-semibold">{language}</div>
                      <div className="text-sm text-gray-400">{count} projects</div>
                    </div>
                  </div>
                </SpotlightCard>
              </button>
            );
          })}
        </div>
      </div>

      {filteredProjects.length ? (
        <div className="grid grid-cols-1 gap-4">
          {filteredProjects.map((project, index) => (
            <ProjectCard
              key={project.github_id}
              project={project}
              background={projectGradient(index, filteredProjects.length)}
            />
          ))}
        </div>
      ) : (
        <SpotlightCard className="bg-transparent backdrop-blur-2xl">
          No projects matched your search.
        </SpotlightCard>
      )}
    </section>
  );
}
