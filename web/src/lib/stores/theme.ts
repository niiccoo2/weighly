import { writable } from 'svelte/store';
import { browser } from '$app/environment';

function detectInitial(): boolean {
  if (!browser) return false;
  const saved = localStorage.getItem('theme');
  if (saved === 'dark') return true;
  if (saved === 'light') return false;
  return window.matchMedia('(prefers-color-scheme: dark)').matches;
}

export const isDark = writable(detectInitial());

if (browser) {
  // Apply initial theme
  document.documentElement.classList.toggle('dark', detectInitial());

  // Listen for system changes if no explicit preference
  if (!localStorage.getItem('theme')) {
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    mq.addEventListener('change', e => {
      isDark.set(e.matches);
      document.documentElement.classList.toggle('dark', e.matches);
    });
  }

  // Reactively apply theme changes
  isDark.subscribe(value => {
    document.documentElement.classList.toggle('dark', value);
    try {
      localStorage.setItem('theme', value ? 'dark' : 'light');
    } catch {
      /* ignore private mode errors */
    }
  });
}
