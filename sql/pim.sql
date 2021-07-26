
DROP TABLE if EXISTS notes cascade; 
DROP TABLE if EXISTS hashtags cascade;
DROP TABLE if EXISTS links;



CREATE TABLE notes(
    id serial PRIMARY KEY,
    created_on date,
    title text unique not null ,
    description text not null
);

CREATE TABLE hashtags(
    id serial PRIMARY KEY,
    tag varchar(20) UNIQUE
    
);

CREATE TABLE links(
    id serial PRIMARY KEY,
    notes_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY (notes_id) references notes(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) references hashtags(id) ON DELETE CASCADE,
    UNIQUE (notes_id,tag_id)
    
);
