SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `commerceapp` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `commerceapp`;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `onlinebanking_account` (
  `id` int(11) NOT NULL,
  `account_number` bigint(20) NOT NULL,
  `last_transaction_number` int(11) NOT NULL,
  `mock_transactions` tinyint(1) NOT NULL,
  `account_type` varchar(8) NOT NULL,
  `balance` decimal(15,2) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `onlinebanking_accounttrigger` (
  `trigger_ptr_id` int(11) NOT NULL,
  `balance_gte` decimal(15,2) DEFAULT NULL,
  `balance_lte` decimal(15,2) DEFAULT NULL,
  `account_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `onlinebanking_notification` (
  `id` int(11) NOT NULL,
  `created` datetime(6) NOT NULL,
  `email_sent` datetime(6) DEFAULT NULL,
  `sms_sent` datetime(6) DEFAULT NULL,
  `read` datetime(6) DEFAULT NULL,
  `deleted` tinyint(1) NOT NULL,
  `title` varchar(50) NOT NULL,
  `message` longtext NOT NULL,
  `triggered_by_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `onlinebanking_transaction` (
  `id` int(11) NOT NULL,
  `transaction_number` int(11) NOT NULL,
  `posted` datetime(6) NOT NULL,
  `amount` decimal(15,2) NOT NULL,
  `description` varchar(100) NOT NULL,
  `balance` decimal(15,2) NOT NULL,
  `account_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `onlinebanking_transactiontrigger` (
  `trigger_ptr_id` int(11) NOT NULL,
  `type_credit` tinyint(1) NOT NULL,
  `type_debit` tinyint(1) NOT NULL,
  `start` time(6) DEFAULT NULL,
  `end` time(6) DEFAULT NULL,
  `amount_gte` decimal(15,2) DEFAULT NULL,
  `amount_lte` decimal(15,2) DEFAULT NULL,
  `description_value` varchar(100) NOT NULL,
  `account_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `onlinebanking_trigger` (
  `id` int(11) NOT NULL,
  `name` varchar(60) NOT NULL,
  `sms` tinyint(1) NOT NULL,
  `email` tinyint(1) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  `trigger_count` int(10) UNSIGNED NOT NULL CHECK (`trigger_count` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `onlinebanking_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone_number` varchar(14) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `onlinebanking_usertrigger` (
  `trigger_ptr_id` int(11) NOT NULL,
  `on_login` tinyint(1) NOT NULL,
  `on_change` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `onlinebanking_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `onlinebanking_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `preventconcurrentlogins_visitor` (
  `id` int(11) NOT NULL,
  `session_key` varchar(40) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_onlinebanking_user_id` (`user_id`);

ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

ALTER TABLE `onlinebanking_account`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `account_number` (`account_number`),
  ADD KEY `onlinebanking_account_user_id_d22a8111_fk_onlinebanking_user_id` (`user_id`);

ALTER TABLE `onlinebanking_accounttrigger`
  ADD PRIMARY KEY (`trigger_ptr_id`),
  ADD KEY `onlinebanking_accoun_account_id_8fac0238_fk_onlineban` (`account_id`),
  ADD KEY `onlinebanking_accoun_user_id_ba3ba3f0_fk_onlineban` (`user_id`);

ALTER TABLE `onlinebanking_notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `onlinebanking_notifi_user_id_fba37e5b_fk_onlineban` (`user_id`),
  ADD KEY `onlinebanking_notifi_triggered_by_id_630102af_fk_onlineban` (`triggered_by_id`);

ALTER TABLE `onlinebanking_transaction`
  ADD PRIMARY KEY (`id`),
  ADD KEY `onlinebanking_transa_account_id_d925fcdf_fk_onlineban` (`account_id`);

ALTER TABLE `onlinebanking_transactiontrigger`
  ADD PRIMARY KEY (`trigger_ptr_id`),
  ADD KEY `onlinebanking_transa_account_id_50893702_fk_onlineban` (`account_id`),
  ADD KEY `onlinebanking_transa_user_id_dd62a67a_fk_onlineban` (`user_id`);

ALTER TABLE `onlinebanking_trigger`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `onlinebanking_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

ALTER TABLE `onlinebanking_usertrigger`
  ADD PRIMARY KEY (`trigger_ptr_id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

ALTER TABLE `onlinebanking_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `onlinebanking_user_groups_user_id_group_id_af80f233_uniq` (`user_id`,`group_id`),
  ADD KEY `onlinebanking_user_groups_group_id_17cbe795_fk_auth_group_id` (`group_id`);

ALTER TABLE `onlinebanking_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `onlinebanking_user_user__user_id_permission_id_a5cd37ce_uniq` (`user_id`,`permission_id`),
  ADD KEY `onlinebanking_user_u_permission_id_61ed3ff5_fk_auth_perm` (`permission_id`);

ALTER TABLE `preventconcurrentlogins_visitor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);


ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `onlinebanking_account`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `onlinebanking_notification`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `onlinebanking_transaction`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `onlinebanking_trigger`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `onlinebanking_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `onlinebanking_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `onlinebanking_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `preventconcurrentlogins_visitor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_onlinebanking_user_id` FOREIGN KEY (`user_id`) REFERENCES `onlinebanking_user` (`id`);

ALTER TABLE `onlinebanking_account`
  ADD CONSTRAINT `onlinebanking_account_user_id_d22a8111_fk_onlinebanking_user_id` FOREIGN KEY (`user_id`) REFERENCES `onlinebanking_user` (`id`);

ALTER TABLE `onlinebanking_accounttrigger`
  ADD CONSTRAINT `onlinebanking_accoun_account_id_8fac0238_fk_onlineban` FOREIGN KEY (`account_id`) REFERENCES `onlinebanking_account` (`id`),
  ADD CONSTRAINT `onlinebanking_accoun_trigger_ptr_id_6631739f_fk_onlineban` FOREIGN KEY (`trigger_ptr_id`) REFERENCES `onlinebanking_trigger` (`id`),
  ADD CONSTRAINT `onlinebanking_accoun_user_id_ba3ba3f0_fk_onlineban` FOREIGN KEY (`user_id`) REFERENCES `onlinebanking_user` (`id`);

ALTER TABLE `onlinebanking_notification`
  ADD CONSTRAINT `onlinebanking_notifi_triggered_by_id_630102af_fk_onlineban` FOREIGN KEY (`triggered_by_id`) REFERENCES `onlinebanking_trigger` (`id`),
  ADD CONSTRAINT `onlinebanking_notifi_user_id_fba37e5b_fk_onlineban` FOREIGN KEY (`user_id`) REFERENCES `onlinebanking_user` (`id`);

ALTER TABLE `onlinebanking_transaction`
  ADD CONSTRAINT `onlinebanking_transa_account_id_d925fcdf_fk_onlineban` FOREIGN KEY (`account_id`) REFERENCES `onlinebanking_account` (`id`);

ALTER TABLE `onlinebanking_transactiontrigger`
  ADD CONSTRAINT `onlinebanking_transa_account_id_50893702_fk_onlineban` FOREIGN KEY (`account_id`) REFERENCES `onlinebanking_account` (`id`),
  ADD CONSTRAINT `onlinebanking_transa_trigger_ptr_id_772642be_fk_onlineban` FOREIGN KEY (`trigger_ptr_id`) REFERENCES `onlinebanking_trigger` (`id`),
  ADD CONSTRAINT `onlinebanking_transa_user_id_dd62a67a_fk_onlineban` FOREIGN KEY (`user_id`) REFERENCES `onlinebanking_user` (`id`);

ALTER TABLE `onlinebanking_usertrigger`
  ADD CONSTRAINT `onlinebanking_usertr_trigger_ptr_id_078b92a1_fk_onlineban` FOREIGN KEY (`trigger_ptr_id`) REFERENCES `onlinebanking_trigger` (`id`),
  ADD CONSTRAINT `onlinebanking_usertr_user_id_82c25658_fk_onlineban` FOREIGN KEY (`user_id`) REFERENCES `onlinebanking_user` (`id`);

ALTER TABLE `onlinebanking_user_groups`
  ADD CONSTRAINT `onlinebanking_user_g_user_id_0e1f64d3_fk_onlineban` FOREIGN KEY (`user_id`) REFERENCES `onlinebanking_user` (`id`),
  ADD CONSTRAINT `onlinebanking_user_groups_group_id_17cbe795_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

ALTER TABLE `onlinebanking_user_user_permissions`
  ADD CONSTRAINT `onlinebanking_user_u_permission_id_61ed3ff5_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `onlinebanking_user_u_user_id_eb74e740_fk_onlineban` FOREIGN KEY (`user_id`) REFERENCES `onlinebanking_user` (`id`);

ALTER TABLE `preventconcurrentlogins_visitor`
  ADD CONSTRAINT `preventconcurrentlog_user_id_d63979bc_fk_onlineban` FOREIGN KEY (`user_id`) REFERENCES `onlinebanking_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
