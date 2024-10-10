# İlk olarak, Flask'i ve gerekli kütüphaneleri projeye dahil edeceğiz.
from flask import Flask, request, jsonify
import requests
import os
from collections import defaultdict

# Projemizi başlatıyoruz.
app = Flask(__name__)

# Root endpoint: Uygulama çalışıyor mesajı göstermek için
@app.route('/')
def home():
    return jsonify({"message": "Uygulama çalışıyor!"})

# Burada bir yapı kuracağız, bu yapı login endpointini kullanarak JWT token alacak.
# Bu token diğer API isteklerinde güvenlik amacıyla kullanılacak.
# get_jwt_token() fonksiyonu, API'ye giriş yaparak bize token sağlar.
# Bu token, diğer API isteklerinde kimlik doğrulama için kullanılır.

def get_jwt_token():
    url = "https://sandbox-reporting.rpdpymnt.com/api/v3/merchant/user/login"
    credentials = {
        "email": "demo@financialhouse.io",
        "password": "cjaiU8CV"
    }
    response = requests.post(url, json=credentials)
    if response.status_code == 200:
        return response.json().get("token")
    else:
        return None

# Şimdi API için token aldık ve kullanabiliriz.
# İlk endpoint: Merchant login ve transaction report için basit bir endpoint yapıyoruz.
# transactions_report() fonksiyonu, belirli bir tarih aralığındaki transaction raporlarını almak için kullanılır.
# Burada, JWT token'ı alıp bu token ile transaction rapor endpointine istek gönderiyoruz.
@app.route('/transactions_report', methods=['GET'])
def transactions_report():
    token = get_jwt_token()
    if not token:
        return jsonify({"error": "Giriş yapılamadı, token alınamadı"}), 401

    # Transaction rapor endpointine istek gönderiyoruz.
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "fromDate": "2024-01-01",
        "toDate": "2024-01-31"
    }
    url = "https://sandbox-reporting.rpdpymnt.com/api/v3/transactions/report"
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Rapor alınamadı"}), response.status_code

# Daha ayrıntılı bir transaction listesi almak için yeni bir endpoint ekliyoruz.
# transaction_list() fonksiyonu, belirli kriterlere göre transaction listesini almak için kullanılır.
# Bu fonksiyon, gelen transaction verilerini filtreler ve tutarlarına göre sıralar.
@app.route('/transaction_list', methods=['GET'])
def transaction_list():
    token = get_jwt_token()
    if not token:
        return jsonify({"error": "Giriş yapılamadı, token alınamadı"}), 401

    # Transaction list endpointine istek gönderiyoruz.
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "fromDate": "2024-01-01",
        "toDate": "2024-01-31",
        "status": "APPROVED",
        "operation": "3D"
    }
    url = "https://sandbox-reporting.rpdpymnt.com/api/v3/transaction/list"
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        transaction_data = response.json().get("data", [])
        # Burada transaction verilerini filtreleyip sıralıyoruz.
        # Onaylanan işlemleri filtreliyoruz ve tutarı büyükten küçüğe sıralıyoruz.
        filtered_transactions = [t for t in transaction_data if t.get("transaction", {}).get("status") == "APPROVED"]
        sorted_transactions = sorted(filtered_transactions, key=lambda x: x.get("transaction", {}).get("amount", 0), reverse=True)
        return jsonify(sorted_transactions)
    else:
        return jsonify({"error": "Transaction listesi alınamadı"}), response.status_code

# Daha dinamik filtreleme ve arama için ek bir endpoint ekliyoruz.
# Bu endpoint, kullanıcıdan alınan parametreler doğrultusunda transaction'ları filtreleyecek.
@app.route('/dynamic_transaction_search', methods=['POST'])
def dynamic_transaction_search():
    token = get_jwt_token()
    if not token:
        return jsonify({"error": "Giriş yapılamadı, token alınamadı"}), 401

    # Kullanıcıdan dinamik filtreleme kriterlerini alıyoruz.
    filters = request.json
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = "https://sandbox-reporting.rpdpymnt.com/api/v3/transaction/list"
    response = requests.post(url, headers=headers, json={
        "fromDate": filters.get("fromDate", "2024-01-01"),
        "toDate": filters.get("toDate", "2024-01-31")
    })

    if response.status_code == 200:
        transaction_data = response.json().get("data", [])
        # Filtreleme işlemi
        for key, value in filters.items():
            if key not in ["fromDate", "toDate"]:
                transaction_data = [t for t in transaction_data if t.get("transaction", {}).get(key) == value]
        return jsonify(transaction_data)
    else:
        return jsonify({"error": "Transaction listesi alınamadı"}), response.status_code

# Bu endpoint, daha dinamik ve esnek arama yapabilmeyi sağlıyor.
# Kullanıcıdan gelen filtre parametrelerine göre transaction'ları filtreliyor ve sonuçları döndürüyor.
# Kullanılan veri yapıları ve teknikler:
# - Dict: Filtre kriterlerini saklamak ve API'den gelen veriler üzerinde arama yapmak için kullanıldı.
# - List comprehension: Dinamik filtreleme işlemlerinde kullanıldı.
# - for döngüsü: Kullanıcının belirttiği filtre kriterlerini işlemede kullanıldı.

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

# Devam ederken, eklediğimiz "dynamic_transaction_search" endpointi ile daha esnek bir arama ve filtreleme sistemi geliştirdik.
# Bu tür esneklikler, gerçek dünyada kullanıcıların farklı ihtiyaçlarına cevap verebilmek için oldukça önemlidir.
# Filtreleme işlemlerinde list comprehension ve dict veri yapısını kullanarak kodun hem okunabilirliğini hem de performansını artırdık.

# Unit testler için pytest'i kullanacağız, fakat bu testleri production ortamına deploy etmeyeceğiz.
# Bu yüzden testleri ayrı bir dosyada tutacağız.

# test_app.py
# import pytest
# from app import app

# @pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# def test_home(client):
#     response = client.get('/')
#     assert response.status_code == 200
#     assert b'Uygulama çalışıyor!' in response.data

# def test_transactions_report(client):
#     response = client.get('/transactions_report')
#     assert response.status_code in [200, 401]

# def test_transaction_list(client):
#     response = client.get('/transaction_list')
#     assert response.status_code in [200, 401]

# def test_dynamic_transaction_search(client):
#     response = client.post('/dynamic_transaction_search', json={"fromDate": "2024-01-01", "toDate": "2024-01-31"})
#     assert response.status_code in [200, 401]