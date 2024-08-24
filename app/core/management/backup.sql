--
-- PostgreSQL database dump
--

-- Dumped from database version 13.16
-- Dumped by pg_dump version 13.16

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
-- Name: auth_group; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO devuser;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO devuser;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO devuser;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO devuser;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO devuser;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO devuser;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO devuser;

--
-- Name: core_drill; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.core_drill (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    "maxScore" integer NOT NULL,
    instructions text NOT NULL,
    image character varying(255) NOT NULL,
    type character varying(255) NOT NULL,
    attempts integer,
    layouts integer,
    "layoutMaxScore" integer,
    "createdAt" timestamp with time zone NOT NULL,
    "createdBy_id" bigint,
    skills jsonb,
    "tableSetup_id" bigint
);


ALTER TABLE public.core_drill OWNER TO devuser;

--
-- Name: core_drill_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.core_drill_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_drill_id_seq OWNER TO devuser;

--
-- Name: core_drill_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.core_drill_id_seq OWNED BY public.core_drill.id;


--
-- Name: core_drillscore; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.core_drillscore (
    id bigint NOT NULL,
    score integer NOT NULL,
    "maxScore" integer NOT NULL,
    user_id bigint NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    drill_id bigint NOT NULL
);


ALTER TABLE public.core_drillscore OWNER TO devuser;

--
-- Name: core_drillscore_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.core_drillscore_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_drillscore_id_seq OWNER TO devuser;

--
-- Name: core_drillscore_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.core_drillscore_id_seq OWNED BY public.core_drillscore.id;


--
-- Name: core_drillset; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.core_drillset (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    "createdBy_id" bigint NOT NULL
);


ALTER TABLE public.core_drillset OWNER TO devuser;

--
-- Name: core_drillset_drills; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.core_drillset_drills (
    id bigint NOT NULL,
    drillset_id bigint NOT NULL,
    drill_id bigint NOT NULL
);


ALTER TABLE public.core_drillset_drills OWNER TO devuser;

--
-- Name: core_drillset_drills_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.core_drillset_drills_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_drillset_drills_id_seq OWNER TO devuser;

--
-- Name: core_drillset_drills_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.core_drillset_drills_id_seq OWNED BY public.core_drillset_drills.id;


--
-- Name: core_drillset_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.core_drillset_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_drillset_id_seq OWNER TO devuser;

--
-- Name: core_drillset_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.core_drillset_id_seq OWNED BY public.core_drillset.id;


--
-- Name: core_drillsetscore; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.core_drillsetscore (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    drill_set_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.core_drillsetscore OWNER TO devuser;

--
-- Name: core_drillsetscore_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.core_drillsetscore_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_drillsetscore_id_seq OWNER TO devuser;

--
-- Name: core_drillsetscore_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.core_drillsetscore_id_seq OWNED BY public.core_drillsetscore.id;


--
-- Name: core_drillsetscore_scores; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.core_drillsetscore_scores (
    id bigint NOT NULL,
    drillsetscore_id bigint NOT NULL,
    drillscore_id bigint NOT NULL
);


ALTER TABLE public.core_drillsetscore_scores OWNER TO devuser;

--
-- Name: core_drillsetscore_scores_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.core_drillsetscore_scores_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_drillsetscore_scores_id_seq OWNER TO devuser;

--
-- Name: core_drillsetscore_scores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.core_drillsetscore_scores_id_seq OWNED BY public.core_drillsetscore_scores.id;


--
-- Name: core_user; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.core_user (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    email character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    is_staff boolean NOT NULL
);


ALTER TABLE public.core_user OWNER TO devuser;

--
-- Name: core_user_groups; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.core_user_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.core_user_groups OWNER TO devuser;

--
-- Name: core_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.core_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_user_groups_id_seq OWNER TO devuser;

--
-- Name: core_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.core_user_groups_id_seq OWNED BY public.core_user_groups.id;


--
-- Name: core_user_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.core_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_user_id_seq OWNER TO devuser;

--
-- Name: core_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.core_user_id_seq OWNED BY public.core_user.id;


--
-- Name: core_user_user_permissions; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.core_user_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.core_user_user_permissions OWNER TO devuser;

--
-- Name: core_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.core_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_user_user_permissions_id_seq OWNER TO devuser;

--
-- Name: core_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.core_user_user_permissions_id_seq OWNED BY public.core_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO devuser;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO devuser;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO devuser;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO devuser;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO devuser;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: devuser
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO devuser;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: devuser
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: devuser
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO devuser;

--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: core_drill id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drill ALTER COLUMN id SET DEFAULT nextval('public.core_drill_id_seq'::regclass);


--
-- Name: core_drillscore id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillscore ALTER COLUMN id SET DEFAULT nextval('public.core_drillscore_id_seq'::regclass);


--
-- Name: core_drillset id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillset ALTER COLUMN id SET DEFAULT nextval('public.core_drillset_id_seq'::regclass);


--
-- Name: core_drillset_drills id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillset_drills ALTER COLUMN id SET DEFAULT nextval('public.core_drillset_drills_id_seq'::regclass);


--
-- Name: core_drillsetscore id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillsetscore ALTER COLUMN id SET DEFAULT nextval('public.core_drillsetscore_id_seq'::regclass);


--
-- Name: core_drillsetscore_scores id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillsetscore_scores ALTER COLUMN id SET DEFAULT nextval('public.core_drillsetscore_scores_id_seq'::regclass);


--
-- Name: core_user id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_user ALTER COLUMN id SET DEFAULT nextval('public.core_user_id_seq'::regclass);


--
-- Name: core_user_groups id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_user_groups ALTER COLUMN id SET DEFAULT nextval('public.core_user_groups_id_seq'::regclass);


--
-- Name: core_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.core_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add user	6	add_user
22	Can change user	6	change_user
23	Can delete user	6	delete_user
24	Can view user	6	view_user
25	Can add Token	7	add_token
26	Can change Token	7	change_token
27	Can delete Token	7	delete_token
28	Can view Token	7	view_token
29	Can add token	8	add_tokenproxy
30	Can change token	8	change_tokenproxy
31	Can delete token	8	delete_tokenproxy
32	Can view token	8	view_tokenproxy
33	Can add drill score	9	add_drillscore
34	Can change drill score	9	change_drillscore
35	Can delete drill score	9	delete_drillscore
36	Can view drill score	9	view_drillscore
37	Can add drill	10	add_drill
38	Can change drill	10	change_drill
39	Can delete drill	10	delete_drill
40	Can view drill	10	view_drill
41	Can add skill	11	add_skill
42	Can change skill	11	change_skill
43	Can delete skill	11	delete_skill
44	Can view skill	11	view_skill
45	Can add drill set	12	add_drillset
46	Can change drill set	12	change_drillset
47	Can delete drill set	12	delete_drillset
48	Can view drill set	12	view_drillset
49	Can add drill set score	13	add_drillsetscore
50	Can change drill set score	13	change_drillsetscore
51	Can delete drill set score	13	delete_drillsetscore
52	Can view drill set score	13	view_drillsetscore
53	Can add table setup	14	add_tablesetup
54	Can change table setup	14	change_tablesetup
55	Can delete table setup	14	delete_tablesetup
56	Can view table setup	14	view_tablesetup
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
bb903a31e8e359670fb6bff5e816956628448fa8	2024-07-10 21:14:33.534299+00	2
2d2a78fa62e8681e8ffe7c0b8254bd154928f09e	2024-07-14 13:07:05.333136+00	1
e2a1c040da6fb83781e01a9d663c449a4c1a4dce	2024-07-14 18:34:45.085452+00	18
17700fad2e25528ef2ad4a03f4598b138c86a427	2024-07-14 18:56:00.379539+00	19
5b40016d530df0cb54577b7437688ab5513ae554	2024-08-11 13:01:23.174118+00	20
\.


--
-- Data for Name: core_drill; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.core_drill (id, name, "maxScore", instructions, image, type, attempts, layouts, "layoutMaxScore", "createdAt", "createdBy_id", skills, "tableSetup_id") FROM stdin;
45	Cut Shot	10	• Start with the cue ball (CB) in position 4. Each time you pocket the object ball (OB), advance\n  the CB one position (e.g., from 4 to 5); and with each miss, move down by one number (e.g., from\n  4 to 3). If you succeed at position 7 or miss at position 1, stay at that position. <br />\n  • Continue for 10 shots total unless you already have a guaranteed score of 10 (e.g., you can\n  stop if you make the first eight shots). <br />	https://res.cloudinary.com/dnc2xvyms/image/upload/v1716658046/Screenshot_2024-05-25_at_1.24.29_PM_wdum1u.png	progressive	\N	\N	\N	2024-08-24 02:30:34.405202+00	\N	["aim"]	\N
46	Stop Shot	10	• The OB must be pocketed, and the stopped CB must overlap at least part of the ghost-ball\n  (GB) outline. <br />\n  • The CB is allowed to contact the cushion. <br />\n  • You are allowed to vary the CB and OB positions away from the rail as long as the CB\n  remains within one diamond of the rail. <br />\n  • If you end up in position 1 you are allowed to place the CB anywhere between positions\n  1 and 2. This will allow you to comfortably avoid a double hit.	https://res.cloudinary.com/dnc2xvyms/image/upload/v1716658045/Screenshot_2024-05-25_at_1.24.40_PM_crpuf3.png	progressive	\N	\N	\N	2024-08-24 02:30:34.406896+00	\N	["position", "cue ball control"]	\N
47	Follow Shot	10	• The rectangular target can be printed and cut out from a template on the website. It is an\n  8.5”x11” sheet of paper with the center removed, leaving a 1” border. <br />\n  • The CB and OB are always 1 diamond apart. <br />\n  • The OB must be pocketed and the CB must end up within or overlapping the target for\n  success. <br />\n  • Both the CB and OB are allowed to contact cushions. <br />\n  • You are allowed to vary the CB and OB positions away from the rail as long as the CB\n  remains within one diamond of the rail.	https://res.cloudinary.com/dnc2xvyms/image/upload/v1716658045/Screenshot_2024-05-25_at_1.24.52_PM_vojx3m.png	progressive	\N	\N	\N	2024-08-24 02:30:34.407555+00	\N	["position", "cue ball control"]	\N
48	Draw Shot	10	• You must pocket the OB and the CB must end up within the 2x1 diamond rectangle adjacent to\n  the side pocket. The CB center (or resting point on the cloth) must be inside of the rectangle\n  border. <br />\n  • The CB is allowed to hit the side cushion. <br />\n  • The target rectangle area is fixed and does not move with the CB. <br />\n  • You are allowed to vary the CB and OB positions away from the rail as long as the CB\n  remains within one diamond of the rail. <br />\n  • If you end up in position 1 you are allowed to place the CB anywhere between positions\n  1 and 2. This will allow you to comfortably avoid a double hit.	https://res.cloudinary.com/dnc2xvyms/image/upload/v1716658047/Screenshot_2024-05-25_at_1.25.07_PM_dshtnm.png	progressive	\N	\N	\N	2024-08-24 02:30:34.408367+00	\N	["position", "cue ball control"]	\N
49	Stun Shot	10	• The OB must be pocketed and the CB must end up within or overlapping the target for\n  success. <br />\n  • Start with the target in position 4. Note that the target center and orientation for position 4 is\n  different from the others, with the long edge against the rail cushion. The target centers for the\n  other positions are aligned with the long-rail diamonds. <br />\n  • The CB must head straight to the target (without cushion contact) for positions 1, 2, and 3, and\n  the CB must rebound off the end rail for target positions 5, 6, and 7. Cushion contact is\n  allowed, but not required, for target position 4. <br />\n  • With each success, advance the target one position (e.g., from 4 to 5); and with each miss,\n  move the target back (e.g., from 4 to 3). If you succeed at position 7 or miss at position 1,\n  keep the target at that position. <br />\n  • Continue for 10 shots total. <br />\n  • Adjust the target position after the 10th shot based on the outcome, but not below 1 or above 7. <br />\n  For example if you succeed on the 10th shot at 6, the final position is 7; and if you miss the 10th\n  shot at 6, the final position is 5.	https://res.cloudinary.com/dnc2xvyms/image/upload/v1716658048/Screenshot_2024-05-25_at_1.25.37_PM_t6kvnj.png	progressive	\N	\N	\N	2024-08-24 02:30:34.409137+00	\N	["position", "cue ball control"]	\N
50	Ball Pocketing	10	• Shoot all 5 shots from each CB position, attempting to pocket the OBs as shown. <br />\n  • You get 1 attempt at each of the 10 shots. You are not allowed to scratch. <br />\n  • This and the remaining drills are not “progressive.” Instead, you attempt each shot, regardless\n  of the previous shot’s outcome.	https://res.cloudinary.com/dnc2xvyms/image/upload/v1716658044/Screenshot_2024-05-25_at_1.26.04_PM_dtnzhq.png	standard	\N	\N	\N	2024-08-24 02:30:34.409726+00	\N	["pocketing, aim"]	\N
51	Wagon Wheel	20	• Pocket the OB and have the CB hit each of the rail target balls. <br />\n  • You score a point by pocketing the OB and hitting the current target ball. <br />\n  • Rail-first contact, adjacent to the target ball, is allowed, but you are not allowed to hit any other\n  cushion on the way to the target ball. <br />\n  • Take 2 attempts at each target ball. <br />\n  • Remove target balls completed, and reposition any remaining balls that are disturbed.	https://res.cloudinary.com/dnc2xvyms/image/upload/v1716658047/Screenshot_2024-05-25_at_1.26.47_PM_iup4bj.png	standard	\N	\N	\N	2024-08-24 02:30:34.410331+00	\N	["position", "cue ball control"]	\N
52	Landing Zone	20	• The OB (1 ball) must be pocketed and the CB must end up within or overlapping each of the\n  targets. <br />\n  • Take 4 attempts at each target, scoring 1 point for each success. <br />\n  • Take any path to the target you desire, off as many rails as you chose or straight to the target.	https://res.cloudinary.com/dnc2xvyms/image/upload/v1716658043/Screenshot_2024-05-25_at_1.26.55_PM_s1pcti.png	standard	\N	\N	\N	2024-08-24 02:30:34.410807+00	\N	["position", "cue ball control"]	\N
53	Line of Balls (I)	4	• Pocket the balls in rotation (i.e., in numerical order) in any pockets without scratching or\n  contacting any of the remaining balls. <br />\n  • If you disturb a ball while pocketing one, the one pocketed counts, but the run ends <br />\n  • Shoot the drill twice and use the higher score of the two attempts <br />	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717526801/Screenshot_2024-06-04_at_2.44.12_PM_zraapz.png	attempt	\N	\N	\N	2024-08-24 02:30:34.411282+00	\N	["position", "cue ball control", "pattern play"]	\N
54	Rail Cut Shot (I)	7	• Do the drill twice, shooting the balls in any order, and use the higher score of the two attempts. <br />\n  • You are not allowed to scratch, shoot combinations, or disturb any of the remaining balls. <br />	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717537740/Screenshot_2024-06-04_at_5.48.55_PM_pbytyt.png	attempt	\N	\N	\N	2024-08-24 02:30:34.41214+00	\N	["aim", "pattern play"]	\N
55	Safety (I)	6	• Take two attempts from each CB position, getting 1 point for each successful snooker, where\n  the OB is hidden from the CB with no direct path of contact between the balls. <br />\n  • The 1 ball may not be pocketed. <br />\n  • You are allowed to contact the balls in the obstacle cluster, but all of them must remain within\n  or overlapping the target.  <br />	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717740461/Screenshot_2024-06-07_at_2.07.26_AM_z3kjxq.png	standard	\N	\N	\N	2024-08-24 02:30:34.413978+00	\N	["cue ball control", "safety"]	\N
56	Kick Shot (I)	3	• Kick at each OB off the same long rail (as shown), with the CB in the same starting position for\n  each kick, getting 1 point for each successful and legal shot (i.e., no scratch, ball to rail).	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717798362/Screenshot_2024-06-07_at_6.12.36_PM_kkxj24.png	standard	\N	\N	\N	2024-08-24 02:30:34.41479+00	\N	["kicking"]	\N
57	Bank Shot (I)	3	• With CB in hand for each shot, bank each ball cross side. <br />\n  • You receive 1 point for each bank pocketed legally (w/o scratching).	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717803152/Screenshot_2024-06-07_at_7.32.26_PM_daom3s.png	standard	\N	\N	\N	2024-08-24 02:30:34.415315+00	\N	["banking", "potting"]	\N
58	Elevated Cue (I)	3	• Pocket each OB from the indicated CB position without scratching.	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717807988/Screenshot_2024-06-07_at_8.53.00_PM_ibqkpx.png	standard	\N	\N	\N	2024-08-24 02:30:34.415921+00	\N	["cueing", "potting"]	\N
59	Jump/Massé (I)	3	• You get 1 point for each successful shot (OB pocketed, no obstacle-ball contact) of 3 attempts. <br />\n  • You are allowed to scratch. <br />\n  • Remove one of the obstacle balls if attempting to curve rather than jump <br />	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717817781/Screenshot_2024-06-07_at_11.36.11_PM_ojfhlc.png	standard	\N	\N	\N	2024-08-24 02:30:34.416477+00	\N	["cueing", "potting"]	\N
60	Break	5	• Break three times and score each break, awarding 1 point for each of the following: <br />\n  a.) no scratch. <br />\n  b.) no scratch, and the CB not driven to a cushion. <br />\n  c.) no scratch, and the center of the CB remains within the center 4-diamond target zone\n  during the entire break. <br />\n  d.) no scratch and 1 or more balls pocketed. <br />\n  e.) no scratch and 3 or more OBs either pocketed and/or driven above the head string. <br />	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717824006/Screenshot_2024-06-08_at_1.19.02_AM_pg8lpq.png	attempt	\N	\N	\N	2024-08-24 02:30:34.417045+00	\N	["break"]	\N
61	Line of Balls (II)	7	• Pocket the balls in rotation (i.e., in numerical order) in any pockets without scratching or\n  contacting any of the remaining balls. <br />\n  • If you disturb a ball while pocketing one, the one pocketed counts, but the run ends <br />\n  • Shoot the drill twice and use the higher score of the two attempts <br />	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717527553/Screenshot_2024-06-04_at_2.59.04_PM_obzasb.png	attempt	\N	\N	\N	2024-08-24 02:30:34.417521+00	\N	["position", "cue ball control", "pattern play"]	\N
62	Rail Cut Shot (II)	11	• Do the drill twice, shooting the balls in any order, and use the higher score of the two attempts. <br />\n  • You are not allowed to scratch, shoot combinations, or disturb any of the remaining balls. <br />	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717537849/Screenshot_2024-06-04_at_5.50.42_PM_oq3gra.png	attempt	\N	\N	\N	2024-08-24 02:30:34.418082+00	\N	["aim", "pattern play"]	\N
63	Safety (II)	10	• Take two attempts from each CB position, getting 1 point for each successful snooker, where\n  the OB is hidden from the CB with no direct path of contact between the balls. <br />\n  • The 1 ball may not be pocketed. <br />\n  • You are allowed to contact the balls in the obstacle cluster, but all of them must remain within\n  or overlapping the target.  <br />	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717795677/Screenshot_2024-06-07_at_5.27.12_PM_zgrxdy.png	standard	\N	\N	\N	2024-08-24 02:30:34.41978+00	\N	["cue ball control", "safety"]	\N
64	Kick Shot (II)	5	• Shots 1-4: Kick at each OB off the same long rail (as shown), with the CB in the same starting\n  position for each kick, getting 1 point for each successful and legal shot (i.e., no scratch, ball to\n  rail). <br />\n  • Shot 5: With CB in hand, kick off any two rails at the 5 ball.	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717798483/Screenshot_2024-06-07_at_6.14.25_PM_nnf6bx.png	standard	\N	\N	\N	2024-08-24 02:30:34.420797+00	\N	["kicking"]	\N
65	Bank Shot (II)	5	• With CB in hand for each shot, bank each ball cross side. <br />\n  • You receive 1 point for each bank pocketed legally (w/o scratching).	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717803280/Screenshot_2024-06-07_at_7.34.25_PM_qcjbqx.png	standard	\N	\N	\N	2024-08-24 02:30:34.421577+00	\N	["banking", "potting"]	\N
66	Elevated Cue (II)	5	• Pocket each OB from the indicated CB position without scratching.	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717808084/Screenshot_2024-06-07_at_8.54.34_PM_sghsen.png	standard	\N	\N	\N	2024-08-24 02:30:34.422255+00	\N	["cueing", "potting"]	\N
67	Jump/Massé (II)	5	• You get 1 point for each successful shot (OB pocketed, no obstacle-ball contact) of 3 attempts. <br />\n  • You are allowed to scratch. <br />\n  • Remove one of the obstacle balls if attempting to curve rather than jump <br />	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717818010/Screenshot_2024-06-07_at_11.40.00_PM_uidmmy.png	standard	\N	\N	\N	2024-08-24 02:30:34.42328+00	\N	["cueing", "potting"]	\N
68	Line of Balls (III)	10	• Pocket the balls in rotation (i.e., in numerical order) in any pockets without scratching or\n  contacting any of the remaining balls. <br />\n  • If you disturb a ball while pocketing one, the one pocketed counts, but the run ends <br />\n  • Shoot the drill twice and use the higher score of the two attempts <br />	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717527553/Screenshot_2024-06-04_at_2.59.04_PM_obzasb.png	attempt	\N	\N	\N	2024-08-24 02:30:34.423871+00	\N	["position", "cue ball control", "pattern play"]	\N
69	Rail Cut Shot (III)	15	• Do the drill twice, shooting the balls in any order, and use the higher score of the two attempts. <br />\n  • You are not allowed to scratch, shoot combinations, or disturb any of the remaining balls. <br />	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717537849/Screenshot_2024-06-04_at_5.50.42_PM_oq3gra.png	attempt	\N	\N	\N	2024-08-24 02:30:34.424446+00	\N	["aim", "pattern play"]	\N
70	Safety (III)	14	• Take two attempts from each CB position, getting 1 point for each successful snooker, where\n  the OB is hidden from the CB with no direct path of contact between the balls. <br />\n  • The 1 ball may not be pocketed. <br />\n  • You are allowed to contact the balls in the obstacle cluster, but all of them must remain within\n  or overlapping the target.  <br />	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717796173/Screenshot_2024-06-07_at_5.36.08_PM_jtt0zq.png	standard	\N	\N	\N	2024-08-24 02:30:34.426192+00	\N	["cue ball control", "safety"]	\N
71	Kick Shot (III)	7	• Shots 1-4: Kick at each OB off the same long rail (as shown), with the CB in the same starting\n  position for each kick, getting 1 point for each successful and legal shot (i.e., no scratch, ball to\n  rail). <br />\n  • Shots 5,6: With CB in hand on each shot, kick off any two rails at the 5 ball and the 6 ball. <br />\n  • Shot 7: With CB in hand, kick off any three rails at the 7 ball.	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717798483/Screenshot_2024-06-07_at_6.14.25_PM_nnf6bx.png	standard	\N	\N	\N	2024-08-24 02:30:34.426905+00	\N	["kicking"]	\N
72	Bank Shot (III)	7	• With CB in hand for each shot, bank each ball cross side. <br />\n  • You receive 1 point for each bank pocketed legally (w/o scratching).	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717803360/Screenshot_2024-06-07_at_7.35.52_PM_uqpnq5.png	standard	\N	\N	\N	2024-08-24 02:30:34.427967+00	\N	["banking", "potting"]	\N
73	Elevated Cue (III)	7	• Pocket each OB from the indicated CB position without scratching.	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717808136/Screenshot_2024-06-07_at_8.55.26_PM_jwijyu.png	standard	\N	\N	\N	2024-08-24 02:30:34.428677+00	\N	["cueing", "potting"]	\N
74	Jump/Massé (III)	7	• You get 1 point for each successful shot (OB pocketed, no obstacle-ball contact) of 3 attempts. <br />\n  • You are allowed to scratch. <br />\n  • Remove one of the obstacle balls if attempting to curve rather than jump <br />	https://res.cloudinary.com/dnc2xvyms/image/upload/v1717818147/Screenshot_2024-06-07_at_11.42.15_PM_lfhdac.png	standard	\N	\N	\N	2024-08-24 02:30:34.429264+00	\N	["cueing", "potting"]	\N
\.


--
-- Data for Name: core_drillscore; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.core_drillscore (id, score, "maxScore", user_id, "createdAt", drill_id) FROM stdin;
\.


--
-- Data for Name: core_drillset; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.core_drillset (id, name, "createdBy_id") FROM stdin;
\.


--
-- Data for Name: core_drillset_drills; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.core_drillset_drills (id, drillset_id, drill_id) FROM stdin;
\.


--
-- Data for Name: core_drillsetscore; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.core_drillsetscore (id, created_at, updated_at, drill_set_id, user_id) FROM stdin;
\.


--
-- Data for Name: core_drillsetscore_scores; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.core_drillsetscore_scores (id, drillsetscore_id, drillscore_id) FROM stdin;
\.


--
-- Data for Name: core_user; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.core_user (id, password, last_login, is_superuser, email, name, is_active, is_staff) FROM stdin;
2	pbkdf2_sha256$320000$itBEIf9eP0eSk5g8534kEP$w6KcK2Rr3Juw19s6gYhyS5USoUsmWOvWuRqevfBhJ18=	\N	f	dog@dog.com	Dog	t	f
3	pbkdf2_sha256$320000$bqxHZy4HKBHVIUpTrXo5CW$3r1CK7KUBsuBJcxmaJqx5AytxB8rOZF4EjUyQGo8AZc=	\N	f	dog2@dog2.com	Dog	t	f
4	pbkdf2_sha256$320000$N04wBF8FQ4JgvZKd8r0A14$W4NzyExcK92uCsRdYJAJN1k2+Sl8AaXrwhtokmf9QIg=	\N	f	poop@poop.com	Phil	t	f
6	pbkdf2_sha256$320000$Udtfkyh9KrpAk6M36k6bF3$Ovl1XYZPi18ZGCG+GgSv4ld3Ttdi9Rd5HGtkUfuEhW4=	\N	f	dog3@dog2.com	Dog	t	f
7	pbkdf2_sha256$320000$cEf4U7hEmd9u8tDDc6GcaE$+DlrUHs0wE0tPfsq2iPijDCjYuGVYwFLbQR913rnvRg=	\N	f	sada@asdas.com	John Doe	t	f
8	pbkdf2_sha256$320000$iaJFkmMgVqbhAlsSeoU7pA$3RthuJXCwpT5BX0DmLM/YsukaChtYHlCC+E+oj3coMY=	\N	f	butterysex@poop.com	John Doe	t	f
9	pbkdf2_sha256$320000$9AaE8PsEyF9QaNzDktmOxl$ZtXHFqHFP+egEzNEEaBRRS1BONHAijkbFY9o6zJ07VQ=	\N	f	balls@balls2.com	John Doe	t	f
10	pbkdf2_sha256$320000$Nzd2bLZFeNbj4aOrkqHh1l$WmOSzcG7lAsVwnfMirsXwtQtb3cKhma1AQy9AM2K29o=	\N	f	testtest@test.com	John Doe	t	f
11	pbkdf2_sha256$320000$d74o8NryBoTlAekvGmeYc4$YYKpCARFVy+ibyWFrKXeO9dMVv0L7CheqFWr6Q4V51A=	\N	f	philman202@yahoo.com	John Doe	t	f
12	pbkdf2_sha256$320000$SdMwNVPP5071ddQOOxtE5V$4AjaA6ubcJtha2PWKgEyvgjOzCaIWeM5U7dEnONVLI0=	\N	f	buttman420@yahoo.com	John Doe	t	f
13	pbkdf2_sha256$320000$NYjIOt4pnnpXSTAXM9Vbcc$Wh5kCyrCAStcfS2LBOnI7GL0ike/p2ips98idxv7trE=	\N	f	23421@234312423.com	John Doe	t	f
14	pbkdf2_sha256$320000$atDMyyrMRVb1sF2M8r5Pk1$OMq55GuibAl5IcgcgwJUmvv+bXjuy/7Jr2mlfn3LeuE=	\N	f	1221312@asdas.com	ass	t	f
15	pbkdf2_sha256$320000$vCIz0wGfpaCYe2xvzFS8Ot$4hKY9UqO4TH9v7CTBrwYv/eRPmscfmrWvOej4VsaZsw=	\N	f	1221312@asdass.com	ass	t	f
16	pbkdf2_sha256$320000$d1UcgggM7jczeHKnkmw9Ri$NXJfo1w06X5KFA1cIvAPAYR+AJn+s8XToZESG4sLBTg=	\N	f	wewaeawe@asdasdas.com	PoopButt	t	f
17	pbkdf2_sha256$320000$nyzWJYWTMY6CSnOH06pKRP$fBPuk9nIdKgUXn1HKmZj9+BhoRDDY+/MEkc92gIuJts=	\N	f	sadas@ijkcd.com	Poopsers	t	f
18	pbkdf2_sha256$320000$6JeTW0UldkF4SOnDaiIidL$CFuyX1Jn1gi9pgrOqwWj+vDWJ8VCnjNRqTUBkx0219M=	\N	f	dog32@dog2.com	Dog23	t	f
19	pbkdf2_sha256$320000$5QHgDG3iFfcJyso5uC37Fh$2dL69rlXnkUOZwdAoPeBC1mpKq2kwFtaVs/K53NugPM=	\N	f	Newbutt123@yahoo.com	Asshole	t	f
20	pbkdf2_sha256$320000$YJIHZiW6LFq9reAJAFdD7V$YggS1XfUutQYHoUyV6E7om/nP/oqfsEyLnWFR4bl0bQ=	\N	f	user5@example.com	string	t	f
1	pbkdf2_sha256$320000$3q6K2rHX2cmzLy0s7CFglQ$VzEWQmkvjA+uNbEFBG7tK1gW1qM0lhWM6v9BaKdluLM=	2024-08-13 19:41:57.321149+00	t	admin@admin.com		t	t
\.


--
-- Data for Name: core_user_groups; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.core_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: core_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.core_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2024-08-24 02:29:05.85001+00	36	Break	3		10	1
2	2024-08-24 02:29:05.856163+00	44	Break	3		10	1
3	2024-08-24 02:30:26.900961+00	1	DRILL	3		10	1
4	2024-08-24 02:30:26.9036+00	2	Test Drill	3		10	1
5	2024-08-24 02:30:26.904566+00	3	Cut Shot	3		10	1
6	2024-08-24 02:30:26.90535+00	4	Stop Shot	3		10	1
7	2024-08-24 02:30:26.906115+00	5	Follow Shot	3		10	1
8	2024-08-24 02:30:26.906847+00	6	Draw Shot	3		10	1
9	2024-08-24 02:30:26.907591+00	7	Stun Shot	3		10	1
10	2024-08-24 02:30:26.908269+00	8	Ball Pocketing	3		10	1
11	2024-08-24 02:30:26.908984+00	9	Wagon Wheel	3		10	1
12	2024-08-24 02:30:26.909712+00	10	Landing Zone	3		10	1
13	2024-08-24 02:30:26.910294+00	11	Line of Balls (I)	3		10	1
14	2024-08-24 02:30:26.910857+00	12	Rail Cut Shot (I)	3		10	1
15	2024-08-24 02:30:26.911295+00	13	Cut Shot	3		10	1
16	2024-08-24 02:30:26.9117+00	14	Stop Shot	3		10	1
17	2024-08-24 02:30:26.912215+00	15	Follow Shot	3		10	1
18	2024-08-24 02:30:26.912699+00	16	Draw Shot	3		10	1
19	2024-08-24 02:30:26.913207+00	17	Stun Shot	3		10	1
20	2024-08-24 02:30:26.913746+00	18	Ball Pocketing	3		10	1
21	2024-08-24 02:30:26.914288+00	19	Wagon Wheel	3		10	1
22	2024-08-24 02:30:26.914711+00	20	Landing Zone	3		10	1
23	2024-08-24 02:30:26.915166+00	21	Line of Balls (I)	3		10	1
24	2024-08-24 02:30:26.915562+00	22	Rail Cut Shot (I)	3		10	1
25	2024-08-24 02:30:26.915988+00	23	Safety (I)	3		10	1
26	2024-08-24 02:30:26.916484+00	24	Kick Shot (I)	3		10	1
27	2024-08-24 02:30:26.91754+00	25	Bank Shot (I)	3		10	1
28	2024-08-24 02:30:26.91822+00	26	Elevated Cue (I)	3		10	1
29	2024-08-24 02:30:26.918766+00	27	Jump/Massé (I)	3		10	1
30	2024-08-24 02:30:26.919182+00	28	Break	3		10	1
31	2024-08-24 02:30:26.919633+00	29	Line of Balls (II)	3		10	1
32	2024-08-24 02:30:26.920139+00	30	Rail Cut Shot (II)	3		10	1
33	2024-08-24 02:30:26.920668+00	31	Safety (II)	3		10	1
34	2024-08-24 02:30:26.921081+00	32	Kick Shot (II)	3		10	1
35	2024-08-24 02:30:26.921457+00	33	Bank Shot (II)	3		10	1
36	2024-08-24 02:30:26.921838+00	34	Elevated Cue (II)	3		10	1
37	2024-08-24 02:30:26.922219+00	35	Jump/Massé (II)	3		10	1
38	2024-08-24 02:30:26.922993+00	37	Line of Balls (III)	3		10	1
39	2024-08-24 02:30:26.923455+00	38	Rail Cut Shot (III)	3		10	1
40	2024-08-24 02:30:26.923947+00	39	Safety (III)	3		10	1
41	2024-08-24 02:30:26.924394+00	40	Kick Shot (III)	3		10	1
42	2024-08-24 02:30:26.924801+00	41	Bank Shot (III)	3		10	1
43	2024-08-24 02:30:26.925242+00	42	Elevated Cue (III)	3		10	1
44	2024-08-24 02:30:26.925719+00	43	Jump/Massé (III)	3		10	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	core	user
7	authtoken	token
8	authtoken	tokenproxy
9	core	drillscore
10	core	drill
11	core	skill
12	core	drillset
13	core	drillsetscore
14	core	tablesetup
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2024-07-07 14:13:34.33253+00
2	contenttypes	0002_remove_content_type_name	2024-07-07 14:13:34.336953+00
3	auth	0001_initial	2024-07-07 14:13:34.359302+00
4	auth	0002_alter_permission_name_max_length	2024-07-07 14:13:34.362167+00
5	auth	0003_alter_user_email_max_length	2024-07-07 14:13:34.364741+00
6	auth	0004_alter_user_username_opts	2024-07-07 14:13:34.367305+00
7	auth	0005_alter_user_last_login_null	2024-07-07 14:13:34.369726+00
8	auth	0006_require_contenttypes_0002	2024-07-07 14:13:34.370674+00
9	auth	0007_alter_validators_add_error_messages	2024-07-07 14:13:34.373591+00
10	auth	0008_alter_user_username_max_length	2024-07-07 14:13:34.376234+00
11	auth	0009_alter_user_last_name_max_length	2024-07-07 14:13:34.380035+00
12	auth	0010_alter_group_name_max_length	2024-07-07 14:13:34.38393+00
13	auth	0011_update_proxy_permissions	2024-07-07 14:13:34.386777+00
14	auth	0012_alter_user_first_name_max_length	2024-07-07 14:13:34.389467+00
15	core	0001_initial	2024-07-07 14:13:34.412788+00
16	admin	0001_initial	2024-07-07 14:13:34.425694+00
17	admin	0002_logentry_remove_auto_add	2024-07-07 14:13:34.429197+00
18	admin	0003_logentry_add_action_flag_choices	2024-07-07 14:13:34.432679+00
19	sessions	0001_initial	2024-07-07 14:13:34.441182+00
20	authtoken	0001_initial	2024-07-10 21:11:31.441999+00
21	authtoken	0002_auto_20160226_1747	2024-07-10 21:11:31.455092+00
22	authtoken	0003_tokenproxy	2024-07-10 21:11:31.456946+00
44	core	0002_drillscore	2024-08-24 06:02:28.448677+00
45	core	0003_remove_drillscore_date_drillscore_createdat	2024-08-24 06:03:17.633975+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: devuser
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
2fjv761ddobjkdqtkhhkjtsx84bcr5qv	.eJxVjEEOwiAQRe_C2hCgM1Jcuu8ZmhmYStVAUtqV8e7apAvd_vfef6mRtjWPW5NlnJO6KKtOvxtTfEjZQbpTuVUda1mXmfWu6IM2PdQkz-vh_h1kavlbe0ZnoYsEziIhCzroORgGAuJgHaC1TrA3Z8-hgymaCI6in4SNQVLvD8F5N0g:1sQTBm:TQVaD4RJG7xl54NK2N4Efw1eRzJ8pr4ul1LQEDq1_Og	2024-07-21 14:48:30.15112+00
bygn4ha1jgb30aex53gsdoz2p5c3w1da	.eJxVjEEOwiAQRe_C2hCgM1Jcuu8ZmhmYStVAUtqV8e7apAvd_vfef6mRtjWPW5NlnJO6KKtOvxtTfEjZQbpTuVUda1mXmfWu6IM2PdQkz-vh_h1kavlbe0ZnoYsEziIhCzroORgGAuJgHaC1TrA3Z8-hgymaCI6in4SNQVLvD8F5N0g:1sVjeP:i9m7DHmSH726THicoTmACq4TIzEz8YuK-dN4VDNgGk8	2024-08-05 03:23:49.080082+00
n3y8v8xxyv3m2cnal2hnlfak6qgjakr1	.eJxVjEEOwiAQRe_C2hCgM1Jcuu8ZmhmYStVAUtqV8e7apAvd_vfef6mRtjWPW5NlnJO6KKtOvxtTfEjZQbpTuVUda1mXmfWu6IM2PdQkz-vh_h1kavlbe0ZnoYsEziIhCzroORgGAuJgHaC1TrA3Z8-hgymaCI6in4SNQVLvD8F5N0g:1sdxP3:CNTWsqteqkWB5pWnKkEr1d5pk_GkHYAlW73xZTphLxU	2024-08-27 19:41:57.322612+00
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 56, true);


--
-- Name: core_drill_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.core_drill_id_seq', 74, true);


--
-- Name: core_drillscore_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.core_drillscore_id_seq', 8, true);


--
-- Name: core_drillset_drills_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.core_drillset_drills_id_seq', 1, false);


--
-- Name: core_drillset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.core_drillset_id_seq', 1, false);


--
-- Name: core_drillsetscore_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.core_drillsetscore_id_seq', 1, false);


--
-- Name: core_drillsetscore_scores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.core_drillsetscore_scores_id_seq', 1, false);


--
-- Name: core_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.core_user_groups_id_seq', 1, false);


--
-- Name: core_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.core_user_id_seq', 20, true);


--
-- Name: core_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.core_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 44, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 14, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: devuser
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 45, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: core_drill core_drill_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drill
    ADD CONSTRAINT core_drill_pkey PRIMARY KEY (id);


--
-- Name: core_drill core_drill_tableSetup_id_key; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drill
    ADD CONSTRAINT "core_drill_tableSetup_id_key" UNIQUE ("tableSetup_id");


--
-- Name: core_drillscore core_drillscore_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillscore
    ADD CONSTRAINT core_drillscore_pkey PRIMARY KEY (id);


--
-- Name: core_drillset_drills core_drillset_drills_drillset_id_drill_id_62aacb95_uniq; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillset_drills
    ADD CONSTRAINT core_drillset_drills_drillset_id_drill_id_62aacb95_uniq UNIQUE (drillset_id, drill_id);


--
-- Name: core_drillset_drills core_drillset_drills_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillset_drills
    ADD CONSTRAINT core_drillset_drills_pkey PRIMARY KEY (id);


--
-- Name: core_drillset core_drillset_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillset
    ADD CONSTRAINT core_drillset_pkey PRIMARY KEY (id);


--
-- Name: core_drillsetscore core_drillsetscore_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillsetscore
    ADD CONSTRAINT core_drillsetscore_pkey PRIMARY KEY (id);


--
-- Name: core_drillsetscore_scores core_drillsetscore_score_drillsetscore_id_drillsc_262b67ac_uniq; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillsetscore_scores
    ADD CONSTRAINT core_drillsetscore_score_drillsetscore_id_drillsc_262b67ac_uniq UNIQUE (drillsetscore_id, drillscore_id);


--
-- Name: core_drillsetscore_scores core_drillsetscore_scores_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillsetscore_scores
    ADD CONSTRAINT core_drillsetscore_scores_pkey PRIMARY KEY (id);


--
-- Name: core_user core_user_email_key; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_user
    ADD CONSTRAINT core_user_email_key UNIQUE (email);


--
-- Name: core_user_groups core_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_user_groups
    ADD CONSTRAINT core_user_groups_pkey PRIMARY KEY (id);


--
-- Name: core_user_groups core_user_groups_user_id_group_id_c82fcad1_uniq; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_user_groups
    ADD CONSTRAINT core_user_groups_user_id_group_id_c82fcad1_uniq UNIQUE (user_id, group_id);


--
-- Name: core_user core_user_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_user
    ADD CONSTRAINT core_user_pkey PRIMARY KEY (id);


--
-- Name: core_user_user_permissions core_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_user_user_permissions
    ADD CONSTRAINT core_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: core_user_user_permissions core_user_user_permissions_user_id_permission_id_73ea0daa_uniq; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_user_user_permissions
    ADD CONSTRAINT core_user_user_permissions_user_id_permission_id_73ea0daa_uniq UNIQUE (user_id, permission_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: core_drill_uploadedBy_id_978e79eb; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX "core_drill_uploadedBy_id_978e79eb" ON public.core_drill USING btree ("createdBy_id");


--
-- Name: core_drillscore_drill_id_cae96feb; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX core_drillscore_drill_id_cae96feb ON public.core_drillscore USING btree (drill_id);


--
-- Name: core_drillscore_user_id_1f7f7277; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX core_drillscore_user_id_1f7f7277 ON public.core_drillscore USING btree (user_id);


--
-- Name: core_drillset_createdBy_id_fd91b3ad; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX "core_drillset_createdBy_id_fd91b3ad" ON public.core_drillset USING btree ("createdBy_id");


--
-- Name: core_drillset_drills_drill_id_b86ad529; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX core_drillset_drills_drill_id_b86ad529 ON public.core_drillset_drills USING btree (drill_id);


--
-- Name: core_drillset_drills_drillset_id_c9647323; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX core_drillset_drills_drillset_id_c9647323 ON public.core_drillset_drills USING btree (drillset_id);


--
-- Name: core_drillsetscore_createdBy_id_62c5a3d5; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX "core_drillsetscore_createdBy_id_62c5a3d5" ON public.core_drillsetscore USING btree (user_id);


--
-- Name: core_drillsetscore_drill_set_id_f7bf8a73; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX core_drillsetscore_drill_set_id_f7bf8a73 ON public.core_drillsetscore USING btree (drill_set_id);


--
-- Name: core_drillsetscore_scores_drillscore_id_efd9261b; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX core_drillsetscore_scores_drillscore_id_efd9261b ON public.core_drillsetscore_scores USING btree (drillscore_id);


--
-- Name: core_drillsetscore_scores_drillsetscore_id_1e25d270; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX core_drillsetscore_scores_drillsetscore_id_1e25d270 ON public.core_drillsetscore_scores USING btree (drillsetscore_id);


--
-- Name: core_user_email_92a71487_like; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX core_user_email_92a71487_like ON public.core_user USING btree (email varchar_pattern_ops);


--
-- Name: core_user_groups_group_id_fe8c697f; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX core_user_groups_group_id_fe8c697f ON public.core_user_groups USING btree (group_id);


--
-- Name: core_user_groups_user_id_70b4d9b8; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX core_user_groups_user_id_70b4d9b8 ON public.core_user_groups USING btree (user_id);


--
-- Name: core_user_user_permissions_permission_id_35ccf601; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX core_user_user_permissions_permission_id_35ccf601 ON public.core_user_user_permissions USING btree (permission_id);


--
-- Name: core_user_user_permissions_user_id_085123d3; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX core_user_user_permissions_user_id_085123d3 ON public.core_user_user_permissions USING btree (user_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: devuser
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_core_user_id; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_core_user_id FOREIGN KEY (user_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_drill core_drill_createdBy_id_383214c2_fk_core_user_id; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drill
    ADD CONSTRAINT "core_drill_createdBy_id_383214c2_fk_core_user_id" FOREIGN KEY ("createdBy_id") REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_drillscore core_drillscore_drill_id_cae96feb_fk_core_drill_id; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillscore
    ADD CONSTRAINT core_drillscore_drill_id_cae96feb_fk_core_drill_id FOREIGN KEY (drill_id) REFERENCES public.core_drill(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_drillscore core_drillscore_user_id_1f7f7277_fk_core_user_id; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillscore
    ADD CONSTRAINT core_drillscore_user_id_1f7f7277_fk_core_user_id FOREIGN KEY (user_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_drillset core_drillset_createdBy_id_fd91b3ad_fk_core_user_id; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillset
    ADD CONSTRAINT "core_drillset_createdBy_id_fd91b3ad_fk_core_user_id" FOREIGN KEY ("createdBy_id") REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_drillset_drills core_drillset_drills_drill_id_b86ad529_fk_core_drill_id; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillset_drills
    ADD CONSTRAINT core_drillset_drills_drill_id_b86ad529_fk_core_drill_id FOREIGN KEY (drill_id) REFERENCES public.core_drill(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_drillset_drills core_drillset_drills_drillset_id_c9647323_fk_core_drillset_id; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillset_drills
    ADD CONSTRAINT core_drillset_drills_drillset_id_c9647323_fk_core_drillset_id FOREIGN KEY (drillset_id) REFERENCES public.core_drillset(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_drillsetscore core_drillsetscore_drill_set_id_f7bf8a73_fk_core_drillset_id; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillsetscore
    ADD CONSTRAINT core_drillsetscore_drill_set_id_f7bf8a73_fk_core_drillset_id FOREIGN KEY (drill_set_id) REFERENCES public.core_drillset(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_drillsetscore_scores core_drillsetscore_s_drillscore_id_efd9261b_fk_core_dril; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillsetscore_scores
    ADD CONSTRAINT core_drillsetscore_s_drillscore_id_efd9261b_fk_core_dril FOREIGN KEY (drillscore_id) REFERENCES public.core_drillscore(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_drillsetscore_scores core_drillsetscore_s_drillsetscore_id_1e25d270_fk_core_dril; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillsetscore_scores
    ADD CONSTRAINT core_drillsetscore_s_drillsetscore_id_1e25d270_fk_core_dril FOREIGN KEY (drillsetscore_id) REFERENCES public.core_drillsetscore(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_drillsetscore core_drillsetscore_user_id_3ffb9131_fk_core_user_id; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_drillsetscore
    ADD CONSTRAINT core_drillsetscore_user_id_3ffb9131_fk_core_user_id FOREIGN KEY (user_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_user_groups core_user_groups_group_id_fe8c697f_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_user_groups
    ADD CONSTRAINT core_user_groups_group_id_fe8c697f_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_user_groups core_user_groups_user_id_70b4d9b8_fk_core_user_id; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_user_groups
    ADD CONSTRAINT core_user_groups_user_id_70b4d9b8_fk_core_user_id FOREIGN KEY (user_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_user_user_permissions core_user_user_permi_permission_id_35ccf601_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_user_user_permissions
    ADD CONSTRAINT core_user_user_permi_permission_id_35ccf601_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_user_user_permissions core_user_user_permissions_user_id_085123d3_fk_core_user_id; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.core_user_user_permissions
    ADD CONSTRAINT core_user_user_permissions_user_id_085123d3_fk_core_user_id FOREIGN KEY (user_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_core_user_id; Type: FK CONSTRAINT; Schema: public; Owner: devuser
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_core_user_id FOREIGN KEY (user_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

