# WazeGasPriceFeed

This command-line application is fetching gas prices from the French government open-data platform and format them to be used by Waze.

----

Cette application récupère les prix des carburants depuis la plateforme open-data du gouvernement français et les formate pour être utilisés par Waze.


## Données initiales

Les scripts générant les données initiales sont disponibles dans le dossier `/init`.

- Les stations sont récupérées depuis le site [https://www.prix-carburants.gouv.fr/rubrique/opendata/](https://www.prix-carburants.gouv.fr/rubrique/opendata/).
- La correspondance entre les ID des stations données par le gouvernement et celles fournies par Waze est fait à l'aide de `matchPOI.py` qui utilise un fichier fourni par Waze (non-inclus dans ce dépôt).

## Synchronisation

La synchronisation se fait toutes les heures via un cronjob. Les données sont récupérées depuis notre base (sur Google Sheets) et la base du gouvernement (en ZIP) puis sont fusionnées et formatées pour être utilisées par Waze.

Le fichier de sortie `output.json` est formaté de la manière suivante :
```
{
    "gas_prices":
    [
        {
            "venue_id": "WAZE_STATION_ID",
            "location":
            [
                latitude,
                longitude
            ],
            "updated": nixtimestamp,
            "prices":
            [
                {
                    "name": "gas1_name",
                    "price": price
                },
                {
                    "name": "gas2_name",
                    "price": price
                }
            ]
        }
    ]
}

```

## Configuration

Le fichier `config.py` contient les variables de configuration suivantes :
- \_\_govURL\_\_ : L'URL des données du gouvernement (ZIP)
- \_\_stationsURL\_\_ :L'URL vers le fichier de correspondance des stations Waze / gouvernement
- gas_map : La correspondance entre les noms des carburants du gouvernement et ceux dans Waze
- overrideSP95 : Si `True` et si le E10 n'est pas proposé dans la station, le prix du SP95 est utilisé à la place
- \_\_extURL\_\_ : L'URL du webhook externe (mise à jour quotidienne)
- \_\_intURL\_\_ : L'URL du webhook interne (mise à jour toutes les heures)
- \_\_brandnames\_\_ : Définit les noms des marques de stations à utiliser afin d'éviter les erreurs de correspondance