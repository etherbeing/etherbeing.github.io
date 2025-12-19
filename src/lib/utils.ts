import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function oklchGradient(
  L0: number, // lightness min
  L1: number, // lightness max
  C: number, // chroma
  h: number, // hue
  i: number,
  n: number,
) {
  const t = n <= 1 ? 0 : i / (n - 1);
  const L = L0 + t * (L1 - L0);
  return `oklch(${L}% ${C} ${h})`;
}
