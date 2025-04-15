create_functions = [
    """
    
    
        CREATE FUNCTION contains_forbidden_word(input_text TEXT)
        RETURNS BOOLEAN
        DETERMINISTIC
        BEGIN
            DECLARE forbidden_found BOOLEAN DEFAULT FALSE;
            DECLARE forbidden_word VARCHAR(100);
            DECLARE done INT DEFAULT FALSE;
            DECLARE cur CURSOR FOR SELECT word FROM ForbiddenWords;
            DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
            OPEN cur;
            read_loop: LOOP
                FETCH cur INTO forbidden_word;
                IF done THEN
                    LEAVE read_loop;
                END IF;
    
                IF LOCATE(LOWER(forbidden_word), LOWER(input_text)) > 0 THEN
                    SET forbidden_found = TRUE;
                    LEAVE read_loop;
                END IF;
            END LOOP;
            CLOSE cur;
    
            RETURN forbidden_found;
        END ;
    
    
    
        """
]