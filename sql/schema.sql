-- schema.sql
DROP DATABASE IF EXISTS recipe_db;
CREATE DATABASE recipe_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE recipe_db;

-- recipes table
CREATE TABLE recipes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  servings INT DEFAULT 1,
  prep_time_minutes INT DEFAULT 0,
  cook_time_minutes INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ingredients table
CREATE TABLE ingredients (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  unit VARCHAR(50) DEFAULT 'unit', -- e.g., grams, ml, pcs
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- steps table
CREATE TABLE steps (
  id INT AUTO_INCREMENT PRIMARY KEY,
  recipe_id INT NOT NULL,
  step_number INT NOT NULL,
  instruction TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- recipe_ingredients (many-to-many) normalized
CREATE TABLE recipe_ingredients (
  id INT AUTO_INCREMENT PRIMARY KEY,
  recipe_id INT NOT NULL,
  ingredient_id INT NOT NULL,
  quantity DECIMAL(10,2) DEFAULT 0,
  note VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
  FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE,
  UNIQUE KEY unique_recipe_ingredient (recipe_id, ingredient_id)
);

-- audit table to record updates (used by triggers)
CREATE TABLE recipe_audit (
  id INT AUTO_INCREMENT PRIMARY KEY,
  recipe_id INT,
  action VARCHAR(50), -- INSERT, UPDATE, DELETE
  action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  details TEXT
);

-- Trigger: after insert on recipes -> audit
DELIMITER $$
CREATE TRIGGER trg_after_insert_recipe
AFTER INSERT ON recipes
FOR EACH ROW
BEGIN
  INSERT INTO recipe_audit (recipe_id, action, details)
  VALUES (NEW.id, 'INSERT', CONCAT('Recipe created: ', NEW.title));
END$$
DELIMITER ;

-- Trigger: after update
DELIMITER $$
CREATE TRIGGER trg_after_update_recipe
AFTER UPDATE ON recipes
FOR EACH ROW
BEGIN
  INSERT INTO recipe_audit (recipe_id, action, details)
  VALUES (NEW.id, 'UPDATE', CONCAT('Recipe updated: ', NEW.title));
END$$
DELIMITER ;

-- Trigger: after delete
DELIMITER $$
CREATE TRIGGER trg_after_delete_recipe
AFTER DELETE ON recipes
FOR EACH ROW
BEGIN
  INSERT INTO recipe_audit (recipe_id, action, details)
  VALUES (OLD.id, 'DELETE', CONCAT('Recipe deleted: ', OLD.title));
END$$
DELIMITER ;

-- Stored Procedure: get ingredient usage (returns ingredient id, name, total_quantity)
DELIMITER $$
CREATE PROCEDURE sp_get_ingredient_usage()
BEGIN
  SELECT i.id, i.name, i.unit, SUM(ri.quantity) AS total_quantity
  FROM recipe_ingredients ri
  JOIN ingredients i ON ri.ingredient_id = i.id
  GROUP BY i.id, i.name, i.unit
  ORDER BY total_quantity DESC;
END$$
DELIMITER ;
