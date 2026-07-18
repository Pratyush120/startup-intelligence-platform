import { useEffect } from "react";

interface ShortcutConfig {
  key: string;
  ctrlKey?: boolean;
  metaKey?: boolean;
  shiftKey?: boolean;
  callback: () => void;
  enabled?: boolean;
}

export function useKeyboardShortcut({ key, ctrlKey, metaKey, shiftKey, callback, enabled = true }: ShortcutConfig): void {
  useEffect(() => {
    if (!enabled) return;

    function handler(e: KeyboardEvent) {
      const matchesKey = e.key.toLowerCase() === key.toLowerCase();
      const matchesShift = shiftKey ? e.shiftKey : true;
      const modRequired = ctrlKey || metaKey;
      const modPressed = modRequired ? (e.ctrlKey || e.metaKey) : true;

      if (matchesKey && modPressed && matchesShift) {
        e.preventDefault();
        callback();
      }
    }

    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [key, ctrlKey, metaKey, shiftKey, callback, enabled]);
}
