CREATE TABLE skill_prerequisites (
    skill_id INTEGER NOT NULL,
    prerequisite_skill_id INTEGER NOT NULL,

    PRIMARY KEY (skill_id, prerequisite_skill_id),

    FOREIGN KEY (skill_id) REFERENCES skills(id),
    FOREIGN KEY (prerequisite_skill_id) REFERENCES skills(id)
);