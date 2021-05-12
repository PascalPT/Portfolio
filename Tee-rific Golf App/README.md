Pascal Pelletier-Thériault
(Charles Berthiaume, Geneviève Moisan, Michaël Nadeau)

Mandat : Élaborer un modèle qui utilise la théorie de la crédibilité afin de prévoir le total d'une ronde de golf d'un quatuor à partir du nombre de coups joués par l'équipe aux trous précédents. 
		 Dans le but d'obtenir le meilleur modèle possible, trois modèles ont été créés. Ils ont été comparés et le meilleur modèle a été utilisé pour produire un prototype d'application 
         	 de calcul des prévisions à l'aide de la technologie Shiny.  


L'url du prototype d'application Shiny : https://pascal-pell-ther.shinyapps.io/tee-rific_golf_app/

         
La branche 'master' du présent dépôt contient des codes sources R Markdown de rapport de production du prototype, ainsi que des scripts qui ont pu nous être utile.
Il y a aussi le code source de ce prototype d'application Shiny.


Les fichiers suivants sont directement dans la racine du dépôt :

	- 'rapport-etape-1.Rmd', le mandat, les réalisations et les apprentissages suite à l'élaboration du premier modèle.

	- 'rapport-etape-2.Rmd', le mandat, les réalisations et les apprentissages suite à l'élaboration du deuxième modèle.

	- 'rapport-etape-3.Rmd', le mandat, les réalisations et les apprentissages suite à l'élaboration du troisième modèle.

	- 'rapport-final.Rmd', le mandat, les réalisations, les apprentissages, le choix du modèle de prévision et les conclusions du travail.

	- 'resultats-partiels.csv', les prévisions pour les 600 rondes de golf dont les résultats finaux sont prédits.

	- 'runApp.R', un simple script pour lancer le prototype d'application shiny.

	- 'README.md', le fichier texte présentement lu.

Le fichier suivant est dans "prototype" :

	- 'app.R', le code source d'une application shiny servant à rendre la prédiction du résultat d'une ronde plus "user friendly" que 'Partiels_Data.R' et dont la totalité du dossier "prototype" est nécessaire à son bon fontionnement.

Les fichiers suivants sont dans "prototype/Data" :

	- 'resultats-complets.csv', les résultats complets de 2000 rondes de golf.
  
	- 'resultats-partiels.csv', les résultats partiels de 600 rondes de golf assimilables à des parties en cours dont les résultats finaux sont manquants.

	- 'normales.csv', les normales (par) des 18 trous du Club de golf Beaconsfield.

Les fichiers suivants sont dans "prototype/Scripts" :

	- 'Gestionnaire_Data.R', le code source des fonctions de gestions de données brutes.

	- 'Init.R', le code source de l'environnement inital nécessaire pour faire des prédictions.

	- 'Modèles.R', le code source des fonctions de prédictions et de leurs paramétrisations.

	- 'Partiels_Data.R', le code source d'un script prédisant les résultats de 'resultats-partiels.csv' situé dans "prototype/Data" et déposant la prédiction à la racine du dépôt.

	- 'Vérifications.R', le code source des fonctions de vérifications des modèles et des données entrées par un utilisateur.

Les fichiers suivants sont dans "Autre" :

	- 'Démarche-Modèle.png', une image montrant certaines démarches complètes de l'élaboration de modèles bayesiens.

	- 'Deprecated.R', le code source de modèles qui ont été retirés, car trop imprécis ou non-fonctionnels.

	- 'Pré-Analyse.R', le code source d'un script illustrant certaines des hypothèses faites dans la gestion des données erronées et dans le choix des modèles.

	- 'server.R', le code source d'un script définissant un serveur shiny qui peut importer un csv quelconque.

	- 'ui.R', le code source de l'interface utilisateur du serveur mentionné juste ci-haut.
