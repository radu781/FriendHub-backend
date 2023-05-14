CREATE TABLE public.comments (
    id character(36) NOT NULL,
    parent_id character(36) NOT NULL,
    body text NOT NULL,
    likes integer NOT NULL,
    dislikes integer NOT NULL
);
ALTER TABLE public.comments
ADD CONSTRAINT comments_pkey PRIMARY KEY (id);
CREATE TABLE public.im_group_members (
    id character(36) NOT NULL,
    group_id character(36) NOT NULL,
    user_or_page_id character(36) NOT NULL,
    permissions integer NOT NULL,
    join_time timestamp without time zone NOT NULL
);
ALTER TABLE public.im_group_members
ADD CONSTRAINT im_group_members_pkey PRIMARY KEY (id);
CREATE TABLE public.im_groups (
    id character(36) NOT NULL,
    name character varying(255) NOT NULL,
    profile_picture character varying(255) NOT NULL
);
ALTER TABLE public.im_groups
ADD CONSTRAINT im_groups_pkey PRIMARY KEY (id);
CREATE TABLE public.message (
    id character(36) NOT NULL,
    "from" character(36) NOT NULL,
    "to" character(36) NOT NULL,
    "time" timestamp without time zone NOT NULL
);
ALTER TABLE public.message
ADD CONSTRAINT message_pkey PRIMARY KEY (id);
CREATE TABLE public.p_group_members (
    id character(36) NOT NULL,
    group_id character(36) NOT NULL,
    user_or_page_id character(36) NOT NULL,
    permissions integer NOT NULL,
    join_time timestamp without time zone NOT NULL
);
ALTER TABLE public.p_group_members
ADD CONSTRAINT p_group_members_pkey PRIMARY KEY (id);
CREATE TABLE public.pages (
    id character(36) NOT NULL,
    name character varying(255) NOT NULL,
    join_time timestamp without time zone NOT NULL,
    profile_picture character varying(255) NOT NULL,
    banner_picture character varying(255) NOT NULL
);
ALTER TABLE public.pages
ADD CONSTRAINT pages_pkey PRIMARY KEY (id);
CREATE TABLE public.pages (
    id character(36) NOT NULL,
    name character varying(255) NOT NULL,
    join_time timestamp without time zone NOT NULL,
    profile_picture character varying(255) NOT NULL,
    banner_picture character varying(255) NOT NULL
);
ALTER TABLE public.pages
ADD CONSTRAINT pages_pkey PRIMARY KEY (id);
CREATE TABLE public.pages_groups (
    id character(36) NOT NULL,
    name character varying(255) NOT NULL,
    profile_picture character varying(255) NOT NULL
);
ALTER TABLE public.pages_groups
ADD CONSTRAINT pages_groups_pkey PRIMARY KEY (id);
CREATE TABLE public.posts (
    id character(36) NOT NULL,
    owner_id character(36) NOT NULL,
    create_time timestamp without time zone NOT NULL,
    likes integer NOT NULL,
    dislikes integer NOT NULL,
    text text NULL,
    image character varying(255) NULL,
    video character varying(255) NULL,
    audio character varying(255) NULL
);
ALTER TABLE public.posts
ADD CONSTRAINT posts_pkey PRIMARY KEY (id);
CREATE TABLE public.relationships (
    id character(36) NOT NULL,
    "from" character(36) NOT NULL,
    "to" character(36) NOT NULL,
    type character varying(255) NOT NULL,
    change_time timestamp without time zone NOT NULL
);
ALTER TABLE public.relationships
ADD CONSTRAINT relationships_pkey PRIMARY KEY (id);
CREATE TABLE public.replies (
    id character(36) NOT NULL,
    parent_id character(36) NOT NULL,
    body text NOT NULL,
    likes integer NOT NULL,
    dislikes integer NOT NULL
);
ALTER TABLE public.replies
ADD CONSTRAINT replies_pkey PRIMARY KEY (id);
CREATE TABLE public.scripts (
    id character(36) NOT NULL,
    author character(36) NOT NULL,
    script text NOT NULL
);
ALTER TABLE public.scripts
ADD CONSTRAINT scripts_pkey PRIMARY KEY (id);
CREATE TABLE public.tokens (id serial NOT NULL, value text NOT NULL);
ALTER TABLE public.tokens
ADD CONSTRAINT tokens_pkey PRIMARY KEY (id);
CREATE TABLE public.users (
    id character(36) NOT NULL,
    first_name character varying(255) NOT NULL,
    middle_name character varying(255) NULL,
    last_name character varying(255) NOT NULL,
    join_time timestamp without time zone NOT NULL,
    country character varying(255) NULL,
    city character varying(255) NULL,
    education character varying(255) NULL,
    extra text NULL,
    profile_picture character varying(255) NULL,
    banner_picture character varying(255) NULL,
    email character varying(32) NOT NULL,
    password character(66) NOT NULL,
    permissions character varying(64) NULL
);
ALTER TABLE public.users
ADD CONSTRAINT users_pkey PRIMARY KEY (id);
CREATE TABLE public.votes (
    id character(36) NOT NULL,
    parent_id character(36) NOT NULL,
    author_id character(36) NOT NULL,
    value character varying(255) NOT NULL
);
ALTER TABLE public.votes
ADD CONSTRAINT votes_pkey PRIMARY KEY (id);
