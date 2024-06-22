CREATE OR REPLACE FUNCTION public.levenshtein_distance (str1 text, str2 text) RETURNS integer LANGUAGE plpgsql AS $function$
DECLARE
    m integer := length(str1);
    n integer := length(str2);
    d integer[][] := array_fill(0, ARRAY[m+1,n+1]);
    i integer;
    j integer;
    cost integer;
BEGIN
    IF m = 0 THEN
        RETURN n;
    END IF;

    IF n = 0 THEN
        RETURN m;
    END IF;

    FOR i IN 1..m LOOP
        d[i][1] := i;
    END LOOP;

    FOR j IN 1..n LOOP
        d[1][j] := j;
    END LOOP;

    FOR j IN 2..n LOOP
        FOR i IN 2..m LOOP
            IF substring(str1 from i for 1) = substring(str2 from j for 1) THEN
                cost := 0;
            ELSE
                cost := 1;
            END IF;

            d[i][j] := least(d[i-1][j] + 1, d[i][j-1] + 1, d[i-1][j-1] + cost);
        END LOOP;
    END LOOP;

    RETURN d[m][n];
END;
$function$
