<script>
	import leaderboard from '../example.json';
</script>

<svelte:head>
	<title>Weighly - Troop 30 Leaderboard</title>
</svelte:head>

<div class="">
	<div class="bg-gray-500 w-full p-4 shadow-lg">
		<!-- Title -->
		<p class="text-center text-7xl shadow-lg text-white">All Time Leaderboard</p>
	</div>
	<div class="p-4 w-full max-w-4xl mx-auto text-center text-2xl">
		<!-- Leaderboard -->

		<table class="mx-auto">
			<thead>
				<tr class="">
					<th>Rank</th>
					<th>Player</th>
					<th>Type</th>
					<th>Score</th>
				</tr>
			</thead>

			<tbody>
				{#each leaderboard.slice(0, 10) as item}
					<tr>
						<td class="px-4 py-2">{item.rank}</td>
						<td class="px-4 py-2">{item.name}</td>
						<td class="px-4 py-2">{item.category}</td>
						<td class="px-4 py-2">{item.score_lbs}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
