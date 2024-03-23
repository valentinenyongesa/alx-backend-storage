-- 101-average_weighted_score.sql
-- Task: Create a stored procedure ComputeAverageWeightedScoreForUsers that computes and stores the average weighted score for all students.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE avg_score FLOAT;
    
    -- Cursor to loop through users
    DECLARE user_cursor CURSOR FOR
        SELECT id FROM users;
    
    -- Declare exit handler
    DECLARE CONTINUE HANDLER FOR NOT FOUND
        SET user_id = NULL;

    -- Initialize variables
    SET total_score = 0;
    SET total_weight = 0;
    
    -- Open cursor
    OPEN user_cursor;
    
    -- Loop through users
    user_loop: LOOP
        FETCH user_cursor INTO user_id;
        IF user_id IS NULL THEN
            LEAVE user_loop;
        END IF;
        
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
    END LOOP;

    -- Close cursor
    CLOSE user_cursor;
END//

DELIMITER ;
