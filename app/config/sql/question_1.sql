WITH hired_emplyees_filtered AS(
SELECT 
	CAST(REPLACE(REPLACE(he.datetime, 'T', ' '), 'Z', '') AS DATE) AS dates ,
    he.department_id,
    he.job_id
FROM hired_employees he),
job_department_by_quarter_cleaned AS (
  SELECT QUARTER(hef.dates) quarter,
		d.department,
    j.job
	FROM hired_emplyees_filtered AS hef 
      INNER JOIN jobs AS j ON j.id = hef.job_id
      INNER JOIN departments AS d ON d.id = hef.department_id
      WHERE year(hef.dates) = 2021)
SELECT 
			jdqc.department,
      jdqc.job,			
			SUM(CASE WHEN jdqc.quarter BETWEEN 1 AND 3 THEN 1 ELSE 0 END) AS  "Q1",
      SUM(CASE WHEN jdqc.quarter BETWEEN 4 AND 6 THEN 1 ELSE 0 END) AS  "Q2",
      SUM(CASE WHEN jdqc.quarter BETWEEN 7 AND 9 THEN 1 ELSE 0 END) AS  "Q3",
      SUM(CASE WHEN jdqc.quarter BETWEEN 10 AND 12 THEN 1 ELSE 0 END) AS  "Q4"
FROM job_department_by_quarter_cleaned AS jdqc 
GROUP BY 1,2 ORDER BY 1,2 ;