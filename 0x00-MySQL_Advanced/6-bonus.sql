-- SQL script that creates a stored procedure AddBonus that adds a new correction for a student.
-- Requirements:
-- Procedure AddBonus is taking 3 inputs (in this order):
-- user_id, a users.id value (you can assume user_id is linked to an existing users)
-- project_name, a new or already exists projects - if no projects.name found in the table, you should create it
-- score, the score value for the correction

DELIMITER //
CREATE PROCEDURE AddBonus (
    IN p_user_id INT,
    IN p_project_name VARCHAR(255),
    IN p_score INT
)
-- local variable v_project_id is declared to store the ID of the project
DECLARE v_project_id INT;

-- checks if the project exists in the projects table based on the provided project name
SELECT id INTO v_project_id FROM projects WHERE name = p_project_name;

-- If the project does not exist, it creates a new project.
IF v_project_id IS NULL THEN
    INSERT INTO projects (name) VALUES (project_name);
    SET project_id = LAST_INSERT_ID();
END IF;

--  inserts the correction into the corrections table using the provided user ID, project ID (either existing or newly created), and score
INSERT INTO corrections (user_id, project_id, score) VALUES (p_user_id, v_project_id, p_score);
//
DELIMITER ;
