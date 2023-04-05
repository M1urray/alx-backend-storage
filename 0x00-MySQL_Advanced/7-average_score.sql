-- SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student.

CREATE PROCEDURE ComputeAverageScoreForUser
    @user_id INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @avg_score DECIMAL(5,2);

    SELECT @avg_score = AVG(score)
    FROM scores
    WHERE user_id = @user_id;

    -- Insert or update the computed average score for the user
    IF EXISTS(SELECT 1 FROM user_scores WHERE user_id = @user_id)
    BEGIN
        UPDATE user_scores
        SET avg_score = @avg_score
        WHERE user_id = @user_id;
    END
    ELSE
    BEGIN
        INSERT INTO user_scores (user_id, avg_score)
        VALUES (@user_id, @avg_score);
    END
END
