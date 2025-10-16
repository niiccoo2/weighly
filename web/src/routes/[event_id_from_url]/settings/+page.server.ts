import type { PageServerLoad } from './$types';
import { getEventId } from '$lib/eventID';
import { error } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ params }) => {
  const eventId = await getEventId(params.event_id_from_url);

  if (eventId === null) {
    throw error(404, 'Event not found');
  }

  return { eventId };
};
