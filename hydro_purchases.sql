DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS item_category;
DROP TABLE IF EXISTS supplier;

CREATE TABLE item_category(
c_id INT PRIMARY KEY,
c_description VARCHAR(50)
);

CREATE TABLE supplier(
s_id INT PRIMARY KEY,
s_name VARCHAR(50) NOT NULL,
s_address VARCHAR(50),
s_city VARCHAR(50),
s_state VARCHAR(2),
s_zip INT,
s_phone VARCHAR(10)
);

CREATE TABLE items(
i_id INT PRIMARY KEY,
i_description VARCHAR(50) NOT NULL,
i_category INT REFERENCES item_category(c_id)
);

CREATE TABLE purchases(
p_id INT PRIMARY KEY,
p_date DATE NOT NULL,
p_price DECIMAL NOT NULL,
p_item INT REFERENCES items(i_id),
p_quantity INT NOT NULL,
p_supplier INT REFERENCES supplier(s_id)
);


/* Comment this following out if using GUI and shit
   Will delete all data from tables though... */

INSERT INTO supplier(s_id, s_name, s_address, s_city, s_state, s_zip, s_phone)
VALUES (1, 'Extended Seasons Indoor Gardening', '613 Central Street West', 'Bagley', 'MN', 56621, '2186942002');

INSERT INTO item_category(c_id, c_description)
VALUES (1, 'Plumbing');

INSERT INTO item_category(c_id, c_description)
VALUES (2, 'Nutrient');

INSERT INTO item_category(c_id, c_description)
VALUES (3, 'Medium');

INSERT INTO item_category(c_id, c_description)
VALUES (4, 'Aeration');

INSERT INTO items(i_id, i_description, i_category)
VALUES (1, 'Botanicare Cal-Mag Plus', 2);

INSERT INTO items(i_id, i_description, i_category)
VALUES (2, 'General Hydroponics FloraGro', 2);

INSERT INTO items(i_id, i_description, i_category)
VALUES (3, 'General Hydroponics FloraBloom', 2);

INSERT INTO items(i_id, i_description, i_category)
VALUES (4, 'General Hydroponics FloraMicro', 2);

-- INSERT INTO purchases
-- VALUES (1, '10-20-2020', 20.50, 1, 1, 1)