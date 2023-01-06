CREATE TABLE "users"(
    "id" CHAR(36) NOT NULL,
    "first_name" VARCHAR(255) NOT NULL,
    "middle_name" VARCHAR(255) NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "join_time" timestamp NOT NULL,
    "country" VARCHAR(255) NULL,
    "city" VARCHAR(255) NULL,
    "education" VARCHAR(255) NULL,
    "extra" TEXT NULL,
    "profile_picture" VARCHAR(255) NULL,
    "banner_picture" VARCHAR(255) NULL
);
ALTER TABLE "users"
ADD PRIMARY KEY "users_id_primary"("id");
CREATE TABLE "relationships"(
    "id" CHAR(36) NOT NULL,
    "user_id1" CHAR(36) NOT NULL,
    "user_id2" CHAR(36) NOT NULL,
    "status" CHAR(255) NOT NULL,
    "change_time" timestamp NOT NULL
);
ALTER TABLE "relationships"
ADD PRIMARY KEY "relationships_id_primary"("id");
CREATE TABLE "pages"(
    "id" CHAR(36) NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "join_time" timestamp NOT NULL,
    "profile_picture" VARCHAR(255) NOT NULL,
    "banner_picture" VARCHAR(255) NOT NULL
);
ALTER TABLE "pages"
ADD PRIMARY KEY "pages_id_primary"("id");
CREATE TABLE "posts"(
    "id" CHAR(36) NOT NULL,
    "owner_id" CHAR(36) NOT NULL,
    "create_time" timestamp NOT NULL,
    "likes" INT NOT NULL,
    "dislikes" INT NOT NULL,
    "text" TEXT NULL,
    "image" VARCHAR(255) NULL,
    "video" VARCHAR(255) NULL,
    "audio" VARCHAR(255) NULL
);
ALTER TABLE "posts"
ADD PRIMARY KEY "posts_id_primary"("id");
CREATE TABLE "comments"(
    "id" CHAR(36) NOT NULL,
    "parent_id" CHAR(36) NOT NULL,
    "body" TEXT NOT NULL,
    "likes" INT NOT NULL,
    "dislikes" INT NOT NULL
);
ALTER TABLE "comments"
ADD PRIMARY KEY "comments_id_primary"("id");
CREATE TABLE "pages_groups"(
    "id" CHAR(36) NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "profile_picture" VARCHAR(255) NOT NULL
);
ALTER TABLE "pages_groups"
ADD PRIMARY KEY "pages_groups_id_primary"("id");
CREATE TABLE "p_group_members"(
    "id" CHAR(36) NOT NULL,
    "group_id" CHAR(36) NOT NULL,
    "user_or_page_id" CHAR(36) NOT NULL,
    "permissions" INT NOT NULL,
    "join_time" timestamp NOT NULL
);
ALTER TABLE "p_group_members"
ADD PRIMARY KEY "p_group_members_id_primary"("id");
CREATE TABLE "im_groups"(
    "id" CHAR(36) NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "profile_picture" VARCHAR(255) NOT NULL
);
ALTER TABLE "im_groups"
ADD PRIMARY KEY "im_groups_id_primary"("id");
CREATE TABLE "im_group_members"(
    "id" CHAR(36) NOT NULL,
    "group_id" CHAR(36) NOT NULL,
    "user_or_page_id" CHAR(36) NOT NULL,
    "permissions" INT NOT NULL,
    "join_time" timestamp NOT NULL
);
ALTER TABLE "im_group_members"
ADD PRIMARY KEY "im_group_members_id_primary"("id");
CREATE TABLE "message"(
    "id" CHAR(36) NOT NULL,
    "from" CHAR(36) NOT NULL,
    "to" CHAR(36) NOT NULL,
    "time" timestamp NOT NULL
);
ALTER TABLE "message"
ADD PRIMARY KEY "message_id_primary"("id");
CREATE TABLE "replies"(
    "id" CHAR(36) NOT NULL,
    "parent_id" CHAR(36) NOT NULL,
    "body" TEXT NOT NULL,
    "likes" INT NOT NULL,
    "dislikes" INT NOT NULL
);
ALTER TABLE "replies"
ADD PRIMARY KEY "replies_id_primary"("id");
ALTER TABLE "relationships"
ADD CONSTRAINT "relationships_user_id1_foreign" FOREIGN KEY("user_id1") REFERENCES "users"("id");
ALTER TABLE "relationships"
ADD CONSTRAINT "relationships_user_id2_foreign" FOREIGN KEY("user_id2") REFERENCES "users"("id");
ALTER TABLE "p_group_members"
ADD CONSTRAINT "p_group_members_group_id_foreign" FOREIGN KEY("group_id") REFERENCES "pages_groups"("id");
ALTER TABLE "comments"
ADD CONSTRAINT "comments_parent_id_foreign" FOREIGN KEY("parent_id") REFERENCES "posts"("id");
ALTER TABLE "posts"
ADD CONSTRAINT "posts_owner_id_foreign" FOREIGN KEY("owner_id") REFERENCES "users"("id");
ALTER TABLE "im_group_members"
ADD CONSTRAINT "im_group_members_group_id_foreign" FOREIGN KEY("group_id") REFERENCES "im_groups"("id");
ALTER TABLE "replies"
ADD CONSTRAINT "replies_parent_id_foreign" FOREIGN KEY("parent_id") REFERENCES "comments"("id");
