SELECT
    ball_1, ball_2, ball_3, ball_4, ball_5, mega, COUNT(*)
FROM
    draws
GROUP BY
    ball_1, ball_2, ball_3, ball_4, ball_5, mega
HAVING 
    COUNT(*) > 1
