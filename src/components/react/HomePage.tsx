import { type CSSProperties, type ReactNode, useEffect, useState } from "react";
import Lightbox from "yet-another-react-lightbox";
import "yet-another-react-lightbox/styles.css";
import {
  FaBookOpen,
  FaBullhorn,
  FaBriefcase,
  FaChartLine,
  FaDiscord,
  FaEnvelope,
  FaGithub,
  FaGraduationCap,
  FaInstagram,
  FaPaypal,
  FaReddit,
  FaTelegram,
  FaYoutube,
} from "react-icons/fa6";
import { FaBug, FaCoffee } from "react-icons/fa";
import { SiBugcrowd, SiHackerone, SiTryhackme, SiX } from "react-icons/si";

import alterEgo from "@/assets/alter-ego.png";
import ferris from "@/assets/ferris.png";
import ContactSection from "./ContactSection";
import GlowingHeader from "./GlowingHeader";
import GlowingText from "./GlowingText";
import ShinyText from "./ShinyText";
import SpotlightCard from "./SpotlightCard";
import StarBorder from "./StarBorder";
import TextType from "./TextType";
import TradingViewAdvancedChart from "./TradingViewAdvancedChart";
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

type GalleryPhoto = {
  title: string;
  image_url: string;
  caption: string;
  sort_order: number;
};

type ContactGroup = {
  title: string;
  sort_order: number;
  links: ContactLink[];
};

type TimelineEntry = {
  year: string;
  title: string;
  place: string;
  description: string;
  tags: string[];
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
  featured_chart_symbol: string;
  featured_chart_title: string;
  strategy_business_idea?: {
    blog_integrations?: string[];
    content_to_publish?: string[];
    other_services?: string[];
  };
  about_highlights: AboutHighlight[];
  skills: Skill[];
  services: Service[];
  contact_groups: ContactGroup[];
  gallery_photos: GalleryPhoto[];
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
  tradingview: <FaChartLine />,
};

const publishedBooks = [
  {
    asin: "B0H8LL6YJB",
    title: "Building Agentic Systems for Offensive Cybersecurity",
    subtitle:
      "A theory of operational intelligence for solving complex cybersecurity benchmarks",
    authors: "Esteban Chacon, Roberto Melipillan, Houda Saadaoui, Jose Zapata",
    url: "https://www.amazon.com/dp/B0H8LL6YJB",
    coverUrl: "https://m.media-amazon.com/images/P/B0H8LL6YJB.01._SCLZZZZZZZ_SX500_.jpg",
  },
];

const opportunities = [
  {
    title: "Volunteer Testers Wanted",
    category: "Real estate agency testing",
    description:
      "We are searching for volunteer testers for our real estate agency experience. Early feedback will help shape the workflows, listings, and client-facing tools before a wider release.",
    ctaLabel: "Contact me",
    ctaUrl: "#contact",
  },
];

const youtubeChannel = {
  title: "Adversashield Technologies",
  handle: "@adversashield",
  url: "https://www.youtube.com/@adversashield",
  uploadsPlaylistId: "UUYBdBIih1vbxqDfcC77PDhg",
};

const educationTimeline: TimelineEntry[] = [
  {
    year: "2014",
    title: "Cybersecurity Foundations",
    place: "Self-directed study",
    description:
      "Started studying cybersecurity through BackTrack Linux, networking, pentesting, and scripting with Visual Basic, shell, Python, and related tooling.",
    tags: ["BackTrack", "Networking", "Pentesting", "Scripting"],
  },
  {
    year: "2017",
    title: "Cybersecurity and Programming Courses",
    place: "DESOFT, Havana",
    description:
      "Attended cybersecurity and programming courses at DESOFT, the Havana software development company.",
    tags: ["Cybersecurity", "Programming", "DESOFT"],
  },
  {
    year: "2018",
    title: "Lic. in Education for Computer Science",
    place: "University studies",
    description:
      "Began university studies focused on computer science education, strengthening pedagogy, computing fundamentals, and technical communication.",
    tags: ["Computer Science", "Education", "University"],
  },
  {
    year: "2020",
    title: "Computer Science Engineering",
    place: "CUJAE",
    description:
      "Entered engineering school for Computer Science Engineering at CUJAE, deepening software engineering, systems, and applied computing skills.",
    tags: ["Engineering", "CUJAE", "Software"],
  },
];

const professionalTimeline: TimelineEntry[] = [
  {
    year: "2020",
    title: "Founder, CTO, and Main Developer",
    place: "ODINF, Havana",
    description:
      "Started ODINF, Informatic Operations, as a private company based in Havana, leading technology direction and core product development.",
    tags: ["Founder", "CTO", "Development"],
  },
  {
    year: "2021",
    title: "CTO, DevOps, Cybersecurity, and Main Developer",
    place: "GoDjango, Florida",
    description:
      "Started GoDjango and covered a broad technical leadership surface across DevOps, cybersecurity, software architecture, and implementation.",
    tags: ["DevOps", "Cybersecurity", "Architecture"],
  },
  {
    year: "2014-Present",
    title: "Independent Engineering Practice",
    place: "Company and side projects",
    description:
      "Built projects across many programming languages and ecosystems, including Python and Rust, both independently and inside company work.",
    tags: ["Python", "Rust", "Products"],
  },
  {
    year: "2026",
    title: "CTO, Cybersecurity Specialist, and Main Developer",
    place: "Adversashield Technologies, Delaware",
    description:
      "Started Adversashield Technologies, leading cybersecurity strategy, software development, and broader technical execution.",
    tags: ["Cybersecurity", "CTO", "Delaware"],
  },
  {
    year: "2026",
    title: "CTO",
    place: "ILORA LLC, Florida",
    description:
      "Started ILORA LLC, a game development company based in Florida, serving as CTO and helping shape the studio's technical direction.",
    tags: ["Game Development", "CTO", "Florida"],
  },
];

function EmptyState({ message }: { message: string }) {
  return (
    <SpotlightCard className="bg-transparent backdrop-blur-2xl cursor-default select-none">
      {message}
    </SpotlightCard>
  );
}

function TimelineColumn({
  title,
  subtitle,
  icon,
  entries,
  tone,
}: {
  title: string;
  subtitle: string;
  icon: ReactNode;
  entries: TimelineEntry[];
  tone: "cyan" | "emerald";
}) {
  const toneClasses =
    tone === "cyan"
      ? {
        badge: "border-cyan-300/20 bg-cyan-300/10 text-cyan-100/85",
        dot: "border-cyan-200/60 bg-cyan-300 shadow-[0_0_22px_rgba(34,211,238,0.55)]",
        tag: "border-cyan-300/16 bg-cyan-300/8 text-cyan-100/80",
      }
      : {
        badge: "border-emerald-300/20 bg-emerald-300/10 text-emerald-100/85",
        dot: "border-emerald-200/60 bg-emerald-300 shadow-[0_0_22px_rgba(52,211,153,0.55)]",
        tag: "border-emerald-300/16 bg-emerald-300/8 text-emerald-100/80",
      };

  return (
    <SpotlightCard className="timeline-panel h-full overflow-hidden border-white/10 bg-white/[0.03] p-0 backdrop-blur-2xl">
      <div className="border-b border-white/8 bg-linear-to-br from-white/8 via-slate-950/10 to-cyan-400/12 px-6 py-5">
        <span className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-[0.68rem] uppercase tracking-[0.24em] ${toneClasses.badge}`}>
          {icon}
          Timeline
        </span>
        <h3 className="mt-4 text-left text-2xl font-bold text-white">{title}</h3>
        <p className="mt-3 text-left text-sm leading-7 text-slate-300">{subtitle}</p>
      </div>
      <ol className="relative space-y-6 px-6 py-6 before:absolute before:bottom-7 before:left-[1.7rem] before:top-7 before:w-px before:bg-linear-to-b before:from-transparent before:via-cyan-200/30 before:to-transparent">
        {entries.map((entry, index) => (
          <li
            key={`${entry.year}-${entry.title}`}
            className="timeline-item relative pl-8"
            style={{ "--timeline-delay": `${index * 110}ms` } as CSSProperties}
          >
            <span className={`absolute left-[-0.02rem] top-1.5 h-3.5 w-3.5 rounded-full border-2 ${toneClasses.dot}`} />
            <time className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-400">
              {entry.year}
            </time>
            <h4 className="mt-2 text-left text-lg font-bold text-white">{entry.title}</h4>
            <p className="mt-1 text-left text-sm font-semibold text-cyan-100/80">{entry.place}</p>
            <p className="mt-3 text-left text-sm leading-7 text-slate-300">{entry.description}</p>
            <ul className="mt-4 flex flex-wrap gap-2">
              {entry.tags.map((tag) => (
                <li
                  key={tag}
                  className={`rounded-full border px-3 py-1 text-[0.68rem] font-semibold uppercase tracking-[0.16em] ${toneClasses.tag}`}
                >
                  {tag}
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ol>
    </SpotlightCard>
  );
}

export default function HomePage({ apiUrl }: { apiUrl: string }) {
  const [content, setContent] = useState<SiteContent | null>(null);
  const [error, setError] = useState<string>("");
  const [activeGalleryIndex, setActiveGalleryIndex] = useState<number>(-1);

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
  const footerLinks = content.contact_groups.flatMap((group) =>
    group.links.map((link) => ({
      ...link,
      groupTitle: group.title,
    })),
  );
  const gallerySlides = content.gallery_photos.map((photoItem) => ({
    src: photoItem.image_url,
    alt: photoItem.title,
    title: photoItem.title,
    description: photoItem.caption,
  }));

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
            <img
              alt="Esteban alter ego illustration"
              src={alterEgo.src}
              className="h-80 w-full object-cover"
            />
            <div className="flex flex-col my-5 px-5">
              <GlowingText>
                <span className="text-xl font-bold select-none">Short bio</span>
              </GlowingText>
              <p className="text-sm text-justify cursor-default select-none">
                {content.about_short_bio}
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

      <section id="background" className="py-20 space-y-6 md:w-[120%] md:-ml-[10%]">
        <div className="text-center">
          <GlowingHeader>Background</GlowingHeader>
        </div>
        <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
          <TimelineColumn
            title="Educational Background"
            subtitle="A path from low-level curiosity into formal computer science, cybersecurity, and engineering foundations."
            icon={<FaGraduationCap />}
            entries={educationTimeline}
            tone="cyan"
          />
          <TimelineColumn
            title="Professional Background"
            subtitle="Companies, leadership roles, and hands-on engineering work across security, DevOps, software, and games."
            icon={<FaBriefcase />}
            entries={professionalTimeline}
            tone="emerald"
          />
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

      <section id="published-books" className="py-20 space-y-6">
        <GlowingHeader>Published Books</GlowingHeader>
        <div className="grid grid-cols-1 place-items-center gap-5">
          {publishedBooks.map((book) => (
            <SpotlightCard
              key={book.asin}
              spotlightColor="rgba(0, 229, 255, 0.24)"
              className="group w-full max-w-[24rem] overflow-hidden border-white/10 bg-white/[0.03] p-0 backdrop-blur-2xl"
            >
              <a
                href={book.url}
                target="_blank"
                rel="noreferrer"
                className="block h-full"
              >
                <div className="relative flex min-h-[31rem] items-end justify-center overflow-hidden bg-slate-950">
                  <img
                    src={book.coverUrl}
                    alt={`${book.title} book cover`}
                    className="absolute inset-0 h-full w-full object-cover transition duration-500 group-hover:scale-[1.03]"
                  />
                  <div className="absolute inset-0 bg-linear-to-t from-slate-950 via-slate-950/20 to-transparent" />
                  <div className="relative w-full px-5 py-5">
                    <span className="inline-flex items-center gap-2 rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-[0.68rem] uppercase tracking-[0.24em] text-cyan-100/85">
                      <FaBookOpen />
                      Amazon
                    </span>
                    <h3 className="mt-4 text-left text-2xl font-bold text-white">
                      {book.title}
                    </h3>
                    <p className="mt-3 text-left text-sm leading-6 text-slate-300">
                      {book.subtitle}
                    </p>
                  </div>
                </div>
                <div className="space-y-4 px-6 py-5">
                  <p className="text-sm leading-6 text-slate-300">{book.authors}</p>
                  <div className="flex items-center justify-between border-t border-white/8 pt-4 text-sm">
                    <span className="text-slate-400">ASIN {book.asin}</span>
                    <span className="font-semibold text-cyan-200">View book {"->"}</span>
                  </div>
                </div>
              </a>
            </SpotlightCard>
          ))}
        </div>
      </section>

      <section id="opportunities" className="py-20 space-y-6">
        <GlowingHeader>Opportunities</GlowingHeader>
        <div className="grid grid-cols-1 gap-5">
          {opportunities.map((opportunity) => (
            <SpotlightCard
              key={opportunity.title}
              spotlightColor="rgba(16, 185, 129, 0.22)"
              className="mx-auto w-full max-w-3xl overflow-hidden border-white/10 bg-white/[0.03] p-0 backdrop-blur-2xl"
            >
              <div className="border-b border-white/8 bg-linear-to-br from-emerald-400/14 via-slate-950/10 to-cyan-400/14 px-6 py-5">
                <span className="inline-flex items-center gap-2 rounded-full border border-emerald-300/20 bg-emerald-300/10 px-3 py-1 text-[0.68rem] uppercase tracking-[0.24em] text-emerald-100/85">
                  <FaBullhorn />
                  Advertisement
                </span>
                <h3 className="mt-4 text-left text-2xl font-bold text-white">
                  {opportunity.title}
                </h3>
                <p className="mt-3 text-left text-xs uppercase tracking-[0.22em] text-cyan-200/80">
                  {opportunity.category}
                </p>
              </div>
              <div className="space-y-5 px-6 py-5">
                <p className="text-sm leading-7 text-slate-300">{opportunity.description}</p>
                <a href={opportunity.ctaUrl} className="inline-flex">
                  <StarBorder as={"button"} className="cursor-pointer">
                    {opportunity.ctaLabel}
                  </StarBorder>
                </a>
              </div>
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

      <section id="youtube" className="py-20 space-y-6">
          <GlowingHeader>YouTube</GlowingHeader>
          <SpotlightCard className="overflow-hidden border-white/10 bg-white/[0.03] p-0 backdrop-blur-2xl">
            <div className="border-b border-white/8 bg-linear-to-br from-red-500/16 via-slate-950/10 to-cyan-400/14 px-6 py-5">
              <span className="inline-flex items-center gap-2 rounded-full border border-red-300/20 bg-red-300/10 px-3 py-1 text-[0.68rem] uppercase tracking-[0.24em] text-red-100/85">
                <FaYoutube />
                Channel
              </span>
              <h3 className="mt-4 text-left text-2xl font-bold text-white">
                {youtubeChannel.title}
              </h3>
              <p className="mt-3 text-left text-sm leading-7 text-slate-300">
                Cybersecurity, tech, programming, and field notes from {youtubeChannel.handle}.
              </p>
            </div>
            <div className="space-y-5 p-5">
              <div className="aspect-video w-full overflow-hidden rounded-[1.2rem] border border-white/10 bg-black">
                <iframe
                  className="h-full w-full"
                  src={`https://www.youtube.com/embed/videoseries?list=${youtubeChannel.uploadsPlaylistId}`}
                  title={`${youtubeChannel.title} YouTube uploads`}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  allowFullScreen
                  loading="lazy"
                />
              </div>
              <div className="flex flex-col items-start justify-between gap-4 border-t border-white/8 pt-4 text-sm sm:flex-row sm:items-center">
                <span className="text-slate-400">Latest public uploads</span>
                <a
                  href={youtubeChannel.url}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 font-semibold text-cyan-200 transition hover:text-white"
                >
                  <FaYoutube />
                  Open channel
                </a>
              </div>
            </div>
          </SpotlightCard>
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

      <ContactSection
        apiUrl={apiUrl}
        contactIntro={content.contact_intro}
        contactGroups={content.contact_groups.map((group) => ({
          ...group,
          links: group.links.map((link) => ({
            ...link,
            icon: iconMap[link.icon] || null,
          })),
        }))}
      />

      <section id="signals" className="py-20 space-y-6">
        <GlowingHeader>Signals & Frames</GlowingHeader>
        <SpotlightCard className="overflow-hidden border-white/10 bg-white/[0.03] p-0 backdrop-blur-2xl">
          <div className="border-b border-white/8 bg-gradient-to-br from-cyan-400/14 via-slate-950/10 to-fuchsia-400/14 px-6 py-5">
            <p className="text-xs uppercase tracking-[0.24em] text-cyan-200/80">
              Photo gallery
            </p>
            <h3 className="mt-2 text-2xl font-bold text-white">
              Personal frames from etherbeing
            </h3>
            <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-300">
              A masonry-style gallery sourced from the backend, so new photos can be added without hardcoding the frontend. Click any frame to open a closer showroom view.
            </p>
          </div>
          <div className="p-5">
            {content.gallery_photos.length ? (
              <div className="etherbeing-gallery-masonry">
                {content.gallery_photos.map((photoItem, index) => (
                  <article
                    key={`${photoItem.title}-${index}`}
                    className="etherbeing-gallery-card group overflow-hidden rounded-[1.6rem] border border-white/10 bg-slate-950/55 shadow-[0_18px_42px_rgba(2,6,23,0.28)]"
                  >
                    <button
                      type="button"
                      onClick={() => setActiveGalleryIndex(index)}
                      className="block w-full cursor-pointer text-left"
                    >
                      <div className="overflow-hidden">
                        <img
                          src={photoItem.image_url}
                          alt={photoItem.title}
                          className="w-full object-cover transition duration-500 group-hover:scale-[1.03]"
                        />
                      </div>
                      <div className="space-y-2 px-4 py-4">
                        <div className="flex items-center justify-between gap-3">
                          <h4 className="text-lg font-semibold text-white">{photoItem.title}</h4>
                          <span className="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-[0.65rem] uppercase tracking-[0.22em] text-cyan-100/85">
                            Showroom
                          </span>
                        </div>
                        <p className="text-sm leading-6 text-slate-300">{photoItem.caption}</p>
                      </div>
                    </button>
                  </article>
                ))}
              </div>
            ) : (
              <div className="rounded-[1.6rem] border border-dashed border-white/10 bg-black/20 p-6 text-sm text-slate-400">
                Gallery images will appear here once they are added in the backend.
              </div>
            )}
          </div>
        </SpotlightCard>

        <SpotlightCard className="overflow-hidden border-white/10 bg-white/[0.03] p-0 backdrop-blur-2xl">
          <div className="border-b border-white/8 bg-gradient-to-br from-emerald-400/14 via-slate-950/10 to-cyan-400/14 px-6 py-5">
            <p className="text-xs uppercase tracking-[0.24em] text-cyan-200/80">
              Market watch
            </p>
            <h3 className="mt-2 text-2xl font-bold text-white">
              {content.featured_chart_title}
            </h3>
            <p className="mt-3 max-w-2xl text-sm leading-7 text-slate-300">
              Live candlestick context rendered through TradingView&apos;s advanced chart widget with the symbol configured from the backend.
            </p>
          </div>
          <div className="p-5">
            <TradingViewAdvancedChart
              symbol={content.featured_chart_symbol}
              title={content.featured_chart_title}
            />
          </div>
        </SpotlightCard>
      </section>

      <Lightbox
        open={activeGalleryIndex >= 0}
        close={() => setActiveGalleryIndex(-1)}
        index={activeGalleryIndex >= 0 ? activeGalleryIndex : 0}
        slides={gallerySlides}
      />

      <footer className="space-y-8 py-14 text-center text-gray-500">
        <div className="mx-auto flex max-w-5xl flex-wrap items-center justify-center gap-3">
          {footerLinks.map((link) => (
            <a
              key={`${link.groupTitle}-${link.label}`}
              href={link.url}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300 transition hover:border-cyan-300/35 hover:text-white"
            >
              {iconMap[link.icon] || null}
              <span>{link.label}</span>
            </a>
          ))}
        </div>
        <p>
          {content.footer_copy}
          <br />
          {content.footer_tagline}
        </p>
      </footer>
    </>
  );
}
