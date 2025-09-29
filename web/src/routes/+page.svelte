<script lang="ts">
  import Header from '$lib/Header.svelte';
  import '$lib/styles_lightmode.css'; // adjust path if you put the CSS somewhere else
  export let data;
</script>

<Header />

<main>
  <slot />
</main>