import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';

export const load: PageLoad = async ({ params, fetch }) => {
  // Convert the route parameter to a number
  const eventId = parseInt(params.event_id_from_url);
  console.log("Fetching leaderboard…");
		
  const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/get_summary", {
    method: "POST",
    headers: {
      apikey: "sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz",
      Authorization: "Bearer sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ event_id: eventId })
  });

  const data = await res.json();
  console.log("Fetched data:", data); // This logs the array

  // If the event data is missing, throw a 404 error.
  if (!data || !data.event) {
    throw error(404, "Event Not Found");
  }

  return {
    eventInfo: data.event,
    totals: data.totals
  };
};