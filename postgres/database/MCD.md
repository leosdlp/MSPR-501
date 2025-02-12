```mermaid
erDiagram
    disease {
        SERIAL id_disease PK
        BOOLEAN is_pandemic
        VARCHAR(50) name
    }

    statement {
        SERIAL id_statement PK
        DATE _date
        INTEGER confirmed
        INTEGER deaths
        INTEGER recovered
        INTEGER active
        INTEGER total_tests
        INTEGER id_disease FK
        INTEGER id_country FK
    }
    statement ||--|| disease : "references"
    statement ||--|| country : "references"

    region {
        SERIAL id_region PK
        VARCHAR(50) name
    }

    continent {
        SERIAL id_continent PK
        VARCHAR(50) name
    }

    country {
        SERIAL id_country PK
        VARCHAR(50) name
        VARCHAR(5) iso_code
        INTEGER population
        DOUBLE pib
        DOUBLE latitude
        DOUBLE longitude
        INTEGER id_region FK
        INTEGER id_continent FK
    }
    country ||--|| continent : "references"
    country ||--|| region : "references"

    climat_type {
        SERIAL id_climat_type PK
        STRING name
        STRING description
    }

    country_climat_type {
        INTEGER id_climat_type PK
        INTEGER id_country PK
    }
    country_climat_type ||--|| climat_type : "references"
    country_climat_type ||--|| country : "references"
```