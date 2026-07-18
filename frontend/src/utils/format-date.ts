import { formatDistanceToNow, format } from "date-fns";

export function formatRelativeTime(date: Date | string): string {
  return formatDistanceToNow(new Date(date), { addSuffix: true });
}

export function formatTimestamp(date: Date | string): string {
  return format(new Date(date), "dd MMM yyyy · HH:mm");
}

export function formatDateShort(date: Date | string): string {
  return format(new Date(date), "dd MMM yyyy");
}
