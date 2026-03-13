import { readFile } from "node:fs/promises";

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

const source = await readFile("src/components/react/GradualBlur.tsx", "utf8");

assert(!source.includes("import React"), "GradualBlur still imports a default React runtime.");
assert(!source.includes("React.memo"), "GradualBlur still uses React.memo via the default runtime.");
assert(!source.includes("React.useRef"), "GradualBlur still uses React.useRef via the default runtime.");
assert(source.includes("memo("), "GradualBlur is expected to memoize the component.");
assert(source.includes("useRef"), "GradualBlur is expected to use the named useRef hook.");

console.log("GradualBlur source guard passed.");
