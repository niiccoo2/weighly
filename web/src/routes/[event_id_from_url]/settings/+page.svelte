<script lang="ts">
  import { onMount } from 'svelte';
  import '$lib/styles_lightmode.css';
  import { supabase } from '$lib/supabaseClient';
  
  export let data: { eventId: number };
  console.log("Page component - received data:", data);
  console.log("Page component - eventId:", data.eventId);
  console.log("Page component - eventId type:", typeof data.eventId);
  
  const { eventId } = data;
  console.log("Page component - destructured eventId:", eventId);

  async function addUserToEvent(event_id: string, email: string) {
    console.log("Sending POST request for new event");
    const { data: { session } } = await supabase.auth.getSession();
    let response;
    if (!session) return;

    const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/add_user_to_event", {
      method: "POST",
      headers: {
        apikey: "sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz",
        Authorization: `Bearer ${session.access_token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ p_event_id: event_id, p_user_email: email })
    });

    response = await res.json();

    if (response != 0) {
      email_error = "Error adding user to event";

      setTimeout(() => {
        email_error = "";
      }, 3000);

      console.log(`Error adding ${email} to event ${event_id}. Response:`, response);
      return;
    } else {
      save_success = "Saved successfully!";

      console.log(`Added ${email} to event ${event_id}. Response:`, response);

      event_users = [...event_users, email];
      email_value = "";

      setTimeout(() => {
        save_success = "";
      }, 3000);
    }}

    async function fetchEventUsers(event_id: string) {
      console.log("Fetching event users");
      const { data: { session } } = await supabase.auth.getSession();
      let response: any = [];
      if (!session) return;

      const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/get_event_users", {
        method: "POST",
        headers: {
          apikey: "sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz",
          Authorization: `Bearer ${session.access_token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ p_event_id: event_id })
      });

      response = await res.json();

      if (response.error) {
        console.log(`Error fetching users for event ${event_id}. Response:`, response);
        return;
      } else {
        console.log(`Fetched users for event ${event_id}. Response:`, response);
        return response;
      }
    }

    async function removeUserFromEvent(event_id: string, email: string) {
      console.log("Sending POST request to remove user from event");
      const { data: { session } } = await supabase.auth.getSession();
      let response;
      if (!session) return;

      const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/remove_user_from_event", {
        method: "POST",
        headers: {
          apikey: "sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz",
          Authorization: `Bearer ${session.access_token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ p_event_id: event_id, p_user_email: email })
      });

      response = await res.json();

      if (response != 0) {
        email_error = "Error removing user from event";

        setTimeout(() => {
          email_error = "";
        }, 3000);

        console.log(`Error removing ${email} from event ${event_id}. Response:`, response);
        return;
      } else {
        save_success = "Removed successfully!";

        console.log(`Removed ${email} from event ${event_id}. Response:`, response);

        setTimeout(() => {
          save_success = "";
        }, 3000);
      }}
    
    async function getCustomURL(event_id: string) {
      console.log("Fetching custom URL");
      const { data: { session } } = await supabase.auth.getSession();
      let response: any = [];
      if (!session) return;

      const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/get_url_for_event", {
        method: "POST",
        headers: {
          apikey: "sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz",
          Authorization: `Bearer ${session.access_token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ p_event_id: event_id })
      });

      response = await res.json();

      if (response.error) {
        console.log(`Error fetching custom URL for event ${event_id}. Response:`, response);
        return;
      } else {
        console.log(`Fetched custom URL for event ${event_id}. Response:`, response);
        return response;
      }
    }

    async function setCustomURL(event_id: string, custom_url: string) {
      console.log("Sending POST request to set custom URL");
      const { data: { session } } = await supabase.auth.getSession();
      let response;

      if (!custom_url || custom_url.trim() === '') {
        custom_url_error = "Custom URL cannot be blank";
        setTimeout(() => { custom_url_error = ""; }, 3000);
        return;
      }
      
      if (/^\d+$/.test(custom_url)) {
        custom_url_error = "Custom URL cannot be only numbers";
        setTimeout(() => { custom_url_error = ""; }, 3000);
        return;
      }
      
      if (!/[a-zA-Z]/.test(custom_url)) {
        custom_url_error = "Custom URL must contain at least one letter";
        setTimeout(() => { custom_url_error = ""; }, 3000);
        return;
      }

      if (!session) return;

      const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/set_event_custom_url", {
        method: "POST",
        headers: {
          apikey: "sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz",
          Authorization: `Bearer ${session.access_token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ p_event_id: event_id, p_custom_url: custom_url })
      });

      response = await res.json();

      if (response != 0) {
        custom_url_error = "Error setting custom URL";

        setTimeout(() => {
          custom_url_error = "";
        }, 3000);

        console.log(`Error setting custom URL for event ${event_id}. Response:`, response);
        return;
      } else {
        custom_url_success = "Saved successfully!";

        custom_url_value = custom_url;
        custom_url_textbox_value = "";

        console.log(`Set custom URL for event ${event_id}. Response:`, response);

        setTimeout(() => {
          custom_url_success = "";
        }, 3000);
      }}
    
    async function removeCustomURL(event_id: string) {
      console.log("Sending POST request to remove custom URL");
      const { data: { session } } = await supabase.auth.getSession();
      let response;
      if (!session) return;

      const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/remove_event_custom_url", {
        method: "POST",
        headers: {
          apikey: "sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz",
          Authorization: `Bearer ${session.access_token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ p_event_id: event_id })
      });

      response = await res.json();

      if (response != 0) {
        custom_url_error = "Error removing custom URL";

        setTimeout(() => {
          custom_url_error = "";
        }, 3000);

        console.log(`Error removing custom URL for event ${event_id}. Response:`, response);
        return;
      } else {
        custom_url_success = "Removed successfully!";

        custom_url_value = "";

        console.log(`Removed custom URL for event ${event_id}. Response:`, response);

        setTimeout(() => {
          custom_url_success = "";
        }, 3000);
      }}
  
  let event_users: any[] = [];
  let custom_url_value = '';
  let loading_users = true;
  
  onMount(async () => {
    event_users = await fetchEventUsers(String(eventId));
    custom_url_value = await getCustomURL(String(eventId));
    loading_users = false;
  });
  
  let save_success = '';
  let email_id = 'email';
  let email_value = '';
  let email_error = '';

  let custom_url_id = 'custom_url';
  let custom_url_textbox_value = '';
  let custom_url_error = '';
  let custom_url_success = '';

</script>

<svelte:head>
	<title>Weighly</title>
</svelte:head>

<main class="flex flex-col items-center mt-8 w-full max-w-4xl mx-auto">
  <!-- Users -->
  <div class="w-full max-w-md p-4 card rounded-xl shadow-lg">
    <div class="flex flex-col items-center space-y-1">
      <p class="text-2xl font-semibold text-center">Users</p>
      <p class="text-center text-sm">Allow other users to add weights and administrate the event. Click on a user to remove them from the event.</p>

      {#if loading_users}
        <p>Loading users…</p>
      {:else if !event_users || event_users.length === 0}
        <p>No users added yet</p>
      {:else}
        <div class="w-full mt-2 space-y-1">
          {#each event_users as email}
            <button 
              on:click={() => { removeUserFromEvent(String(eventId), email); event_users = event_users.filter(e => e !== email); }}
              class="text-lg font-semibold text-center hover:underline w-full block cursor-pointer">
              {email}
            </button> 
          {/each}
        </div>
      {/if}


      <input
        id={email_id}
        bind:value={email_value}
        placeholder="Email"
        class="w-full rounded textbox focus:outline-none text-2xl thick_text px-2 py-1 mt-4"
        aria-invalid={email_error ? "true" : "false"}
        aria-describedby={email_error ? email_id + "-err" : undefined}
      />
      {#if email_error}
        <p id={email_id + "-err"} class="text-sm text-red-600 mt-1">{email_error}</p>
      {/if}
      {#if save_success}
        <p class="text-green-600 mt-2">{save_success}</p>
      {/if}

      <button 
      on:click={() => addUserToEvent(String(eventId), email_value)}
      class="accent_color_button rounded hover:scale-105 px-4 py-2 transition-transform cursor-pointer w-full mt-4 text-2xl">
      Add User
      </button>
    </div>
  </div>

  <!-- Custom URL -->
   <div class="w-full max-w-md p-4 card rounded-xl shadow-lg mt-8">
    <div class="flex flex-col items-center space-y-1">
      <p class="text-2xl font-semibold text-center">Custom URL</p>
      <p class="text-center text-sm">Set a custom slug for your event.</p>
      {#if custom_url_value != "0"}
        <a class="text-lg font-semibold text-center hover:underline w-full block cursor-pointer mt-2" href="https://weighly.app/{custom_url_value}">weighly.app/{custom_url_value}</a>
      {:else}
        <a class="text-lg font-semibold text-center hover:underline w-full block cursor-pointer mt-2" href="https://weighly.app/{eventId}">weighly.app/{eventId}</a>
      {/if}

      <input
        id={custom_url_id}
        bind:value={custom_url_textbox_value}
        placeholder="Custom URL"
        class="w-full rounded textbox focus:outline-none text-2xl thick_text px-2 py-1 mt-4"
        aria-invalid={custom_url_error ? "true" : "false"}
        aria-describedby={custom_url_error ? custom_url_id + "-err" : undefined}
      />
      {#if custom_url_error}
        <p id={custom_url_id + "-err"} class="text-sm text-red-600 mt-1">{custom_url_error}</p>
      {/if}
      {#if custom_url_success}
        <p class="text-green-600 mt-2">{custom_url_success}</p>
      {/if}

      <div class="flex gap-2 w-full mt-4">
        <button 
          on:click={() => setCustomURL(String(eventId), custom_url_textbox_value)}
          class="accent_color_button rounded hover:scale-105 px-4 py-2 transition-transform cursor-pointer flex-1 text-2xl">
          Set
        </button>
        <button 
          on:click={() => removeCustomURL(String(eventId))}
          class="accent_color_button rounded hover:scale-105 px-4 py-2 transition-transform cursor-pointer flex-1 text-2xl">
          Remove
        </button>
      </div>
    </div>
  </div>

  <!-- Save Weights Link -->
  <div class="w-full max-w-md p-4 card rounded-xl shadow-lg mt-8">
    <div class="flex flex-col items-center space-y-1">
      <p class="text-2xl font-semibold text-center">Save Weights</p>
      <p class="text-center text-sm">Go here to add weights to your event.</p>
      <a
        href="/{eventId}/add_weight"
        class="w-full max-w-md flex text-2xl items-center justify-center accent_color_button rounded hover:scale-105 px-4 py-2 leading-normal transition-transform block mt-4">
        Save Weights
      </a>
    </div>
  </div>
</main>