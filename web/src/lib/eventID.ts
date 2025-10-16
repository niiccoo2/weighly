import { supabase } from '$lib/supabaseClient';

async function getEventIdFromDB(event_string: string): Promise<number | null> {
  console.log("Sending POST request for custom URL lookup:", event_string);
  const { data: { session } } = await supabase.auth.getSession();

  const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/get_event_id_by_custom_url", {
    method: "POST",
    headers: {
      apikey: "sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz",
      Authorization: `Bearer sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ p_custom_url: event_string })
  });

  const response = await res.json();
  console.log("Response from get_event_id_by_custom_url:", response);

  // Check if response is a valid number (as string or number)
  if (typeof response === 'number' && !isNaN(response)) {
    console.log("Found event ID:", response);
    return response;
  }
  
  if (typeof response === 'string' && /^\d+$/.test(response.trim())) {
    const eventId = parseInt(response);
    console.log("Found event ID (from string):", eventId);
    return eventId;
  }
  
  console.log("Error: Invalid response format:", response);
  return null;
}

export async function getEventId(event_string: string): Promise<number | null> {
  console.log("Fetching event ID for:", event_string);
  
  // If it's a number, return it immediately
  if (!isNaN(parseInt(event_string)) && /^\d+$/.test(event_string)) {
    console.log("Event ID is a number:", event_string);
    return parseInt(event_string);
  }
  
  // Otherwise look it up in the DB
  return await getEventIdFromDB(event_string);
}