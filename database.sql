CREATE TABLE allergies (
    PRIMARY KEY (id),
    id   INT(11)      NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
) CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE allergies_ingredients (
    PRIMARY KEY (id),
    id            INT(11) NOT NULL AUTO_INCREMENT,
    allergy_id    INT(11) NOT NULL,
                  CONSTRAINT delete_allergy_allergies_ingredients -- delete if allergy is removed
                  FOREIGN KEY (allergy_id)
                  REFERENCES allergies (id)
                  ON DELETE CASCADE,
    ingredient_id INT(11) NOT NULL,
                  CONSTRAINT delete_ingredient_allergies_ingredients -- delete if ingredient is removed
                  FOREIGN KEY (ingredient_id)
                  REFERENCES ingredients (id)
                  ON DELETE CASCADE
) CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE extra_info (
    PRIMARY KEY (id),
    id   INT(11)      NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
) CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE images (
    PRIMARY KEY (id),
    id       INT(11)      NOT NULL AUTO_INCREMENT,
    name     VARCHAR(255) NOT NULL,
    url      VARCHAR(255) NOT NULL
) CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE ingredients (
    PRIMARY KEY (id),
    id   INT(11)      NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
) CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE recipes (
    PRIMARY KEY (id),
    id       INT(11)      NOT NULL AUTO_INCREMENT,
    image_id INT(11)               DEFAULT NULL,
    name     VARCHAR(255) NOT NULL,
    url      VARCHAR(255) NOT NULL
) CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE recipes_extra_info (
    PRIMARY KEY (id),
    id            INT(11) NOT NULL AUTO_INCREMENT,
    extra_info_id INT(11) NOT NULL,
                  CONSTRAINT delete_info_recipes_extra_info -- delete if extra info is removed
                  FOREIGN KEY (extra_info_id)
                  REFERENCES extra_info (id)
                  ON DELETE CASCADE,
    recipe_id     INT(11) NOT NULL,
                  CONSTRAINT delete_recipe_recipes_extra_info -- delete if recipe is removed
                  FOREIGN KEY (recipe_id)
                  REFERENCES recipes (id)
                  ON DELETE CASCADE
) CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE recipes_ingredients (
    PRIMARY KEY (id),
    id            INT(11) NOT NULL AUTO_INCREMENT,
    recipe_id     INT(11) NOT NULL,
                  CONSTRAINT delete_recipe_recipes_ingredients -- delete if recipe is removed
                  FOREIGN KEY (recipe_id)
                  REFERENCES recipes (id)
                  ON DELETE CASCADE,
    ingredient_id INT(11) NOT NULL,
                  CONSTRAINT delete_ingredient_recipes_ingredients -- delete if ingredient is removed
                  FOREIGN KEY (ingredient_id)
                  REFERENCES ingredients (id)
                  ON DELETE CASCADE
) CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE roommates (
    PRIMARY KEY (id),
    id          INT(11)      NOT NULL AUTO_INCREMENT,
    handle      INT(11)      NOT NULL,
    user_id     INT(11)      NOT NULL,
                CONSTRAINT delete_user_roommates -- delete if user is removed
                FOREIGN KEY (user_id)
                REFERENCES users (id)
                ON DELETE CASCADE,
    first_name  VARCHAR(255),
    middle_name VARCHAR(255),
    last_name   VARCHAR(255)
) CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE roommates_allergies (
    PRIMARY KEY (id),
    id          INT(11) NOT NULL AUTO_INCREMENT,
    roommate_id INT(11) NOT NULL,
                CONSTRAINT delete_roommate_roommates_allergies -- delete if roommate is removed
                FOREIGN KEY (roommate_id)
                REFERENCES roommates (id)
                ON DELETE CASCADE,
    allergy_id  INT(11) NOT NULL,
                CONSTRAINT delete_allergy_roommates_allergies -- delete if allergy is removed
                FOREIGN KEY (allergy_id)
                REFERENCES allergies (id)
                ON DELETE CASCADE,
    flag        INT(2)  NOT NULL DEFAULT 0
) CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE roommates_preferences (
    PRIMARY KEY (id),
    id            INT(11) NOT NULL AUTO_INCREMENT,
    roommate_id   INT(11) NOT NULL,
                  CONSTRAINT delete_roommate_roommates_preferences -- delete if roommate is removed
                  FOREIGN KEY (roommate_id)
                  REFERENCES roommates (id)
                  ON DELETE CASCADE,
    ingredient_id INT(11) NOT NULL,
                  CONSTRAINT delete_ingredient_roommates_preferences -- delete if ingredient is removed
                  FOREIGN KEY (ingredient_id)
                  REFERENCES ingredients (id)
                  ON DELETE CASCADE,
    flag          INT(2)  NOT NULL DEFAULT 0
) CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE users (
    PRIMARY KEY (id),
    id          INT(11)      NOT NULL AUTO_INCREMENT,
    username    VARCHAR(80)  NOT NULL,
    email       VARCHAR(255) NOT NULL,
    first_name  VARCHAR(255),
    middle_name VARCHAR(255),
    last_name   VARCHAR(255),
    hash        CHAR(255)    NOT NULL,
    salt        CHAR(255)    NOT NULL,
    join_date   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (id, username, email)
) CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE users_allergies (
    PRIMARY KEY (id),
    id         INT(11) NOT NULL AUTO_INCREMENT,
    user_id    INT(11) NOT NULL,
               CONSTRAINT delete_user_users_allergies -- delete if user is removed
               FOREIGN KEY (user_id)
               REFERENCES users (id)
               ON DELETE CASCADE,
    allergy_id INT(11) NOT NULL,
               CONSTRAINT delete_allergy_users_allergies -- delete if allergy is removed
               FOREIGN KEY (allergy_id)
               REFERENCES allergies (id)
               ON DELETE CASCADE,
    flag       INT(2)  NOT NULL DEFAULT 0
) CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE users_preferences (
    PRIMARY KEY (id),
    id            INT(11) NOT NULL AUTO_INCREMENT,
    user_id       INT(11) NOT NULL,
                  CONSTRAINT delete_user_users_preferences -- delete if user is removed
                  FOREIGN KEY (user_id)
                  REFERENCES users (id)
                  ON DELETE CASCADE,
    ingredient_id INT(11) NOT NULL,
                  CONSTRAINT delete_ingredient_users_preferences -- delete if ingredient is removed
                  FOREIGN KEY (ingredient_id)
                  REFERENCES ingredients (id)
                  ON DELETE CASCADE,
    flag          INT(2)  NOT NULL DEFAULT 0
) CHARSET=utf8 COLLATE utf8_general_ci;
