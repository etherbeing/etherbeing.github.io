import HeaderBreadcrumb from "./HeaderBreadcrumb";
import SpotlightCard from "./SpotlightCard";

export default function Header() {
  return (
    <header className="z-20 fixed w-screen flex items-center justify-center mt-10">
      <div className="absolute max-w-4xl rounded-3xl  z-15 w-full h-full backdrop-blur-2xl"></div>
      <SpotlightCard className="z-20 max-w-4xl h-20 w-full flex justify-between bg-transparent">
        <a href="/" className="flex gap-3 justify-center items-center">
          <img
            className="h-10 shadow-lg shadow-gray-900 aspect-square rounded-full"
            src={`https://github.com/${import.meta.env.PUBLIC_GITHUB_USER}.png`}
          />
          <span> etherbeing </span>
        </a>
        {/*<HeaderBreadcrumb title={title} />*/}
      </SpotlightCard>
    </header>
  );
}
