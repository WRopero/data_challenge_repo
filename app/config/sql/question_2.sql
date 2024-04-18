WITH hired_emplyees_filtered AS
  (SELECT CAST(REPLACE(REPLACE(he.datetime, 'T', ' '), 'Z', '') AS DATE) AS dates,
          he.department_id,
          he.job_id
   FROM hired_employees he),
     job_department_by_quarter_cleaned AS
  (SELECT YEAR(hef.dates) AS years,
          d.department,
          j.job,
          hef.department_id
   FROM hired_emplyees_filtered AS hef
   INNER JOIN jobs AS j ON j.id = hef.job_id
   INNER JOIN departments AS d ON d.id = hef.department_id),
     jobs_2021_by_department AS
  (SELECT jdqc.department,
          count(*) num_jobs_year
   FROM job_department_by_quarter_cleaned AS jdqc
   WHERE jdqc.years = 2021
   GROUP BY 1),
     avg_jobs21 AS
  (SELECT round(AVG(jbd21.num_jobs_year)) avg_jobs21
   FROM jobs_2021_by_department AS jbd21)
SELECT jc.department_id AS id,
       jc.department,
       count(*) hired
FROM job_department_by_quarter_cleaned AS jc
GROUP BY 1,
         2
HAVING count(*) >
  (SELECT avg_jobs21
   FROM avg_jobs21)
ORDER BY 3 DESC