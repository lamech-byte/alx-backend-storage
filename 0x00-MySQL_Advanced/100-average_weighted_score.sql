-- Create the ComputeAverageWeightedScoreForUser stored procedure
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE total_weight FLOAT DEFAULT 0;
    DECLARE weighted_average FLOAT DEFAULT 0;
    
    -- Calculate the total score and total weight for the user
    SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
    INTO total_score, total_weight
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;
    
    -- Calculate the weighted average score
    IF total_weight > 0 THEN
        SET weighted_average = total_score / total_weight;
    ELSE
        SET weighted_average = 0;
    END IF;
    
    -- Update the average_score for the user
    UPDATE users
    SET average_score = weighted_average
    WHERE id = user_id;
END //
DELIMITER ;
