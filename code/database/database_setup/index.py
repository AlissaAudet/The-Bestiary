create_indexs = [
    """
    CREATE INDEX user_name ON User(first_name, last_name);
    """
    ,
    """
    CREATE INDEX observed_species ON Observation(species);
    """
]