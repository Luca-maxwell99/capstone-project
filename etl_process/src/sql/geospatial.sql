SELECT
    period,
    org_code,
    org_name,
    ae_attendances_type_1,
    attendances_over_4hrs_type_1,
    patients_12hr_wait,
    emergency_admissions_type_1,
    postcode,
    latitude,
    longitude
FROM
    de_2506_a.ae_attendances
WHERE
    (ae_attendances_type_1 > 0 OR attendances_over_4hrs_type_1 > 0 OR patients_12hr_wait > 0)
    AND latitude IS NOT NULL
    AND longitude IS NOT NULL
ORDER BY
    period DESC;