-- Create required tables

CREATE TABLE IF NOT EXISTS drinks(
  drink_name TEXT,
  alternate_drink_name TEXT,
  date_modified TEXT,
  glass_id INTEGER NOT NULL,
  category_id INTEGER NOT NULL,
  alcoholic_id INTEGER NOT NULL,
  id INTEGER NOT NULL,
  PRIMARY KEY(id),
  CONSTRAINT glass_drink FOREIGN KEY (glass_id) REFERENCES glass (id),
  CONSTRAINT category_drink FOREIGN KEY (category_id) REFERENCES category (id),
  CONSTRAINT alcoholic_drink FOREIGN KEY (alcoholic_id) REFERENCES alcoholic (id),
  CONSTRAINT visual_details_drink
    FOREIGN KEY (id) REFERENCES drink_media_info (drink_id)
);

CREATE TABLE IF NOT EXISTS alcoholic(id INTEGER NOT NULL, alcohol TEXT, PRIMARY KEY(id));

CREATE TABLE IF NOT EXISTS category(id INTEGER NOT NULL, category_name TEXT, PRIMARY KEY(id));

CREATE TABLE IF NOT EXISTS drink_tags(
  drink_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  PRIMARY KEY(drink_id),
  CONSTRAINT drink_drink_tags FOREIGN KEY (drink_id) REFERENCES drinks (id),
  CONSTRAINT tags_drink_tags FOREIGN KEY (tag_id) REFERENCES tags (id)
);

CREATE TABLE IF NOT EXISTS drink_media_info(
  drink_id INTEGER NOT NULL,
  video TEXT,
  drink_thumb TEXT,
  image_source TEXT,
  image_attribution TEXT,
  creative_commons_id INTEGER NOT NULL,
  PRIMARY KEY(drink_id),
  CONSTRAINT creative_commons_drink_media_info
    FOREIGN KEY (creative_commons_id) REFERENCES creative_commons (id)
);

CREATE TABLE IF NOT EXISTS glass(id INTEGER NOT NULL, glass_name TEXT, PRIMARY KEY(id));

CREATE TABLE IF NOT EXISTS instructions(
  instructions_en TEXT,
  instructions_es TEXT,
  instructions_de TEXT NOT NULL,
  instructions_fr TEXT,
  instructions_it TEXT,
  instructions_zh_hans TEXT,
  instructions_zh_hant TEXT,
  drink_id INTEGER NOT NULL,
  PRIMARY KEY(drink_id),
  CONSTRAINT drinks_instructions FOREIGN KEY (drink_id) REFERENCES drinks (id)
);

CREATE TABLE IF NOT EXISTS ingredients
  (id INTEGER NOT NULL, ingredient_name TEXT, PRIMARY KEY(id));

CREATE TABLE IF NOT EXISTS measures
  (id INTEGER NOT NULL, measure_quantity INTEGER, PRIMARY KEY(id));

CREATE TABLE IF NOT EXISTS drink_recipe(
  --id INTEGER NOT NULL,
  ingredient_id INTEGER NOT NULL,
  measure_id INTEGER NOT NULL,
  drink_id INTEGER NOT NULL,
  PRIMARY KEY(ingredient_id, measure_id, drink_id),
  CONSTRAINT ingredients_drink_receipe
    FOREIGN KEY (ingredient_id) REFERENCES ingredients (id),
  CONSTRAINT measures_drink_receipe
    FOREIGN KEY (measure_id) REFERENCES measures (id),
  CONSTRAINT drink_drink_receipe FOREIGN KEY (drink_id) REFERENCES drinks (id)
);

CREATE TABLE IF NOT EXISTS tags(id INTEGER NOT NULL, tag_name TEXT, PRIMARY KEY(id));

CREATE TABLE IF NOT EXISTS drink_iba_tags(
  drink_id INTEGER NOT NULL,
  iba_tags_id INTEGER NOT NULL,
  PRIMARY KEY(drink_id),
  CONSTRAINT drink_drink_iba_tags FOREIGN KEY (drink_id) REFERENCES drinks (id),
  CONSTRAINT iba_tags_drink_iba_tags
    FOREIGN KEY (iba_tags_id) REFERENCES iba_tags (id)
);

CREATE TABLE IF NOT EXISTS iba_tags(id INTEGER NOT NULL, iba_tag_name TEXT, PRIMARY KEY(id));

CREATE TABLE IF NOT EXISTS creative_commons
  (id INTEGER NOT NULL, creative_commons_confirmed TEXT, PRIMARY KEY(id));
