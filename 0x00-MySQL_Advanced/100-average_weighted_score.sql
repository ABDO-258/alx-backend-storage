-- script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.
-- Requirements:
-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (
            IN user_id INT
)
BEGIN
    -- local variables
    DECLARE v_total_score FLOAT;
    DECLARE v_total_weight FLOAT;
    DECLARE v_average_score FLOAT;

    -- Calculate total weighted score and total weight
    SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
    INTO v_total_score, v_total_weight
    FROM corrections
    INNER JOIN projects  ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Calculate average weighted score
    IF v_total_weight > 0 THEN
        SET v_average_score = v_total_score / v_total_weight;
    ELSE
        SET v_average_score = 0;
    END IF;

    -- Update average_score in the users table
    UPDATE users
    SET average_score = v_average_score
    WHERE id = user_id;
END;
//
DELIMITER ;
