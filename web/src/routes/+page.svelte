<script lang="ts">
  import { page } from '$app/stores';
  
  let leaderboard: any[] = [];
  let kg_mode: string = "lbs"
  let op_kg_mode: string = "kgs"
  $: kgMode = $page.url.searchParams.has('kgs');

  $: (async () => {
    if (kgMode) {
	  const module = await import('../example.json');
	  leaderboard = module.default;
	  leaderboard = leaderboard.map(item => ({
		...item,
		score_lbs: Math.round(item.score_lbs * 0.45359237 * 100) / 100
	  }));
	  kg_mode = "kgs";
	  op_kg_mode = "lbs";
    } else {
      const module = await import('../example.json');
      leaderboard = module.default;
      kg_mode = "lbs";
      op_kg_mode = "kgs";
    }
  })();
</script>

<style>
  /* .bevel-box {
    padding: 1.5rem;
    background: #e0e0e0;
    border-radius: 12px;
    box-shadow: inset 4px 4px 8px #b8b8b8,
                inset -4px -4px 8px #ffffff;
    font-family: sans-serif;
    text-align: center;
  } */
  .lightmode-background {
	background-color: #F5F5F7;
	/* background-color: aqua; */
  }
  .lightmode-foreground {
	background-color: #ffffff;
  }

</style>

<svelte:head>
	<title>Weighly - Troop 30 Leaderboard</title>
</svelte:head>

<div class="lightmode-background" style="width: 100vw; height: 100vh;">
	<div class="w-full p-4">
		<!-- Title -->
		<p class="text-center text-7xl" style="color: #99ccff; -webkit-text-stroke: 2px black; font-weight: 1000;">
			Troop 30 - All Time Leaderboard
		</p>
	</div>
	<div class="p-4 w-full max-w-4xl mx-auto text-center text-2xl">
		<!-- Leaderboard -->

		<table class="mx-auto border-separate border-spacing-y-4">
			<thead>
				<tr>
					<th></th>
					<th></th>
					<th></th>
					<th></th>
				</tr>
			</thead>

			<tbody>
				{#each leaderboard.slice(0, 10) as item}
					<tr class="p-6 rounded-xl bg-gray-200 rounded-xl hover:shadow-[4px_4px_8px_#b8b8b8,-4px_-4px_8px_#ffffff] shadow-[2px_2px_4px_#b8b8b8,-2px_-2px_4px_#ffffff] text-center font-semibold hover:scale-105 lightmode-foreground">
						<td class="px-4 py-2">{item.rank}.</td>
						<td class="px-4 py-2">{item.name}</td>
						<td class="px-2 py-2"  style="color: grey; font-size: 1rem;">{item.category}</td>
						<td class="px-4 py-2">{item.score_lbs} <a href="?{op_kg_mode}">{kg_mode}</a></td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
