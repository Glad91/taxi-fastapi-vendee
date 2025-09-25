# 🚀 Guide de déploiement Dokku

## Pré-requis

- Serveur avec Dokku 0.31.3 installé
- Accès SSH au serveur
- Git configuré localement

## Étapes de déploiement

### 1. Préparer le serveur Dokku

```bash
# Se connecter au serveur
ssh root@your-server.com

# Créer l'application
dokku apps:create taxi-api

# Configurer le sous-domaine pour l'API
dokku domains:set taxi-api api.b-tech.ovh

# Configurer les variables d'environnement
dokku config:set taxi-api PORT=8000
dokku config:set taxi-api LOG_LEVEL=INFO
dokku config:set taxi-api PRODUCTION=true

# Configurer HTTPS avec Let's Encrypt pour le sous-domaine
dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
dokku letsencrypt:set taxi-api email your-email@b-tech.ovh
dokku letsencrypt:enable taxi-api
```

### 2. Déployer depuis votre machine locale

```bash
# Ajouter le remote Dokku
git remote add dokku dokku@your-server.com:taxi-api

# Pousser et déployer
git push dokku main

# Vérifier le statut
ssh dokku@your-server.com apps:list
```

### 3. Vérification post-déploiement

```bash
# Vérifier les logs
ssh dokku@your-server.com logs taxi-api

# Tester l'API
curl https://api.b-tech.ovh/verifier-sante

# Vérifier la documentation automatique
# Aller sur: https://api.b-tech.ovh/docs
```

## Commandes utiles

### Gestion de l'application
```bash
# Redémarrer l'application
ssh dokku@your-server.com ps:restart taxi-api

# Voir les informations de l'app
ssh dokku@your-server.com apps:info taxi-api

# Voir les variables d'environnement
ssh dokku@your-server.com config taxi-api
```

### Logs et debugging
```bash
# Voir les logs en temps réel
ssh dokku@your-server.com logs taxi-api -f

# Entrer dans le container
ssh dokku@your-server.com enter taxi-api web
```

### Scaling (optionnel)
```bash
# Scaler l'application (si nécessaire)
ssh dokku@your-server.com ps:scale taxi-api web=2
```

## Configuration avancée

### Backup automatique (recommandé)
```bash
# Installer le plugin de backup
ssh root@your-server.com
dokku plugin:install https://github.com/dokku/dokku-postgres.git

# Configurer les backups automatiques si base de données
# (pas nécessaire pour cette API sans BDD)
```

### Monitoring
```bash
# Voir l'utilisation des ressources
ssh dokku@your-server.com resource:report taxi-api
```

## Mise à jour de l'application

```bash
# Faire les modifications localement
# Puis pousser les changements
git add .
git commit -m "Mise à jour de l'API"
git push dokku main
```

## Dépannage

### Warning locales (normal, peut être ignoré)
```bash
# Si vous voulez corriger le warning des locales sur le serveur
ssh root@your-server.com
apt-get update && apt-get install -y locales-all
# ou
dpkg-reconfigure locales
```

### Si le déploiement échoue
```bash
# Vérifier les logs de build
ssh dokku@your-server.com logs taxi-api --tail 100

# Vérifier la configuration
ssh dokku@your-server.com config taxi-api
```

### Si l'application ne répond pas
```bash
# Vérifier que l'app est running
ssh dokku@your-server.com ps:report taxi-api

# Redémarrer si nécessaire
ssh dokku@your-server.com ps:restart taxi-api
```