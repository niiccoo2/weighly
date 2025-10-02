<script lang="ts">
  import Header from '$lib/Header.svelte';
  import Footer from '$lib/Footer.svelte';
  import '$lib/styles_lightmode.css';
  import { onMount, onDestroy, tick } from 'svelte';
  import { fly } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';

  const words = ["food.", "clothes.", "books.", "gear.", "anything!"];
  let currentIndex = 0;
  let currentWord = words[0];

  // Controls the show/hide cycle so the old word fully slides out before the new one slides in
  let showWord = true;

  // Reserve width to keep the sentence from shifting
  let maxWidth = 0;
  let measurer: HTMLSpanElement;

  let interval: ReturnType<typeof setInterval>;
  const intervalMs = 3000;
  const transitionMs = 400;

  function nextWord() {
    // Start the outro; once it's done, we'll switch the word and intro the new one.
    if (!showWord) return; // guard against overlapping calls
    showWord = false;
  }

  function handleOutroEnd() {
    currentIndex = (currentIndex + 1) % words.length;
    currentWord = words[currentIndex];
    // Wait a tick so DOM updates then show new word with intro transition
    tick().then(() => (showWord = true));
  }

  async function measureMaxWidth() {
    // Measure each word width using an offscreen measurer with the same styles
    await tick();
    let max = 0;
    for (const w of words) {
      measurer.textContent = w;
      await tick();
      const width = measurer.offsetWidth;
      if (width > max) max = width;
    }
    maxWidth = max;
  }

  onMount(async () => {
    await measureMaxWidth();
    interval = setInterval(nextWord, intervalMs);
  });

  onDestroy(() => clearInterval(interval));
</script>

<main class="flex flex-col items-center justify-center h-[80vh] text-center space-y-6">
  <h1 class="text-4xl md:text-6xl thick_text">
    Save weights of
    <!-- Keep the rotating slot a fixed width so the rest of the sentence doesn't move -->
    <span
      class="rotator inline-block align-baseline"
      style="width: {maxWidth ? `${maxWidth}px` : 'auto'}"
      aria-live="polite"
    >
      {#if showWord}
        <span
          class="accent_color inline-block"
          out:fly={{ x: -30, duration: transitionMs, easing: cubicOut }}
          in:fly={{ x: 30, duration: transitionMs, easing: cubicOut }}
          on:outroend={handleOutroEnd}
        >
          {currentWord}
        </span>
      {/if}

      <!-- Offscreen measurer to reserve the maximum width; inherits the same font sizing -->
      <span
        bind:this={measurer}
        class="measure-helper accent_color"
        aria-hidden="true"
      ></span>
    </span>
  </h1>

  <p class="text-lg md:text-xl max-w-xl opacity-80">
    Track and compare weights easily for your events.<br>
    Made for <a class="hover:underline" href="https://troop30bsa.com/">Troop 30 BSA</a>.
  </p>

  <button 
    class="accent_color_button rounded px-6 py-3 text-lg hover:scale-105 transition-transform cursor-pointer"
    on:click={() => (window.location.href = "/login")}
  >
    Get Started
  </button>
</main>

<Footer />

<style>
  .rotator {
    white-space: nowrap;
    position: relative;
  }

  .measure-helper {
    position: absolute;
    visibility: hidden;
    white-space: nowrap;
    inset: 0; /* keep it in the same context for accurate font metrics */
  }
</style>