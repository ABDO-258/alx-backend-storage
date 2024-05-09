-- script that creates a trigger that decreases the quantity of an item after adding a new order.
-- Quantity in the table items can be negative.

CREATE TRIGGER quantity_decrease AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;
