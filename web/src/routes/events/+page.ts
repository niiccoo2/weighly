// import { supabase } from '$lib/supabaseClient';
// import type { PageLoad } from './$types';
// import { error } from '@sveltejs/kit';
// import type { User } from '@supabase/supabase-js';
// import { onMount } from 'svelte';

// export const load: PageLoad = async ({ params, fetch }) => {
//   onMount(() => {
//     let subscription: { unsubscribe: () => void };
//     // Convert the route parameter to a number
//     const { data: { session } } = await supabase.auth.getSession();
//     const accessToken = session?.access_token;
//     let user: User | null = null;
//     // Check if user is already signed in
//     const { data: authData } = await supabase.auth.getSession();
//     user = authData.session?.user || null;

//     // Listen for auth changes
//     const authListener = supabase.auth.onAuthStateChange(
//       (_event, session) => {
//         user = session?.user || null;
//       }
//     );

//     subscription = authListener.data.subscription;

//     console.log("Fetching allowed events…");

//     const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/get_allowed_events", {
//       method: "POST",
//       headers: {
//         apikey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9pZmpya3hoanJ0d2xyYW5jZGhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkwNjQ4NDUsImV4cCI6MjA3NDY0MDg0NX0.dBUGNaqc6-hcYQzEEUKnwD9gPji6RxqHfRhDeUA6hto",
//         Authorization: `Bearer ${accessToken}`,
//         "Content-Type": "application/json"
//       },
//       body: JSON.stringify({ user_id: user?.id })
//     });

//     const data = await res.json();
//     console.log("Fetched data:", data); // This logs the array

//     // If the event data is missing, throw a 404 error.
//     if (!data || !data.event) {
//       throw error(404, "Event Not Found");
//     }

//     return {
//       events: data
//     };
//   });
// };