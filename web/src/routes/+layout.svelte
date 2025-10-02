<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.png';
	import Header from '$lib/Header.svelte';
  	import Footer from '$lib/Footer.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<Header />

{@render children?.()}

<Footer />