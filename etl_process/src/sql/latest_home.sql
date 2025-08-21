SELECT
    CAST(period AS DATE) AS month,
    SUM(ae_attendances_type_1) AS attendances_type_1,
    SUM(attendances_over_4hrs_type_1) AS breaches,
    SUM(patients_12hr_wait) AS patients_12hr_wait,
    ROUND(
        (
            100.0 * (
                SUM(ae_attendances_type_1) - SUM(attendances_over_4hrs_type_1)
            ) / NULLIF(SUM(ae_attendances_type_1), 0)
        )::numeric,
        1
    ) AS pct_seen_within_4hrs
FROM de_2506_a.ae_attendances
GROUP BY CAST(period AS DATE)
ORDER BY month;