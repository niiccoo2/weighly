<script lang="ts">
	import { page } from '$app/stores';
	import Header from '$lib/Header.svelte';
	import '$lib/styles_lightmode.css';
	import { onMount, tick } from 'svelte';
	export let data;

	let eventInfo = data.eventInfo;
  	let totals = data.totals ?? [];

	let leaderboard: any[] = [{ "rank": "???", "name": "Loading...", "category": "Leaderboard Fall back", "score_lbs": 0 }];
	let kg_mode: string = "lbs";
	let op_kg_mode: string = "kgs";
	$: kgMode = $page.url.searchParams.has('kgs');
	
	// Reactive page title updates whenever eventInfo changes
	$: pageTitle = eventInfo?.name
		? `${eventInfo.name} Leaderboard`
		: "Leaderboard";

	async function getLeaderboard() {
		leaderboard = [...totals.map((item: any, i: number) => ({
			...item,
			rank: i + 1,
			score_lbs: item.weight,
			category: item.type
		}))];
		if (kgMode) {
			leaderboard = leaderboard.map(item => ({
				...item,
				score_lbs: Math.round(item.score_lbs * 0.45359237 * 100) / 100
			}));
			kg_mode = "kgs";
			op_kg_mode = "lbs";
		} else {
			kg_mode = "lbs";
			op_kg_mode = "kgs";
		}
		await tick();
	}

	onMount(() => {
		getLeaderboard();
		console.log("Fetched leaderboard:", leaderboard);
	});

	function toggleUnits() {
		if (kg_mode === "lbs") {
			leaderboard = leaderboard.map(item => ({
				...item,
				score_lbs: Math.round(item.score_lbs * 0.45359237 * 100) / 100
			}));
			kg_mode = "kgs";
			op_kg_mode = "lbs";
		} else {
			leaderboard = leaderboard.map(item => ({
				...item,
				score_lbs: Math.round(item.score_lbs / 0.45359237 * 100) / 100
			}));
			kg_mode = "lbs";
			op_kg_mode = "kgs";
		}
	}

</script>

<svelte:head>
	<title>{pageTitle}</title>
</svelte:head>

<Header />

<div class="background" style="width: 100vw; height: 100vh;">
	<div class="w-full p-4">
		<!-- Title -->
		<p class="text-center text-7xl thick_text">
			{pageTitle}
		</p>
	</div>
	<div class="p-4 w-full max-w-4xl mx-auto text-center text-2xl">
		<!-- Leaderboard -->

		<table class="mx-auto border-separate border-spacing-y-4">

			<tbody>
				{#each leaderboard.slice() as item}
					<tr class="w-full max-w-md p-4 card rounded-xl shadow-lg hover:scale-105 transition-transform block">
						<td class="px-4 py-2">{item.rank}.</td>
						<td class="px-4 py-2">{item.name}</td>
						<td class="px-2 py-2"  style="color: grey; font-size: 1rem;">{item.type}</td>
						<td class="px-4 py-2">
						{item.score_lbs} 
						<button on:click={() => toggleUnits()}>{kg_mode}</button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
