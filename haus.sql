--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5
-- Dumped by pg_dump version 12.2

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
-- Name: Inhabitant; Type: TABLE; Schema: public; Owner: ozko
--

CREATE TABLE public."Inhabitant" (
    id integer NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    flat_number integer NOT NULL
);


ALTER TABLE public."Inhabitant" OWNER TO ozko;

--
-- Name: Inhabitant_id_seq; Type: SEQUENCE; Schema: public; Owner: ozko
--

CREATE SEQUENCE public."Inhabitant_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Inhabitant_id_seq" OWNER TO ozko;

--
-- Name: Inhabitant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ozko
--

ALTER SEQUENCE public."Inhabitant_id_seq" OWNED BY public."Inhabitant".id;


--
-- Name: Inquiry; Type: TABLE; Schema: public; Owner: ozko
--

CREATE TABLE public."Inquiry" (
    id integer NOT NULL,
    items character varying NOT NULL,
    status character varying,
    tag character varying,
    inquirer_id integer NOT NULL
);


ALTER TABLE public."Inquiry" OWNER TO ozko;

--
-- Name: Inquiry_id_seq; Type: SEQUENCE; Schema: public; Owner: ozko
--

CREATE SEQUENCE public."Inquiry_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Inquiry_id_seq" OWNER TO ozko;

--
-- Name: Inquiry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ozko
--

ALTER SEQUENCE public."Inquiry_id_seq" OWNED BY public."Inquiry".id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: ozko
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO ozko;

--
-- Name: Inhabitant id; Type: DEFAULT; Schema: public; Owner: ozko
--

ALTER TABLE ONLY public."Inhabitant" ALTER COLUMN id SET DEFAULT nextval('public."Inhabitant_id_seq"'::regclass);


--
-- Name: Inquiry id; Type: DEFAULT; Schema: public; Owner: ozko
--

ALTER TABLE ONLY public."Inquiry" ALTER COLUMN id SET DEFAULT nextval('public."Inquiry_id_seq"'::regclass);


--
-- Data for Name: Inhabitant; Type: TABLE DATA; Schema: public; Owner: ozko
--

COPY public."Inhabitant" (id, name, email, flat_number) FROM stdin;
1	oez	oez@ko.io	1029
\.


--
-- Data for Name: Inquiry; Type: TABLE DATA; Schema: public; Owner: ozko
--

COPY public."Inquiry" (id, items, status, tag, inquirer_id) FROM stdin;
1	grocery items	open	groceries	1
2	grocery items	open	groceries	1
3	grocery items	open	groceries	1
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: ozko
--

COPY public.alembic_version (version_num) FROM stdin;
cb031a456fb8
\.


--
-- Name: Inhabitant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ozko
--

SELECT pg_catalog.setval('public."Inhabitant_id_seq"', 1, true);


--
-- Name: Inquiry_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ozko
--

SELECT pg_catalog.setval('public."Inquiry_id_seq"', 3, true);


--
-- Name: Inhabitant Inhabitant_email_key; Type: CONSTRAINT; Schema: public; Owner: ozko
--

ALTER TABLE ONLY public."Inhabitant"
    ADD CONSTRAINT "Inhabitant_email_key" UNIQUE (email);


--
-- Name: Inhabitant Inhabitant_pkey; Type: CONSTRAINT; Schema: public; Owner: ozko
--

ALTER TABLE ONLY public."Inhabitant"
    ADD CONSTRAINT "Inhabitant_pkey" PRIMARY KEY (id);


--
-- Name: Inquiry Inquiry_pkey; Type: CONSTRAINT; Schema: public; Owner: ozko
--

ALTER TABLE ONLY public."Inquiry"
    ADD CONSTRAINT "Inquiry_pkey" PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: ozko
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: Inquiry Inquiry_inquirer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ozko
--

ALTER TABLE ONLY public."Inquiry"
    ADD CONSTRAINT "Inquiry_inquirer_id_fkey" FOREIGN KEY (inquirer_id) REFERENCES public."Inhabitant"(id);


--
-- PostgreSQL database dump complete
--

