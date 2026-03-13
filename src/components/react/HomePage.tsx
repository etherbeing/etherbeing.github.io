import { type ReactNode, useEffect, useState } from "react";
import {
  FaDiscord,
  FaEnvelope,
  FaGithub,
  FaInstagram,
  FaPaypal,
  FaReddit,
  FaTelegram,
} from "react-icons/fa6";
import { FaBug, FaCoffee } from "react-icons/fa";
import { SiBugcrowd, SiHackerone, SiTryhackme, SiX } from "react-icons/si";

import alterEgo from "@/assets/alter-ego.png";
import ferris from "@/assets/ferris.png";
import photo from "@/assets/photo.jpg";
import AlterEgoCard from "./AlterEgoCard";
import DecryptedText from "./DecryptedText";
import GlowingHeader from "./GlowingHeader";
import GlowingText from "./GlowingText";
import ShinyText from "./ShinyText";
import SpotlightCard from "./SpotlightCard";
import StarBorder from "./StarBorder";
import TextType from "./TextType";
import { BlogCard, ProjectCard, projectGradient } from "./contentCards";
import type { BlogEntry, Project, Service } from "./contentTypes";

type AboutHighlight = {
  title: string;
  content: string;
  column: "left" | "right";
  sort_order: number;
};

type Skill = {
  name: string;
  image_key: string;
  image_url: string;
  headline: string;
  description: string;
  sort_order: number;
};

type ContactLink = {
  label: string;
  url: string;
  icon: string;
  sort_order: number;
};

type ContactGroup = {
  title: string;
  sort_order: number;
  links: ContactLink[];
};

type SiteContent = {
  site_title: string;
  hero_titles: string[];
  hero_summary: string;
  hero_cta_label: string;
  hero_cta_url: string;
  about_short_bio: string;
  buy_me_a_coffee_url: string;
  contact_intro: string;
  footer_copy: string;
  footer_tagline: string;
  strategy_business_idea?: {
    blog_integrations?: string[];
    content_to_publish?: string[];
    other_services?: string[];
  };
  about_highlights: AboutHighlight[];
  skills: Skill[];
  services: Service[];
  contact_groups: ContactGroup[];
  featured_projects: Project[];
  featured_blog_entries: BlogEntry[];
};

const iconMap: Record<string, ReactNode> = {
  github: <FaGithub />,
  x: <SiX />,
  telegram: <FaTelegram />,
  instagram: <FaInstagram />,
  reddit: <FaReddit />,
  email: <FaEnvelope />,
  hackerone: <SiHackerone />,
  bugcrowd: <SiBugcrowd />,
  tryhackme: <SiTryhackme />,
  discord: <FaDiscord />,
  bug: <FaBug />,
};

function EmptyState({ message }: { message: string }) {
  return (
    <SpotlightCard className="bg-transparent backdrop-blur-2xl cursor-default select-none">
      {message}
    </SpotlightCard>
  );
}

export default function HomePage({ apiUrl }: { apiUrl: string }) {
  const [content, setContent] = useState<SiteContent | null>(null);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    fetch(`${apiUrl}/api/site/content/`)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("Unable to load site content");
        }
        const raw = await response.json();
        const data: SiteContent = {
          strategy_business_idea: {
            blog_integrations: [],
            content_to_publish: [],
            other_services: [],
            ...(raw.strategy_business_idea || {}),
          },
          ...raw,
        };
        setContent(data);
      })
      .catch((err: Error) => {
        console.error(err);
        setError("There was a problem loading the site content from the backend.");
      });
  }, [apiUrl]);

  if (error) {
    return (
      <section className="py-32">
        <EmptyState message={error} />
      </section>
    );
  }

  if (!content) {
    return (
      <section className="py-32">
        <EmptyState message="Loading site content..." />
      </section>
    );
  }

  const leftHighlights = content.about_highlights.filter(
    (highlight) => highlight.column === "left",
  );
  const rightHighlights = content.about_highlights.filter(
    (highlight) => highlight.column === "right",
  );

  return (
    <>
      <section
        id="home"
        className="relative min-h-screen flex justify-center items-center flex-col py-32 text-center select-none cursor-default"
      >
        <h1 className="z-10 text-5xl font-bold animate-fade-up">
          <TextType
            text={content.hero_titles}
            typingSpeed={75}
            pauseDuration={1500}
            showCursor={true}
            cursorCharacter="|"
          />
        </h1>
        <p className="z-10 mt-6 text-xl max-w-xl mx-auto">
          <ShinyText text={content.hero_summary} disabled={false} speed={3} />
        </p>
        <div className="z-10 mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a href={content.hero_cta_url}>
            <StarBorder as={"button"} className="cursor-pointer min-w-44" color="magenta" speed="5s">
              {content.hero_cta_label}
            </StarBorder>
          </a>
          <a
            href="https://paypal.me/etherbeing"
            target="_blank"
            rel="noreferrer"
          >
            <StarBorder
              as={"button"}
              className="cursor-pointer flex min-w-44 items-center justify-center gap-2"
              color="cyan"
            >
              <span>Donate me</span>
              <FaPaypal />
            </StarBorder>
          </a>
        </div>
      </section>

      <section id="about" className="py-20 space-y-4 md:w-[120%] md:-ml-[10%]">
        <div className="text-center animate-fade-up mb-20">
          <GlowingHeader>About</GlowingHeader>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <SpotlightCard className="text-justify select-none cursor-default bg-transparent backdrop-blur-2xl">
            {leftHighlights.map((highlight) => (
              <div className="flex flex-col text-justify gap-1 mt-5" key={highlight.title}>
                <GlowingText>
                  <h3 className="text-xl font-bold">{highlight.title}</h3>
                </GlowingText>
                {highlight.content}
              </div>
            ))}
          </SpotlightCard>
          <SpotlightCard
            className="flex justify-center items-center p-0 bg-size-[90%] bg-center bg-no-repeat bg-transparent border-none px-10 min-h-50"
            style={{ backgroundImage: `url(${ferris.src})` }}
          />
          <SpotlightCard className="text-justify select-none cursor-default bg-transparent backdrop-blur-2xl">
            {rightHighlights.map((highlight) => (
              <div className="flex flex-col text-justify gap-1 mt-5" key={highlight.title}>
                <GlowingText>
                  <h3 className="text-xl font-bold">{highlight.title}</h3>
                </GlowingText>
                {highlight.content}
              </div>
            ))}
          </SpotlightCard>
        </div>

        <div className="flex flex-col items-center justify-center relative">
          <SpotlightCard className="flex flex-col justify-between aspect-9/16 p-0! w-75 bg-transparent backdrop-blur-2xl overflow-hidden">
            <AlterEgoCard alterSrc={alterEgo.src} baseSrc={photo.src} />
            <div className="flex flex-col my-5 px-5">
              <GlowingText>
                <span className="text-xl font-bold select-none">Short bio</span>
              </GlowingText>
              <p className="text-sm text-justify cursor-default select-none">
                <DecryptedText
                  sequential={true}
                  text={content.about_short_bio}
                  animateOn="view"
                  speed={50}
                  maxIterations={3}
                />
              </p>
              <div className="w-full flex justify-end items-end px-3 mt-5 mb-3 z-10 cursor-pointer">
                <a target="_blank" href={content.buy_me_a_coffee_url} className="w-full">
                  <StarBorder className="flex flex-row gap-3 justify-center items-center w-full">
                    <span className="font-bold text-sm">Buy me a coffee</span>
                    <FaCoffee />
                  </StarBorder>
                </a>
              </div>
            </div>
          </SpotlightCard>
        </div>
      </section>

      <section id="core-skills" className="py-20 space-y-6">
        <GlowingHeader>Core Skills</GlowingHeader>
        <ul className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {content.skills.map((skill) => (
            <li className="mx-auto w-full max-w-2xl" key={skill.name}>
              <SpotlightCard
                spotlightColor="rgba(0, 229, 255, 0.2)"
                className="flex h-full flex-col justify-between border-white/10 bg-white/[0.03] p-0 backdrop-blur-2xl cursor-default select-none"
              >
                <div className="border-b border-white/8 bg-linear-to-br from-cyan-400/14 via-slate-950/10 to-violet-400/14 px-6 py-5">
                  <div className="mb-4 flex items-center justify-between gap-4">
                    <span className="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-[0.68rem] uppercase tracking-[0.24em] text-cyan-100/85">
                      Core skill
                    </span>
                    <img
                      draggable="false"
                      className="h-14 w-auto select-none object-contain drop-shadow-[0_0_18px_rgba(125,249,255,0.24)]"
                      src={skill.image_url}
                      alt={skill.name}
                    />
                  </div>
                  <h3 className="text-left text-xl font-bold text-white">{skill.name}</h3>
                  <p className="mt-3 text-left text-xs uppercase tracking-[0.22em] text-cyan-200/80">
                    {skill.headline}
                  </p>
                </div>
                <div className="flex h-full flex-col justify-between px-6 py-5">
                  <p className="text-sm leading-7 text-slate-300">{skill.description}</p>
                  <div className="mt-6 flex items-center justify-between border-t border-white/8 pt-4 text-sm">
                    <span className="text-slate-400">Backend-driven content</span>
                    <span className="font-semibold text-cyan-200">{skill.image_key}</span>
                  </div>
                </div>
              </SpotlightCard>
            </li>
          ))}
        </ul>
      </section>

      <section id="services" className="py-20 space-y-6">
        <GlowingHeader>Services</GlowingHeader>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 md:ml-[-10%] md:w-[120%]">
          {content.services.map((service) => (
            <SpotlightCard
              key={service.title}
              spotlightColor="rgba(0, 229, 255, 0.2)"
              className="mx-auto flex min-h-[340px] w-full max-w-[23rem] flex-col border-white/10 bg-white/[0.03] p-0 backdrop-blur-2xl"
            >
              <a
                href={`/services/entry?slug=${service.slug}`}
                className="flex h-full flex-col justify-between overflow-hidden rounded-3xl"
              >
                <div className="border-b border-white/8 bg-gradient-to-br from-cyan-400/14 via-slate-950/10 to-fuchsia-400/14 px-6 py-5">
                  <div className="mb-4 flex items-start justify-between gap-4">
                    <span className="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-[0.68rem] uppercase tracking-[0.24em] text-cyan-100/85">
                      Service
                    </span>
                    <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs font-semibold text-white/90">
                      From {service.starting_price} USD
                    </span>
                  </div>
                  <GlowingText className="my-auto">
                    <h2 className="text-left text-xl font-bold text-white">{service.title}</h2>
                  </GlowingText>
                  <p className="mt-3 text-left text-xs uppercase tracking-[0.22em] text-cyan-200/80">
                    {service.headline}
                  </p>
                </div>
                <div className="flex h-full flex-col justify-between px-6 py-5">
                  <p className="text-sm leading-7 text-slate-300">{service.description}</p>
                  <ul className="mt-5 flex flex-wrap gap-2 text-sm">
                    {service.skills.slice(0, 4).map((serviceSkill) => (
                      <li
                        className="rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs font-semibold text-slate-100"
                        key={serviceSkill}
                      >
                        {serviceSkill}
                      </li>
                    ))}
                  </ul>
                  <div className="mt-6 flex items-center justify-between border-t border-white/8 pt-4 text-sm">
                    <span className="text-slate-400">
                      {service.skills.length} capability{service.skills.length === 1 ? "" : "ies"}
                    </span>
                    <span className="font-semibold text-cyan-200">View details {"->"}</span>
                  </div>
                </div>
              </a>
            </SpotlightCard>
          ))}
        </div>
      </section>

      <section id="projects" className="py-20 space-y-4">
        <GlowingHeader>Projects</GlowingHeader>
        {content.featured_projects.length ? (
          content.featured_projects.map((project, index, array) => (
            <ProjectCard
              background={projectGradient(index, array.length)}
              project={project}
              key={project.github_id}
            />
          ))
        ) : (
          <EmptyState message="No projects available yet." />
        )}
        <div className="flex justify-center pt-6">
          <a href="/projects">
            <StarBorder as={"button"} className="cursor-pointer">
              See more projects
            </StarBorder>
          </a>
        </div>
      </section>

      <section id="blog" className="py-20 space-y-4">
        <GlowingHeader>Blog</GlowingHeader>
        {content.featured_blog_entries.length ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {content.featured_blog_entries.map((entry, index) => (
              <BlogCard key={entry.gist_id} post={entry} index={index} />
            ))}
          </div>
        ) : (
          <EmptyState message="No blog entries available yet." />
        )}
        <div className="flex justify-center pt-6">
          <a href="/blog">
            <StarBorder as={"button"} className="cursor-pointer">
              See more posts
            </StarBorder>
          </a>
        </div>
      </section>

      <section id="contact" className="py-20 space-y-4 cursor-default select-none text-justify">
        <GlowingHeader>Contact</GlowingHeader>
        <SpotlightCard className="flex flex-col items-start gap-5">
          {content.contact_intro}
          {content.contact_groups.map((group) => (
            <div className="flex flex-col gap-2 w-fit" key={group.title}>
              <b className="w-full">{group.title}</b>
              <ul className="flex gap-2 flex-wrap">
                {group.links.map((link) => (
                  <li key={`${group.title}-${link.label}`}>
                    <a target="_blank" className="flex gap-1 items-center" href={link.url}>
                      {iconMap[link.icon] || null}
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </SpotlightCard>
      </section>

      <footer className="py-14 text-center text-gray-500">
        <p>
          {content.footer_copy}
          <br />
          {content.footer_tagline}
        </p>
      </footer>
    </>
  );
}
