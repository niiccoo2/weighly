<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';

  const year = new Date().getFullYear();

  // Measure footer height so we can add a spacer above it,
  // preventing overlap and ensuring at least 1rem (spacing-4) gap.
  let footerEl: HTMLElement;
  let footerHeight = 0;

  let ro: ResizeObserver | undefined;

  function updateHeight() {
    if (footerEl) {
      footerHeight = footerEl.offsetHeight;
    }
  }

  onMount(() => {
    if (!browser) return; // SSR safety

    updateHeight();

    if (typeof ResizeObserver !== 'undefined' && footerEl) {
      ro = new ResizeObserver(updateHeight);
      ro.observe(footerEl);
    }

    if (typeof window !== 'undefined') {
      window.addEventListener('resize', updateHeight);
    }
  });

  onDestroy(() => {
    if (!browser) return;

    ro?.disconnect();

    if (typeof window !== 'undefined') {
      window.removeEventListener('resize', updateHeight);
    }
  });
</script>

<!-- Spacer to keep content from being covered by the fixed footer.
     Ensures a minimum 1rem (spacing-4) gap above the footer. -->
<div class="footer-spacer" style="--footer-h: {footerHeight}px" aria-hidden="true"></div>

<footer
  bind:this={footerEl}
  class="fixed inset-x-0 bottom-0 z-40 w-full border-t border-gray-200/70 dark:border-gray-800/70 bg-white/70 dark:bg-black/40 backdrop-blur supports-[backdrop-filter]:bg-white/60"
>
  <div class="mx-auto max-w-6xl px-5 py-8">
    <div class="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
      <!-- Brand + tagline -->
      <div>
        <div class="text-xl md:text-2xl font-semibold">Weighly</div>
        <p class="text-sm opacity-70">Track and compare weights easily for your events.</p>
      </div>

      <!-- Social / actions (Email + GitHub only) -->
      <div class="flex items-center gap-3">
        <a href="mailto:contact@weighly.com" aria-label="Email Weighly" class="opacity-80 hover:opacity-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[--accent-color] rounded p-1">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M4 6h16a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1zm0 0 8 6 8-6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </a>
        <a href="https://github.com/niiccoo2/weighly" target="_blank" rel="noopener noreferrer" aria-label="GitHub" class="opacity-80 hover:opacity-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[--accent-color] rounded p-1">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path fill="currentColor" d="M12 .5a12 12 0 0 0-3.79 23.39c.6.11.82-.26.82-.58v-2.03c-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.35-1.76-1.35-1.76-1.1-.75.08-.74.08-.74 1.21.09 1.84 1.24 1.84 1.24 1.08 1.85 2.83 1.32 3.52 1.01.11-.79.42-1.32.77-1.62-2.66-.3-5.47-1.33-5.47-5.9 0-1.3.47-2.37 1.24-3.21-.12-.3-.54-1.52.12-3.16 0 0 1.01-.32 3.3 1.23a11.46 11.46 0 0 1 6 0c2.29-1.55 3.3-1.23 3.3-1.23.66 1.64.24 2.86.12 3.16.77.84 1.24 1.91 1.24 3.21 0 4.58-2.81 5.6-5.49 5.9.43.37.82 1.1.82 2.22v3.29c0 .32.21.7.83.58A12 12 0 0 0 12 .5Z"/>
          </svg>
        </a>
      </div>
    </div>

    <div class="mt-6 flex flex-col items-start gap-2 sm:flex-row sm:items-center sm:justify-between text-xs opacity-70">
      <p>&copy; {year} Nico Smith &amp; Ben Elliott. All rights reserved.</p>
      <p>
        <span class="mr-1">Need help?</span>
        <a href="mailto:contact@weighly.com" class="accent_color underline underline-offset-2">contact@weighly.com</a>
      </p>
    </div>
  </div>
</footer>

<style>
  .accent_color { color: var(--accent-color); }

  /* Spacer equals footer height + 1rem (Tailwind spacing-4) */
  .footer-spacer {
    height: calc(var(--footer-h, 0px) + 1rem);
  }

  /* Optional: respect iOS safe area at the bottom */
  footer > div {
    padding-bottom: calc(2rem + env(safe-area-inset-bottom, 0px));
  }
</style>