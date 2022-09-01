--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Debian 14.5-1.pgdg110+1)
-- Dumped by pg_dump version 14.5 (Debian 14.5-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: rin_help; Type: TABLE; Schema: public; Owner: Rin
--

CREATE TABLE public.rin_help (
    uuid character varying NOT NULL,
    name character varying,
    description character varying,
    parent_name character varying,
    module character varying
);


ALTER TABLE public.rin_help OWNER TO "Rin";

--
-- Data for Name: rin_help; Type: TABLE DATA; Schema: public; Owner: Rin
--

COPY public.rin_help (uuid, name, description, parent_name, module) FROM stdin;
db492eb9-0a7f-4111-94b6-7e0b4b10a479	advice	Gives some advice from Adviceslip	None	advice
f42a9669-1eda-4039-8817-997468ec7bc5	anilist search anime	Searches for up to 25 animes on AniList	anilist search	anilist
ac3427dd-f054-4054-a04d-4ae3f9a23fb1	anilist search manga	Searches for up to 25 mangas on AniList	anilist search	anilist
ef378b08-625d-4557-99f0-99051bdffc8f	anilist search tags	Searches up to 25 animes and mangas based on the given tag	anilist search	anilist
a3b95cf6-0ab2-4580-9e60-3300e83a4b1a	anilist search users	Provides up to 25 users from the given username	anilist search	anilist
b908b5ad-c7de-47bb-a5fb-2fd40b529861	anilist search characters	Searches up to 25 anime characters on AniList	anilist search	anilist
e4fed73e-11eb-4766-9dc6-20e1851df09b	anilist search actors	Searches for up to 25 voice actors or staff that have worked on an anime and/or its characters	anilist search	anilist
484f0d3e-e9e9-46a2-870a-dcc0f27f207d	blue-alliance matches team	Returns the general info for each match that a team was in during the given event	blue-alliance matches	blue-alliance
829a8b3b-7ff7-46e6-9777-924d40b3a226	blue-alliance matches all	Returns all of the matches for an FRC event	blue-alliance matches	blue-alliance
9724e22c-fc22-49ba-8156-aa46f213359d	blue-alliance teams info	Returns info about an FRC team	blue-alliance teams	blue-alliance
e3a44388-250e-4f53-8675-9d9711f1f5cc	blue-alliance teams events	Returns what events an FRC team has attended	blue-alliance teams	blue-alliance
2c797716-79c2-4260-b1da-7c3796ac6a3b	blue-alliance rankings	Returns the event ranking	blue-alliance	blue-alliance
9d1b61f7-cf34-4ae2-bd9b-2ec16aefeba9	discordbots search bots	Searches for up to 25 of any Discord Bots listed on discord.bots.gg	discordbots search	discord-bots
f3989ec5-a7cc-4af3-9fd9-8f9361d56052	frc events list	Returns events for the current FRC season	frc events	first-frc-events
c0b3ada9-0e04-4924-baec-3f4fac3eb8eb	frc events top	Returns the top 25 FRC teams within a given event	frc events	first-frc-events
1db1fde0-b8de-40c6-8755-e039116b9fa7	frc events schedule	Returns the schedule for a given FRC event	frc events	first-frc-events
03732848-dfa6-4625-8fba-55428103c87e	frc events alliances	Returns the alliances within an given event	frc events	first-frc-events
df797700-2255-498f-83fc-958bf7f1f229	frc season	Returns the season summary for the current FRC season	frc	first-frc-events
80d32580-a41a-4fd3-9329-6db40f11969e	frc score	Returns the FRC team's score details for a given event	frc	first-frc-events
d2d68a45-5faa-4dc5-b40f-1f99a1326fff	frc results	Returns the FRC team's results for a given event (the results of each matches that the team is in)	frc	first-frc-events
cfa269b5-4ed6-44fe-a408-9dc6fe4bf551	github user one	Returns info on a user in GitHub	github user	github
67141f19-7085-4791-b708-ae8edf0202ae	github search repos	Searches for repositories on GitHub	github search	github
d0913d42-c583-4235-87ef-01cea48117f2	github search users	Searches for users on GitHub	github search	github
f2e503ad-268e-4b5f-8c55-5956a67876e2	github issues all	Gets all issues from a repo	github issues	github
00a07fd9-b1e8-4b3a-8741-f84cc55fd164	github issues one	Gets info about one issue on any repo on GitHub	github issues	github
65f8ac1f-ff95-4180-9d0f-b718d5c6d9f3	github releases list	Lists out up to 25 releases of any repo	github releases	github
18bea5c2-13f2-4063-995d-5dcdb83c22bd	github releases latest	Gets the latest published full release for any repo	github releases	github
916fe360-b710-41e6-9961-0a11432f9c6c	github repo	Returns info about any repo	github	github
ccc04191-4b79-44ff-8a13-903c2f28f4ae	hypixel count	Returns the amount of players in each game server	hypixel	hypixel
15ce5cf4-d6b1-48da-8fa4-ab32377edba0	hypixel punishments	Shows the stats for the amount of punishments given on Hypixel (All Users)	hypixel	hypixel
ea814cf1-0145-4c53-956f-968b5dead4bc	jisho search	Searches for words on Jisho	jisho	jisho
5b66a753-d9eb-44e1-a487-d2e66673ef96	mangadex search manga	Searches for up to 25 manga on MangaDex	mangadex search	mangadex
4e147e4a-59f3-4afa-b6d8-627dceb1ef0d	mangadex search scanlation	Returns up to 25 scanlation groups via the name given	mangadex search	mangadex
d97a5b57-e415-4e47-88c0-e784c344af1b	mangadex search author	Returns up to 25 authors and their info	mangadex search	mangadex
90e88c37-d39d-47c3-8b12-fe29b6c0ac07	mangadex random	Returns an random manga from MangaDex	mangadex	mangadex
43c78afe-c5b6-46f3-9bf1-6ab1fdc2286d	minecraft java	Checks and returns info about the given Minecraft Java server	minecraft	mcsrvstats
3124accb-dfe3-42bd-87fb-e900be672e8d	minecraft bedrock	Returns the status and info of any Bedrock or Geyser-compatible server	minecraft	mcsrvstats
8e00ab3a-cdec-4f57-8a30-48018db93b65	modrinth mod list	Gets info about the mod requested	modrinth mod	modrinth
f1290a5d-55eb-4ff5-90ac-7cc527a78f99	modrinth versions all	Lists out all of the versions for a mod	modrinth versions	modrinth
026afed7-a047-4429-aead-46fe17e50f72	modrinth user search	Returns info on the given user	modrinth user	modrinth
ee35c896-f584-4ece-9bd0-a8176fb24b18	modrinth user projects	Returns info on the given user's projects	modrinth user	modrinth
f8fe42a4-2923-48c2-9263-a75b203cd2d0	modrinth search	Searches for up to 25 mods on Modrinth	modrinth	modrinth
90b2c4c5-7398-4007-bc80-31a57c2f25f0	mal search anime	Fetches up to 25 anime from MAL	mal search	myanimelist
12d0a31f-2e6a-48d6-85c2-2d725a6e05d5	mal search manga	Fetches up to 25 mangas from MAL	mal search	myanimelist
dc9b8ce7-4971-4967-9293-441db96d14f9	mal seasons list	Returns animes for the given season and year	mal seasons	myanimelist
2929ef61-323b-4d67-86ea-5c1e3aa3b58a	mal seasons upcoming	Returns anime for the upcoming season	mal seasons	myanimelist
971b24b0-16e7-4491-8fb3-826c0203647b	mal random anime	Fetches a random anime from MAL	mal random	myanimelist
aa2e028f-acc5-4489-8148-79c5c08aa8dc	mal random manga	Fetches a random manga from MAL	mal random	myanimelist
0af9ad6d-7fd3-4bc3-b65e-45f53e67796a	mal user	Returns info about the given user on MAL	mal	myanimelist
31756229-cc0c-4bfb-8f56-84b1b3f63748	reddit users info	Provides info about a Redditor	reddit users	reddit
2b45e45e-ea39-4712-a740-2bc2313c6849	reddit users comments	Returns up to 25 comments from a given Redditor	reddit users	reddit
ef497980-8c83-4a87-8e58-4994be316f0d	reddit search	Searches on Reddit for Content	reddit	reddit
3380fdf4-18e4-4ef4-93cf-2470a871e625	reddit memes	Gets some memes from Reddit	reddit	reddit
0a6cfc9f-7c45-47b5-b805-6ba370773280	reddit feed	Returns up to 25 reddit posts based on the current filter	reddit	reddit
4132a9e6-1487-4904-82c8-ea17ba62a3a8	reddit egg_irl	Literally just shows you r/egg_irl posts. No comment.	reddit	reddit
5c17f56a-a925-4d5e-97a2-1c76032e0e09	spigot search	Finds up to 25 plugins matching the name of the given plugin	spigot	spiget
6ee70460-5980-4076-aa70-be1db9469925	tenor search multiple	Searches for up to 25 gifs on Tenor	tenor search	tenor
f20b6b63-7907-4367-b3a2-f9c4ac446388	tenor search one	Searches for a single gif on Tenor	tenor search	tenor
96879a29-ba83-444e-9698-32c80f5b47f0	tenor search suggestions	Gives a list of suggested search terms based on the given topic	tenor search	tenor
3a7322fe-36e2-48e7-909d-3911782399b3	tenor trending terms	Gives a list of trending search terms on Tenor	tenor trending	tenor
58428757-a20e-4959-bb81-812a60553bd3	tenor featured	Returns up to 25 featured gifs from Tenor	tenor	tenor
f43b1a65-633e-4f26-8ded-c20b2b42b0a5	tenor random	Gives out 25 random gifs from Tenor based on given search term	tenor	tenor
0026335e-c8cc-4404-9fb5-995fcbc1475e	topgg search bot	Searches up to 25 bots on Top.gg	topgg search	top-gg
2fa37f66-2f2b-4959-a4c5-c90f6e7ba0bd	twitch search channels	Returns up to 25 streams from the given channel	twitch search	twitch
76a3437a-a5e5-4a61-963e-d88968b8c8a9	twitch top games	Gets the top 100 games on Twitch	twitch top	twitch
daa1509d-e01c-4ab2-b737-054d9c9db5fb	twitch streams	Gets up to 25 active streams on Twitch	twitch	twitch
6178b7c1-44d1-4f14-8df2-a0cc8a732706	twitter search	Returns up to 25 recent tweets from the given the Twitter user	twitter	twitter
b14deb18-c910-48b3-b3b0-a9c7a7498bd8	invite	Invite links for Rin	None	misc
b533c69f-50b6-41ea-87e5-1524c64a274b	info	Info about Rin	None	misc
fc0dec78-82af-4c89-a9e4-7768cdd9539c	help	The Help Page for Rin	None	misc
dfee9310-b3a8-4383-95b7-e08ddbecb318	twitter user	Returns Info about the given Twitter user	twitter	twitter
a76dcdca-2064-4d3d-a872-3e423578c440	waifu random one	Gets one random waifu pics	waifu random	waifu
605ca53d-0e5b-44da-a080-7d86d7a967a1	waifu random many	Returns many random waifu pics	waifu random	waifu
847352d5-ba81-4eaa-bfb4-7ce707d4d9d8	waifu pics	Returns a random image of a waifu from waifu.pics	waifu	waifu
7e295c3c-bc64-4d6f-9df0-4a2abc9c9d55	youtube search	Finds up to 25 videos on YouTube based on the given search term	youtube	youtube
6bb254ec-7406-45aa-856a-cd118ab7f6fb	youtube channel	Returns info about the given YouTube channel	youtube	youtube
f7ec6849-c6a1-4e99-88db-96d5149ba173	youtube playlist	Returns up to 25 YouTube playlists based on the given YT channel	youtube	youtube
47502cdb-4403-4190-85e6-392ea86fe8c5	botinfo	Returns Stats for Rin	None	misc
ebe2d97f-a069-4096-b2a8-f7ca90cbf757	version	Returns Current Version of Rin	None	misc
fb240182-4523-4cf9-9215-1762dd88032b	uptime	Returns Uptime for Rin	None	misc
2477d82f-de02-4467-ac31-5bb7cbe9f717	ping	Measures the ping of Rin	None	misc
\.


--
-- Name: rin_help rin_help_pkey; Type: CONSTRAINT; Schema: public; Owner: Rin
--

ALTER TABLE ONLY public.rin_help
    ADD CONSTRAINT rin_help_pkey PRIMARY KEY (uuid);


--
-- PostgreSQL database dump complete
--

