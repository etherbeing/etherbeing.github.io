import { useState } from "react";
import SpotlightCard from "./SpotlightCard";
import { Sling as Hamburger } from "hamburger-react";
import { GoArrowUpRight } from "react-icons/go";

const navs: Array<{
  label: string;
  links: Array<{ label: string; href: string }>;
}> = [
  {
    label: "Info",
    links: [
      { label: "About", href: "#about" },
      { label: "Core Skills", href: "#core-skills" },
      { label: "Services", href: "#services" },
      { label: "Projects", href: "#projects" },
      { label: "Blog", href: "#blog" },
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
  const [isOpen, setIsOpen] = useState(false);

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
          </a>
          <Hamburger
            size={20}
            label="Show options"
            toggled={isOpen}
            onToggle={setIsOpen}
          ></Hamburger>
        </div>
        <nav
          style={{
            animationDelay: `${navs.length * 100}ms`,
          }}
          className={`w-full grid grid-cols-1 md:grid-cols-2 gap-3 overflow-hidden transition-all duration-300 h-0 ${isOpen ? "nav-expand" : "nav-collapse"}`}
        >
          {navs.map((nav, i) => (
            <SpotlightCard
              key={i}
              className={`mt-5 w-full flex flex-col gap-3 translate-y-100 opacity-0`}
              style={{
                animationDelay: `${i * 100 + 100}ms`,
              }}
            >
              <h3 className="text-lg font-bold cursor-default">{nav.label}</h3>
              <div className="flex flex-col gap-3">
                {nav.links.map((link, i) => (
                  <a
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      const hash = new URL(e.currentTarget.href).hash;
                      let section = document.querySelector(hash);
                      if (section) {
                        section.scrollIntoView({
                          behavior: "smooth",
                        });
                      } else {
                        location.assign(`/${hash}`);
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
        </nav>
      </SpotlightCard>
    </header>
  );
}
