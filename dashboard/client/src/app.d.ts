/// <reference types="@sveltejs/kit" />

// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
// and what to do when importing types
declare namespace App {
	// interface Locals {}
	// interface Platform {}
	// interface Session {}
	// interface Stuff {}
}

/* Guilds */
interface BaseGuild {
	id: string;
	name: string;
	icon: (string | undefined);
	icon_url: (string | undefined);
}

interface PartialGuild extends BaseGuild {
	can_manage: boolean;
	has_munchi: boolean;
}


interface Guild extends BaseGuild {
	approximate_member_count: number;
	roles: {id: string; name: string; color: string; position: number;}[];
	channels: {id: string; name: string; type: number;}[];

	// Munchi attributes
	welcome_message: string;
	welcome_channel: string;
	welcome_embed: {
		title?: string;
		description?: string;
	} ;

	goodbye_message: string;
	goodbye_channel: string;
	goodbye_embed: {
		title?: string;
		description?: string;
	};

	reaction_roles_message: {
		message: string,
		channel?: string,
		guild: string,
		type: string,
		roles: {
			[key: string]: any,
		}
	}[];
}
