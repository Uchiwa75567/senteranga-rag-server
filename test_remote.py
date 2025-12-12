import requests
import sys

# URL de production
URL = "https://senteranga-rag-server.onrender.com"

def test_remote():
    print(f"🌍 Test de connexion vers {URL}...")
    
    # 1. Test Health
    try:
        resp = requests.get(f"{URL}/health")
        print(f"Health Status: {resp.status_code}")
        print(f"Health Body: {resp.json()}")
    except Exception as e:
        print(f"❌ Health Error: {e}")

    # 2. Test Chat (Payload Correct)
    print("\n📨 Envoi d'une requête Chat correcte...")
    payload = {
        "message": "Test de connexion",
        "userContext": {}
    }
    
    try:
        resp = requests.post(f"{URL}/chat", json=payload)
        
        if resp.status_code == 200:
            print("✅ Succès (200 OK)")
            print("Réponse:", resp.json())
        elif resp.status_code == 422:
            print("❌ Erreur 422: Format de données invalide sent par le script (ne devrait pas arriver)")
            print(resp.json())
        else:
            print(f"❌ Erreur {resp.status_code}")
            try:
                print(resp.json())
            except:
                print(resp.text)
                
    except Exception as e:
        print(f"❌ Chat Error: {e}")

if __name__ == "__main__":
    test_remote()
