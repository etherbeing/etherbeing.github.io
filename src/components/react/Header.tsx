import { useLayoutEffect, useRef, useState } from "react";
import SpotlightCard from "./SpotlightCard";
import { Sling as Hamburger } from "hamburger-react";
import { GoArrowUpRight } from "react-icons/go";
import { FaGithub } from "react-icons/fa";
import { oklchGradient } from "@/lib/utils";
import { useGithubSession } from "./useGithubSession";
import { Button } from "../ui/button";
import { useOnlineStatus } from "./useOnlineStatus";
import GlowingText from "./GlowingText";

const navs: Array<{
  label: string;
  links: Array<{ label: string; href: string }>;
}> = [
    {
      label: "Info",
      links: [
        { label: "About", href: "#about" },
        { label: "Background", href: "#background" },
        { label: "Core Skills", href: "#core-skills" },
        { label: "Services", href: "#services" },
        { label: "Published Books", href: "#published-books" },
        { label: "Opportunities", href: "#opportunities" },
        { label: "Projects", href: "#projects" },
        { label: "YouTube", href: "#youtube" },
        { label: "Blog", href: "#blog" },
        { label: "Projects Archive", href: "/projects" },
        { label: "Blog Archive", href: "/blog" },
        { label: "Inbox", href: "/inbox" },
        { label: "Contact", href: "#contact" },
      ],
    },
    {
      label: "Projects",
      links: [
        { label: "CVE Forge", href: "https://github.com/etherbeing/cveforge" },
        {
          label: "This Website",
          href: "https://github.com/etherbeing/etherbeing.github.io",
        },
        { label: "Senjor", href: "https://github.com/etherbeing/senjor" },
        { label: "Powerhouse", href: "https://github.com/etherbeing/powerhouse" },
        { label: "TFProtocol", href: "https://github.com/etherbeing/tfprotocol" },
      ],
    },
  ];

export default function Header() {
  const [isOpen, setIsOpen] = useState<boolean | undefined>();
  const [navHeight, setNavHeight] = useState<number>(0);
  const navContentRef = useRef<HTMLDivElement | null>(null);
  const apiUrl = import.meta.env.PUBLIC_API_URL;
  const { session, isLoading, login, logout } = useGithubSession(apiUrl);
  const { isOnline, showOfflineSnackbar } = useOnlineStatus();

  useLayoutEffect(() => {
    if (isOpen === undefined) return;

    const updateNavHeight = () => {
      const contentHeight = navContentRef.current?.scrollHeight ?? 0;
      const viewportLimit = Math.max(280, window.innerHeight - 120);
      setNavHeight(Math.min(contentHeight, viewportLimit));
    };

    updateNavHeight();
    window.addEventListener("resize", updateNavHeight);
    const resizeObserver = new ResizeObserver(updateNavHeight);
    if (navContentRef.current) {
      resizeObserver.observe(navContentRef.current);
    }

    return () => {
      window.removeEventListener("resize", updateNavHeight);
      resizeObserver.disconnect();
    };
  }, [isOpen, isLoading, session.is_authenticated]);

  return (
    <header className="z-20 fixed w-screen flex items-center justify-center mt-10">
      <div className="absolute max-w-[95%] md:max-w-4xl rounded-3xl z-15 w-full h-full backdrop-blur-2xl"></div>
      <SpotlightCard className="z-20 max-w-[95%] md:max-w-4xl py-3 w-full flex flex-col justify-center items-center bg-transparent">
        <div className="flex justify-between items-center w-full">
          <a href="/" className="flex gap-3 justify-center items-center">
            <img
              className="h-10 shadow aspect-square rounded-full"
              src={`https://github.com/${import.meta.env.PUBLIC_GITHUB_USER}.png`}
            />
            <GlowingText>
              <h1 className="text-2xl font-bold my-0 py-0 select-none">
                etherbeing
              </h1>
            </GlowingText>
          </a>
          <div className="flex items-center gap-3">
            <div
              className={`hidden md:inline-flex items-center gap-2 rounded-full border px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.22em] transition ${isOnline
                ? "border-emerald-300/30 bg-emerald-300/10 text-emerald-100"
                : "border-amber-300/30 bg-amber-300/10 text-amber-100"
                }`}
            >
              <span
                className={`h-2 w-2 rounded-full ${isOnline ? "bg-emerald-300" : "bg-amber-300"
                  }`}
              />
              {isOnline ? "Online" : "Offline"}
            </div>
            <Hamburger
              size={20}
              label="Show options"
              toggled={isOpen}
              onToggle={setIsOpen}
            ></Hamburger>
          </div>
        </div>
        {isOpen !== undefined ? (
          <>
            <nav
              style={{
                animationDelay: `${navs.length * 100}ms`,
                height: isOpen ? `${navHeight}px` : "0px",
              }}
              className={`mt-3 w-full overflow-hidden text-center transition-[height] duration-300 ease-in-out ${isOpen ? "nav-expand overflow-y-auto" : "nav-collapse"}`}
            >
              <div ref={navContentRef} className="pb-1">
                {session.is_authenticated ? (
                  <Button
                    type="button"
                    onClick={() => void logout()}
                    className="text-sm inline-flex items-center"
                  >
                    <FaGithub className="mr-2" />
                    Logout @{session.github_login || session.username}
                  </Button>
                ) : (
                  <Button
                    type="button"
                    disabled={isLoading}
                    onClick={() => login()}
                    className="text-sm inline-flex items-center disabled:opacity-60"
                  >
                    <FaGithub className="mr-2" />
                    {isLoading ? "Loading login..." : "Login with GitHub"}
                  </Button>
                )}
                <div className="w-full grid grid-cols-1 md:grid-cols-2 gap-3">
                  {navs.map((nav, i) => (
                    <SpotlightCard
                      key={i}
                      className="nav-menu-card mt-5 w-full flex flex-col gap-3"
                      style={{
                        animationDelay: `${i * 100 + 100}ms`,
                        backgroundColor: oklchGradient(
                          0,
                          10,
                          0.05,
                          300,
                          i,
                          navs.length,
                        ),
                      }}
                    >
                      <h3 className="text-lg font-bold cursor-default">{nav.label}</h3>
                      <div className="flex flex-col gap-3">
                        {nav.links.map((link, i) => (
                          <a
                            onClick={(e) => {
                              e.preventDefault();
                              e.stopPropagation();
                              const target = new URL(e.currentTarget.href);
                              const hash = target.hash;
                              let section = hash ? document.querySelector(hash) : null;
                              if (section) {
                                section.scrollIntoView({
                                  behavior: "smooth",
                                });
                              } else {
                                location.assign(`${target.pathname}${target.search}${target.hash}`);
                              }
                              setIsOpen(false);
                            }}
                            key={i}
                            href={link.href}
                            className="text-sm inline-flex items-center"
                          >
                            <GoArrowUpRight className="mr-2" />
                            {link.label}
                          </a>
                        ))}
                      </div>
                    </SpotlightCard>
                  ))}
                </div>
              </div>
            </nav>
          </>
        ) : null}
      </SpotlightCard>
      {showOfflineSnackbar ? (
        <div className="fixed right-4 top-4 z-40 w-[min(22rem,calc(100vw-2rem))] rounded-3xl border border-amber-300/25 bg-slate-950/88 p-4 text-sm text-amber-50 shadow-2xl shadow-black/40 backdrop-blur-2xl md:right-8 md:top-8">
          <div className="flex items-start gap-3">
            <span className="mt-1 h-2.5 w-2.5 rounded-full bg-amber-300" />
            <div className="space-y-1">
              <p className="m-0 text-xs font-semibold uppercase tracking-[0.28em] text-amber-200/80">
                No Internet
              </p>
              <p className="m-0 leading-6 text-slate-200">
                You are offline right now. Cached pages are still available, and fresh data will sync back once your connection returns.
              </p>
            </div>
          </div>
        </div>
      ) : null}
    </header>
  );
}
