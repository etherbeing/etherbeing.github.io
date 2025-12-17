
import HeaderBreadcrumb from "./HeaderBreadcrumb";

export default function Header({ title }: { title: string }) {
    return (

        <header
            className="relative flex items-center justify-between max-w-4xl h-full"
        >
            <a href="/" className="flex gap-3 justify-center items-center">
                <img
                    className="h-15 shadow-lg shadow-gray-900 aspect-square rounded-full"
                    src={`https://github.com/${import.meta.env.PUBLIC_GITHUB_USER}.png`}
                />
                <span> etherbeing </span>
            </a>
            <HeaderBreadcrumb title={title} />
        </header>
    )
}
