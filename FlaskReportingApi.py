# İlk olarak, Flask'i ve gerekli kütüphaneleri projeye dahil edeceğiz.
from flask import Flask, request, jsonify
import requests
import os

# Projemizi başlatıyoruz.
app = Flask(__name__)

# Burada bir yapı kuracağız, bu yapı login endpointini kullanarak JWT token alacak.
# Bu token diğer API isteklerinde güvenlik amacıyla kullanılacak.

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

# Bu endpoint, daha ayrıntılı transaction bilgilerini almak için bir GET isteği oluşturur.
# Kullanılan veri yapıları:
# - Dict (Sözlük): Gönderilen ve alınan verileri tutmak için kullanılır.
# - List (Liste): Daha fazla veri eklenmesi gerektiğinde veya birden fazla transaction bilgisi dönerken kullanabiliriz.
# - JSON: API ile veri alışverişi yapmak için kullanılır.
# - List comprehension: Filtreleme işlemleri için kullanıldı.
# - sorted() fonksiyonu: Listeyi belirli bir kritere göre sıralamak için kullanıldı.

if __name__ == '__main__':
    app.run(debug=True)

# Devam ederken, yeni eklediğimiz "transaction_list" endpointinde daha karmaşık veri yapıları kullanmaya başladık.
# "List" veri yapısı, birden fazla transaction döndüğünde işimizi kolaylaştıracak. Bu kısımda ayrıca filtreleme ve sıralama işlemleri ekledik.
# "List comprehension" ve "sorted()" fonksiyonları kullanarak onaylanan işlemleri filtreleyip, tutarı büyükten küçüğe sıraladık.
# Bu tür işlemler, veri üzerinde analiz yaparken oldukça önemlidir ve mülakatlarda da sıklıkla sorulabilir.