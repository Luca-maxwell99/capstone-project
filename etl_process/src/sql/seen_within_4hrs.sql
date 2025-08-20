SELECT
  CAST(period AS date)          AS period,
  org_code,
  org_name,
  SUM(ae_attendances_type_1)    AS attendances_type_1,
  SUM(attendances_over_4hrs_type_1) AS over_4hrs_type_1,

  CASE
    WHEN SUM(ae_attendances_type_1) = 0 THEN NULL
    ELSE 100.0 * (SUM(ae_attendances_type_1) - SUM(attendances_over_4hrs_type_1))
               / SUM(ae_attendances_type_1)
  END AS pct_seen_within_4hrs
FROM de_2506_a.ae_attendances   
GROUP BY CAST(period AS date), org_code, org_name
ORDER BY period, org_name;
