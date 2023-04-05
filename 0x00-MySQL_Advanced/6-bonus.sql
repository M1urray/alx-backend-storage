-- SQL script that creates a stored procedure AddBonus that adds a new correction for a student.

CREATE PROCEDURE AddBonus
    @user_id INT,
    @project_name VARCHAR(50),
    @score INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Check if project already exists, create if it does not
    IF NOT EXISTS (SELECT 1 FROM projects WHERE name = @project_name)
    BEGIN
        INSERT INTO projects (name) VALUES (@project_name);
    END
    
    -- Insert correction for the student
    DECLARE @project_id INT;
    SELECT @project_id = id FROM projects WHERE name = @project_name;
    
    INSERT INTO corrections (user_id, project_id, score) VALUES (@user_id, @project_id, @score);
    
    -- Return success message
    SELECT 'Correction added successfully.' AS message;
END

