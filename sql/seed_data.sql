USE recipe_db;

-- Ingredients
INSERT INTO ingredients (name, unit) VALUES
('Chicken Breast','grams'),
('Salt','grams'),
('Pepper','grams'),
('Olive Oil','ml'),
('Garlic','grams'),
('Onion','grams'),
('Tomato','grams'),
('Basil','grams'),
('Pasta','grams'),
('Milk','ml');

-- Recipes
INSERT INTO recipes (title, description, servings, prep_time_minutes, cook_time_minutes)
VALUES
('Garlic Chicken', 'Pan-seared garlic chicken.', 2, 10, 15),
('Tomato Pasta', 'Easy tomato basil pasta.', 3, 15, 20);

-- Steps for Garlic Chicken (recipe_id 1)
INSERT INTO steps (recipe_id, step_number, instruction) VALUES
(1,1,'Marinate chicken with salt and pepper for 10 minutes.'),
(1,2,'Heat olive oil in pan and sear chicken 6-7 minutes per side.'),
(1,3,'Add minced garlic, cook 1-2 minutes and serve.');

-- Steps for Tomato Pasta (recipe_id 2)
INSERT INTO steps (recipe_id, step_number, instruction) VALUES
(2,1,'Boil pasta until al dente.'),
(2,2,'Saute onion and garlic, add tomatoes and simmer.'),
(2,3,'Toss pasta with sauce and garnish with basil.');

-- Recipe ingredients
-- Garlic Chicken
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, note) VALUES
(1, (SELECT id FROM ingredients WHERE name='Chicken Breast'), 400, 'sliced'),
(1, (SELECT id FROM ingredients WHERE name='Salt'), 5, 'to taste'),
(1, (SELECT id FROM ingredients WHERE name='Pepper'), 2, 'to taste'),
(1, (SELECT id FROM ingredients WHERE name='Olive Oil'), 30, 'for frying'),
(1, (SELECT id FROM ingredients WHERE name='Garlic'), 10, 'minced');

-- Tomato Pasta
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, note) VALUES
(2, (SELECT id FROM ingredients WHERE name='Pasta'), 300, 'dried'),
(2, (SELECT id FROM ingredients WHERE name='Tomato'), 400, 'chopped'),
(2, (SELECT id FROM ingredients WHERE name='Onion'), 80, 'sliced'),
(2, (SELECT id FROM ingredients WHERE name='Garlic'), 8, 'minced'),
(2, (SELECT id FROM ingredients WHERE name='Basil'), 5, 'fresh');
