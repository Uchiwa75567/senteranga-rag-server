#!/usr/bin/env python3
"""
Test script pour vérifier que le serveur RAG fonctionne avant déploiement
"""
import os
import sys
import requests
import time

def test_server():
    """Test local du serveur avant déploiement"""
    print("🧪 Test du serveur RAG avant déploiement")
    print("=" * 50)

    # Test health endpoint
    try:
        print("1. Test du health endpoint...")
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health OK")
            print(f"   - Index chargé: {data.get('index_loaded', False)}")
            print(f"   - Chunks: {data.get('index_chunks', 0)}")
            print(f"   - Gemini configuré: {data.get('gemini_configured', False)}")
        else:
            print(f"❌ Health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health error: {e}")
        return False

    # Test chat endpoint
    try:
        print("\n2. Test du chat endpoint...")
        payload = {
            "message": "Bonjour, que fait SENTERANGA?",
            "userContext": {"userType": "agriculteur", "region": "Dakar"}
        }
        response = requests.post("http://localhost:8000/chat", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat OK")
            print(f"   - Réponse: {data.get('response', '')[:100]}...")
            print(f"   - Sources: {len(data.get('sources', []))}")
            print(f"   - Backend: {data.get('backend', 'unknown')}")
        else:
            print(f"❌ Chat failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return False

    print("\n🎉 Tous les tests sont passés ! Le serveur est prêt pour le déploiement.")
    return True

if __name__ == "__main__":
    # Vérifier que le serveur tourne
    try:
        requests.get("http://localhost:8000/health", timeout=5)
    except:
        print("❌ Le serveur ne tourne pas. Lancez d'abord:")
        print("   cd server/local_rag && ./start.sh")
        sys.exit(1)

    success = test_server()
    sys.exit(0 if success else 1)