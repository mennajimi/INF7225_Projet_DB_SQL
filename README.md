# INF7225_Projet_DB_SQL
<h3>Contexte du projet</h3>
Dans le cadre de mon travail d’analyste de données cliniques pour une société de recherche contractuelle, je dois analyser les données de patients inscrit dans des études cliniques. La compagnie doit donc gérer un grand volume de données de patients ainsi que de données expérimentales. Cependant, les employés de ce genre de sociétés ont généralement une formation dans le domaine de la biologie, la médecine ou la biotechnologie. Ils sont ainsi peu formés dans le domaine de l’informatique. Ainsi, les données de patients sont gérées et entreposé sous la forme de fichier excel. Il y a un fichier excel par étude, dont l’information est éditée manuellement et révisée aussi manuellement. Ainsi, à chaque fois qu’on désire accéder à une information spécifique sur le patient il faut aller sur le serveur et aller chercher le fichier excel dans le dossier propre à l’étude d’intérêt. Considérant que c’est une compagnie internationale avec des laboratoires sur chaque continent, l’architecture et la hiérarchie ne sont pas uniformisées et peuvent varier en fonction de la branche de la compagnie. Toutefois, le département d’analyse de donnée est centralisé à une seule branche, mais doit gérer de l’information qui ne l’est pas. Accéder aux informations sur les expériences que l’on analyse devient donc une tâche inefficace limitant la productivité.

<h4>Objectif du projet</h4>
Générer un outil de query web permettant de centraliser l’information à une base de données pour le département d’analyse de données. Mon objectif dans le cadre du projet est de modelisé les données qui sont utlisé par ma firme sous forme d’une base de données relationnelles pour simplifier l’usage quotidien de ces données. L’usager devrait être capable de téléverser les différents documents contenant les informations sur les patients sur un serveur afin que ces informations soient intégrées à une base de donnée que l’on peut ensuite interroger.

<h4>Utilisation du programme</h4>
<pre>
-Initialiser la DB avec le fichier Db_init.sql
-Faire rouler le serveur Flask avec le fichier main2.py
-Loader fichier csv provenant de DataSetTest pour pouvoir effectuer des query sur le serveur
</pre>


