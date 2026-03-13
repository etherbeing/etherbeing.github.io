import { type ReactNode, useEffect, useState } from "react";
import {
  FaDiscord,
  FaEnvelope,
  FaGithub,
  FaInstagram,
  FaReddit,
  FaTelegram,
} from "react-icons/fa6";
import { FaBug, FaCoffee } from "react-icons/fa";
import { SiBugcrowd, SiHackerone, SiTryhackme, SiX } from "react-icons/si";

import alterEgo from "@/assets/alter-ego.png";
import ferris from "@/assets/ferris.png";
import kali from "@/assets/kali.png";
import metasploit from "@/assets/metasploit.png";
import photo from "@/assets/photo.jpg";
import python from "@/assets/python.svg";
import reactLogo from "@/assets/react.svg";
import rust from "@/assets/rust.png";
import tensorflow from "@/assets/tensorflow.png";
import AlterEgoCard from "./AlterEgoCard";
import DecryptedText from "./DecryptedText";
import GlowingHeader from "./GlowingHeader";
import GlowingText from "./GlowingText";
import ShinyText from "./ShinyText";
import SpotlightCard from "./SpotlightCard";
import StarBorder from "./StarBorder";
import TextType from "./TextType";
import { BlogCard, ProjectCard, projectGradient } from "./contentCards";
import type { BlogEntry, Project } from "./contentTypes";

type AboutHighlight = {
  title: string;
  content: string;
  column: "left" | "right";
  sort_order: number;
};

type Skill = {
  name: string;
  image_key: string;
  sort_order: number;
};

type Service = {
  title: string;
  starting_price: number;
  description: string;
  skills: string[];
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

const skillImages: Record<string, string> = {
  kali: kali.src,
  rust: rust.src,
  metasploit: metasploit.src,
  tensorflow: tensorflow.src,
  python: python.src,
  react: reactLogo.src,
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
        <a href={content.hero_cta_url} className="z-10 mt-10">
          <StarBorder as={"button"} className="cursor-pointer" color="magenta" speed="5s">
            {content.hero_cta_label}
          </StarBorder>
        </a>
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
            <li className="h-[300px] md:h-[275px] mx-auto" key={skill.name}>
              <SpotlightCard
                spotlightColor="rgba(0, 229, 255, 0.2)"
                className="bg-transparent backdrop-blur-2xl flex aspect-square justify-center items-center flex-col gap-3 h-full cursor-default select-none text-sm uppercase text-center font-bold"
              >
                <img
                  draggable="false"
                  className="h-20 w-auto select-none"
                  src={skillImages[skill.image_key]}
                  alt={skill.name}
                />
                {skill.name}
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
              className="mx-auto h-[300px] aspect-square flex flex-col justify-between px-auto py-5 cursor-default"
            >
              <div className="flex flex-col justify-between h-full gap-3">
                <GlowingText className="my-auto">
                  <h2 className="mx-auto text-xl font-bold text-center">{service.title}</h2>
                </GlowingText>
                <span className="text-sm text-gray-500">{service.description}</span>
              </div>
              <ul className="flex flex-col justify-center h-full items-center w-full my-5 font-bold text-sm">
                {service.skills.map((serviceSkill) => (
                  <li className="w-full flex justify-between items-center" key={serviceSkill}>
                    <span className="text-green-200">+</span>
                    {serviceSkill}
                  </li>
                ))}
              </ul>
              <span className="flex justify-end w-full text-sm">From {service.starting_price} USD</span>
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
