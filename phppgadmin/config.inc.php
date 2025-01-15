<?php
/* phpPgAdmin configuration file */
$conf['servers'] = array(
    0 => array(
        'host' => 'postgres', // Nom de votre service PostgreSQL dans le réseau Docker
        'port' => 5432,
        'database' => 'postgres', // Nom de la base de données
        'username' => 'mspr501',  // Nom d'utilisateur
        'password' => 's5t4v5',   // Mot de passe
        'sslmode' => 'prefer',
    ),
);