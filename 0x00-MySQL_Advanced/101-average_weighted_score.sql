-- Create the ComputeAverageWeightedScoreForUsers stored procedure
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    DECLARE done INT DEFAULT FALSE;
    
    -- Declare cursor for selecting users
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Open cursor
    OPEN cur;
    
    -- Loop over users
    read_loop: LOOP
        -- Fetch user_id from cursor
        FETCH cur INTO user_id;
        
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Compute and store the average weighted score for the user
        CALL ComputeAverageWeightedScoreForUser(user_id);
    END LOOP;
    
    -- Close cursor
    CLOSE cur;
END //
DELIMITER ;
