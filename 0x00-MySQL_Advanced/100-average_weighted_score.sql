-- 100-average_weighted_score.sql
-- Task: Create a stored procedure ComputeAverageWeightedScoreForUser that computes and stores the average weighted score for a student.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE avg_score FLOAT;

    -- Initialize variables
    SET total_score = 0;
    SET total_weight = 0;
    
    -- Calculate total weighted score
    SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
    INTO total_score, total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;
    
    -- Calculate average weighted score
    IF total_weight > 0 THEN
        SET avg_score = total_score / total_weight;
    ELSE
        SET avg_score = 0;
    END IF;

    -- Update average_score for the user
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END//

DELIMITER ;
