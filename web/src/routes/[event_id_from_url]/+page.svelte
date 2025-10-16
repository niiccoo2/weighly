<script lang="ts">
	import { page } from '$app/stores';
	import '$lib/styles_lightmode.css';
	import { onMount, tick } from 'svelte';
	import { supabase } from '$lib/supabaseClient';
	export let data;

	let apikey = "sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz";

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

	async function getAllowedEvents(): Promise<number[]> {
    console.log("Fetching allowed events");
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) return [];

    const res = await fetch(
      "https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/get_allowed_events",
      {
        method: "POST",
        headers: {
          apikey: apikey,
          Authorization: `Bearer ${session.access_token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ user_id: session.user.id })
      }
    );

    if (!res.ok) {
      console.error("Failed to fetch allowed events:", await res.json());
      return [];
    }

    const events = await res.json();
    console.log("Fetched events:", events);

    // return an array of event IDs
    return events.map((e: any) => e.event_id);
  }
  
  let allowedToSave = false;

  onMount(async () => {
  const allowedEventIds = await getAllowedEvents();
  if (allowedEventIds.includes(eventInfo.event_id)) {
  	allowedToSave = true;
}
});
</script>

<svelte:head>
	<title>{pageTitle}</title>
</svelte:head>

<main class="flex flex-col items-center mt-8 w-full max-w-4xl mx-auto">
  <!-- Title centered with button top-right -->
  <div class="relative w-full mb-4">
    <p class="text-xl font-semibold text-center">{pageTitle}:</p>

    {#if allowedToSave}
	  <a href="/{eventInfo.event_id}/settings"
         class="absolute right-4 top-0 accent_color_button rounded px-4 py-2 hover:scale-105 transition-transform cursor-pointer">
        Settings
      </a>
    {/if}
  </div>

  <!-- Leaderboard -->
  {#if leaderboard.length === 0}
    <p>No weights yet.</p>
  {:else}
    <div class="flex flex-col items-center space-y-4 w-full">
      {#each leaderboard.slice() as item}
        <div class="w-full max-w-md p-4 card rounded-xl shadow-lg hover:scale-105 transition-transform block">
          <div class="flex items-center px-4">
            <div class="flex items-center gap-2">
              <p class="m-0 text-2xl font-bold">{item.rank}.</p>
              <p class="m-0 text-2xl font-bold">{item.name}</p>
            </div>

            <p class="m-0 text-2xl font-bold flex-1 text-center" class:invisible={!item.middle}>
              {item.middle}
            </p>

            <div class="flex items-center space-x-2">
              <p class="m-0 text-2xl font-bold">
                {item.score_lbs} 
                <button class="text-sm cursor-pointer" on:click={() => toggleUnits()}>{kg_mode}</button>
              </p>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</main>


