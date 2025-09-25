import time
import requests
import statistics
from concurrent.futures import ThreadPoolExecutor

# Test de performance pour l'API optimisée
API_BASE = "https://api.b-tech.ovh:8000"

def test_taxi_endpoint():
    """Test l'endpoint taxi"""
    data = {
        "distance_km": 25.5,
        "minutes_attente": 5,
        "aller_retour": True
    }
    start = time.time()
    response = requests.post(f"{API_BASE}/calculer-tarif", json=data)
    end = time.time()
    return end - start, response.status_code == 200

def test_cpam_endpoint():
    """Test l'endpoint CPAM"""
    data = {
        "distance_km": 30.0,
        "ville_depart": "La Roche sur Yon",
        "ville_arrivee": "Nantes",
        "departement": "85",
        "tarif_nuit": True,
        "type_transport": "simple",
        "nb_patients": 2,
        "tpmr": True,
        "peages": 5.50
    }
    start = time.time()
    response = requests.post(f"{API_BASE}/calculer-tarif-cpam", json=data)
    end = time.time()
    return end - start, response.status_code == 200

def run_performance_test(test_func, test_name, iterations=50):
    """Execute un test de performance"""
    print(f"\n🚀 Test de performance: {test_name}")
    print(f"Exécution de {iterations} requêtes...")

    times = []
    success_count = 0

    for i in range(iterations):
        duration, success = test_func()
        times.append(duration)
        if success:
            success_count += 1

        # Affichage du progrès
        if (i + 1) % 10 == 0:
            print(f"  {i + 1}/{iterations} requêtes terminées")

    # Statistiques
    avg_time = statistics.mean(times) * 1000  # en ms
    min_time = min(times) * 1000
    max_time = max(times) * 1000
    median_time = statistics.median(times) * 1000
    success_rate = (success_count / iterations) * 100

    print(f"\n📊 Résultats pour {test_name}:")
    print(f"  ✅ Taux de succès: {success_rate:.1f}%")
    print(f"  ⏱️  Temps moyen: {avg_time:.2f} ms")
    print(f"  ⚡ Temps minimum: {min_time:.2f} ms")
    print(f"  🐌 Temps maximum: {max_time:.2f} ms")
    print(f"  📈 Temps médian: {median_time:.2f} ms")

    return {
        "test_name": test_name,
        "avg_time_ms": avg_time,
        "min_time_ms": min_time,
        "max_time_ms": max_time,
        "median_time_ms": median_time,
        "success_rate": success_rate
    }

def test_cache_effectiveness():
    """Test l'efficacité du cache LRU en répétant les mêmes calculs"""
    print("\n🎯 Test d'efficacité du cache LRU")

    # Mêmes données répétées pour tester le cache
    taxi_data = {"distance_km": 15.0, "minutes_attente": 3, "aller_retour": False}
    cpam_data = {"distance_km": 20.0, "ville_depart": "Nantes", "ville_arrivee": "Paris", "departement": "85"}

    # Premier appel (cache miss)
    start = time.time()
    requests.post(f"{API_BASE}/calculer-tarif", json=taxi_data)
    first_call = time.time() - start

    # Appels suivants (cache hit)
    cache_times = []
    for _ in range(10):
        start = time.time()
        requests.post(f"{API_BASE}/calculer-tarif", json=taxi_data)
        cache_times.append(time.time() - start)

    avg_cache_time = statistics.mean(cache_times)

    print(f"  🥇 Premier appel (cache miss): {first_call*1000:.2f} ms")
    print(f"  ⚡ Appels suivants (cache hit): {avg_cache_time*1000:.2f} ms")
    print(f"  📈 Amélioration: {((first_call - avg_cache_time) / first_call * 100):.1f}%")

if __name__ == "__main__":
    print("🔥 Test de performance de l'API Taxi Vendée optimisée")
    print("=" * 60)

    try:
        # Test de connectivité
        response = requests.get(f"{API_BASE}/verifier-sante")
        if response.status_code != 200:
            print("❌ Impossible de se connecter à l'API")
            exit(1)

        print(f"✅ API accessible sur {API_BASE}")

        # Tests de performance
        taxi_results = run_performance_test(test_taxi_endpoint, "Endpoint Taxi", 30)
        cpam_results = run_performance_test(test_cpam_endpoint, "Endpoint CPAM", 30)

        # Test du cache
        test_cache_effectiveness()

        # Résumé final
        print("\n" + "=" * 60)
        print("📋 RÉSUMÉ DES PERFORMANCES")
        print("=" * 60)
        print(f"🚕 Taxi - Temps moyen: {taxi_results['avg_time_ms']:.2f} ms")
        print(f"🏥 CPAM - Temps moyen: {cpam_results['avg_time_ms']:.2f} ms")
        print("\n✨ Optimisations appliquées:")
        print("  • Cache LRU pour calculs répétitifs")
        print("  • Compression GZip pour réponses")
        print("  • Méthodes cachées pour performance")

    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API. Vérifiez qu'elle est bien démarrée.")
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")