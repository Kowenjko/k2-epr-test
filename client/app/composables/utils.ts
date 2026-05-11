import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/** Merges Tailwind classes safely, resolving conflicts */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/** Format price from decimal string to UAH */
export function formatPrice(value: string | number): string {
  return new Intl.NumberFormat("uk-UA", {
    style: "currency",
    currency: "UAH",
    minimumFractionDigits: 2,
  }).format(Number(value));
}

/** Format ISO date string to readable Ukrainian format */
export function formatDate(iso: string): string {
  return new Intl.DateTimeFormat("uk-UA", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(iso));
}

/** Extracts a human-readable message from a FastAPI error response */
export function extractApiError(err: unknown): string {
  if (err instanceof Error) return err.message;
  return "Невідома помилка";
}
