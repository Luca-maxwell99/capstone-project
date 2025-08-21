SELECT
    CAST(period AS DATE) AS month,
    org_code,
    org_name,
    patients_12hr_wait,
    latitude,
    longitude
FROM de_2506_a.ae_attendances
WHERE CAST(period AS DATE) = (
    SELECT MAX(CAST(period AS DATE)) FROM de_2506_a.ae_attendances
)
ORDER BY patients_12hr_wait DESC
