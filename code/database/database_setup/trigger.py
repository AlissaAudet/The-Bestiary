create_triggers = [
    """
       CREATE TRIGGER after_note_insert
       AFTER INSERT ON Note
       FOR EACH ROW
       BEGIN
       DECLARE avg_rating FLOAT;
   
       SELECT AVG(N.rating)
       INTO avg_rating
       FROM Note N
       WHERE N.observation_oid = NEW.observation_oid;
   
       UPDATE Observation
       SET rating = avg_rating
       WHERE oid = NEW.observation_oid;
       END
       """
    ,
    """
    CREATE TRIGGER after_note_update
    AFTER UPDATE ON Note
    FOR EACH ROW
    BEGIN
    DECLARE avg_rating FLOAT;

    SELECT AVG(N.rating)
    INTO avg_rating
    FROM Note N
    WHERE N.observation_oid = NEW.observation_oid;

    UPDATE Observation
    SET rating = avg_rating
    WHERE oid = NEW.observation_oid;
    END
    """
    ,
    """
    CREATE TRIGGER observation_count_update_insert
    AFTER INSERT ON Observation
    FOR EACH ROW
    BEGIN
    UPDATE User
    SET observation_count = observation_count + 1
    WHERE uid = NEW.author_uid;
    END;
    """
    ,
    """
    CREATE TRIGGER observation_count_update_delete
    AFTER DELETE ON Observation
    FOR EACH ROW
    BEGIN
    UPDATE User
    SET observation_count = observation_count - 1
    WHERE uid = OLD.author_uid;
    END;
    """
    ,
    """
    CREATE TRIGGER filter_language_comment_insert
BEFORE INSERT ON Comment
FOR EACH ROW
BEGIN
    IF contains_forbidden_word(NEW.text) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Profanity is not allowed in comments.';
    END IF;
END;
    """
    ,
    """
    CREATE TRIGGER filter_language_update BEFORE UPDATE ON Comment
    FOR EACH ROW
    BEGIN
    IF contains_forbidden_word(NEW.text) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Profanity is not allowed in comments.';
    END IF;
END;
    """
]