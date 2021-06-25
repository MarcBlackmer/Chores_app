--
-- PostgreSQL database dump
--
 -- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

SET statement_timeout = 0;


SET lock_timeout = 0;


SET idle_in_transaction_session_timeout = 0;


SET client_encoding = 'UTF8';


SET standard_conforming_strings = ON;


SELECT pg_catalog.set_config('search_path', '', FALSE);


SET check_function_bodies = FALSE;


SET xmloption = content;


SET client_min_messages = warning;


SET row_security = OFF;


SET default_tablespace = '';


SET default_table_access_method = heap;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: udacity
--

CREATE TABLE public.categories (id integer NOT NULL,
                                           cat_name CHARACTER varying(20) NOT NULL);


ALTER TABLE public.categories OWNER TO udacity;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: udacity
--

CREATE SEQUENCE public.categories_id_seq AS integer
START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO udacity;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: udacity
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;

--
-- Name: chores; Type: TABLE; Schema: public; Owner: udacity
--

CREATE TABLE public.chores (id integer NOT NULL,
                                       chore_name CHARACTER varying(150) NOT NULL,
                                                                         recurrence CHARACTER varying(15) NOT NULL,
                                                                                                          category_id integer NOT NULL,
                                                                                                                              user_id integer NOT NULL,
                                                                                                                                              status CHARACTER varying(15) NOT NULL,
                                                                                                                                                                           points integer NOT NULL);


ALTER TABLE public.chores OWNER TO udacity;

--
-- Name: chores_id_seq; Type: SEQUENCE; Schema: public; Owner: udacity
--

CREATE SEQUENCE public.chores_id_seq AS integer
START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;


ALTER TABLE public.chores_id_seq OWNER TO udacity;

--
-- Name: chores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: udacity
--

ALTER SEQUENCE public.chores_id_seq OWNED BY public.chores.id;

--
-- Name: users; Type: TABLE; Schema: public; Owner: udacity
--

CREATE TABLE public.users (id integer NOT NULL,
                                      user_name CHARACTER varying(50) NOT NULL,
                                                                      user_role CHARACTER varying(10) NOT NULL);


ALTER TABLE public.users OWNER TO udacity;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: udacity
--

CREATE SEQUENCE public.users_id_seq AS integer
START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO udacity;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: udacity
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;

--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: udacity
--

ALTER TABLE ONLY public.categories
ALTER COLUMN id
SET DEFAULT nextval('public.categories_id_seq'::regclass);

--
-- Name: chores id; Type: DEFAULT; Schema: public; Owner: udacity
--

ALTER TABLE ONLY public.chores
ALTER COLUMN id
SET DEFAULT nextval('public.chores_id_seq'::regclass);

--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: udacity
--

ALTER TABLE ONLY public.users
ALTER COLUMN id
SET DEFAULT nextval('public.users_id_seq'::regclass);

--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: udacity
--
 COPY public.categories (id, cat_name)
FROM STDIN;

1 Dishes 3 cleaning 4 yard
WORK \. --
-- Data for Name: chores; Type: TABLE DATA; Schema: public; Owner: udacity
--
 COPY public.chores (id, chore_name, recurrence, category_id, user_id, status, points)
FROM STDIN;

1 Empty dishwasher daily 1 5 incomplete 10 2 Clean bedroom Daily 3 3 complete 5 \. --
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: udacity
--
 COPY public.users (id, user_name, user_role)
FROM STDIN;

1 marc ADMIN 2 tom ADMIN 3 katie USER 5 bob USER 8 gary USER \. --
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: udacity
--

SELECT pg_catalog.setval('public.categories_id_seq', 6, TRUE);

--
-- Name: chores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: udacity
--

SELECT pg_catalog.setval('public.chores_id_seq', 3, TRUE);

--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: udacity
--

SELECT pg_catalog.setval('public.users_id_seq', 9, TRUE);

--
-- Name: categories categories_cat_name_key; Type: CONSTRAINT; Schema: public; Owner: udacity
--

ALTER TABLE ONLY public.categories ADD CONSTRAINT categories_cat_name_key UNIQUE (cat_name);

--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: udacity
--

ALTER TABLE ONLY public.categories ADD CONSTRAINT categories_pkey PRIMARY KEY (id);

--
-- Name: chores chores_chore_name_key; Type: CONSTRAINT; Schema: public; Owner: udacity
--

ALTER TABLE ONLY public.chores ADD CONSTRAINT chores_chore_name_key UNIQUE (chore_name);

--
-- Name: chores chores_pkey; Type: CONSTRAINT; Schema: public; Owner: udacity
--

ALTER TABLE ONLY public.chores ADD CONSTRAINT chores_pkey PRIMARY KEY (id);

--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: udacity
--

ALTER TABLE ONLY public.users ADD CONSTRAINT users_pkey PRIMARY KEY (id);

--
-- Name: users users_user_name_key; Type: CONSTRAINT; Schema: public; Owner: udacity
--

ALTER TABLE ONLY public.users ADD CONSTRAINT users_user_name_key UNIQUE (user_name);

--
-- Name: chores chores_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: udacity
--

ALTER TABLE ONLY public.chores ADD CONSTRAINT chores_category_id_fkey
FOREIGN KEY (category_id) REFERENCES public.categories(id);

--
-- Name: chores chores_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: udacity
--

ALTER TABLE ONLY public.chores ADD CONSTRAINT chores_user_id_fkey
FOREIGN KEY (user_id) REFERENCES public.users(id);

--
-- PostgreSQL database dump complete
--
