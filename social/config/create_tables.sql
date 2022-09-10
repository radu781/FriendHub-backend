DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
    `id` char(36) NOT NULL,
    `parent_id` char(36) NOT NULL COMMENT 'can be a post or another comment',
    `body` text NOT NULL,
    `likes` int unsigned NOT NULL,
    `dislikes` int unsigned NOT NULL,
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `comments_parent_id_foreign` (`parent_id`),
    CONSTRAINT `comments_parent_id_foreign` FOREIGN KEY (`parent_id`) REFERENCES `posts` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `im_group_members`;
CREATE TABLE `im_group_members` (
    `id` char(36) NOT NULL,
    `group_id` char(36) NOT NULL,
    `user_or_page_id` char(36) NOT NULL,
    `permissions` int unsigned NOT NULL,
    `join_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `im_group_members_group_id_foreign` (`group_id`),
    KEY `im_group_members_user_or_page_id_foreign1` (`user_or_page_id`),
    CONSTRAINT `im_group_members_group_id_foreign` FOREIGN KEY (`group_id`) REFERENCES `im_groups` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `im_groups`;
CREATE TABLE `im_groups` (
    `id` char(36) NOT NULL,
    `name` varchar(255) NOT NULL,
    `profile_picture` varchar(255) NOT NULL,
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `message`;
CREATE TABLE `message` (
    `id` char(36) NOT NULL,
    `from` char(36) NOT NULL,
    `to` char(36) NOT NULL,
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `body` text NOT NULL,
    PRIMARY KEY (`id`),
    KEY `message_from_foreign` (`from`),
    KEY `message_to_foreign1` (`to`),
    CONSTRAINT `message_from_foreign` FOREIGN KEY (`from`) REFERENCES `users` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `p_group_members`;
CREATE TABLE `p_group_members` (
    `id` char(36) NOT NULL,
    `group_id` char(36) NOT NULL,
    `user_or_page_id` char(36) NOT NULL,
    `permissions` int unsigned NOT NULL,
    `join_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `p_group_members_group_id_foreign` (`group_id`),
    KEY `p_group_members_user_or_page_id_foreign1` (`user_or_page_id`),
    CONSTRAINT `p_group_members_group_id_foreign` FOREIGN KEY (`group_id`) REFERENCES `pages_groups` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `pages`;
CREATE TABLE `pages` (
    `id` char(36) NOT NULL,
    `name` varchar(255) NOT NULL,
    `join_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `profile_picture` varchar(255) NOT NULL,
    `banner_picture` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `pages_groups`;
CREATE TABLE `pages_groups` (
    `id` char(36) NOT NULL,
    `name` varchar(255) NOT NULL,
    `profile_picture` varchar(255) NOT NULL,
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts` (
    `id` char(36) NOT NULL,
    `owner_id` char(36) NOT NULL,
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `likes` int NOT NULL,
    `dislikes` int NOT NULL,
    `text` text,
    `image` varchar(255) DEFAULT NULL,
    `video` varchar(255) DEFAULT NULL,
    `audio` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `posts_owner_id_foreign2` (`owner_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `relationships`;
CREATE TABLE `relationships` (
    `id` char(36) NOT NULL,
    `user_id1` char(36) NOT NULL,
    `user_id2` char(36) NOT NULL,
    `status` char(255) NOT NULL COMMENT '1->2: PENDING/ACCEPTED/BLOCKED/HIDDEN',
    `change_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `relationships_user_id1_foreign` (`user_id1`),
    KEY `relationships_user_id2_foreign` (`user_id2`),
    CONSTRAINT `relationships_user_id1_foreign` FOREIGN KEY (`user_id1`) REFERENCES `users` (`id`),
    CONSTRAINT `relationships_user_id2_foreign` FOREIGN KEY (`user_id2`) REFERENCES `users` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `replies`;
CREATE TABLE `replies` (
    `id` char(36) NOT NULL,
    `parent_id` char(36) NOT NULL,
    `body` text NOT NULL,
    `likes` int unsigned NOT NULL,
    `dislikes` int unsigned NOT NULL,
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `replies_parent_id_foreign` (`parent_id`),
    CONSTRAINT `replies_parent_id_foreign` FOREIGN KEY (`parent_id`) REFERENCES `comments` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id` char(36) NOT NULL,
    `first_name` varchar(255) NOT NULL,
    `middle_name` varchar(255) DEFAULT NULL,
    `last_name` varchar(255) NOT NULL,
    `join_time` datetime NOT NULL,
    `country` varchar(255) DEFAULT NULL,
    `city` varchar(255) DEFAULT NULL,
    `education` varchar(255) DEFAULT NULL,
    `extra` text,
    `profile_picture` varchar(255) DEFAULT NULL,
    `banner_picture` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
