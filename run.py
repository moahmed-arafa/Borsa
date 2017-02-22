from app import app, q, update_stock

q.enqueue_call(func=update_stock, args=(), result_ttl=5000)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
